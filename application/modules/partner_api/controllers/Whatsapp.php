<?php  if ( ! defined('BASEPATH')) exit('No Direct Script Access Allowed');

/**
 * Send a WhatsApp text message through this install's own WhatsApp Business
 * number, on behalf of an authenticated partner.
 *
 *   POST partner_api/whatsapp/send   {to, body, external_ref?}
 *
 * Meta only allows a free-form message within 24 hours of the recipient's
 * last message to this number; outside that window it is rejected and an
 * approved template would be required, which this endpoint does not send.
 * That is a platform rule enforced by Meta, not something to route around.
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
        $this->load->library('partner_api_base');
        $this->api = $this->partner_api_base;
    }

    public function send()
    {
        if ($this->input->method() !== 'post') {
            $this->api->die_error('Use POST.', 405);
        }
        $key = $this->api->authenticate();
        $body = $this->api->json_body();

        $to = isset($body['to']) ? preg_replace('/[^0-9]/', '', $body['to']) : '';
        $text = isset($body['body']) ? trim($body['body']) : '';
        $external_ref = isset($body['external_ref']) ? substr(trim($body['external_ref']), 0, 191) : null;

        if ($to === '' || strlen($to) < 8 || strlen($to) > 15) {
            $this->api->die_error('"to" must be a phone number in international format, digits only (e.g. 2348012345678).');
        }
        if ($text === '') {
            $this->api->die_error('"body" is required.');
        }

        $config = $this->api->config();
        if (empty($config['whatsapp_phone_number_id']) || empty($config['whatsapp_access_token'])) {
            $this->api->die_error('WhatsApp is not configured yet. An admin must set it up under Admin > Partner API.', 503);
        }

        $result = $this->api->meta()->send_whatsapp_text($config['whatsapp_phone_number_id'], $config['whatsapp_access_token'], $to, substr($text, 0, 4096));

        $now = date('Y-m-d H:i:s');
        $this->basic->insert_data('partner_api_whatsapp_messages', array(
            'api_key_id' => $key['id'],
            'external_ref' => $external_ref,
            'to_number' => $to,
            'body' => substr($text, 0, 4096),
            'status' => $result['ok'] ? 'sent' : 'failed',
            'provider_message_id' => isset($result['provider_message_id']) ? $result['provider_message_id'] : null,
            'error_message' => $result['ok'] ? null : substr($result['error'], 0, 1000),
            'created_at' => $now,
        ));

        if (!$result['ok']) {
            $this->api->respond(array('success' => false, 'error' => $result['error']), 502);
        }
        $this->api->respond(array('success' => true, 'provider_message_id' => $result['provider_message_id']), 201);
    }
}
