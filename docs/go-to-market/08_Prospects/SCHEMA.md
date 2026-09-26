# Prospect record schema

One JSON file per prospect in `docs/go-to-market/08_Prospects/data/<id>.json`, rendered to a Word proposal by
`_build/prospects/build_prospects.py`. Write **valid JSON only** (UTF-8, no comments, no trailing commas).
Plain sentences, South African English, no jargon. Rands as "R1,999" in prose. Dates as ISO `YYYY-MM-DD`.

The example below is synthetic. Replace every value with real, sourced content.

```json
{
  "id": "07-example-studio",
  "slot": "Beauty and fashion: braiding studio",
  "name": "Example Studio",
  "legal_or_trading_name": "",
  "segment": "creator|solo|sme|agency",
  "trade": "Hair braiding studio",
  "location": "Soweto, Johannesburg",
  "wave": 1,
  "why_wave": "One sentence.",
  "one_line_pitch": "What FluxMuse does for THEM, in one sentence, no hype.",

  "public_facts": [
    { "fact": "Takes bookings through Instagram DMs and a WhatsApp number listed on its profile.",
      "source": "https://example.com/page", "retrieved": "2026-09-26" }
  ],
  "businesses": [
    { "name": "Example Records", "what": "record label", "source": "https://example.com/about" }
  ],
  "channels_observed": ["Website has a WhatsApp chat button (example.com/contact)"],
  "decision_maker": "Role and, only if published on their own site or in reputable press, the name.",

  "approach": {
    "route": "The legitimate channel: official website enquiry form / published business email / management or booking / warm intro.",
    "contact_source": "URL where that route is published, or 'none found: needs warm intro'",
    "opening_message": "60-90 words, sent by a HUMAN. Who we are, why them (one specific, true observation), the ask (a 20-minute call), an opt-out line. No trial or discount language.",
    "compliance_note": "One sentence on why this route is appropriate (POPIA s69)."
  },

  "pains": [
    { "pain": "Booking enquiries arrive as DMs and get answered late.",
      "basis": "observed|inferred",
      "evidence": "If observed: what you saw and the URL. If inferred: the pattern typical for the trade.",
      "validate_with": "The one question to ask on the call." }
  ],

  "fit": {
    "attainability": 3,
    "revenue_potential": "R499/month (Starter)",
    "reasoning": "2-3 honest sentences, including what could make this a poor fit."
  },

  "recommended_plan": {
    "tier": "micro|nano|starter|growth|scale|corporate|agency|custom",
    "why": "One sentence tied to their business.",
    "upgrade_path": "One sentence: what would make the next tier worth it."
  },

  "what_we_would_do": [
    { "capability": "WhatsApp Concierge: photos to catalogue",
      "status": "live|in_setup",
      "for_them": "How it helps THIS business, concretely." }
  ],
  "first_30_days": [ { "week": 1, "actions": ["..."] } ],
  "we_would_track": ["WhatsApp conversations started from your shop link"],
  "objections": [ { "objection": "I already take orders on WhatsApp.", "response": "Honest, specific, no hype." } ],
  "related_reading": [ { "title": "...", "url": "https://fluxmuse.ai/blog/..." } ],
  "gaps": ["Anything you could not verify or find. Be blunt."]
}
```

Counts: `public_facts` 6 to 10; `pains` 3 to 5; `what_we_would_do` 4 to 6; `first_30_days` exactly 4 weeks;
`we_would_track` 3 to 5; `objections` exactly 3.

## Non-negotiables

1. **Every public fact has a source URL you actually opened**, and the fact is worded no more strongly than the source.
   If you can't source it, it doesn't go in `public_facts`. Put the gap in `gaps`.
2. **Never invent** an email, phone number, owner name, revenue, follower count, headcount, opening date or quote.
3. **Pains are hypotheses** (see `basis`). Never assert a pain as fact about a named business.
4. **Only capabilities from `CURRENT_OFFER.md` §3**, each with the right status. Nothing outside that list.
5. **No trial, free-period, discount, pilot, customer, result, or guarantee language.** Pricing goes in via the generator.
6. **Nothing about finances, health, family, legal matters, personal life or controversy.** Business facts only.
7. Skip anyone who is a minor, in a public legal dispute, or whose public presence is mainly personal.
