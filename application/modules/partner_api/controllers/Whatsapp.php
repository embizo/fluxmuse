<?php  if ( ! defined('BASEPATH')) exit('No Direct Script Access Allowed');

/**
 * Send WhatsApp messages through the WhatsApp number bound to the caller's API
 * key (or the legacy single number, for keys with no sender bound).
 *
 *   POST partner_api/whatsapp/send       {to, body}                    free-form text
 *   POST partner_api/whatsapp/send       {to, template:{name,language,otp|components}}
 *   GET  partner_api/whatsapp/templates  approval status of the sender's templates
 *
 * Free-form text is only accepted by Meta within 24 hours of the recipient's
 * last message to the number. Business-initiated messages -- a login code, an
 * alert to someone who has not written first -- must use an approved template.
 * That is Meta's rule, not something to route around. Template parameters are
 * never stored: for an authentication template they are a live login code.
 */
class Whatsapp extends CI_Controller
{
    private $api;

    public function __construct()
    {
        parent::__construct();
        // load->library, not `new`, because CI3 does not autoload plain
        // application/libraries/*.php classes -- the library loader is what
        // requires the file and instantiates it onto $this->partner_api_base.
        $this->load->library(array('partner_api_base', 'partner_api_whatsapp_payload'));
        $this->api = $this->partner_api_base;
    }

    public function send()
    {
        if ($this->input->method() !== 'post') {
            $this->api->die_error('Use POST.', 405);
        }
        $key = $this->api->authenticate();
        $body = $this->api->json_body();

        $to = isset($body['to']) && is_scalar($body['to']) ? preg_replace('/[^0-9]/', '', $body['to']) : '';
        $external_ref = isset($body['external_ref']) && is_scalar($body['external_ref']) ? substr(trim($body['external_ref']), 0, 191) : null;

        if ($to === '' || strlen($to) < 8 || strlen($to) > 15) {
            $this->api->die_error('"to" must be a phone number in international format, digits only (e.g. 27711234567).');
        }

        $sender = $this->api->whatsapp_sender($key);
        $meta = $this->api->meta();

        if (isset($body['template'])) {
            $built = $this->partner_api_whatsapp_payload->build_template_message($to, $body['template']);
            if (!$built['ok']) {
                $this->api->die_error($built['error']);
            }
            $type = 'template';
            $template_name = $built['name'];
            $logged_body = $this->partner_api_whatsapp_payload->log_summary($built['name'], $built['language']);
            $result = $meta->send_whatsapp_template($sender['phone_number_id'], $sender['access_token'], $built['payload']);
        } else {
            $text = isset($body['body']) && is_string($body['body']) ? trim($body['body']) : '';
            if ($text === '') {
                $this->api->die_error('Send "body" for text, or "template" for an approved template.');
            }
            $type = 'text';
            $template_name = null;
            $logged_body = substr($text, 0, 4096);
            $result = $meta->send_whatsapp_text($sender['phone_number_id'], $sender['access_token'], $to, $logged_body);
        }

        $this->basic->insert_data('partner_api_whatsapp_messages', array(
            'api_key_id' => $key['id'],
            'sender_id' => $sender['id'],
            'message_type' => $type,
            'template_name' => $template_name,
            'external_ref' => $external_ref,
            'to_number' => $to,
            'body' => $logged_body,
            'status' => $result['ok'] ? 'sent' : 'failed',
            'provider_message_id' => isset($result['provider_message_id']) ? $result['provider_message_id'] : null,
            'error_message' => $result['ok'] ? null : substr($result['error'], 0, 1000),
            'created_at' => date('Y-m-d H:i:s'),
        ));

        if (!$result['ok']) {
            $this->api->respond(array('success' => false, 'error' => $result['error']), 502);
        }
        $this->api->respond(array('success' => true, 'provider_message_id' => $result['provider_message_id']), 201);
    }

    /** Where each of the sender's templates stands with Meta review. Lets a
     *  caller ask "is my login-code template approved yet" instead of finding
     *  out by failing a send. Needs the sender to have a WABA id. */
    public function templates()
    {
        if ($this->input->method() !== 'get') {
            $this->api->die_error('Use GET.', 405);
        }
        $key = $this->api->authenticate();
        $sender = $this->api->whatsapp_sender($key);
        if (empty($sender['waba_id'])) {
            $this->api->die_error('This sender has no WhatsApp Business Account id set, so its templates cannot be listed. An admin can add it under Admin > Partner API.', 409);
        }
        $result = $this->api->meta()->list_whatsapp_templates($sender['waba_id'], $sender['access_token']);
        if (!$result['ok']) {
            $this->api->respond(array('success' => false, 'error' => $result['error']), 502);
        }
        $this->api->respond(array('success' => true, 'templates' => $result['templates']));
    }
}
