# 08 Prospects: first 20 South African prospects

Prepared 2026-09-26. Everything here is written to [CURRENT_OFFER.md](CURRENT_OFFER.md), which supersedes the 11 Sept pack where they differ.

| File | What it is |
|---|---|
| [Outreach_Playbook.md](Outreach_Playbook.md) | Sequencing, pre-flight gates, cadence, call plan, objections, kill criteria. Read first. |
| [Prospect_List.xlsx](Prospect_List.xlsx) | Ranked list, pipeline maths (yellow cells are inputs), sources, outreach rules |
| [Prospect_Briefs.docx](Prospect_Briefs.docx) | Internal briefs: facts with sources, pains (observed or inferred), opening message, gaps. Not for prospects. |
| [proposals/](proposals/) | One client-facing proposal per prospect (`NN_slug.docx`, about 6 pages) |
| [CURRENT_OFFER.md](CURRENT_OFFER.md) | Prices, policy, live / in-setup / not-available capabilities, never-write list |
| [SCHEMA.md](SCHEMA.md) | JSON record format for `data/` |
| `data/` | One JSON per prospect, plus fact-check reports (`_verification_*.md`). `*.DROPPED.json.txt` failed verification. |

## Rebuild

From `docs/go-to-market/_build/prospects/` (needs `python-docx`, `openpyxl`, `pillow`):

```bash
python build_prospects.py --check
```

```bash
python build_prospects.py
```

`--check` validates every record (forbidden wording, opt-out line, counts) without building.

## Status and caveats

- Nothing has been sent. Every message must be human-sent through a channel the business publishes (POPIA s69).
- Placeholders still open: `[[GUARANTEE TERMS]]`, VAT wording, checkout fee wording, partner price for agencies.
- Instagram and Facebook facts were verified by a summariser only; contact routes were not tested. Hand-check both before sending.
- Realistic expectation: about one paying merchant from these 20 (see Pipeline maths).
