# FluxMuse pitch decks: guide

Four 16:9 PowerPoint decks for selling FluxMuse, all built from one script and one facts file
(`../00_FACTS_AND_ASSUMPTIONS.md`). Every slide has a 60–120-word talk track in the speaker notes.

| File | Slides | Use it for |
|---|---|---|
| `FluxMuse_Brand_Pitch_Deck.pptx` | 30 (23 core + 7 appendix) | The master. Mixed or unknown audiences, events, and as the source to copy slides from. |
| `FluxMuse_Pitch_Solo_Entrepreneurs.pptx` | 16 (14 core + 2 FAQ) | Founder-run businesses of 1–5 people. Starter R499, Founding Member R349. Short, self-serve close. |
| `FluxMuse_Pitch_SMEs.pptx` | 25 (19 core + 6 appendix) | Businesses with 5–200 staff. Growth R1,999 / Scale R4,999. Adds a platform stack slide and an integrations & teamwork slide. |
| `FluxMuse_Partner_Programme_Deck.pptx` | 24 (18 core + 6 appendix) | Agencies, freelancers and resellers managing 5–50 clients. Wholesale R5,599/mo, illustrative economics, onboarding, co-marketing. No Founding Member offer. |

Enterprise isn't a launch target: there's no Enterprise deck. Handle inbound enterprise
conversations with the SME deck plus a proposal.

## Which deck when

- **Don't know yet?** Open with the master and ask the questions in slide 1's notes. Jump to the matching segment slide (10, 11 or 12).
- **Solo owner-operator, sells on Instagram, Facebook or WhatsApp:** Solo deck.
- **Has staff, several tools, or several brands or locations:** SME deck.
- **Manages marketing for clients:** Partner Programme deck. Never show agencies Founding Member prices.
- **Prospect outside South Africa:** use the appendix regional pricing (NGN, KES, GHS, USD). If their country has no payment rail (including Botswana and Namibia, "coming soon"), show no prices; share `[[WAITLIST LINK]]`.

## Master deck running order

1 Title · 2 The reality for SA businesses · 3 Meet FluxMuse · 4 How it works · 5 Your AI marketing team ·
6 Sell inside the chat · 7 One platform, every channel · 8 Get paid locally · 9 Built for you ·
10 Solo entrepreneurs · 11 SMEs · 12 Agencies & partners · 13 Partner model (illustrative economics) ·
14 See it in action · 15 How we work together · 16 Proof: the Gauteng pilot · 17 Case study template ·
18 Pricing (ZAR) · 19 Plans at a glance (editable table) · 20 Founding Member offer · 21 Trust & compliance ·
22 What's coming · 23 Next steps · 24 Appendix divider · 25 A1 Regional pricing · 26 A1 Local-currency table ·
27 A2 Payment rails by country · 28 A3 Partner wholesale pricing · 29–30 A4 FAQ

## Filling the placeholders

Anything in `[[DOUBLE BRACKETS]]` must be replaced or deleted before a deck leaves the building.
Search for `[[` in PowerPoint (Find, Ctrl/Cmd+F) to find them all.

| Placeholder | Slide | Fill with |
|---|---|---|
| `[[PROSPECT NAME]]`, `[[DATE]]`, `[[PRESENTER]]` | Title | Business name, meeting date, your name and title |
| `[[CONTACT NAME]]`, `[[EMAIL]]`, `[[WHATSAPP NUMBER]]` | Next steps | Your details |
| `[[wa.me QR CODE]]`, `wa.me/[[NUMBER]]` | Next steps | Paste a QR image over the dashed box; number in international format, no + or spaces |
| `[[CONFIRM TERMS]]` | FAQ | Cancellation terms, once the founder confirms them |
| `[[TBC]]` | Partner: onboarding, co-marketing | Partner obligations, minimum clients, brand/POPIA standards, co-marketing support |
| `[[FOUNDER DECISION: referral commission %]]` | Partner: co-marketing | Referral commission, once decided |
| `[[WAITLIST LINK]]` | Appendix divider notes | Waitlist URL for gated countries |
| Case study fields (`[[BRAND NAME]]`, `[[N]]`, quote, logo, photo) | Case study (image) | Only in December 2026, with measured pilot data and signed consent. Until then leave the slide as a template, or hide it |

## Slide swap guide

- **Tailoring the master:** keep one segment slide (10, 11 or 12) and hide the other two. Hide 13 (partner model) and A3 for non-agencies. Hide 17 (case study) if you're short on time.
- **Instagram-first prospects:** keep slide 7 and say plainly that Instagram is in Meta review. Start them on WhatsApp and Facebook.
- **Live demo:** slide 14. Only walk the catalog, cart and confirmation steps; the payment-method screens on the live demo list a provider outside the five rails.
- **December 2026 onwards:** replace slides 16–17 with the consented pilot results and the finished case study. Don't show projected results before then.
- **After 31 January 2027:** remove or replace the Founding Member slide (20) and the Founding Member row of the pricing table (19), and the matching lines on the Solo and SME segment slides.
- **Mixing slides across decks:** copy from the master (Reuse Slides / Keep source formatting). Speaker notes in the variant decks are tailored to that audience, so re-read them after copying.

## Rules (from the facts file)

- **Prices:** Starter R499 · Growth R1,999 · Scale R4,999 · Agency R7,999 per month. Annual = 10× monthly. Enterprise "from R19,999", inbound only. 14-day free trial, no card required.
- **Founding Member:** South Africa, 1 Dec 2026 – 31 Jan 2027. 30% off the first 2 monthly bills (R349 / R1,399 / R3,499) or 2 extra months on annual. Badge and priority support, with **no duration** stated. Never for the Agency tier. Never "for life".
- **Partners:** Agency tier at R5,599/mo wholesale (30% off), ongoing, never presented as a launch discount. The R24,401 spread (20 clients × R1,500) is always labelled illustrative. Never quote a fixed margin percentage.
- **Pilot pricing** (R249 / R999 / R2,499 / R3,999) is for the 12 Gauteng pilot brands only. It isn't in these decks.
- **Rails:** only Yoco, Ozow, Paystack, pawaPay and Fincra; 23 countries; Botswana and Namibia "coming soon". Never mention SnapScan, Stitch, Flutterwave, PayFast or M-Pesa direct.
- **Channels:** Instagram is "in Meta review". TikTok, LinkedIn, X, YouTube, Threads and Pinterest are "coming soon".
- **Claims:** no customer counts, ratings, testimonials, "guaranteed" or projected results. Trust claims are limited to POPIA/NDPR/GDPR ready, verified Meta Tech Provider, row-level security, encrypted tokens, audit export, and data export and deletion. If asked for certifications or a DPA, follow up in writing.
- **Accessibility:** no white text on Flux Orange (use Night or Ink); orange text on white uses Deep Orange #C24E00; body text 14pt minimum.
- **Fonts:** Poppins (headlines) and Inter (body). Install both before presenting or editing, otherwise PowerPoint substitutes a fallback font and line breaks may shift.
- **Screenshots:** use only images marked deck-safe in `../assets/ASSETS_INDEX.md`. Never the live home hero, the agencies page, SnapScan screens or anything in `assets/charts/`.

## Rebuilding

Edit `../_build/brand_deck/build_deck.py` (not the .pptx files) so that all four decks stay consistent, then:

```bash
cd docs/go-to-market/_build/brand_deck
python build_deck.py   # needs python-pptx + Pillow; embeds the current images from ../../assets
python qa_deck.py      # notes, fonts, overlaps, forbidden claims, headless-Chrome preview in ./preview
```
