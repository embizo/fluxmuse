<section class="section">
  <div class="section-header">
    <h1><i class="fas fa-sitemap"></i> <?php echo $page_title; ?></h1>
    <div class="section-header-button">
      <a class="btn btn-primary" href="<?php echo site_url('agency_provisioning/new_instance'); ?>">
        <i class="fas fa-plus-circle"></i> <?php echo $this->lang->line("New Agency Instance"); ?>
      </a>
    </div>
    <div class="section-header-breadcrumb">
      <div class="breadcrumb-item"><?php echo $this->lang->line("System"); ?></div>
      <div class="breadcrumb-item"><?php echo $page_title; ?></div>
    </div>
  </div>

  <?php $this->load->view('admin/theme/message'); ?>

  <div class="section-body">
    <div class="card">
      <div class="card-body">
        <?php if (empty($instances)) { ?>
          <p class="text-muted"><?php echo $this->lang->line("No Agency instances have been requested yet."); ?></p>
        <?php } else { ?>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th><?php echo $this->lang->line("Company"); ?></th>
                <th><?php echo $this->lang->line("Host"); ?></th>
                <th><?php echo $this->lang->line("DNS Status"); ?></th>
                <th><?php echo $this->lang->line("Instance Status"); ?></th>
                <th><?php echo $this->lang->line("Created"); ?></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <?php foreach ($instances as $row) { ?>
              <tr>
                <td><?php echo $row['id']; ?></td>
                <td><?php echo htmlspecialchars($row['company_name']); ?></td>
                <td>
                  <?php if ($row['domain_mode'] === 'custom_domain') { ?>
                    <?php echo htmlspecialchars($row['custom_domain']); ?> <span class="badge badge-info"><?php echo $this->lang->line("Custom Domain"); ?></span>
                  <?php } else { ?>
                    <?php echo htmlspecialchars($row['subdomain']); ?>.&lt;base_domain&gt;
                  <?php } ?>
                </td>
                <td><span class="badge badge-secondary"><?php echo $row['dns_status']; ?></span></td>
                <td><span class="badge badge-primary"><?php echo $row['instance_status']; ?></span></td>
                <td><?php echo $row['created_at']; ?></td>
                <td>
                  <a class="btn btn-sm btn-outline-primary" href="<?php echo site_url('agency_provisioning/show/' . $row['id']); ?>">
                    <?php echo $this->lang->line("View"); ?>
                  </a>
                </td>
              </tr>
              <?php } ?>
            </tbody>
          </table>
        </div>
        <?php } ?>
      </div>
    </div>
  </div>
</section>
