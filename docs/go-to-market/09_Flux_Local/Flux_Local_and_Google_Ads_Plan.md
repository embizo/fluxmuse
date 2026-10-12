# Flux Local + Google Ads: value proposition, AI workers and build plan

*Drafted 2026-10-12. Labels: **FACT** means verified in the code or the production config on this date. **ASSUMPTION** means a planning number to test. **FOUNDER DECISION** means the founder has to choose it.*

---

## 0. What exists today (FACT)

The code is built and deployed, but Google has not switched it on yet.

| Piece | Where (foundation-zero-point) | State |
|---|---|---|
| Flux Local UI: Performance, Reviews, Posts, Business info, Review requests | `src/pages/FluxLocal.tsx` | Deployed (PR #235, tag `direct-deploy/20261011-210813`) |
| GBP API: location, info/hours, categories, attributes, AI post draft, post, review sync, AI reply draft, send reply, insights | `supabase/functions/google-business/index.ts`, `_shared/ads-platforms/google-business.ts` | Deployed. Every action returns 503 until approved |
| Google Ads: overview, AI ad copy, Keyword Planner, create campaign (paused), status/budget, Customer Match, conversions, metrics sync | `supabase/functions/google-ads/index.ts`, `_shared/ads-platforms/google-ads.ts`, `src/components/ads/GoogleAdsPanel.tsx` | Deployed. Answers `not_configured` |
| Closed loop: gclid/gbraid/wbraid captured on hosted pages → WhatsApp order → offline conversion upload | `ads-click-capture`, `match_ad_click_for_order`, `ads_conversion_uploads` | Built |
| Review request after a paid order (WhatsApp `review_request` template) | `gbp_review_requests`, `ads-platforms-sweep` | Built. Each business needs its own approved template |
| Paid-boost agent (Meta only, approval-gated, `max_boost_zar` ceiling) | `supabase/functions/flux-ads-run` | Live for Meta |
| Application pack for every approval | `docs/ads-platform-approvals.md` | Written |

**Production secrets on 2026-10-12:** `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set. **`GOOGLE_ADS_DEVELOPER_TOKEN` and `GOOGLE_BUSINESS_PROFILE_API_APPROVED` are not.** Neither integration works for a customer yet.

**Gaps found while mining the code:**
1. No tier gating. `google-ads` and `google-business` never call `tier-gate.ts`, so the features can't be sold as an upgrade.
2. No FluxMuse revenue on ad spend. There is no fee, take-rate or managed-spend ledger.
3. No agent loop for Google. Every Flux Local and Google Ads action is a button a human clicks. `flux-ads-run` only boosts Meta posts.
4. Google Ads RMF gaps block Standard Access: negative keywords, ad-group/keyword/ad reporting, ad policy status, and pause/edit per ad group, keyword and ad.
5. The critical path is calendar time. The GBP API form wants FluxMuse's own **verified** Business Profile, "ideally 60+ days" old.

---

## 1. The value chain: where a local business wins or loses money on Google

```
 DISCOVER          CONSIDER             ACT                 TRANSACT              RETAIN / ADVOCATE
 Search, Maps  →   Profile, photos,  →  Call, directions, → WhatsApp order,   →   Review request,
 "near me",        reviews, hours,      website, WhatsApp   shop checkout,        reply, repeat
 Google Ads        posts, offers        click               pay link (rails)      offers, rebook
     ▲                                                                                │
     └──────── more reviews + fresh posts + conversion data = higher rank, cheaper clicks ◄┘
```

| Stage | What the owner loses today | What FluxMuse does | Built? |
|---|---|---|---|
| Discover | Not on Maps or wrong category. Ads money wasted on broad keywords | Profile Keeper fixes categories and attributes. Keyword Scout and Campaign Builder run tight local Search campaigns | Partly (manual) |
| Consider | Stale hours, no posts, unanswered reviews. Customers pick the competitor with 4.6★ and 200 reviews | Weekly posts from the catalogue. AI review replies within 24 hours | Partly (manual) |
| Act | Calls and clicks go to a number nobody answers | WhatsApp click lands in the FluxMuse AI chatbot, 24/7 | Yes |
| Transact | Google never sees the sale, because it closes on WhatsApp or in cash | Order + pay link on the rails. **gclid is matched to the paid order and uploaded to Google** | Yes |
| Retain / advocate | Happy customers never review | Review request on WhatsApp after every paid order, once, no incentive | Yes |

**The moat:** Google can't see sales that close in WhatsApp chats, and in African SMB commerce that is most of them. FluxMuse sees the click, the chat, the order and the payment, and sends the sale back to Google. Google's Smart Bidding then learns to buy customers who pay, not just clicks. Agencies and generic tools can't close that loop. The pitch line:

> **"Found on Google. Sold on WhatsApp. Paid on FluxMuse. And Google learns from every sale."**

### Value proposition by segment

| Segment | Pain | Flux Local promise | Proof metric (pilot KPI, not a claim) |
|---|---|---|---|
| Solo (salon, kota shop, physio) | Invisible on Maps. Reviews ignored | "Get found on Google Maps and turn the clicks into WhatsApp orders, done for you" | Calls + directions + WhatsApp clicks per week; reviews per month |
| SME (multi-branch retail, clinics) | Agency charges R15k+/mo with no attribution | "Every rand of Google Ads traced to a paid order" | Cost per *paid* order (from offline conversions) |
| Agency / Flux_Partner | Manual GBP work across 50 clients | "White-label Google Local for all your clients at partner price" | Locations managed per staff member |

---

## 2. How FluxMuse makes money from it

| # | Revenue line | Mechanism | Price | Needs |
|---|---|---|---|---|
| R1 | **Tier upgrade pull** | Flux Local: 1 location on Starter, 3 on Growth, 10 on Scale. Google Ads on Growth and up | Existing tiers (R499 / R1,999 / R4,999) | Tier gate (gap 1) |
| R2 | **Extra locations add-on** | Per location beyond the tier allowance | ASSUMPTION R149/location/mo · FOUNDER DECISION | Add-on SKU |
| R3 | **Managed Google Ads ("Autopilot")** | Agent runs the campaigns inside a spend ceiling the owner sets | ASSUMPTION 10% of managed spend, min R500/mo · FOUNDER DECISION | Fee ledger + disclosure (Google's third-party policy requires transparent fees) |
| R4 | **Google Local Booster (once-off setup)** | Claim/verify, categories, 10 photos, 4 posts, review-reply backlog, review template | ASSUMPTION R1,500 once-off | **Nothing. Sellable this week, manually** |
| R5 | **Payment-rail margin on Google-sourced orders** | Existing rails take-rate on orders the loop creates | Existing (see payment-rail fee memo) | Built |
| R6 | **AI credits** | Post drafts, reply drafts, post images | Existing credit pricing (image 8 credits) | Built |
| R7 | **WhatsApp review-request messages** | Template sends billed through the WhatsApp wallet | Pass-through + margin | Built |
| R8 | **Partner white-label** | Agencies run Flux Local for clients on the Agency/partner tier | R5,599/mo partner wholesale | Bulk multi-location UI |

Guardrails (FACT, from founder policy): pay first, no free trials or free months. Guarantee **leads** (calls + directions + WhatsApp clicks), not sales. Money-back if the lead floor is missed.

---

## 3. AI workers: orchestrator → agents → sub-agents

Every worker follows the existing Flux_* pattern: cron or manual run, then `flux-approval.ts` for approval (in-app or Slack buttons), then execution, tier-gated through `tier-gate.ts`, metered with AI credits. **Anything that spends money or speaks publicly is approval-gated by default.** Owners can opt into auto-approval per sub-agent, except spend, which always stays gated (same rule as `flux-ads-run`).

```
                    ┌──────────────────────────────────────────────┐
 L0 orchestrator    │  Flux_Local Growth Manager (weekly loop)     │
                    │  goal: leads/week & cost per paid order      │
                    └───────┬───────────────────────────┬──────────┘
 L1 agents          Flux_Local (organic)            Flux_Ads·Google (paid)
                    │                               │
 L2 sub-agents      ├ Profile Keeper                ├ Keyword Scout
                    ├ Review Concierge              ├ Ad Copywriter
                    ├ Review Harvester              ├ Campaign Builder
                    ├ Post Publisher                ├ Budget Pacer
                    └ Local Insights Analyst        ├ Negative-Keyword Gardener
                                                    ├ Conversion Closer
                                                    └ Audience Builder
```

| Worker | Does | Cadence | Gate | Reuses | Moves metric |
|---|---|---|---|---|---|
| **Growth Manager (L0)** | Reads the week's GBP insights + ads metrics + orders. Picks 1–3 actions. Writes the owner's Monday WhatsApp digest | Weekly | Plan is approved as a bundle | `merchant-daily-digest`, `flux-insights-run` | Leads/week, cost per paid order |
| Profile Keeper | Holiday/special hours, NAP consistency vs site and shop, missing attributes/categories | Weekly + SA public-holiday calendar | Category/name changes gated. Hours auto | `update_info`, `update_attributes` | Profile completeness |
| Review Concierge | Syncs reviews, drafts replies in the reviewer's language, escalates 1–2★ to the owner | Every 4 h (`ads-platforms-sweep`) | 4–5★ auto-reply opt-in. 1–3★ always gated | `ai_draft_reply`, `sentiment-analyze`, `sentiment-escalation-sweep`, `translate-ui` | Reply rate, reply time |
| Review Harvester | After a paid order, sends one review request on WhatsApp. Never to opted-out numbers, never with an incentive | On order paid | Auto (policy-bound) | `gbp_review_requests` | Reviews/month |
| Post Publisher | 1–2 GBP posts/week from the catalogue, offers and events, with an image | Weekly | Gated until 4 approvals in a row, then opt-in auto | `ai_draft_post`, `flux-loop-creative`, media routing | Views → actions |
| Local Insights Analyst | Calls/directions/clicks trend vs last period and vs scraped competitors | Weekly | Read-only | `insights`, `competitor-scrape-sweep` | Insight → action rate |
| Keyword Scout | Local intent keywords ("near me", suburb + service) with volumes | On campaign build, monthly | Read-only | `keyword_ideas` | CTR |
| Ad Copywriter | RSA headlines/descriptions from the taste profile, in the customer's language | On build/refresh | Gated (Google policy: advertiser approves) | `ai_ad_copy`, `taste-profile` | CTR, ad strength |
| Campaign Builder | Builds a **paused** Search campaign (location radius, schedule = opening hours, WhatsApp/call assets) | On request | Launch is gated (spend) | `create_campaign` | — |
| Budget Pacer | Holds spend to the ceiling. Moves budget to winners | Daily | Raising budget is always gated. Cutting is auto | `set_budget`, `set_status`, `ads_daily_metrics` | Cost per paid order |
| Negative-Keyword Gardener | Mines search terms, proposes negatives ("free", "jobs", other suburbs) | Weekly | Gated (bulk), auto for an obvious list | **New (RMF gap)** | Wasted spend % |
| Conversion Closer | Matches gclid → paid order and uploads it. Retries failures | Hourly | Auto | `match_ad_click_for_order`, `ads_conversion_uploads` | Conversions uploaded / paid orders |
| Audience Builder | Customer Match from consented customers (hashed). Lookalike-style expansion through PMax later | Monthly | Gated (consent confirmation) | `create_audience` | Repeat-order rate |

**Human roles this creates (not cuts):** a *Local Growth Specialist* who approves batches for 100+ locations and handles 1★ escalations, and a *Partner success* role for agencies. The Booster (R4) is done by a human first, then the agents take over the playbook.

---

## 4. Development plan

### Phase 0: unblock Google (founder-only, start today, calendar-bound)

| # | Action | Owner | Done when |
|---|---|---|---|
| 0.1 | Create the Workspace mailbox `ads@fluxmuse.com`. Verify `fluxmuse.com` in Search Console | Founder | DNS TXT verified |
| 0.2 | **Create and verify FluxMuse's own Google Business Profile.** This starts the ~60-day clock for the GBP API form | Founder | Profile verified |
| 0.3 | Create the FluxMuse Google Ads MCC. Accept API terms (Test Access token is issued at once) | Founder | Token in hand |
| 0.4 | Set `GOOGLE_ADS_DEVELOPER_TOKEN` (Test). Smoke-test against a Google Ads **test account** | Eng | Paused test campaign created via the app |
| 0.5 | Apply for Basic Access (answers + design doc in `ads-platform-approvals.md` §1) | Founder | Submitted |
| 0.6 | OAuth verification for `adwords` + `business.manage` (Limited Use line in /privacy, demo video §3) | Founder + Eng | Submitted |
| 0.7 | Submit the GBP API access form (§2) as soon as 0.2 allows | Founder | Submitted |

### Phase 1: monetisation plumbing (week 1–2)

- Add `checkAndConsumeUsage` / tier checks to `google-business` and `google-ads`, plus location limits per tier (R1).
- Add-on SKU for extra locations (R2) and the Booster once-off product (R4) in the existing checkout.
- `ads_managed_fees` ledger: monthly managed spend × fee, invoiced through the existing billing. Disclosure copy in the Ads hub and terms (R3).
- Public `/local` landing page with the pitch line and a "free Google Local check" lead form. The output is a human-run audit at first.
- **Acceptance:** a Starter account sees an upgrade prompt on a 2nd location. A managed-spend fee line shows up on a test invoice.

### Phase 2: Flux_Local agent (week 2–4)

- New `flux-local-run` function: L1 organic agent with Profile Keeper, Review Concierge, Review Harvester, Post Publisher and Insights Analyst as modules in `_shared/flux-local-logic.ts` (pure, unit-tested like `flux-seo-logic.ts`).
- Approval records through `flux-approval.ts`, Slack buttons for the founder's own tenant, in-app queue for customers.
- Per-sub-agent auto-approve toggles (never for 1–3★ replies).
- SA public-holiday table feeding Profile Keeper.
- **Acceptance:** on FluxMuse's own profile, one weekly run produces post + replies + hours proposals, approval publishes them, and the digest reaches the founder on WhatsApp.

### Phase 3: Flux_Ads·Google agent + Standard Access (week 3–6)

- Extend `flux-ads-run` with a Google branch: Budget Pacer, Negative-Keyword Gardener, Conversion Closer health. Spend is always gated, ceiling enforced server-side.
- Close the RMF gaps: negative keywords, ad-group/keyword/ad reporting, `ad_group_ad.policy_summary` display, pause/edit at each level.
- **"Google → WhatsApp → Rand" report** in the Ads hub: clicks → chats → paid orders → revenue → cost per paid order. This is the sales demo.
- Apply for Standard Access once RMF is green.
- **Acceptance:** on a test account, a gclid click, then a WhatsApp order, then payment shows as an uploaded conversion within 1 hour.

### Phase 4: L0 Growth Manager + partner scale (week 6–10)

- `flux-local-growth-run` orchestrator: weekly hypothesis → action → measure loop across both agents, one approval bundle, Monday digest.
- Bulk multi-location view + batch approvals for Flux_Partners (R8). Location groups.
- Performance Max for local/store goals once a customer has 30+ uploaded conversions.
- Lead guarantee tracker: leads/week vs the guaranteed floor, with a refund trigger.

### Phase 5 (H3): FluxMuse as the local-commerce network

- Aggregate demand across tenants: "near me" WhatsApp ordering, where one FluxMuse number routes a Google searcher to the nearest open tenant.
- Apply to Google Partners once managed spend qualifies. Partner status brings new-advertiser credits that can be packaged into the Booster offer. *Verify the current programme thresholds before promising anything.*

---

## 5. Revenue plays (Super Brain)

| Horizon | Play | Offer × buyers | Build between offer and invoice | Owner |
|---|---|---|---|---|
| **72 h** | Google Local Booster | ASSUMPTION R1,500 once-off + Starter R499/mo × first 5 buyers = R7,500 + R2,495/mo | **None.** Founder does it as a Manager on the client's profile. Gating step: a one-page offer + Paystack link | Founder |
| 30 d | Flux Local on tiers + review harvester live on FluxMuse's own profile | Upgrade pull Starter→Growth | Phase 1 + 2 | Eng |
| 90 d | Managed Google Ads with the closed-loop report | 10% of spend, min R500 × first 10 SMEs | Phase 3 + Basic/Standard Access | Founder + Eng |
| H3 | Local-commerce network + partner white-label | Partner R5,599/mo × agencies | Phase 4–5 | Founder |

First buyers by segment (names come from the founder, not this doc): Gauteng solo service businesses already in `08_Prospects` (two prospect files note no confirmed Google Business listing: Fifi's Kotas, Hyde Park Physiotherapy), WhatsApp enquirers already in FluxMuse, and the braiding/hair-studio case-study archetype.

---

## 6. Risks

| Risk | Mitigation |
|---|---|
| GBP API approval takes months (60-day profile age + review) | Booster sells manually now. Agents run on FluxMuse's own profile first |
| OAuth verification sent back on a domain mismatch | Workspace account on the same domain as the homepage and privacy page (pack §0) |
| Review gating or incentive breaches Google policy | Harvester asks every paid customer once, with no incentive and no sentiment filter before the ask |
| AI replies say something wrong in public | 1–3★ always human-approved. Replies quote no prices or medical claims |
| Ad spend runaway | Server-side ceiling. Budget raises always gated. Daily pacer |
| Fee on spend seen as hidden | Fee shown in the hub, on the invoice and in the terms (Google third-party policy) |

---

## 7. Founder decisions needed

1. Extra-location price (R149/mo suggested).
2. Managed Google Ads fee (10% of spend, min R500 suggested) and which tiers can buy it.
3. Booster price (R1,500 suggested) and whether it includes the first month's subscription.
4. Location allowance per tier (1 / 3 / 10 suggested).
5. Go-ahead for Phase 0.1–0.3 today. 0.2 starts the critical-path clock.

---

```
SUPER BRAIN STATUS — FluxMuse / Flux Local + Google Ads — 2026-10-12
Sector: SaaS → SMB marketing & WhatsApp commerce (Africa)   Business model: subscription + rails take-rate + credits
Stage: pilot     Revenue last 30d: [[founder to confirm]]
AI already present (this scope): 4 items (google-business AI drafts, google-ads AI copy, flux-ads-run Meta boost, flux-seo-run) — 0 R / 0 C measured / Google pieces Z (switched off pending approval)
72h play: Google Local Booster — R1,500 + R499/mo × 5 = R7,500 + R2,495 MRR — founder
30d plays: Flux Local tier pull + harvester on own profile
90d plays: Managed Google Ads with closed-loop "Google → WhatsApp → Rand" report
H2 workflows in redesign: local profile ops, review ops, paid search ops
Belts: n/a (team size 1)   Bridge packages built: 0 (new roles: Local Growth Specialist, Partner success)
Owner capacity: Booster ~3 h per client × 5 = 15 h this week / [[founder hours available]]
Next loop runs: 2026-10-19
```
