-- Per-brand WhatsApp senders for the Partner API, plus template-send logging.
-- Idempotent: safe to run more than once, on MySQL 5.7+/MariaDB.
-- Run AFTER partner_api.sql.

CREATE TABLE IF NOT EXISTS `partner_api_whatsapp_senders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(100) NOT NULL,
  `phone_number_id` varchar(64) NOT NULL,
  `display_number` varchar(32) DEFAULT NULL,
  `waba_id` varchar(64) DEFAULT NULL,
  `access_token_enc` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone_number_id` (`phone_number_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- partner_api_keys.whatsapp_sender_id : which sender a key sends as. NULL keeps
-- the legacy single number in partner_api_config, so existing keys are unchanged.
SET @s = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `partner_api_keys` ADD COLUMN `whatsapp_sender_id` int(11) DEFAULT NULL',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'partner_api_keys' AND COLUMN_NAME = 'whatsapp_sender_id');
PREPARE st FROM @s; EXECUTE st; DEALLOCATE PREPARE st;

SET @s = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `partner_api_whatsapp_messages` ADD COLUMN `sender_id` int(11) DEFAULT NULL',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'partner_api_whatsapp_messages' AND COLUMN_NAME = 'sender_id');
PREPARE st FROM @s; EXECUTE st; DEALLOCATE PREPARE st;

SET @s = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `partner_api_whatsapp_messages` ADD COLUMN `message_type` varchar(16) NOT NULL DEFAULT ''text''',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'partner_api_whatsapp_messages' AND COLUMN_NAME = 'message_type');
PREPARE st FROM @s; EXECUTE st; DEALLOCATE PREPARE st;

SET @s = (SELECT IF(COUNT(*) = 0,
  'ALTER TABLE `partner_api_whatsapp_messages` ADD COLUMN `template_name` varchar(512) DEFAULT NULL',
  'SELECT 1') FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'partner_api_whatsapp_messages' AND COLUMN_NAME = 'template_name');
PREPARE st FROM @s; EXECUTE st; DEALLOCATE PREPARE st;
