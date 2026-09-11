<?php
$host = $instance['domain_mode'] === 'custom_domain' && $instance['custom_domain'] !== ''
    ? $instance['custom_domain']
    : $instance['subdomain'] . '.' . $provisioning_config['base_domain'];
?>
<section class="section">
  <div class="section-header">
    <h1><i class="fas fa-sitemap"></i> <?php echo htmlspecialchars($instance['company_name']); ?></h1>
    <div class="section-header-breadcrumb">
      <div class="breadcrumb-item"><a href="<?php echo site_url('agency_provisioning/index'); ?>"><?php echo $this->lang->line("Agency Instances"); ?></a></div>
      <div class="breadcrumb-item"><?php echo $host; ?></div>
    </div>
  </div>

  <?php $this->load->view('admin/theme/message'); ?>

  <div class="section-body">
    <div class="row">
      <div class="col-12 col-md-7">
        <div class="card">
          <div class="card-header"><h4><?php echo $this->lang->line("Instance Details"); ?></h4></div>
          <div class="card-body">
            <table class="table table-borderless">
              <tr><th><?php echo $this->lang->line("Host"); ?></th><td><?php echo htmlspecialchars($host); ?></td></tr>
              <tr><th><?php echo $this->lang->line("Domain Mode"); ?></th><td><?php echo htmlspecialchars($instance['domain_mode']); ?></td></tr>
              <tr><th><?php echo $this->lang->line("White-labeled Product Name"); ?></th><td><?php echo htmlspecialchars($instance['product_name']); ?></td></tr>
              <tr><th><?php echo $this->lang->line("Primary Color"); ?></th><td><span class="badge" style="background:<?php echo htmlspecialchars($instance['primary_color']); ?>">&nbsp;&nbsp;&nbsp;</span> <?php echo htmlspecialchars($instance['primary_color']); ?></td></tr>
              <tr><th><?php echo $this->lang->line("Admin"); ?></th><td><?php echo htmlspecialchars($instance['admin_name']); ?> &lt;<?php echo htmlspecialchars($instance['admin_email']); ?>&gt;</td></tr>
              <tr><th><?php echo $this->lang->line("License Key"); ?></th><td><code><?php echo htmlspecialchars($instance['license_key']); ?></code></td></tr>
              <tr><th><?php echo $this->lang->line("Suggested DB Name"); ?></th><td><code><?php echo htmlspecialchars($instance['suggested_db_name']); ?></code></td></tr>
              <tr><th><?php echo $this->lang->line("Config Export"); ?></th><td><?php echo $instance['config_export_path'] !== '' ? '<code>' . htmlspecialchars($instance['config_export_path']) . '</code>' : $this->lang->line("Not generated yet"); ?></td></tr>
              <tr><th><?php echo $this->lang->line("DNS Status"); ?></th><td><span class="badge badge-secondary"><?php echo $instance['dns_status']; ?></span></td></tr>
              <tr><th><?php echo $this->lang->line("Instance Status"); ?></th><td><span class="badge badge-primary"><?php echo $instance['instance_status']; ?></span></td></tr>
              <tr><th><?php echo $this->lang->line("Created"); ?></th><td><?php echo $instance['created_at']; ?></td></tr>
            </table>

            <form action="<?php echo site_url('agency_provisioning/regenerate_config/' . $instance['id']); ?>" method="POST" class="d-inline">
              <input type="hidden" name="csrf_token" value="<?php echo $this->session->userdata('csrf_token_session'); ?>">
              <button type="submit" class="btn btn-outline-primary"><i class="fas fa-sync"></i> <?php echo $this->lang->line("Regenerate Config Export"); ?></button>
            </form>
            <form action="<?php echo site_url('agency_provisioning/delete/' . $instance['id']); ?>" method="POST" class="d-inline" onsubmit="return confirm('<?php echo $this->lang->line("Delete this provisioning request?"); ?>');">
              <input type="hidden" name="csrf_token" value="<?php echo $this->session->userdata('csrf_token_session'); ?>">
              <button type="submit" class="btn btn-outline-danger"><i class="fas fa-trash"></i> <?php echo $this->lang->line("Delete"); ?></button>
            </form>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-5">
        <div class="card">
          <div class="card-header"><h4><?php echo $this->lang->line("Update Status"); ?></h4></div>
          <div class="card-body">
            <p class="text-muted"><?php echo $this->lang->line("No live DNS/hosting automation is wired up yet (see docs/agency_provisioning.md). Flip this manually once you've actually completed the corresponding step outside the app."); ?></p>
            <form action="<?php echo site_url('agency_provisioning/update_status/' . $instance['id']); ?>" method="POST">
              <input type="hidden" name="csrf_token" value="<?php echo $this->session->userdata('csrf_token_session'); ?>">
              <div class="form-group">
                <select class="form-control" name="instance_status">
                  <?php foreach (array('pending', 'config_generated', 'dns_configured', 'active', 'suspended', 'failed') as $status) { ?>
                    <option value="<?php echo $status; ?>" <?php echo $instance['instance_status'] === $status ? 'selected' : ''; ?>><?php echo $status; ?></option>
                  <?php } ?>
                </select>
              </div>
              <button type="submit" class="btn btn-primary"><?php echo $this->lang->line("Update"); ?></button>
            </form>
          </div>
        </div>

        <div class="card">
          <div class="card-header"><h4><?php echo $this->lang->line("DNS To Configure"); ?></h4></div>
          <div class="card-body">
            <?php if ($instance['domain_mode'] === 'custom_domain') { ?>
              <p><?php echo $this->lang->line("Client creates a CNAME:"); ?></p>
              <pre><?php echo htmlspecialchars($instance['custom_domain']); ?>  CNAME  <?php echo htmlspecialchars($provisioning_config['base_domain']); ?></pre>
            <?php } else { ?>
              <p><?php echo $this->lang->line("Fluxmuse issues a record under the wildcard:"); ?></p>
              <pre><?php echo htmlspecialchars($instance['subdomain']); ?>.<?php echo htmlspecialchars($provisioning_config['base_domain']); ?>  A/CNAME  &lt;clone host&gt;</pre>
            <?php } ?>
            <p class="text-muted"><?php echo $this->lang->line("DNS provider configured for this control plane:"); ?> <strong><?php echo htmlspecialchars($provisioning_config['dns_provider']); ?></strong></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
