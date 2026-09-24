<?php require_once("Home.php"); // including home controller

/**
 * Admin settings for the partner_api module: the one Facebook Page / Instagram
 * Business Account / WhatsApp Business number this install posts and sends as
 * on behalf of an authenticated partner (imanami.ai, in place of Zernio), and
 * the API keys that may call it. See assets/backup_db/partner_api.sql for why
 * this is a separate credential set from customer-connected pages.
 *
 * Same Admin-only gate as Agency_provisioning.php / Custom_theme_manager.php:
 * this is an install-wide operator action, not something a Member does.
 */
class Partner_api_settings extends Home
{
    public function __construct()
    {
        parent::__construct();

        if ($this->session->userdata('logged_in') != 1) {
            redirect('home/login_page', 'location');
        }
        if ($this->session->userdata('user_type') != 'Admin') {
            redirect('home/login_page', 'location');
        }

        $this->load->library(array('partner_api_crypto'));
    }

    public function index()
    {
        $config_rows = $this->basic->get_data('partner_api_config');
        $config = !empty($config_rows) ? $config_rows[0] : null;

        $data['page_title'] = $this->lang->line("Partner API");
        $data['body'] = 'admin/partner_api_settings/index';
        $data['config'] = $config;
        // Tokens are never sent back to the browser once saved -- only whether
        // one is on file, so the form can say "leave blank to keep the current
        // one" instead of showing (or silently blanking) a real secret.
        $data['has_fb_token'] = !empty($config['fb_page_access_token_enc']);
        $data['has_whatsapp_token'] = !empty($config['whatsapp_access_token_enc']);
        $data['senders'] = $this->basic->get_data('partner_api_whatsapp_senders', '', '', '', '', '', 'created_at desc');
        $data['api_keys'] = $this->basic->get_data('partner_api_keys', '', '', '', '', '', 'created_at desc');
        $data['new_key_plaintext'] = $this->session->flashdata('new_key_plaintext');
        $this->_viewcontroller($data);
    }

    public function save_config()
    {
        $fb_page_id = trim($this->input->post('fb_page_id', true));
        $ig_business_account_id = trim($this->input->post('ig_business_account_id', true));
        $whatsapp_phone_number_id = trim($this->input->post('whatsapp_phone_number_id', true));
        $fb_page_access_token = trim($this->input->post('fb_page_access_token', true));
        $whatsapp_access_token = trim($this->input->post('whatsapp_access_token', true));

        $existing = $this->basic->get_data('partner_api_config');
        $data = array(
            'fb_page_id' => $fb_page_id,
            'ig_business_account_id' => $ig_business_account_id,
            'whatsapp_phone_number_id' => $whatsapp_phone_number_id,
            'updated_at' => date('Y-m-d H:i:s'),
        );
        // A blank token field keeps whatever is already stored -- re-saving
        // the other settings must not silently wipe a token nobody re-typed.
        if ($fb_page_access_token !== '') {
            $data['fb_page_access_token_enc'] = $this->partner_api_crypto->encrypt($fb_page_access_token);
        }
        if ($whatsapp_access_token !== '') {
            $data['whatsapp_access_token_enc'] = $this->partner_api_crypto->encrypt($whatsapp_access_token);
        }

        if (!empty($existing)) {
            $this->basic->update_data('partner_api_config', array('id' => $existing[0]['id']), $data);
        } else {
            $this->basic->insert_data('partner_api_config', $data);
        }

        $this->session->set_flashdata('success_text', $this->lang->line('Partner API settings saved.'));
        redirect('partner_api_settings/index', 'location');
    }

    public function create_key()
    {
        $label = trim($this->input->post('label', true));
        if ($label === '') $label = 'Untitled key';

        // 32 random bytes -> 64 hex chars, prefixed so the type of key is
        // self-evident in a log line the way a Stripe or GitHub key is.
        $key = 'fm_' . bin2hex(random_bytes(32));

        $this->basic->insert_data('partner_api_keys', array(
            'label' => $label,
            'key_prefix' => substr($key, 0, 11),
            'key_hash' => hash('sha256', $key),
            'created_at' => date('Y-m-d H:i:s'),
        ));

        // Shown exactly once, via flashdata, immediately after creation. It is
        // never stored in plaintext and this page will never show it again.
        $this->session->set_flashdata('new_key_plaintext', $key);
        redirect('partner_api_settings/index', 'location');
    }

    /** Add or update a WhatsApp sender (one number per brand). A blank token on
     *  update keeps the stored one, same as the legacy config form. */
    public function save_sender()
    {
        $id = (int) $this->input->post('id', true);
        $label = trim($this->input->post('label', true));
        $phone_number_id = trim($this->input->post('phone_number_id', true));
        $display_number = trim($this->input->post('display_number', true));
        $waba_id = trim($this->input->post('waba_id', true));
        $token = trim($this->input->post('access_token', true));

        if ($label === '' || !preg_match('/^[0-9]{5,32}$/', $phone_number_id)) {
            $this->session->set_flashdata('error_message', $this->lang->line('A label and a numeric Phone Number ID are required.'));
            redirect('partner_api_settings/index', 'location');
        }
        if ($waba_id !== '' && !preg_match('/^[0-9]{5,32}$/', $waba_id)) {
            $this->session->set_flashdata('error_message', $this->lang->line('The WhatsApp Business Account ID must be numeric.'));
            redirect('partner_api_settings/index', 'location');
        }

        $data = array(
            'label' => $label,
            'phone_number_id' => $phone_number_id,
            'display_number' => $display_number,
            'waba_id' => $waba_id === '' ? null : $waba_id,
            'updated_at' => date('Y-m-d H:i:s'),
        );
        if ($token !== '') {
            $data['access_token_enc'] = $this->partner_api_crypto->encrypt($token);
        }

        if ($id > 0) {
            $this->basic->update_data('partner_api_whatsapp_senders', array('id' => $id), $data);
        } else {
            if ($token === '') {
                $this->session->set_flashdata('error_message', $this->lang->line('An access token is required for a new sender.'));
                redirect('partner_api_settings/index', 'location');
            }
            $data['created_at'] = date('Y-m-d H:i:s');
            $this->basic->insert_data('partner_api_whatsapp_senders', $data);
        }
        $this->session->set_flashdata('success_text', $this->lang->line('WhatsApp sender saved.'));
        redirect('partner_api_settings/index', 'location');
    }

    /** Bind an API key to a sender, or unbind it (sender 0) to fall back to the
     *  legacy single number. */
    public function bind_key()
    {
        $key_id = (int) $this->input->post('key_id', true);
        $sender_id = (int) $this->input->post('sender_id', true);
        if ($key_id > 0) {
            $this->basic->update_data('partner_api_keys', array('id' => $key_id), array('whatsapp_sender_id' => $sender_id > 0 ? $sender_id : null));
        }
        $this->session->set_flashdata('success_text', $this->lang->line('API key updated.'));
        redirect('partner_api_settings/index', 'location');
    }

    public function revoke_key($id = null)
    {
        $id = (int) $id;
        if ($id > 0) {
            $this->basic->update_data('partner_api_keys', array('id' => $id), array('revoked_at' => date('Y-m-d H:i:s')));
        }
        $this->session->set_flashdata('success_text', $this->lang->line('API key revoked.'));
        redirect('partner_api_settings/index', 'location');
    }
}
