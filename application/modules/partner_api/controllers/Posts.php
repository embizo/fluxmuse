<?php  if ( ! defined('BASEPATH')) exit('No Direct Script Access Allowed');

/**
 * Publish or schedule a post to this install's own Facebook Page / Instagram
 * Business account, on behalf of an authenticated partner (imanami.ai today,
 * in place of Zernio). See assets/backup_db/partner_api.sql for why this has
 * its own credential set, separate from customer-connected pages.
 *
 *   POST   partner_api/posts            create (publishes now, or schedules)
 *   GET    partner_api/posts/{id}       status of one post
 *
 * Scheduled posts are published by Cron_job's existing dispatcher, wired to
 * call partner_api/posts/run_due (see Cron_job.php).
 */
class Posts extends CI_Controller
{
    private $api;

    public function __construct()
    {
        parent::__construct();
        // load->library, not `new`, because CI3 does not autoload plain
        // application/libraries/*.php classes -- the library loader is what
        // requires the file and instantiates it onto $this->partner_api_base.
        $this->load->library('partner_api_base');
        $this->api = $this->partner_api_base;
    }

    public function index()
    {
        if ($this->input->method() !== 'post') {
            $this->api->die_error('Use POST to create a post.', 405);
        }
        $this->create();
    }

    private function create()
    {
        $key = $this->api->authenticate();
        $body = $this->api->json_body();

        $network = isset($body['network']) ? strtolower(trim($body['network'])) : '';
        $message = isset($body['message']) ? trim($body['message']) : '';
        $media_url = isset($body['media_url']) ? trim($body['media_url']) : null;
        $link = isset($body['link']) ? trim($body['link']) : null;
        $scheduled_at = isset($body['scheduled_at']) ? trim($body['scheduled_at']) : null;
        $external_ref = isset($body['external_ref']) ? substr(trim($body['external_ref']), 0, 191) : null;

        if (!in_array($network, array('facebook', 'instagram'), true)) {
            $this->api->die_error('"network" must be "facebook" or "instagram".');
        }
        if ($message === '' && $network === 'facebook' && !$link) {
            $this->api->die_error('"message" (or "link") is required.');
        }
        if ($network === 'instagram' && empty($media_url)) {
            $this->api->die_error('"media_url" is required for Instagram: it cannot publish a text-only post.');
        }

        $scheduled_ts = null;
        if (!empty($scheduled_at)) {
            $scheduled_ts = strtotime($scheduled_at);
            if ($scheduled_ts === false) {
                $this->api->die_error('"scheduled_at" is not a valid date/time.');
            }
        }

        $now = date('Y-m-d H:i:s');
        $post = array(
            'api_key_id' => $key['id'],
            'external_ref' => $external_ref,
            'network' => $network,
            'message' => $message,
            'media_url' => $media_url,
            'link' => $link,
            'scheduled_at' => $scheduled_ts ? date('Y-m-d H:i:s', $scheduled_ts) : null,
            'status' => 'scheduled',
            'created_at' => $now,
            'updated_at' => $now,
        );
        $this->basic->insert_data('partner_api_posts', $post);
        $id = $this->db->insert_id();

        // A future scheduled_at is left for the cron dispatcher; anything else
        // (none given, or in the past -- "now" from the caller's clock skew)
        // publishes immediately, in the same request.
        if ($scheduled_ts && $scheduled_ts > time() + 30) {
            $this->api->respond(array('success' => true, 'id' => $id, 'status' => 'scheduled', 'scheduled_at' => $post['scheduled_at']), 201);
        }

        $result = $this->publish($id);
        $this->api->respond(array_merge(array('id' => $id), $result), $result['success'] ? 201 : 502);
    }

    public function show($id = null)
    {
        $key = $this->api->authenticate();
        $rows = $this->basic->get_data('partner_api_posts', array('where' => array('id' => (int) $id, 'api_key_id' => $key['id'])));
        if (empty($rows)) $this->api->die_error('Not found.', 404);
        $row = $rows[0];
        $this->api->respond(array(
            'id' => (int) $row['id'],
            'network' => $row['network'],
            'status' => $row['status'],
            'platform_post_id' => $row['platform_post_id'],
            'permalink' => $row['permalink'],
            'error' => $row['error_message'],
            'scheduled_at' => $row['scheduled_at'],
            'created_at' => $row['created_at'],
        ));
    }

    /** Engagement metrics for a published post, looked up by the Graph post id
     *  this API returned from `posts` (`platform_post_id`), NOT this table's own
     *  `id` -- the caller (imanami.ai's campaign-analytics-sync) only ever holds
     *  the platform id it stored alongside its own post row, not this one. */
    public function metrics($platform_post_id = null)
    {
        $key = $this->api->authenticate();
        $rows = $this->basic->get_data('partner_api_posts', array('where' => array('platform_post_id' => (string) $platform_post_id, 'api_key_id' => $key['id'])));
        if (empty($rows)) $this->api->die_error('Not found.', 404);
        $post = $rows[0];
        if ($post['status'] !== 'published' || empty($post['platform_post_id'])) {
            $this->api->die_error('This post has not published yet, so it has no metrics.', 409);
        }

        $config = $this->api->config();
        if (empty($config['fb_page_access_token'])) {
            $this->api->die_error('Facebook/Instagram is not configured.', 503);
        }
        $result = $post['network'] === 'facebook'
            ? $this->api->meta()->get_facebook_metrics($post['platform_post_id'], $config['fb_page_access_token'])
            : $this->api->meta()->get_instagram_metrics($post['platform_post_id'], $config['fb_page_access_token']);

        if (!$result['ok']) {
            $this->api->respond(array('success' => false, 'error' => $result['error']), 502);
        }
        $this->api->respond(array_merge(array('success' => true), $result['metrics']));
    }

    /** Called by Cron_job (service-role context, no partner key) to publish
     *  every post whose scheduled_at has arrived. Not part of the public API
     *  surface -- Cron_job.php calls it internally the same way it dispatches
     *  its other child cron jobs. */
    public function run_due()
    {
        $due = $this->basic->get_data('partner_api_posts', array('where' => array(
            'status' => 'scheduled',
            'scheduled_at <=' => date('Y-m-d H:i:s'),
        )), '', '', 20, NULL, 'scheduled_at ASC');
        foreach ((array) $due as $row) {
            $this->publish($row['id']);
        }
        echo json_encode(array('processed' => count((array) $due)));
    }

    /** Does the actual Graph API call and records the outcome. Shared by the
     *  immediate-publish path and the cron dispatcher so they cannot drift. */
    private function publish($id)
    {
        $rows = $this->basic->get_data('partner_api_posts', array('where' => array('id' => (int) $id)));
        if (empty($rows)) return array('success' => false, 'error' => 'Post row disappeared.');
        $post = $rows[0];

        $this->basic->update_data('partner_api_posts', array('id' => $id), array('status' => 'publishing', 'attempts' => $post['attempts'] + 1, 'updated_at' => date('Y-m-d H:i:s')));
        $config = $this->api->config();

        if ($post['network'] === 'facebook') {
            if (empty($config['fb_page_id']) || empty($config['fb_page_access_token'])) {
                return $this->fail($id, 'Facebook is not configured (missing Page id or access token).');
            }
            $result = $this->api->meta()->post_to_facebook_page($config['fb_page_id'], $config['fb_page_access_token'], $post['message'], $post['link']);
        } else {
            if (empty($config['ig_business_account_id']) || empty($config['fb_page_access_token'])) {
                return $this->fail($id, 'Instagram is not configured (missing Business Account id or access token).');
            }
            $result = $this->api->meta()->post_to_instagram($config['ig_business_account_id'], $config['fb_page_access_token'], $post['message'], $post['media_url']);
        }

        if (!$result['ok']) {
            return $this->fail($id, $result['error']);
        }
        $this->basic->update_data('partner_api_posts', array('id' => $id), array(
            'status' => 'published',
            'platform_post_id' => $result['platform_post_id'],
            'permalink' => isset($result['permalink']) ? $result['permalink'] : null,
            'error_message' => null,
            'updated_at' => date('Y-m-d H:i:s'),
        ));
        return array('success' => true, 'status' => 'published', 'platform_post_id' => $result['platform_post_id'], 'permalink' => isset($result['permalink']) ? $result['permalink'] : null);
    }

    private function fail($id, $message)
    {
        $this->basic->update_data('partner_api_posts', array('id' => $id), array('status' => 'failed', 'error_message' => substr($message, 0, 1000), 'updated_at' => date('Y-m-d H:i:s')));
        return array('success' => false, 'status' => 'failed', 'error' => $message);
    }
}
