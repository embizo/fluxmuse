<?php require_once("Home.php"); // including home controller

/**
 * Provisioning flow for the Agency ($346/mo) pricing tier.
 *
 * Fluxmuse is a single-tenant-per-install app (see CLAUDE.md) — there is no
 * `tenant_id` scoping anywhere in the schema. An Agency client therefore does not
 * become a scoped row inside THIS install; they get a request tracked here for a
 * genuinely separate clone of the whole app + database ("clone-per-client"), which
 * a human or a follow-up automation actually stands up. This controller is the
 * first stage of that pipeline: it captures the request, generates the branding/
 * license/config artifacts a clone needs, and tracks status through to "active".
 *
 * See docs/agency_provisioning.md for the full architecture write-up, including
 * exactly what infrastructure automation (DNS + hosting) is NOT wired up here.
 *
 * Deliberately NOT in scope for this controller (see docs/agency_provisioning.md):
 *  - Actually calling a DNS provider API to create the subdomain record.
 *  - Actually spinning up hosting (containers/DB) for the clone.
 *  - Actually copying the generated config files onto a new instance.
 *  - Billing integration for the $346/mo charge itself (Payment.php's existing
 *    gateways + `package` table are assumed to already gate access to `new_instance`
 *    via the purchasing user's `package_id`; this controller does not re-implement
 *    checkout).
 */
class Agency_provisioning extends Home
{
    public function __construct()
    {
        parent::__construct();

        if ($this->session->userdata('logged_in') != 1) {
            redirect('home/login_page', 'location');
        }

        // Provisioning new white-labeled instances is a Fluxmuse-operator action,
        // not something an Agency client does to themselves — same gate used by
        // Custom_theme_manager.php / Update_system.php for install-wide actions.
        if ($this->session->userdata('user_type') != 'Admin') {
            redirect('home/login_page', 'location');
        }

        $this->load->library('agency_branding_generator');
    }

    public function index()
    {
        $data['page_title'] = $this->lang->line("Agency Instances");
        $data['body'] = 'admin/agency_provisioning/list';
        $data['instances'] = $this->basic->get_data('agency_instances', '', '', '', '', '', 'id desc');
        $this->_viewcontroller($data);
    }

    public function new_instance()
    {
        $data['page_title'] = $this->lang->line("New Agency Instance");
        $data['body'] = 'admin/agency_provisioning/create';
        $data['members'] = $this->basic->get_data('users', array('where' => array('user_type' => 'Member', 'deleted' => '0')), 'id, name, email, package_id');
        $data['packages'] = $this->basic->get_data('package', array('where' => array('deleted' => '0')));
        $this->_viewcontroller($data);
    }

    public function create_action()
    {
        if (!$_POST) {
            exit();
        }

        $this->form_validation->set_rules('company_name', '<b>' . $this->lang->line("Company Name") . '</b>', 'trim|required');
        $this->form_validation->set_rules('subdomain', '<b>' . $this->lang->line("Subdomain") . '</b>', 'trim|required|alpha_dash|min_length[3]|max_length[63]');
        $this->form_validation->set_rules('admin_name', '<b>' . $this->lang->line("Admin Name") . '</b>', 'trim|required');
        $this->form_validation->set_rules('admin_email', '<b>' . $this->lang->line("Admin Email") . '</b>', 'trim|required|valid_email');
        $this->form_validation->set_rules('purchased_by_user_id', '<b>' . $this->lang->line("Purchasing Member") . '</b>', 'trim|required|integer');
        $this->form_validation->set_rules('package_id', '<b>' . $this->lang->line("Package") . '</b>', 'trim|required|integer');
        $this->form_validation->set_rules('domain_mode', '<b>' . $this->lang->line("Domain Mode") . '</b>', 'trim|required|in_list[fluxmuse_subdomain,custom_domain]');

        if ($this->form_validation->run() == false) {
            return $this->new_instance();
        }

        $this->csrf_token_check();

        $subdomain = strtolower(strip_tags($this->input->post('subdomain', true)));
        $domain_mode = $this->input->post('domain_mode', true);
        $custom_domain = $domain_mode === 'custom_domain' ? strtolower(strip_tags($this->input->post('custom_domain', true))) : '';

        if ($domain_mode === 'custom_domain' && $custom_domain === '') {
            $this->session->set_flashdata('error_message', 1);
            $this->session->set_flashdata('error_text', $this->lang->line("Custom domain is required when domain mode is custom_domain"));
            redirect('agency_provisioning/new_instance', 'location');
        }

        if ($this->basic->is_exist('agency_instances', array('subdomain' => $subdomain))) {
            $this->session->set_flashdata('error_message', 1);
            $this->session->set_flashdata('error_text', $this->lang->line("That subdomain is already taken by another Agency instance"));
            redirect('agency_provisioning/new_instance', 'location');
        }

        $company_name = strip_tags($this->input->post('company_name', true));
        $product_name = $this->input->post('product_name', true) !== '' ? strip_tags($this->input->post('product_name', true)) : $company_name;
        $primary_color = $this->input->post('primary_color', true) !== '' ? strip_tags($this->input->post('primary_color', true)) : '#3abaf4';

        $now = date('Y-m-d H:i:s');

        $instance = array(
            'purchased_by_user_id' => (int) $this->input->post('purchased_by_user_id', true),
            'package_id' => (int) $this->input->post('package_id', true),
            'company_name' => $company_name,
            'domain_mode' => $domain_mode,
            'subdomain' => $subdomain,
            'custom_domain' => $custom_domain,
            'admin_name' => strip_tags($this->input->post('admin_name', true)),
            'admin_email' => strip_tags($this->input->post('admin_email', true)),
            'product_name' => $product_name,
            'primary_color' => $primary_color,
            'logo_path' => '',
            'license_key' => $this->_generate_license_key($subdomain),
            'suggested_db_name' => $this->_suggest_db_name($subdomain),
            'config_export_path' => '',
            'dns_status' => 'pending',
            'instance_status' => 'pending',
            'notes' => '',
            'created_at' => $now,
            'updated_at' => $now,
        );

        if (!$this->basic->insert_data('agency_instances', $instance)) {
            $this->session->set_flashdata('error_message', 1);
            redirect('agency_provisioning/new_instance', 'location');
        }

        $insert_id = $this->db->insert_id();

        // Generating the config export is local file work (no external calls), so we
        // do it synchronously right after the row is created rather than deferring it.
        $this->_generate_config_export($insert_id);

        $this->session->set_flashdata('success_message', 1);
        redirect('agency_provisioning/show/' . $insert_id, 'location');
    }

    public function show($id = 0)
    {
        if ($id == 0) {
            exit();
        }

        $rows = $this->basic->get_data('agency_instances', array('where' => array('id' => $id)));

        if (!isset($rows[0])) {
            exit();
        }

        $data['page_title'] = $this->lang->line("Agency Instance");
        $data['body'] = 'admin/agency_provisioning/show';
        $data['instance'] = $rows[0];
        $data['provisioning_config'] = $this->_get_provisioning_config();
        $this->_viewcontroller($data);
    }

    /**
     * Regenerates the branding/config export for an instance (e.g. after the
     * operator edits primary_color/product_name) without re-issuing a license key.
     */
    public function regenerate_config($id = 0)
    {
        if ($id == 0) {
            exit();
        }

        $this->csrf_token_check();
        $this->_generate_config_export($id);
        $this->session->set_flashdata('success_message', 1);
        redirect('agency_provisioning/show/' . $id, 'location');
    }

    /**
     * Manual status transition. Until DNS + hosting automation exists (see
     * docs/agency_provisioning.md), an operator flips instance_status here once
     * they've actually done the corresponding step by hand.
     */
    public function update_status($id = 0)
    {
        if ($id == 0 || !$_POST) {
            exit();
        }

        $this->csrf_token_check();

        $allowed_statuses = array('pending', 'config_generated', 'dns_configured', 'active', 'suspended', 'failed');
        $status = $this->input->post('instance_status', true);

        if (!in_array($status, $allowed_statuses, true)) {
            exit();
        }

        $this->basic->update_data('agency_instances', array('id' => $id), array(
            'instance_status' => $status,
            'updated_at' => date('Y-m-d H:i:s'),
        ));

        $this->session->set_flashdata('success_message', 1);
        redirect('agency_provisioning/show/' . $id, 'location');
    }

    public function delete($id = 0)
    {
        if ($id == 0) {
            exit();
        }

        $this->csrf_token_check();
        $this->basic->delete_data('agency_instances', array('id' => $id));
        $this->session->set_flashdata('success_message', 1);
        redirect('agency_provisioning/index', 'location');
    }

    protected function _generate_config_export($id)
    {
        $rows = $this->basic->get_data('agency_instances', array('where' => array('id' => $id)));

        if (!isset($rows[0])) {
            return false;
        }

        $instance = $rows[0];
        $provisioning_config = $this->_get_provisioning_config();

        $export_path = $this->agency_branding_generator->generate($instance, $provisioning_config);

        $this->basic->update_data('agency_instances', array('id' => $id), array(
            'config_export_path' => $export_path,
            'instance_status' => $instance['instance_status'] === 'pending' ? 'config_generated' : $instance['instance_status'],
            'updated_at' => date('Y-m-d H:i:s'),
        ));

        return $export_path;
    }

    protected function _get_provisioning_config()
    {
        $rows = $this->basic->get_data('agency_provisioning_config', array('where' => array('id' => 1)));
        return isset($rows[0]) ? $rows[0] : array(
            'base_domain' => 'fluxmuse.app',
            'dns_provider' => 'manual',
            'hosting_provider' => 'manual',
            'acme_email' => '',
        );
    }

    /**
     * Fluxmuse's own per-instance license key — deliberately NOT the legacy Envato
     * purchase_code flow in Home.php (that mechanism activates against a third-party
     * xeroneit.net/mostofa.club endpoint Fluxmuse doesn't control, and is scoped to
     * one domain per Envato purchase). This is a self-issued signed token instead,
     * verifiable offline by anything holding the same encryption_key.
     */
    protected function _generate_license_key($subdomain)
    {
        $secret = $this->config->item('encryption_key');
        $payload = $subdomain . '.' . time() . '.' . bin2hex(random_bytes(8));
        $signature = substr(hash_hmac('sha256', $payload, $secret), 0, 32);
        return strtoupper(substr(md5($payload), 0, 8)) . '-' . $signature;
    }

    protected function _suggest_db_name($subdomain)
    {
        return 'fluxmuse_' . preg_replace('/[^a-z0-9_]/', '', strtolower($subdomain));
    }
}
