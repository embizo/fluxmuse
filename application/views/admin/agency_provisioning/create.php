<section class="section">
  <div class="section-header">
    <h1><i class="fas fa-sitemap"></i> <?php echo $page_title; ?></h1>
    <div class="section-header-breadcrumb">
      <div class="breadcrumb-item"><a href="<?php echo site_url('agency_provisioning/index'); ?>"><?php echo $this->lang->line("Agency Instances"); ?></a></div>
      <div class="breadcrumb-item"><?php echo $page_title; ?></div>
    </div>
  </div>

  <?php $this->load->view('admin/theme/message'); ?>
  <?php if ($this->session->flashdata('error_text') != '') { ?>
    <div class="alert alert-danger"><?php echo $this->session->flashdata('error_text'); ?></div>
  <?php } ?>
  <?php echo validation_errors('<div class="alert alert-danger">', '</div>'); ?>

  <div class="section-body">
    <div class="card">
      <div class="card-body">
        <form class="form-horizontal" action="<?php echo site_url('agency_provisioning/create_action'); ?>" method="POST">
          <input type="hidden" name="csrf_token" id="csrf_token" value="<?php echo $this->session->userdata('csrf_token_session'); ?>">

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Purchasing Member"); ?></label>
            <div class="col-9">
              <select class="form-control select2" name="purchased_by_user_id" required>
                <option value=""></option>
                <?php foreach ($members as $member) { ?>
                  <option value="<?php echo $member['id']; ?>"><?php echo htmlspecialchars($member['name']) . ' (' . htmlspecialchars($member['email']) . ')'; ?></option>
                <?php } ?>
              </select>
              <small class="text-muted"><?php echo $this->lang->line("The Member row already on this control-plane install who purchased the Agency package."); ?></small>
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Package"); ?></label>
            <div class="col-9">
              <select class="form-control select2" name="package_id" required>
                <option value=""></option>
                <?php foreach ($packages as $package) { ?>
                  <option value="<?php echo $package['id']; ?>"><?php echo htmlspecialchars($package['package_name']); ?></option>
                <?php } ?>
              </select>
              <small class="text-muted"><?php echo $this->lang->line("Should be the Agency ($346/mo) package."); ?></small>
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Company Name"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="company_name" value="<?php echo set_value('company_name'); ?>" required>
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("White-labeled Product Name"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="product_name" value="<?php echo set_value('product_name'); ?>" placeholder="<?php echo $this->lang->line("Defaults to Company Name"); ?>">
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Primary Color"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="primary_color" value="<?php echo set_value('primary_color', '#3abaf4'); ?>">
            </div>
          </div>

          <hr>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Domain Mode"); ?></label>
            <div class="col-9">
              <select class="form-control" name="domain_mode" id="domain_mode" required>
                <option value="fluxmuse_subdomain"><?php echo $this->lang->line("Fluxmuse-issued subdomain (clientname.fluxmuse.app)"); ?></option>
                <option value="custom_domain"><?php echo $this->lang->line("Client's own domain/subdomain via CNAME"); ?></option>
              </select>
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Subdomain"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="subdomain" value="<?php echo set_value('subdomain'); ?>" placeholder="clientname" required>
              <small class="text-muted"><?php echo $this->lang->line("Always required: used as the Fluxmuse-issued host when Domain Mode is subdomain, and as the internal instance slug either way."); ?></small>
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Custom Domain"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="custom_domain" value="<?php echo set_value('custom_domain'); ?>" placeholder="marketing.clientdomain.com">
              <small class="text-muted"><?php echo $this->lang->line("Required only when Domain Mode is custom domain. The client points this at Fluxmuse via CNAME."); ?></small>
            </div>
          </div>

          <hr>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Instance Admin Name"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="admin_name" value="<?php echo set_value('admin_name'); ?>" required>
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Instance Admin Email"); ?></label>
            <div class="col-9">
              <input type="email" class="form-control" name="admin_email" value="<?php echo set_value('admin_email'); ?>" required>
              <small class="text-muted"><?php echo $this->lang->line("This becomes user_type=Admin on the new clone once it's stood up."); ?></small>
            </div>
          </div>

          <div class="form-group row">
            <div class="col-9 offset-3">
              <button type="submit" class="btn btn-primary"><?php echo $this->lang->line("Create Provisioning Request"); ?></button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>
