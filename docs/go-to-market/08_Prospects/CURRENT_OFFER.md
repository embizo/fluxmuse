# Current offer: source of truth for prospect proposals

Prepared **2026-09-26** from the live pricing tables and the founder's decisions since 11 Sept.
**This supersedes `docs/go-to-market/00_FACTS_AND_ASSUMPTIONS.md` wherever they differ.** That file is from
11 Sept and is stale on pricing, trials and the pilot (see §7). Every prospect proposal is written to this file.

## 1. Prices (live in `subscription_tiers`, read 2026-09-26)

ZAR per month. Annual billing is 10× the monthly price for 12 months. VAT treatment: `[[CONFIRM]]`.

| Band | Tier | Monthly | Annual | Brands | Channels | Notes |
|---|---|---|---|---|---|---|
| Small | Free | R0 | R0 | 1 | 1 | Permanent plan, not a trial. Don't lead with it. |
| Small | **Nano** | R149 | R1,490 | 1 | 3 | Entry paid plan for side-hustles |
| Small | **Micro** | R289 | R2,890 | 1 | 4 | 1 WhatsApp number |
| Medium | **Starter** | R499 | R4,990 | 1 | 3 | |
| Medium | **Growth** | R1,999 | R19,990 | 3 | 15 | + inbound AI Voice (beta) |
| Medium | **Scale** | R4,999 | R49,990 | 10 | 40 | + inbound and outbound AI Voice (beta) |
| Enterprise | **Corporate** | R6,999 | R69,990 | 25 | 60 | BYOC ("bring your own cloud") |
| Enterprise | **Agency** | R9,999 | R99,990 | unlimited | 80 | BYOC, white-label, multi-client |
| Enterprise | Custom | on request | | | | sold by consultation |

- **AI credits:** 1 credit is about R1 of real provider cost (chat 1, image 2, 8-second 720p video 7). Monthly
  allowances changed on 24 Sept, so **never quote per-tier credit numbers**; point to the pricing page.
- **Launch pricing:** the `founding-member-za` promotion is enabled in the database: **30% off the first two monthly
  billing cycles** for South African sign-ups. It is a discount, not a free period. Re-confirm it is still active
  before quoting. The generator shows it as one optional line (`SHOW_FOUNDING_MEMBER` in
  `_build/prospects/build_prospects.py`).
- **Partner wholesale:** the earlier decision was "30% off the Agency tier". Agency list price is now **R9,999**, so
  30% off would be about **R6,999**, not the R5,599 in the older pack. **Founder to confirm before any agency
  proposal quotes a partner price.** Until then agency proposals show list price and say "partner terms on request".

## 2. Policy (founder, 25 Sept: "pay first")

- **No free trials and no "first month free"** in any offer or copy, unless the founder approves it for a named account.
- **Payment first, backed by a money-back guarantee.** The founder floated ~30 days; it is **not finalised**. Proposals
  use the placeholder `[[GUARANTEE TERMS]]`, set once in the generator config.
- **FluxMuse guarantees leads, not sales**, and only against a measurable, auditable lead definition. **That definition
  doesn't exist yet**, so proposals do not promise a lead number. A candidate definition is in
  `Outreach_Playbook.md` for the founder to decide.
- **Sales should flow through FluxMuse checkout** (oversight). Steer merchants to shop checkout, not off-platform.

## 3. What is real today (label every capability with one of these three)

**LIVE, newly launched.** Built and deployed. **No real merchant has run these end to end yet**, so say
"newly launched", never "proven", and never quote results.
- **WhatsApp Concierge:** the merchant sends product photos to FluxMuse on WhatsApp; AI drafts the catalogue entry
  (name, description, price guess); the merchant replies YES / NO / edit. (1 credit per photo.)
- **Hosted shop link** (`fluxmuse.ai/s/<name>`): a public shop page; orders arrive as a pre-typed WhatsApp message to the
  merchant's own number.
- **Order alerts and SOLD:** merchant is alerted on WhatsApp per order and replies SOLD to mark it sold.
- **AI captions and images for posts** (POST keyword): a caption and photo come back on WhatsApp, ready to forward to
  WhatsApp Status.
- **AI video clips** (short, 720p by default) and **voice-note transcription** on WhatsApp.
- **WhatsApp Business setup:** number connection, profile, templates, quick replies, broadcast to **consented** contacts.
- **Answers in the customer's language** (the assistant follows the customer's language).
- **TikTok posting** (video only) is approved.

**IN SETUP.** Depends on approvals or wiring that isn't finished. Describe as "being switched on", never as available.
- **Auto-publishing to Facebook Pages and Instagram:** the Meta permissions are **not approved yet**. Until then the real
  value is forwarding to WhatsApp Status.
- **Daily digest** message: dry run only; needs a Meta-approved message template.
- **Checkout through FluxMuse** (Paystack, South African bank accounts; FluxMuse doesn't hold the money): built but **not
  yet tested end to end with real money**. Fees and terms `[[FOUNDER TO CONFIRM FEE WORDING]]` before it is offered.
- **AI Voice** (inbound on Growth; inbound and outbound on Scale): beta, with known latency and language-switching
  issues. Offer as "beta, evaluated together", never as a receptionist replacement.
- **Click-to-WhatsApp ads (FluxLoop):** FluxMuse runs it on its own account first; **not offered to tenants yet**.
- **Sync from Shopify, WooCommerce, Takealot:** exists in part; tenant catalogue sync is a known gap. Don't promise it.

**NOT AVAILABLE.** Instagram DMs and comments (not approved), X posting (off), Nigeria/Kenya/Ghana checkout
(Fincra/pawaPay accounts pending), anything outside South Africa for paid checkout.

## 4. Company facts you may state

- Fluxmuse (Pty) Ltd, South Africa; a **verified Meta Tech Provider** (business and access verification, as of Sept 2026).
- Payments in South Africa run on Paystack (live). Yoco and Ozow are integrated on FluxMuse's own subscription billing.
- Built for African small businesses: WhatsApp-first, priced in rands, multilingual.
- **No customer counts, no ratings, no testimonials, no results, no "pilot brands".** FluxMuse has **no paying
  customers yet** and **no pilot cohort**. The honest, credible angle is *"we are opening with a small first group of
  businesses, and we set you up by hand"*, not social proof.

## 5. Never write

"Free trial", "free month", "14 days free", "try it free", "risk-free", "pilot" (as if a cohort exists), "our customers",
"trusted by", "proven", "guaranteed results/sales/ROI", "10x", any revenue or sales uplift number for the prospect,
Instagram/Facebook auto-posting as live, SnapScan, Stitch, Flutterwave, PayFast, M-Pesa direct, or any statement about a
prospect's finances, health, family, legal matters or personal life.

## 6. Outreach rules (POPIA s69 and good manners)

- **Human-sent only.** No bulk automation, no AI cold calls, no auto-DMs. Electronic direct marketing to people who haven't
  consented is restricted (POPIA s69); a person-to-person, relevant, one-to-one business approach with a clear opt-out
  is the defensible route. Not legal advice.
- **Use only channels the business itself publishes** for enquiries (website contact form or listed business email/number,
  their public business social account) or a warm introduction. **Never guess or scrape an email address or personal
  number.** For public figures, go through management or booking.
- Every first message states who FluxMuse is, why this business, what we're asking (a 20-minute call), and how to opt out.
- Public facts about a business come only from its own site/social or reputable press, each with a source URL and date.
  **Pains are hypotheses**, labelled as such, and phrased as questions to validate, never as claims about the business.

## 7. Stale in the 11 Sept go-to-market pack (do not reuse)

Agency at R7,999 and partner wholesale R5,599; the old five-tier ladder as the whole offer; the 14-day free trial; the
"Gauteng pilot of 12 brands" (none exist); the Founding Member window of 1 Dec 2026 – 31 Jan 2027 (the promotion is now
enabled early); per-tier AI credit numbers; and the claim that WhatsApp checkout is the headline product (it is built but
untested with real money). A refresh pass on the pack is recommended.
