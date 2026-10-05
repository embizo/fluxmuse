# Avatar video test: run pack

Everything needed to run the stage 0 test in `../Avatar_Video_Test_Kit.md`.
The kit says *what* to test and how to decide. This folder says *who does
what, on which day*, and holds the materials.

| File | What it's for |
|---|---|
| `Runbook.md` | Day-by-day plan for the test owner (Thabo), with every message ready to send by hand |
| `Avatar_Test_Scoring.xlsx` | Brands, videos, voice check and tracking links, with the six decision gates calculated automatically |
| `Tracking_Codes.md` | How each video gets its own WhatsApp link and code, so every conversation traces back to one video |
| `FluxMuse_Dry_Run.md` | The whole test run on FluxMuse itself first ("brand 0"), with all three formats scripted |
| `Production_Prompts.md` | Avatar image prompts, the voice-check script, and the production log rules |
| `FluxMuse_Avatar_Test_Colab.ipynb` | Open-source route on a free Colab GPU: avatar images (SDXL / FLUX.1 schnell), English voice (Kokoro), Afrikaans voice check (MMS, internal only) and talking clips (SadTalker). Not yet run; treat the first run as a test |

**Order:** do the dry run on FluxMuse first. It tests the process, the tools
and the tracking on us before we ask any business for their time.

**What only a person can do:** recruit businesses, get consent, send the
videos to owners, post, and judge whether the Afrikaans voice sounds
natural (a fluent speaker must do that). Outreach is one to one and
hand-sent, never bulk (POPIA s69, `../../08_Prospects/CURRENT_OFFER.md` §6).

**Rebuild the notebook:** `python3 docs/go-to-market/_build/avatar_test/build_colab_notebook.py`.

**Rebuild the spreadsheet:** `python3 docs/go-to-market/_build/avatar_test/build_scoring_sheet.py`
(it overwrites the file, so copy it before you start filling it in, or fill in
a copy).
