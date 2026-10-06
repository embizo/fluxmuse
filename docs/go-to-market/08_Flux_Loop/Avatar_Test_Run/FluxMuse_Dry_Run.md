# Dry run: FluxMuse as brand 0

Run the whole test on FluxMuse before asking any business. It tests the
tools, the timings, the costs and the tracking on us. The decision gates
still need real businesses, so this is a rehearsal, not a result.

**Brand:** FluxMuse · **Code:** 00 · **Taste Profile:**
`../FluxMuse_Taste_Profile.md` (v2) · **WhatsApp:** +27 74 242 6065 (Fluxy
answers)

**Product and offer:** the Nano plan, R149 a month, with Founding Member
(30% off the first two monthly bills for South African sign-ups). Both are
real and live. **Proof:** a verified Meta Tech Provider; our team sets the first
group up by hand. No customer claims, ever.

---

## The script (same words in all three formats)

Built from the Taste Profile's hook "Still answering DMs at 11pm?"

| Part | Time | Words |
|---|---|---|
| Hook | 0–4 s | "Still answering DMs at eleven at night?" |
| Proof | 4–20 s | "Send FluxMuse your product photos on WhatsApp and get a shop link back. Our assistant answers your customers in their language, day and night, and you get a WhatsApp alert for every order." |
| Offer | 20–25 s | "It's R149 a month. Sign up in South Africa now and your first two months are 30% off." |
| Call to action | 25–30 s | "Tap the link and say hi. Our team is ready to set your business up." |

**Caption** (all formats): `Still answering DMs at 11pm? 📱 Shop link from your photos, replies in your customers' language, an alert for every order. From R149/month. Tap to chat: <link>`

**What the presenter may not say:** "I use FluxMuse", "my business grew",
"free", "trial", or any number other than R149 and 30%.

---

## Format A: avatar presenter (`AV00A`)
1. Pick an avatar from the roster (`Production_Prompts.md` §1). Avatar 1 is
   suggested. Note it in the log.
2. Make the voiceover with the voice that scored best for South African
   English in the voice check.
3. **Hook clip:** the avatar image plus the hook audio, made in Seedance 2.5
   or MiniMax H3, 9:16, 4–5 seconds.
4. **Middle:** use the refreshed infographics as product visuals instead of
   screenshots. The old screenshots show "Start free trial"; see
   `../../assets/ASSETS_INDEX.md`. Use:
   - `whatsapp-commerce-flow_square`
   - `how-fluxmuse-works_square`
   - `founding-member-offer_square`

   Pan slowly across each one, with the proof and offer voiceover over them.
5. **Call-to-action clip:** the same avatar, 3–5 seconds.
6. **Edit:** burn in the captions and keep the **"AI presenter"** label in a
   corner for the whole video.

## Format B: product plus voiceover (`AV00B`)
Same voiceover and the same infographics, with no face. Open on the hook as
large text over `how-fluxmuse-works_square` for the first 4 seconds.

## Format C: founder selfie (`AV00C`)
Thabo records two vertical phone clips in good light:
- **Hook (4 s):** "Still answering DMs at eleven at night?"
- **Call to action (4 s):** "Tap the link and say hi. Our team is ready to set your business up."

Cut them around the same middle section, with Thabo's own voice or the
voiceover over it.

---

## Posting (FluxMuse's own channels)
- **Planned order:** C on day 1, A on day 4, B on day 7. **Actual:** B went first
  (6 Oct 2026); A and C not posted (founder prefers no avatar; C not filmed).
  Recorded on the sheet's Brands tab so the rotation isn't misread.
- **Where:** FluxMuse's WhatsApp Status and TikTok. TikTok video posting is
  approved; switch on its AI-generated label for A. Don't post to Facebook or
  Instagram through the app, because auto-posting isn't live; post there by
  hand only if you want to.
- **Paid boost:** none.
- **Links:** use the brand-0 links in `Tracking_Codes.md`.

## What the dry run should tell us
- **Cost and time:** what one finished video of each format really costs, in
  rand and staff time. This sets the cost-gate limit on the **Gates** tab.
- **Quality:** whether Seedance or MiniMax clears the quality bar within 2
  attempts.
- **Tracking:** whether the codes reach Live Chat, and whether Fluxy handles
  those chats sensibly.
- **Process:** anything in the runbook that's unclear or slow. Fix it before
  approaching businesses.

Record everything on the sheet as business `00`. Leave business 00 out of the
gate calculations: it's FluxMuse, not a test business. The **Gates** tab
already excludes it.

---

## Status (6 Oct 2026)

| Format | Status | What's needed |
|---|---|---|
| **B** (`AV00B`) | **Voiced version rendered:** `dry_run_output/AV00B.mp4`, 24 s, 1080×1920, Kokoro-82M (Apache 2.0) voice `bf_emma` (British English; Kokoro has no South African voice), captions burned in over the dark infographics. Voice generated here on CPU with kokoro-onnx. CTA re-voiced and re-rendered 5 Oct after the founder asked for the team line instead of a named person. Variants with `bf_isabella` and `bm_george` were made for the voice choice. The earlier no-voice timing draft is kept alongside. | **Posted 6 Oct 2026:** TikTok 08:15, WhatsApp Status 08:20 (SAST), with the `AV00B` link. Voice: emma. Measure 72 h later (9 Oct, ~08:20): views from screenshots, conversations by searching Live Chat for `AV00B`, orders, any AI/fake/scam comments. |
| **A** (`AV00A`) | **Rendered:** `dry_run_output/AV00A.mp4`, 24 s, emma voice, "AI presenter" label. Visuals: a 30 s animated avatar clip the founder made elsewhere (1280×720, cropped to 9:16) on the hook and CTA beats, infographics in the middle. The clip's own speech was a different script and opened in a customer's voice, so only the footage is used; the lips therefore don't match the words. A Wav2Lip re-sync was tried on CPU and its face detector failed on the cropped frames; not pursued. Note: the avatar's jacket has three shoulder stripes (adidas-style trade dress), so regenerate without it before any public use. **Founder's verdict on watching A next to B: the video is better with no avatar.** Recorded as the first trust-gate signal for business 00. | Nothing further unless the test businesses disagree. |
| **C** (`AV00C`) | **Not filmed.** | Two 4-second vertical clips by Thabo himself. Not made with someone else's photo or a generated "Thabo": format C tests the real owner's face, and a fake founder is what the trust gate forbids. Record on the sheet as "owner didn't film" until then; the kit counts that as a result. |

**Assembler:** `docs/go-to-market/_build/avatar_test/assemble_video.py` (ffmpeg via the
`imageio-ffmpeg` pip package, Poppins/Inter for captions). Examples:

```
python3 docs/go-to-market/_build/avatar_test/assemble_video.py B --audio <unzipped>/audio
python3 docs/go-to-market/_build/avatar_test/assemble_video.py A --audio <unzipped>/audio --clips <unzipped>/clips
python3 docs/go-to-market/_build/avatar_test/assemble_video.py C --audio <unzipped>/audio --clips <dir with selfie_hook.mp4, selfie_cta.mp4>
```

Format A carries the "AI presenter" label for the whole video. Nothing is
posted until the voiced versions exist and Thabo has watched them.

**Noted from the draft:** the infographics' small print is hard to read at
phone size, so the captions carry the message. If the voiced version still
feels busy, make simpler single-message stills for the proof and offer beats.
