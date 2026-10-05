# Production prompts and log rules

Higgsfield is the main tool for this test: one account covers images, voices
and talking video. Any other tool in the kit (HeyGen, D-ID, Google TTS, Veo,
CapCut) is fine as a comparison. Log what each one costs.

| Step | Higgsfield model | Notes |
|---|---|---|
| Avatar images | **Soul 2.0** (realistic, UGC-style people) or **Nano Banana Pro** | 9:16 or 3:4, one person, chest up |
| Same face across shots | **Soul Cast** or the **AI Influencer** builder | Keeps one presenter consistent across hook and call to action |
| Voice check and voiceovers | **ElevenLabs v4**, **Text to Speech v2** (ElevenLabs / MiniMax engines), **Seed Audio** | Try at least two engines per language |
| Talking avatar (format A) | **Seedance 2.5** (omni-reference: start image + audio reference) or **MiniMax H3** | Feed the avatar image and the voiceover; 9:16; 4–8 s for the hook, 3–5 s for the call to action |
| Product video (format B) | Image-to-video from product photos (e.g. **FLUX 3 Video**), turn off generated audio | Add the voiceover and captions in the edit |
| Edit, captions, "AI presenter" label | CapCut | Burn in the captions and the corner label |

The account needs credits first: it was on the free plan with 1.52 credits on
5 Oct 2026.

**Open-source route (no paid tool):** `FluxMuse_Avatar_Test_Colab.ipynb` runs on a
free Colab T4. It uses SDXL or FLUX.1 [schnell] for avatars, Kokoro for the
English voice and SadTalker for talking clips, all with licences that allow
commercial use (check each one, and every model SadTalker downloads, before
publishing). Meta MMS covers the isiZulu and Sesotho voice check, but it is
non-commercial, so it's for the internal check only and never in a published
video. Expect SadTalker's lip-sync to be weaker than the paid tools: that's
exactly what the quality bar measures.

---

## 1. Avatar roster (make 6, keep the best 4–6)

**Rules for every avatar** (from the kit §3):
- Faces the camera directly, even soft light, mouth closed, chest up.
- Plain or softly blurred background, everyday clothes.
- No logos, no text, no jewellery that moves.
- Everyday Gauteng presenters with a mix of ages and genders. **Don't match a
  face to an industry.** Any avatar can present any product.
- After generating, check the face doesn't closely resemble a real,
  recognisable person (do a reverse image search). Record the tool, prompt,
  seed and date in the log.

**Shared ending for every prompt:**
`Photorealistic vertical portrait, chest-up, looking straight into the camera, relaxed natural expression, mouth gently closed, soft even daylight, shallow depth of field, plain softly blurred background, natural skin texture, no text, no logo.`

| # | Prompt start |
|---|---|
| 1 | A friendly Black South African woman in her late 20s, short natural hair, plain mustard knit top, warm smile in her eyes, in a bright kitchen |
| 2 | A Black South African man in his early 40s, neat beard, navy crew-neck jersey, calm and reassuring, against a softly lit shop interior |
| 3 | A South African woman of mixed heritage in her mid 30s, hair tied back, denim shirt, open and practical look, in front of a plain green wall |
| 4 | A young Black South African man in his early 20s, short fade, plain white T-shirt, energetic but natural, on a sunny street, background blurred |
| 5 | A Black South African woman in her early 50s, headwrap, plain dark cardigan, kind and confident, in a softly lit living room |
| 6 | A South African Indian man in his 30s, short hair, olive polo shirt, approachable, against a neutral studio backdrop |

Keep a note of which businesses use which avatar. No avatar may be used for
more than 2 businesses.

---

## 2. Voice-check script

Generate the same short script with each voice tool, in each language. A
fluent speaker of each language rates every clip **natural / OK / poor / not
available** on the **Voice check** tab. **Don't rate isiZulu or Sesotho
yourself unless you're fluent.**

**South African English (source):**
> Sawubona! Are you still answering DMs at eleven at night? Send us your product photos on WhatsApp and we'll send you back a shop link, plus an assistant that answers your customers in their language. It's from R149 a month. Message us today.

**isiZulu and Sesotho:** have a fluent speaker translate the English source
before generating. Don't use machine translation for this test, because the
point is to judge the voice, not the translation. Paste the approved text
here:

- isiZulu: `[[translation by a fluent speaker]]`
- Sesotho: `[[translation by a fluent speaker]]`

**Also listen for:**
- The brand name "FluxMuse" pronounced the same way every time.
- "R149" read as "one hundred and forty-nine rand", not "R one four nine".
- No change in voice between two clips made with the same settings.

---

## 3. Video settings

| | Format A (avatar) | Format B (product + voiceover) | Format C (owner selfie) |
|---|---|---|---|
| Length | 20–30 s | 20–30 s | 20–30 s |
| Ratio | 9:16 | 9:16 | 9:16 |
| Face on screen | Avatar 0–4 s and last 3–5 s only | None | Owner 0–4 s and last 3–5 s |
| Middle | Product photos/clips, avatar voice over them | Product photos/clips, voiceover | Product photos/clips, owner's voice or voiceover |
| Captions | Burned in | Burned in | Burned in |
| Label | "AI presenter" in a corner, whole video | None needed (no AI face), but AI voice noted in caption if posted on Meta/TikTok | None |

---

## 4. Production log (one row per attempt, on the Videos tab)

Record for every attempt, including failed ones:
- business code and format;
- tool and model;
- cost in rand (convert credits at the plan's rate) and staff minutes;
- **quality bar check** (format A fails if any of these is true):
  - lips visibly out of sync;
  - distorted teeth, hands or face;
  - the brand or product name mispronounced;
  - the voice changing between hook and call to action;
  - the owner calling it embarrassing.
- **what went wrong**, in one line.
