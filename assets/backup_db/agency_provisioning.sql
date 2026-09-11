-- Agency ($346/mo) tier provisioning: white-labeled per-client instance tracking.
--
-- This is an ADDITIVE migration for existing Fluxmuse installs (initial_db.sql already
-- ships the base schema; new installs get these tables the same way, by importing this
-- file once alongside initial_db.sql). It follows the same `CREATE TABLE IF NOT EXISTS`
-- style as initial_db.sql so it is safe to re-run.
--
-- Architecture: this app is single-tenant per install (see CLAUDE.md). An Agency client
-- does NOT get a row of tenant-scoped data inside THIS install; they get their own clone
-- of the whole application + database, provisioned separately. These tables live on the
-- Fluxmuse "control plane" install (the one that sells the Agency package) and just track
-- which clones have been requested/provisioned and what to seed them with. See
-- docs/agency_provisioning.md for the full design.

CREATE TABLE IF NOT EXISTS `agency_provisioning_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `base_domain` varchar(255) NOT NULL DEFAULT 'fluxmuse.app',
  `dns_provider` enum('cloudflare','route53','manual') NOT NULL DEFAULT 'manual',
  `dns_zone_id` varchar(255) NOT NULL DEFAULT '',
  `dns_api_token` varchar(255) NOT NULL DEFAULT '',
  `hosting_provider` enum('docker_compose','hosting_panel_api','manual') NOT NULL DEFAULT 'manual',
  `hosting_api_endpoint` varchar(255) NOT NULL DEFAULT '',
  `hosting_api_token` varchar(255) NOT NULL DEFAULT '',
  `acme_email` varchar(255) NOT NULL DEFAULT '',
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Single settings row, same convention as `ecommerce_config` / `sms_api_config` etc.
INSERT INTO `agency_provisioning_config` (`id`, `base_domain`, `dns_provider`, `dns_zone_id`, `dns_api_token`, `hosting_provider`, `hosting_api_endpoint`, `hosting_api_token`, `acme_email`, `updated_at`)
SELECT 1, 'fluxmuse.app', 'manual', '', '', 'manual', '', '', '', NOW()
WHERE NOT EXISTS (SELECT 1 FROM `agency_provisioning_config` WHERE `id` = 1);

CREATE TABLE IF NOT EXISTS `agency_instances` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `purchased_by_user_id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `domain_mode` enum('fluxmuse_subdomain','custom_domain') NOT NULL DEFAULT 'fluxmuse_subdomain',
  `subdomain` varchar(100) NOT NULL DEFAULT '',
  `custom_domain` varchar(255) NOT NULL DEFAULT '',
  `admin_name` varchar(255) NOT NULL,
  `admin_email` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `primary_color` varchar(20) NOT NULL DEFAULT '#3abaf4',
  `logo_path` varchar(255) NOT NULL DEFAULT '',
  `license_key` varchar(255) NOT NULL DEFAULT '',
  `suggested_db_name` varchar(100) NOT NULL DEFAULT '',
  `config_export_path` varchar(255) NOT NULL DEFAULT '',
  `dns_status` enum('pending','issued','failed') NOT NULL DEFAULT 'pending',
  `instance_status` enum('pending','config_generated','dns_configured','active','suspended','failed') NOT NULL DEFAULT 'pending',
  `notes` text,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subdomain` (`subdomain`),
  KEY `purchased_by_user_id` (`purchased_by_user_id`),
  KEY `package_id` (`package_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Sidebar entry (System > Agency Instances), matching the DB-driven menu convention used
-- by application/modules/menu_manager/controllers/Menu_manager.php (parent_id 47 = "System").
-- Uses id 97 since 96 is the highest id inserted into `menu_child_1` in initial_db.sql.
INSERT INTO `menu_child_1` (`id`, `name`, `url`, `serial`, `icon`, `module_access`, `parent_id`, `have_child`, `only_admin`, `only_member`, `is_external`, `is_menu_manager`, `custom_page_id`)
SELECT 97, 'Agency Instances', 'agency_provisioning/index', 33, 'fas fa-sitemap', '', 47, '0', '1', '0', '0', '0', 0
WHERE NOT EXISTS (SELECT 1 FROM `menu_child_1` WHERE `id` = 97);
