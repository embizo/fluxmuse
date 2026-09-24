# Partner API — social posting + WhatsApp, for external callers

Lets an authenticated external system (currently **imanami.ai**, in place of
Zernio) publish to this install's own Facebook Page / Instagram Business
account and send messages through this install's own WhatsApp Business
number. See `assets/backup_db/partner_api.sql` for why this uses its own
credential set, separate from `facebook_rx_fb_page_info` (customer-connected
pages): a partner API call posts as **Fluxmuse's own marketing identity**,
never as one of this install's users.

## Set up (Admin → Partner API)

1. Facebook: a long-lived Page access token (Graph API Explorer, for a Page
   you administer) + that Page's numeric id.
2. Instagram: the Instagram Business Account id linked to that same Page
   (Meta Business Suite → Page settings → Linked accounts). Publishing uses
   the Facebook Page's access token.
3. WhatsApp: a WhatsApp Business phone number id + a **permanent** System
   User access token (Meta Business Settings) — the 24-hour test token
   expires and will start failing silently otherwise.
4. Generate an API key on the same page and give it to the caller. A key is
   only ever shown once, at creation; only its SHA-256 hash is stored.

## Endpoints

All require `Authorization: Bearer fm_...`. Responses are JSON.

```
POST   partner_api/posts
       { network: "facebook"|"instagram", message, media_url?, link?,
         scheduled_at?, external_ref? }
       Instagram requires media_url (no text-only posts). No scheduled_at,
       or one in the past/near future, publishes immediately in the same
       request; a future one is picked up by Cron_job's existing dispatcher
       (added to braodcast_message(), the 1-minute tier) within a minute.

GET    partner_api/posts/show/{id}                    status, permalink (id = the id this API returned)
GET    partner_api/posts/metrics/{platform_post_id}   engagement, once published (the Graph post id, not this API's own id)

POST   partner_api/whatsapp/send
       { to, body, external_ref? }                              free-form text
       { to, template: { name, language?, otp | components }, external_ref? }
       `to` is digits only, international format (e.g. 27711234567). Meta
       only allows free-form text within 24 hours of the recipient's last
       message to this number. Anything business-initiated (a login code,
       an alert to someone who has not written first) must be a template
       that Meta has approved in WhatsApp Manager.

       Login code: { "to": "...", "template": { "name": "sedilaka_login_code",
       "language": "en", "otp": "482913" } }. `otp` fills both the body and
       the copy-code button, which Meta requires for Authentication
       templates. Other templates: pass `components` (header/body/button,
       text/payload/coupon_code parameters). Template parameters are NEVER
       stored -- the log keeps only `[template NAME / LANG]`.

GET    partner_api/whatsapp/templates
       Approval status (APPROVED / PENDING / REJECTED) of the templates on
       the caller's sender. Needs the sender's WABA id.

The number a key sends from is its bound sender (Admin > Partner API >
WhatsApp senders, then pick it in the key's row). Keys with no sender keep
using the single number in Marketing identity. Run
`assets/backup_db/partner_api_whatsapp_senders.sql` once to enable senders.
```

Every post and every WhatsApp send is logged (`partner_api_posts`,
`partner_api_whatsapp_messages`), including failures with Meta's own error
text, so a problem is diagnosable without server log access.

## What this deliberately does not do

- No LinkedIn or X: this codebase has never had those integrations, and
  imanami.ai's own adapters for them are left in place there instead of
  being rebuilt here.
- No per-partner tenancy, scopes or credit metering yet — one shared
  marketing identity, any valid key can use all of it. That is the right
  scope for "one internal caller replacing Zernio"; a real multi-partner
  reseller model is a separate, larger piece of work (see
  `agent-pal-ai/docs/partner-and-internal-api-design.md` on the imanami
  side for that design).
- Template *creation*: templates are written and submitted in WhatsApp
  Manager; this only sends approved ones. Also no Instagram
  video/carousel posts (image only).
