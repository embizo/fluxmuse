-- Partner/internal API: lets an external system (currently imanami.ai, replacing
-- Zernio) publish to this install's connected Facebook/Instagram Pages and send
-- WhatsApp messages through this install's own WhatsApp Business number.
--
-- Deliberately its own credential set, separate from `facebook_rx_fb_page_info`
-- and the bot/autoposting tables: those belong to Fluxmuse's own end users and
-- their connected pages, and this API posts as Fluxmuse's OWN marketing
-- identity, not as any user's. Mixing the two would let an API caller post
-- through a customer's page by mistake.
--
-- Additive, same `CREATE TABLE IF NOT EXISTS` style as initial_db.sql.

CREATE TABLE IF NOT EXISTS `partner_api_keys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(100) NOT NULL,
  `key_prefix` varchar(16) NOT NULL COMMENT 'shown in the admin UI so a key can be told apart without revealing it',
  `key_hash` varchar(64) NOT NULL COMMENT 'sha256 of the full key; the key itself is shown once, at creation, and never stored',
  `last_used_at` datetime DEFAULT NULL,
  `revoked_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_hash` (`key_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Single-row settings, same pattern as `sms_api_config`/`ecommerce_config`.
-- Tokens are stored encrypted (AES-256-CBC, keyed on config['encryption_key'],
-- see Partner_api_crypto.php) -- this install had no precedent for encrypting
-- a credential column, so this does not reuse a Fluxmuse "at rest" scheme that
-- does not exist; it is the one introduced here.
CREATE TABLE IF NOT EXISTS `partner_api_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fb_page_id` varchar(64) DEFAULT NULL,
  `fb_page_access_token_enc` text DEFAULT NULL,
  `ig_business_account_id` varchar(64) DEFAULT NULL,
  `whatsapp_phone_number_id` varchar(64) DEFAULT NULL,
  `whatsapp_access_token_enc` text DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `partner_api_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_key_id` int(11) NOT NULL,
  `external_ref` varchar(191) DEFAULT NULL COMMENT 'the caller''s own id for this post, for their idempotency/lookup',
  `network` enum('facebook','instagram') NOT NULL,
  `message` text NOT NULL,
  `media_url` text DEFAULT NULL,
  `link` text DEFAULT NULL,
  `scheduled_at` datetime DEFAULT NULL COMMENT 'NULL = publish immediately',
  `status` enum('scheduled','publishing','published','failed') NOT NULL DEFAULT 'scheduled',
  `platform_post_id` varchar(191) DEFAULT NULL,
  `permalink` text DEFAULT NULL,
  `error_message` text DEFAULT NULL,
  `attempts` int(11) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `status_scheduled` (`status`,`scheduled_at`),
  KEY `api_key_id` (`api_key_id`),
  KEY `platform_post_id` (`platform_post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `partner_api_whatsapp_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_key_id` int(11) NOT NULL,
  `external_ref` varchar(191) DEFAULT NULL,
  `to_number` varchar(20) NOT NULL,
  `body` text NOT NULL,
  `status` enum('sent','failed') NOT NULL,
  `provider_message_id` varchar(191) DEFAULT NULL,
  `error_message` text DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_key_id` (`api_key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sidebar entry (System > Partner API), same DB-driven menu convention as
-- agency_provisioning.sql. Uses id 98 (97 is agency_provisioning's).
INSERT INTO `menu_child_1` (`id`, `name`, `url`, `serial`, `icon`, `module_access`, `parent_id`, `have_child`, `only_admin`, `only_member`, `is_external`, `is_menu_manager`, `custom_page_id`)
SELECT 98, 'Partner API', 'partner_api_settings/index', 34, 'fas fa-plug', '', 47, '0', '1', '0', '0', '0', 0
WHERE NOT EXISTS (SELECT 1 FROM `menu_child_1` WHERE `id` = 98);
