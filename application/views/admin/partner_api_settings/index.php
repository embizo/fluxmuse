<section class="section">
  <div class="section-header">
    <h1><i class="fas fa-plug"></i> <?php echo $page_title; ?></h1>
  </div>

  <?php $this->load->view('admin/theme/message'); ?>
  <?php if ($this->session->flashdata('success_text') != '') { ?>
    <div class="alert alert-success"><?php echo $this->session->flashdata('success_text'); ?></div>
  <?php } ?>

  <?php if (!empty($new_key_plaintext)) { ?>
    <div class="alert alert-warning">
      <strong><?php echo $this->lang->line("New API key -- copy it now, it will not be shown again:"); ?></strong>
      <div class="mt-2"><code style="user-select:all;word-break:break-all;"><?php echo htmlspecialchars($new_key_plaintext); ?></code></div>
    </div>
  <?php } ?>

  <div class="section-body">
    <p class="text-muted">
      <?php echo $this->lang->line("The Facebook Page, Instagram Business Account and WhatsApp Business number this install publishes and sends as, on behalf of an authenticated partner (currently imanami.ai, replacing Zernio). This is separate from your users' own connected pages."); ?>
    </p>

    <div class="card">
      <div class="card-header"><h4><?php echo $this->lang->line("Marketing identity"); ?></h4></div>
      <div class="card-body">
        <form class="form-horizontal" action="<?php echo site_url('partner_api_settings/save_config'); ?>" method="POST">
          <input type="hidden" name="csrf_token" id="csrf_token" value="<?php echo $this->session->userdata('csrf_token_session'); ?>">

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Facebook Page ID"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="fb_page_id" value="<?php echo htmlspecialchars($config['fb_page_id'] ?? ''); ?>">
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Facebook Page Access Token"); ?></label>
            <div class="col-9">
              <input type="password" class="form-control" name="fb_page_access_token" autocomplete="off"
                placeholder="<?php echo $has_fb_token ? $this->lang->line('Set -- leave blank to keep it') : $this->lang->line('Not set'); ?>">
              <small class="text-muted"><?php echo $this->lang->line("A long-lived Page access token from Meta's Graph API Explorer, for a Page you administer. Used for both Facebook and Instagram (Instagram publishing calls use the linked Page's token)."); ?></small>
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("Instagram Business Account ID"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="ig_business_account_id" value="<?php echo htmlspecialchars($config['ig_business_account_id'] ?? ''); ?>">
            </div>
          </div>

          <hr>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("WhatsApp Phone Number ID"); ?></label>
            <div class="col-9">
              <input type="text" class="form-control" name="whatsapp_phone_number_id" value="<?php echo htmlspecialchars($config['whatsapp_phone_number_id'] ?? ''); ?>">
            </div>
          </div>

          <div class="form-group row">
            <label class="col-form-label col-3"><?php echo $this->lang->line("WhatsApp Access Token"); ?></label>
            <div class="col-9">
              <input type="password" class="form-control" name="whatsapp_access_token" autocomplete="off"
                placeholder="<?php echo $has_whatsapp_token ? $this->lang->line('Set -- leave blank to keep it') : $this->lang->line('Not set'); ?>">
              <small class="text-muted"><?php echo $this->lang->line("A permanent System User token from Meta Business Settings, not the 24-hour test token."); ?></small>
            </div>
          </div>

          <div class="form-group row">
            <div class="col-9 offset-3">
              <button type="submit" class="btn btn-primary"><?php echo $this->lang->line("Save"); ?></button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><h4><?php echo $this->lang->line("WhatsApp senders"); ?></h4></div>
      <div class="card-body">
        <p class="text-muted"><?php echo $this->lang->line("One WhatsApp number per brand. Bind an API key to a sender below and that key sends from that number. Keys with no sender use the number in Marketing identity."); ?></p>
        <table class="table table-striped">
          <thead><tr><th><?php echo $this->lang->line("Label"); ?></th><th><?php echo $this->lang->line("Number"); ?></th><th><?php echo $this->lang->line("Phone Number ID"); ?></th><th><?php echo $this->lang->line("WABA ID"); ?></th></tr></thead>
          <tbody>
            <?php foreach ($senders as $sd) { ?>
              <tr>
                <td><?php echo htmlspecialchars($sd['label']); ?></td>
                <td><?php echo htmlspecialchars($sd['display_number'] ?? ''); ?></td>
                <td><code><?php echo htmlspecialchars($sd['phone_number_id']); ?></code></td>
                <td><?php echo $sd['waba_id'] ? '<code>' . htmlspecialchars($sd['waba_id']) . '</code>' : '<span class="text-muted">' . $this->lang->line('not set') . '</span>'; ?></td>
              </tr>
            <?php } ?>
            <?php if (empty($senders)) { ?>
              <tr><td colspan="4" class="text-muted"><?php echo $this->lang->line("No senders yet."); ?></td></tr>
            <?php } ?>
          </tbody>
        </table>

        <form action="<?php echo site_url('partner_api_settings/save_sender'); ?>" method="POST">
          <input type="hidden" name="csrf_token" value="<?php echo $this->session->userdata('csrf_token_session'); ?>">
          <div class="form-row">
            <div class="col-md-3 mb-2"><input type="text" class="form-control" name="label" placeholder="<?php echo $this->lang->line('Label, e.g. Sedilaka'); ?>" required></div>
            <div class="col-md-3 mb-2"><input type="text" class="form-control" name="display_number" placeholder="<?php echo $this->lang->line('Number, e.g. +27 71 000 0000'); ?>"></div>
            <div class="col-md-3 mb-2"><input type="text" class="form-control" name="phone_number_id" placeholder="<?php echo $this->lang->line('Phone Number ID'); ?>" required></div>
            <div class="col-md-3 mb-2"><input type="text" class="form-control" name="waba_id" placeholder="<?php echo $this->lang->line('WhatsApp Business Account ID'); ?>"></div>
          </div>
          <div class="form-row">
            <div class="col-md-9 mb-2"><input type="password" class="form-control" name="access_token" autocomplete="off" placeholder="<?php echo $this->lang->line('Permanent System User token'); ?>"></div>
            <div class="col-md-3 mb-2"><button type="submit" class="btn btn-primary btn-block"><?php echo $this->lang->line("Add sender"); ?></button></div>
          </div>
          <small class="text-muted"><?php echo $this->lang->line("The WABA ID is needed to see template approval status."); ?></small>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><h4><?php echo $this->lang->line("API keys"); ?></h4></div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th><?php echo $this->lang->line("Label"); ?></th>
              <th><?php echo $this->lang->line("Key"); ?></th>
              <th><?php echo $this->lang->line("Last used"); ?></th>
              <th><?php echo $this->lang->line("WhatsApp sender"); ?></th>
              <th><?php echo $this->lang->line("Status"); ?></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <?php foreach ($api_keys as $k) { ?>
              <tr>
                <td><?php echo htmlspecialchars($k['label']); ?></td>
                <td><code><?php echo htmlspecialchars($k['key_prefix']); ?>…</code></td>
                <td><?php echo $k['last_used_at'] ? htmlspecialchars($k['last_used_at']) : $this->lang->line('Never'); ?></td>
                <td>
                  <?php if (!$k['revoked_at']) { ?>
                    <form class="form-inline" action="<?php echo site_url('partner_api_settings/bind_key'); ?>" method="POST">
                      <input type="hidden" name="csrf_token" value="<?php echo $this->session->userdata('csrf_token_session'); ?>">
                      <input type="hidden" name="key_id" value="<?php echo (int) $k['id']; ?>">
                      <select name="sender_id" class="form-control form-control-sm mr-1" onchange="this.form.submit()">
                        <option value="0"><?php echo $this->lang->line("Default number"); ?></option>
                        <?php foreach ($senders as $sd) { ?>
                          <option value="<?php echo (int) $sd['id']; ?>" <?php echo ((int) ($k['whatsapp_sender_id'] ?? 0) === (int) $sd['id']) ? 'selected' : ''; ?>><?php echo htmlspecialchars($sd['label']); ?></option>
                        <?php } ?>
                      </select>
                    </form>
                  <?php } ?>
                </td>
                <td>
                  <?php if ($k['revoked_at']) { ?>
                    <span class="badge badge-secondary"><?php echo $this->lang->line("Revoked"); ?></span>
                  <?php } else { ?>
                    <span class="badge badge-success"><?php echo $this->lang->line("Active"); ?></span>
                  <?php } ?>
                </td>
                <td>
                  <?php if (!$k['revoked_at']) { ?>
                    <a href="<?php echo site_url('partner_api_settings/revoke_key/' . $k['id']); ?>"
                       class="btn btn-sm btn-danger"
                       onclick="return confirm('<?php echo $this->lang->line('Revoke this key? Any partner using it will start failing immediately.'); ?>');">
                      <?php echo $this->lang->line("Revoke"); ?>
                    </a>
                  <?php } ?>
                </td>
              </tr>
            <?php } ?>
            <?php if (empty($api_keys)) { ?>
              <tr><td colspan="6" class="text-muted"><?php echo $this->lang->line("No API keys yet."); ?></td></tr>
            <?php } ?>
          </tbody>
        </table>

        <form class="form-inline" action="<?php echo site_url('partner_api_settings/create_key'); ?>" method="POST">
          <input type="hidden" name="csrf_token" id="csrf_token" value="<?php echo $this->session->userdata('csrf_token_session'); ?>">
          <input type="text" class="form-control mr-2" name="label" placeholder="<?php echo $this->lang->line('e.g. imanami.ai production'); ?>" required>
          <button type="submit" class="btn btn-primary"><?php echo $this->lang->line("Generate new key"); ?></button>
        </form>
      </div>
    </div>
  </div>
</section>
