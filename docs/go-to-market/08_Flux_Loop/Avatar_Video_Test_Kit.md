# AI Brand Ambassador: stage 0 test kit

**Status: TEST PLAN.** Nothing here is a product feature. Don't promise avatar
videos to any brand, and don't mention them in external materials, until this
test passes and the feature ships.

**The question this test answers:** will small business owners actually *post*
an AI-presenter video under their brand, and does it bring more WhatsApp
conversations or orders than simpler video formats? A "wow" reaction to a demo
isn't the answer we need.

**Run time:** 2 weeks, one sprint (see `Sprint_Report_Template.md`).
**Who:** 6–10 Gauteng pilot brands. **Owner of the test:** `[[NAME]]`.

---

## 1. Pick the brands

Choose 6–10 brands from the 12 pilot brands, aiming for a mix:

| Need | Why |
|---|---|
| At least 3 solo entrepreneurs (beauty, fashion, food) | Biggest launch segment, and the camera-shy problem is sharpest there |
| At least 2 SMEs | They have more products and budget, and are likelier Growth upgrades |
| At least 2 brands whose customers mostly speak isiZulu or Sesotho | Tests the local-voice promise, the riskiest assumption |
| At least 1 owner who already films themselves | Tests whether the avatar beats the real owner |
| Already posting on WhatsApp Status or Facebook at least weekly | We need a real posting habit to measure against |

**Leave out** for this test anything in regulated categories: financial products,
insurance, property, health or medical claims, alcohol, gambling, weight loss.
An AI presenter in those categories looks like the deepfake scams people
already know about, and there are advertising and consumer-law risks.

**Consent first.** Before you make anything, get written consent on WhatsApp
covering:
- making AI videos about their products;
- using their product photos;
- their choice of whether to post (no pressure either way);
- sharing anonymised results internally.

| # | Brand | Segment | Category | Main language | Self-films? | Consent date |
|---|---|---|---|---|---|---|
| 1 | `[[ ]]` | `[[Solo/SME]]` | `[[ ]]` | `[[ ]]` | `[[Y/N]]` | `[[ ]]` |

---

## 2. The three formats

Make all three formats for **the same product and the same offer** for each
brand, so the only thing that changes is the format. Each video is vertical
9:16, 20–30 seconds, with burned-in captions.

| Format | What it is | Hypothesis |
|---|---|---|
| **A. Avatar sandwich** | AI avatar speaks the hook (3–5 s), then product footage and photos with the avatar's voice over them, then the avatar again for the call to action (last 3 s) | Owners will post it, and a face performs better than no face |
| **B. Product + voiceover** | Product footage and photos only, AI voiceover in the brand's language, captions. No face | Covers most of the value at lower cost and with no uncanny-valley risk |
| **C. Owner selfie, AI-edited** | The owner records one 10-second phone selfie (hook + call to action). We cut it with product footage, captions and music | A real face beats an AI face, if the owner will film |

If an owner won't film for C, write that down. It's a result in itself: it
tells us how many owners really are camera-shy.

### Shared script skeleton (same words in every format)

Write it from the brand's **Taste Profile** AI brief (`Taste_Profile_Template.md`,
Part G). Use the brand's language mix, and say no claims the owner can't back up.

```
HOOK (0–4 s):     [[one line that stops the scroll, from the Taste Profile's hooks to test]]
PROOF (4–20 s):   [[what it is, why it's good, price, one real trust signal]]
OFFER (20–25 s):  [[price / deal / deadline, only if real]]
CTA (25–30 s):    "Tap the link to WhatsApp us" / "Send us a message to book"
```

**Rules for format A:**
- The avatar speaks *as the brand's presenter*: "At [[BRAND]] we…". It never
  says "I bought this", "I tried this" or anything that sounds like a real
  customer's testimonial.
- The video carries an on-screen label in the corner the whole time, e.g.
  **"AI presenter"**. Also turn on the "AI-generated" label on Meta or TikTok
  if the video is posted there.

---

## 3. Making the videos (manual)

**Avatars.** Use 4–6 avatars made for this test with one of the image tools
below. Each must face the camera, with even lighting, mouth closed, chest up,
and a plain or softly blurred background.
- Make avatars that fit our real customers: everyday Gauteng presenters, a mix
  of ages and genders, in normal clothes. Don't match ethnicity to industry.
- Check that each avatar doesn't closely resemble a real, recognisable person.
- Keep a record of how each avatar was made: tool, prompt and date.
- Use each avatar for no more than 2 brands, to test the shared-face problem
  without overdoing it.

**Tools to try** (free trials or pay-as-you-go; note what each costs):

| Step | Option 1 | Option 2 |
|---|---|---|
| Script | Gemini (already in the product) | — |
| Voice | Google Cloud Text-to-Speech | ElevenLabs or similar |
| Talking avatar | Veo 3.x, image to video with speech (already in the product for video) | HeyGen or D-ID trial |
| Edit (all formats) | CapCut | — |

**Check the voice first**, before making any video: can each tool say the
script naturally in isiZulu, Sesotho and South African English? Record the
answer in §6. If none can do isiZulu or Sesotho naturally, the local-language
promise fails in version 1, which is a key finding.

**Keep a log for every video:** tool, cost in rands (credits converted), number
of attempts, minutes of staff time, and what went wrong (lips out of sync, odd
teeth or hands, mispronunciations, voice changing between clips).

---

## 4. Showing the owner (and asking the right questions)

Send all three videos together, labelled 1, 2 and 3 **in a random order**, not
A/B/C, so the order doesn't sway them. Ask the questions below on a short call
or by WhatsApp voice note. Don't sell; just listen.

1. "Which one would you post today, under your business name?" *(Which, and
   why? If none, why not?)*
2. "Is there anything in any of them that looks off, fake or embarrassing?"
3. *(After they've answered 1 and 2, tell them which one uses an AI presenter.)*
   "Does knowing it's AI change whether you'd post it?"
4. "How do you think your customers would react if they knew?"
5. "If FluxMuse made videos like your favourite every week, what would that be
   worth to you a month?" *(Let them name a number first, then compare it with
   Growth at R1,999/mo.)*
6. *(Only if they never filmed format C:)* "What stops you filming yourself?"

Write their exact words. Owner answers aren't the result; posting and
conversations are (§5). They tell us *why*.

---

## 5. Posting and measuring

Ask each owner to post the videos they're willing to post, **one per format,
about 3 days apart**, on the same channel at the same time of day. Rotate
which format goes first across brands.

- Use a different link per video: a separate wa.me short link or tracking code
  in each caption ("Send 'GLOW1' to book" or similar), so each conversation can
  be traced back to a video.
- WhatsApp Status can't be posted through the API, so owners post by hand.
  Note whether they actually did, and when.
- Don't run paid ads in this test. Keep it organic so spend doesn't skew the
  comparison.

**Measure for 72 hours after each post:**

| Measure | Source |
|---|---|
| Did the owner post it? (Y/N, date and time) | Owner, screenshot |
| Views / Status viewers | Platform |
| WhatsApp conversations started from that video's code or link | FluxMuse inbox |
| Orders / paid bookings from those conversations | FluxMuse orders |
| Any customer comments about it being AI, fake or a scam | Inbox and comments (paraphrased, no names) |

The numbers are small, so look for clear differences and patterns across
brands, not statistical significance.

---

## 6. Scoring sheet

One row per brand per format.

| Brand | Format | Owner would post? | Actually posted? | Views | Conversations | Orders | "AI/fake" comments | Quality issues seen | Cost (R) | Attempts | Staff min |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `[[ ]]` | A | `[[Y/N]]` | `[[Y/N]]` | `[[ ]]` | `[[ ]]` | `[[ ]]` | `[[ ]]` | `[[ ]]` | `[[ ]]` | `[[ ]]` | `[[ ]]` |
| `[[ ]]` | B | | | | | | | | | | |
| `[[ ]]` | C | | | | | | | | | | |

**Voice check** (before any videos):

| Tool | South African English | isiZulu | Sesotho | Notes |
|---|---|---|---|---|
| `[[Google TTS]]` | `[[natural / OK / poor / not available]]` | | | |
| `[[Veo speech]]` | | | | |
| `[[other]]` | | | | |

**Quality bar for format A:** a video fails if any one of these is true: lips
visibly out of sync, distorted teeth, hands or face, a mispronounced brand or
product name, the voice changing between the hook and the call to action, or
the owner calling it embarrassing.

---

## 7. Decision gates

At the end of the sprint, fill this in and decide.

| Gate | Pass if | Result |
|---|---|---|
| **Owners post it** | At least half of owners actually posted format A | `[[ ]]` |
| **It works at least as well** | Across brands, A brings at least as many conversations per post as B | `[[ ]]` |
| **No trust damage** | No owner reports customers calling it fake or a scam; no more than 1 such comment per brand | `[[ ]]` |
| **Quality** | At least 80% of format A videos pass the quality bar within 2 attempts | `[[ ]]` |
| **Local voice** | At least one tool sounds natural in isiZulu or Sesotho | `[[ ]]` |
| **Cost** | Real cost per finished A video, including failed attempts, known and under `[[R ]]` | `[[ ]]` |

**What to do with the result:**
- **All gates pass:** go to stage 2 (avatar studio for Growth and up), with the
  guardrails from the strategy discussion.
- **A fails but B does well:** ship stage 1 (product + voiceover videos) first.
  Retest avatars in 6 months as the models improve.
- **C wins clearly:** prioritise owner-led video (simple filming prompts plus
  AI editing), and jump to the consented owner digital twin later.
- **Local voice fails:** launch any video feature in English first, say so
  plainly, and keep testing local voices.
- **Trust gate fails:** stop avatar work. Don't retry until the disclosure
  approach changes.

**Decision:** `[[ ]]` · **Decided by:** `[[ ]]` · **Date:** `[[ ]]`

---

## 8. Message to owners (WhatsApp, under 600 characters)

> Hi `[[FIRST NAME]]`, we're testing a few new video styles for `[[BRAND]]` this sprint, all made by FluxMuse from your product photos, and one uses an AI presenter. It's free and you choose what (if anything) to post. Can we use your `[[PRODUCT]]` photos and send you 3 short videos by `[[DATE]]`? Reply YES and I'll send them over, with a quick 3-question check after.

Never present this to a pilot brand as a feature they'll get, and don't mention
upgrading to Growth during the test.
