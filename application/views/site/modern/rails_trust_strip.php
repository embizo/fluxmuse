<!--====== PAYMENT RAILS TRUST STRIP START ======-->
<!--
  Shows the native banking/mobile-money rails only. The aggregators that
  actually process these behind the scenes are intentionally not named
  on this public page. Do not add aggregator names or logos to this partial.

  Logo assets: assets/site_new/img/rails/*.svg|png — sourced from Wikimedia
  Commons or each institution's own official site. Three still fall back to
  a text monogram because no legitimate official asset could be sourced in
  this pass: MTN Mobile Money, Airtel Money, Standard Bank Group. Replace
  those with real logo files (same naming convention: rail-mtn-momo.*,
  rail-airtel-money.*, rail-standard-bank.*) and swap their <span class=
  "rails-strip__mono-text"> block below for an <img> once available.
-->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="<?php echo base_url('assets/site_new/css/rails-trust-strip.css'); ?>">

<section class="rails-strip">
  <div class="rails-strip__inner">

    <div class="rails-strip__verified-row">
      <span class="rails-strip__verified-badge">
        <img class="rails-strip__badge-logo" src="<?php echo base_url('assets/site_new/img/rails/badge-meta.svg'); ?>" alt="Meta">
        <strong>Tech&nbsp;Provider</strong>&nbsp;(Verified)
      </span>
      <span class="rails-strip__verified-badge">
        <img class="rails-strip__badge-logo rails-strip__badge-logo--icon" src="<?php echo base_url('assets/site_new/img/rails/badge-whatsapp.svg'); ?>" alt="WhatsApp">
        <strong>Cloud API</strong>
      </span>
    </div>

    <div class="rails-strip__headline">
      <span class="rails-strip__eyebrow"><?php echo $this->lang->line('Payment infrastructure'); ?></span>
      <h2><?php echo $this->lang->line('Deep, native integrations into the rails you trust.'); ?></h2>
      <p><?php echo $this->lang->line('Customers pay you the way they already pay everyone else — no new habits, no friction at checkout.'); ?></p>
    </div>

    <div class="rails-strip__viewport">
      <div class="rails-strip__track" id="railsTrustStripTrack">
        <?php
        // 'logo' is the filename (without extension guessing) under assets/site_new/img/rails/,
        // or null where no legitimate official asset could be sourced (falls back to a monogram).
        $rails_trust_strip_rails = array(
          array('MoMo', 'MTN Mobile Money', 'Mobile Wallet', null),
          array('M-P', 'M-Pesa', 'Mobile Wallet', 'rail-mpesa.svg'),
          array('AM', 'Airtel Money', 'Mobile Wallet', null),
          array('OM', 'Orange Money', 'Mobile Wallet', 'rail-orange-money.svg'),
          array('TB', 'Telebirr', 'Mobile Wallet', 'rail-telebirr.png'),
          array('WV', 'Wave', 'Mobile Wallet', 'rail-wave.png'),
          array('SB', 'Standard Bank Group', 'Bank Rail', null),
          array('AB', 'Access Bank', 'Bank Rail', 'rail-access-bank.png'),
          array('EB', 'Ecobank', 'Bank Rail', 'rail-ecobank.svg'),
          array('KCB', 'KCB Bank', 'Bank Rail', 'rail-kcb.png'),
          array('UBA', 'United Bank for Africa', 'Bank Rail', 'rail-uba.png'),
          array('SEPA', 'SEPA', 'Bank Rail · Eurozone', 'rail-sepa.svg'),
          array('FP', 'Faster Payments', 'Bank Rail · UK', 'rail-faster-payments.svg'),
        );

        // Rendered twice (second copy aria-hidden) so the CSS animation loop is seamless.
        for ($rails_trust_strip_pass = 0; $rails_trust_strip_pass < 2; $rails_trust_strip_pass++) :
          foreach ($rails_trust_strip_rails as $rails_trust_strip_rail) :
            list($rails_trust_strip_mono, $rails_trust_strip_name, $rails_trust_strip_kind, $rails_trust_strip_logo) = $rails_trust_strip_rail;
            ?>
            <div class="rails-strip__rail"<?php echo $rails_trust_strip_pass === 1 ? ' aria-hidden="true"' : ''; ?>>
              <span class="rails-strip__rail-mark">
                <?php if ($rails_trust_strip_logo) : ?>
                  <img src="<?php echo base_url('assets/site_new/img/rails/' . $rails_trust_strip_logo); ?>" alt="<?php echo htmlspecialchars($rails_trust_strip_name); ?>" loading="lazy">
                <?php else : ?>
                  <span class="rails-strip__mono-text"><?php echo htmlspecialchars($rails_trust_strip_mono); ?></span>
                <?php endif; ?>
              </span>
              <span class="rails-strip__rail-copy">
                <span class="rails-strip__rail-name"><?php echo htmlspecialchars($rails_trust_strip_name); ?></span>
                <span class="rails-strip__rail-kind"><?php echo htmlspecialchars($rails_trust_strip_kind); ?></span>
              </span>
            </div>
            <?php
          endforeach;
        endfor;
        ?>
      </div>
    </div>

    <p class="rails-strip__note"><?php echo $this->lang->line("All trademarks and logos are the property of their respective owners."); ?></p>

  </div>
</section>

<script src="<?php echo base_url('assets/site_new/js/rails-trust-strip.js'); ?>"></script>
<!--====== PAYMENT RAILS TRUST STRIP ENDS ======-->
