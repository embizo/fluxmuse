# FluxMuse proposal templates

Word templates for the South African launch segments, plus a campaign proposal and a worked example.
All prices and claims come from `../08_Prospects/CURRENT_OFFER.md` (1 Oct 2026). If that file changes, rebuild
(see the end of this file) rather than editing prices by hand in every template.

Each template opens with a yellow **"How to use this template"** box. Work through it, then delete it.

## Which template to use

| Prospect | Template | Pages (approx.) | Main plans in the template |
|---|---|---|---|
| **Solo entrepreneur or side-hustle** (braiding and beauty, fashion resellers, home bakers, informal retailers) | `FluxMuse_Proposal_Solo_Entrepreneur.docx` | 8 | Nano R149 or Micro R289, Starter R499 as the step up |
| **SME** (5–200 staff) wanting set-up and a 60-day growth plan | `FluxMuse_Proposal_SME_Growth.docx` | 12 | Starter R499, Growth R1,999, Scale R4,999 |
| **SME** running one campaign (festive season, Black Friday, back-to-school, product launch) | `FluxMuse_Proposal_Brand_Campaign.docx` | 11 | Starter, Growth or Scale, with separate budget tables |
| **Agency or freelancer** managing several clients | `FluxMuse_Proposal_Agency_Partner.docx` | 9 | Agency list R9,999/mo; partner wholesale R6,999/mo |
| Worked example to learn from | `FluxMuse_Proposal_Sample_Braiding_Studio.docx` | 8 | An imagined braiding studio on Micro. Not a real client, no results |

Also in this folder: `Proposal_Snippets.md` (cover email, WhatsApp intro, follow-ups and objection handling).

Page counts are estimates. Check the real count in Word after filling in.

## The offer in one place

- **Nine tiers, ZAR per month** (annual = 10× monthly for 12 months): Free R0, Nano R149, Micro R289, Starter R499,
  Growth R1,999, Scale R4,999, Corporate R6,999, Agency R9,999, Custom by consultation.
- **Payment first.** Every paid plan starts with payment. The Free plan is a permanent plan (1 brand, 1 channel, no
  card), not a trial; mention it as an option, don't lead with it.
- **Founding Member** (live now, no end date set): South African sign-ups pay 30% less for their first two monthly
  bills on Starter, Growth and Scale (R349, R1,399, R3,499). A discount, not a free period. Not on Agency or partner
  wholesale. `[[FOUNDER TO CONFIRM]]` whether it also covers Nano and Micro.
- **Lead guarantee:** 3 qualified leads in 30 days of go-live (unique WhatsApp numbers that start a conversation
  through a FluxMuse-tracked link or QR). If fewer arrive and the merchant shared the link and posted at least weekly,
  we keep supporting them at no extra charge until 3 arrive. Always quote it with these conditions.
- **Agency partners:** wholesale R6,999/mo (30% off R9,999). Partner economics are always labelled illustrative:
  20 clients × R1,500 = R30,000, minus R6,999 = R23,001/mo gross spread before the partner's own costs.
- **Sender:** Thabo Malebadi, thabo@fluxmuse.com. Product at fluxmuse.ai.

## Fill-in checklist

- [ ] Pick the right template and save a copy named `FluxMuse_Proposal_[[CLIENT]]_[[YYYY-MM-DD]].docx`.
- [ ] Cover: client name, date, proposal number `FM-PRO-YYYY-###`, WhatsApp number, valid-until date (30 days).
- [ ] Search for `[[` and replace every placeholder. Filled fields keep yellow shading so a reviewer can check them.
- [ ] Use the client's own words in "What we heard", and tick only the pains they raised. Pains are hypotheses until confirmed.
- [ ] Choose one recommended plan and give a one-sentence reason.
- [ ] KPI tables: the target column is labelled **Target (goal)** and is agreed with the client.
- [ ] Optional service fees stay `[[TBC]]` until the founder publishes a services price list.
- [ ] Terms and POPIA: leave every `[[LEGAL REVIEW REQUIRED]]` for legal counsel.
- [ ] Get a second person to review, then clear the yellow shading (Home › Shading › No Colour) and search for `[[` once more.
- [ ] Delete the "How to use this template" box, update the contents list, save as PDF and send with the cover email.

## Rules

1. **No social proof.** FluxMuse has no paying customers, no cohort and no results yet. Don't write customer counts, ratings, testimonials or case-study numbers. The honest line: "we're opening with a small first group of businesses, and we set you up by hand." Case studies come later, only with written consent.
2. **Label every capability.** Live features are "newly launched": WhatsApp Concierge, hosted shop link, order alerts and SOLD, AI captions and images (POST), short AI video clips, voice-note transcription, WhatsApp Business set-up and broadcasts to consented contacts, answers in the customer's language, TikTok video posting.
3. **Being switched on, don't present as live:** Facebook and Instagram auto-posting (Meta approval), checkout through FluxMuse (not yet tested end to end with real money), AI Voice (beta, evaluated together), daily digest, FluxLoop ads, Shopify/WooCommerce/Takealot sync.
4. **Not available:** Instagram DMs and comments, X posting, paid checkout outside South Africa. Prospects outside South Africa join the waitlist; don't send them prices.
5. **Checkout fee wording** ("Card payments carry Paystack's standard fee (2.9% + R1), deducted before payout; EFT is 2%") is used only once checkout through FluxMuse has been tested end to end. Until then say it is being switched on.
6. **No trials and no cash-back offers.** Only the lead guarantee, with its conditions. Don't promise sales, revenue or ROI.
7. **No VAT line.** Fluxmuse (Pty) Ltd is not VAT-registered; the price shown is the amount charged.
8. **Never quote per-tier AI credit numbers.** Point to fluxmuse.ai/pricing.
9. **Screenshots:** check `../assets/ASSETS_INDEX.md` before adding an image. Don't use internal-only screenshots or anything from `assets/charts/`.
10. **Referral commission is undecided** (`[[FOUNDER DECISION: referral commission %]]`). Don't offer one.
11. **POPIA:** message only people who opted in or a business's own published enquiry channel, one to one, human-sent, with an opt-out. Blur customer names and numbers in any screenshot you share.

## Founder decisions and placeholders still open

- `[[FOUNDER TO CONFIRM]]` whether Founding Member covers Nano and Micro, and whether Nano includes its own WhatsApp number.
- `[[FOUNDER TO CONFIRM]]` reseller billing, partner directory and sub-account limits on the Agency tier.
- `[[FOUNDER DECISION: referral commission %]]`, basis, duration and payout for partner referrals.
- `[[TBC]]` Optional FluxMuse service fees and partner obligations.
- `[[FEE WORDING ONLY ONCE CHECKOUT IS TESTED]]` in every "How you'll get paid" section.
- `[[FLUXMUSE INFORMATION OFFICER NAME AND EMAIL]]` and hosting regions for the POPIA clause.
- `[[LEGAL REVIEW REQUIRED]]` All terms, operator agreement, cancellation, the lead guarantee wording, liability, governing law.

## Rebuilding and checking

```bash
python3 docs/go-to-market/_build/proposals/build_proposals.py   # writes the five .docx files here
python3 docs/go-to-market/_build/proposals/qa_proposals.py      # structure, placeholders, table headers, forbidden claims
```
