# FluxMuse Brand Kit v1.0 (September 2026)

- **Web version:** `../FluxMuse_Brand_Kit.html` (single page, sticky section nav, light and dark themes, copy buttons for colours and copy blocks). Images are referenced as relative `assets/...` paths, so publish with `docs/go-to-market` as the root.
- **PDF:** `FluxMuse_Brand_Kit.pdf` (A4 landscape, light theme, one section per page break, nav hidden).

## Rebuild

```bash
cd docs/go-to-market/_build/brand_kit
node build.mjs        # src/*.html -> ../../FluxMuse_Brand_Kit.html, asset table from assets/ASSETS_INDEX.md, image_report.json
node export_pdf.mjs   # -> 01_Brand_Kit/FluxMuse_Brand_Kit.pdf (headless Chrome on port 9445)
node shots.mjs <dir>  # optional QA screenshots: 1440 and 390 wide, light and dark (port 9444)
```

Set `CDP_UDD` to a scratch directory for the Chrome profile. Edit content in `_build/brand_kit/src/`, not in the generated HTML. The asset library table and the optional revenue chart (`assets/charts/revenue_by_stream_fy1_fy5.png`, included only if present) are regenerated on every build.

## Sections

01 Brand story · 02 Who we serve · 03 Personality & voice · 04 Messaging house · 05 Logo · 06 Colour · 07 Typography · 08 Imagery & motifs · 09 Data visualisation · 10 Product in context · 11 Workflows · 12 Payments & markets · 13 Pricing & launch offer · 14 Pilot & proof · 15 Templates & channels · 16 Partners & resellers · 17 Legal & compliance · 18 Asset library · 19 Contacts & versions

## Needs founder input before external use

- Mission, vision and brand promise (v1.0 drafts), and the proposed alternate tagline "Your AI marketing team, right inside WhatsApp."
- Vector logo masters (`[[COMMISSION VECTOR LOGO]]`) and a fixed light logo (the "F" is clipped). Until then the kit prescribes the dark logo on Night for external work.
- Founding Member perks duration (`[[FOUNDER DECISION]]`); referral commission for partners; partner agreement terms.
- Agency segment promise: section 4b of the facts file still says "keep 40–60% margin", while the partner pricing rule says never quote a fixed margin. The kit follows the pricing rule; reconcile the facts file.
- Trademark registration status (`[[TM STATUS]]`); legal review of the trademark line and the WhatsApp POPIA opt-in wording.
- Native-speaker check of all isiZulu, Sesotho, Afrikaans, Nigerian Pidgin and Swahili sample phrases.
- Placeholders: `[[BRAND OWNER NAME]]`, `[[EMAIL]]`, `[[PHONE / WHATSAPP]]`, `[[SUPPORT HOURS]]`, `[[HOSTED BANNER URL]]`, `[[PILOT NAME]]`.
- Once pawaPay and Fincra go-live is confirmed (week of 14 September 2026), change "Live Sept 2026" to "Live" in section 12.
- Clear space, minimum sizes and post-spec safe zones are design recommendations; confirm platform specs before production.
