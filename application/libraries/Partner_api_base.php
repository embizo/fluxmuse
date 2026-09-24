<?php  if ( ! defined('BASEPATH')) exit('No Direct Script Access Allowed');

/**
 * Shared bootstrap and bearer-key auth for the partner_api module's public
 * JSON controllers (Posts, Whatsapp). Not a CI_Controller subclass: HMVC
 * controllers already extend CI_Controller directly, so this is used as a
 * plain helper the controller's constructor calls into, rather than a base
 * class -- keeps every check in one place without fighting CI3's single-
 * inheritance controllers.
 */
class Partner_api_base
{
    /** @var CI_Controller */
    private $CI;

    public function __construct()
    {
        $this->CI =& get_instance();
        $this->CI->load->database();
        $this->CI->load->model('basic');
        $this->CI->load->library(array('partner_api_crypto', 'partner_api_meta'));
    }

    /** Sends the JSON body and stops. Every controller action ends by calling
     *  this (or die_error), so a caller always gets a JSON response, never a
     *  CI error page or a redirect (this API has no session to redirect to). */
    public function respond($data, $http_status = 200)
    {
        $this->CI->output
            ->set_status_header($http_status)
            ->set_content_type('application/json')
            ->set_output(json_encode($data));
        exit;
    }

    public function die_error($message, $http_status = 400)
    {
        $this->respond(array('success' => false, 'error' => $message), $http_status);
    }

    /** Reads `Authorization: Bearer fm_...`, hashes it, and looks it up. Dies
     *  with 401 on anything short of an exact match against a non-revoked key
     *  -- same shape of check as every other bearer-token integration in this
     *  build (imanami's execute-agent, Slack's signing secret). Returns the
     *  matched key row (never the key itself; only its hash is stored). */
    public function authenticate()
    {
        $header = $this->CI->input->get_request_header('Authorization', true);
        if (empty($header) || stripos($header, 'Bearer ') !== 0) {
            $this->die_error('Missing or malformed Authorization header.', 401);
        }
        $key = trim(substr($header, 7));
        if ($key === '' || strpos($key, 'fm_') !== 0) {
            $this->die_error('Invalid API key.', 401);
        }
        $hash = hash('sha256', $key);
        $row = $this->CI->basic->get_data('partner_api_keys', array('where' => array('key_hash' => $hash, 'revoked_at' => NULL)));
        if (empty($row)) {
            $this->die_error('Invalid or revoked API key.', 401);
        }
        $this->CI->basic->update_data('partner_api_keys', array('id' => $row[0]['id']), array('last_used_at' => date('Y-m-d H:i:s')));
        return $row[0];
    }

    /** Accessors so the calling controller never touches $this->CI directly --
     *  keeps every dependency this module needs funnelled through one place. */
    public function meta()
    {
        return $this->CI->partner_api_meta;
    }

    public function basic()
    {
        return $this->CI->basic;
    }

    /** The single-row marketing identity every call posts/sends as. Dies with
     *  a clear message (not a generic 500) when the admin has not configured
     *  it yet, since that is the expected state right after this ships. */
    public function config()
    {
        $row = $this->CI->basic->get_data('partner_api_config');
        if (empty($row)) {
            $this->die_error('Partner API is not configured yet. An admin must set it up under Admin > Partner API.', 503);
        }
        $config = $row[0];
        $config['fb_page_access_token'] = $this->CI->partner_api_crypto->decrypt($config['fb_page_access_token_enc']);
        $config['whatsapp_access_token'] = $this->CI->partner_api_crypto->decrypt($config['whatsapp_access_token_enc']);
        return $config;
    }

    /** Body of a JSON POST request as an associative array, or a 400 on
     *  malformed JSON -- CI3's $this->input->post() expects form-encoded
     *  bodies, which is not what a JSON API client sends. */
    public function json_body()
    {
        $raw = $this->CI->input->raw_input_stream;
        $decoded = json_decode($raw, true);
        if ($raw !== '' && $decoded === null && json_last_error() !== JSON_ERROR_NONE) {
            $this->die_error('Request body is not valid JSON.', 400);
        }
        return is_array($decoded) ? $decoded : array();
    }
}
