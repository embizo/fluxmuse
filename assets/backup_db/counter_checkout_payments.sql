-- Counter/in-person checkout, per-order QR/pay-link (Paystack hosted checkout,
-- M-Pesa STK push), and verified-vs-declared payment status.
-- See docs/counter_checkout_and_cardless_payments.md for the design writeup.
--
-- Additive only: run once against an existing Fluxmuse/ChatPion database.
-- All new columns are nullable or DEFAULT-backed so existing rows/behaviour
-- are unaffected until the new flows are actually used.

-- Distinguishes an online chat-storefront order from one rung up at the
-- counter (Ecommerce::counter_start_sale()).
ALTER TABLE `ecommerce_cart`
  ADD COLUMN `sale_channel` enum('online','counter') NOT NULL DEFAULT 'online' AFTER `action_type`;

-- Distinguishes a gateway-confirmed payment from a merchant's own unverified
-- declaration (manual_payment()/cod_payment()). Defaults to 'gateway_verified'
-- so every existing/new gateway callback needs no code change to be correct;
-- manual_payment()/cod_payment() explicitly override it to 'merchant_declared'.
ALTER TABLE `ecommerce_cart`
  ADD COLUMN `payment_verification_method` enum('gateway_verified','merchant_declared') NOT NULL DEFAULT 'gateway_verified' AFTER `sale_channel`;

-- Safaricom Daraja's CheckoutRequestID (~24-27 chars) doesn't reliably fit
-- ecommerce_cart.transaction_id (varchar(25)), so it gets its own column as
-- a pre-settlement placeholder; Ecommerce::mpesa_webhook() overwrites
-- transaction_id with the short, final MpesaReceiptNumber once paid.
ALTER TABLE `ecommerce_cart`
  ADD COLUMN `mpesa_checkout_request_id` varchar(50) NOT NULL DEFAULT '' AFTER `payment_verification_method`;

-- The "is this gateway on" flag follows the existing convention of living on
-- ecommerce_store (alongside paystack_enabled, xendit_enabled, etc.), not on
-- ecommerce_config, which holds credentials only.
ALTER TABLE `ecommerce_store`
  ADD COLUMN `mpesa_enabled` enum('0','1') NOT NULL DEFAULT '0' AFTER `cod_enabled`;

-- M-Pesa gateway credentials, alongside the other per-store gateway
-- credential columns already on ecommerce_config.
ALTER TABLE `ecommerce_config`
  ADD COLUMN `mpesa_consumer_key` text NOT NULL AFTER `xendit_secret_api_key`,
  ADD COLUMN `mpesa_consumer_secret` text NOT NULL AFTER `mpesa_consumer_key`,
  ADD COLUMN `mpesa_shortcode` varchar(50) NOT NULL DEFAULT '' AFTER `mpesa_consumer_secret`,
  ADD COLUMN `mpesa_passkey` text NOT NULL AFTER `mpesa_shortcode`,
  ADD COLUMN `mpesa_environment` enum('sandbox','live') NOT NULL DEFAULT 'sandbox' AFTER `mpesa_passkey`;

-- Scoped WhatsApp Business (Cloud API) sender, used only to push checkout
-- payment links/order confirmations for a store (not the general WhatsApp
-- livechat/inbox concept — see docs/counter_checkout_and_cardless_payments.md).
ALTER TABLE `ecommerce_config`
  ADD COLUMN `whatsapp_business_enabled` enum('0','1') NOT NULL DEFAULT '0' AFTER `mpesa_environment`,
  ADD COLUMN `whatsapp_business_phone_number_id` varchar(50) NOT NULL DEFAULT '' AFTER `whatsapp_business_enabled`,
  ADD COLUMN `whatsapp_business_access_token` text NOT NULL AFTER `whatsapp_business_phone_number_id`;
