# Voice (text-to-speech) options by language

Research notes for the avatar test and the later language sprints. Compiled
2026-10-05 from web search results only: the vendors' own pages (Microsoft,
Google, ElevenLabs, Lelapa, CSIR, Botlhale, Hugging Face) were blocked from
this environment, so **verify every row on the vendor's page before buying or
publishing**. Language support changes often.

**Scope now:** South African English and Afrikaans (founder decision,
2026-10-05). Everything else here is for later sprints, as businesses that
need those languages come on board.

## The short version

- **One commercial vendor covers the most South African ground: Microsoft
  Azure Speech.** It has Afrikaans (`af-ZA`: Adri, Willem), isiZulu (`zu-ZA`:
  Thando, Themba), South African English (`en-ZA`) and Swahili (`sw-KE`), on
  pay-as-you-go pricing with a free monthly allowance. Nothing else found has a
  commercial isiZulu voice except the South African specialists below.
- **Google Cloud Text-to-Speech** has Afrikaans (`af-ZA`, Standard voices since
  2021) and Swahili (`sw-KE`, Chirp 3 HD), with a free tier (about 4M
  characters a month on Standard voices, 1M on Chirp 3 HD, per the pricing
  pages found). No isiZulu, isiXhosa, Sesotho or Setswana.
- **ElevenLabs v3** (the engine Higgsfield wraps) has Afrikaans, Swahili and
  Hausa, but **not** isiZulu, isiXhosa or Sesotho.
- **isiXhosa, Sesotho and Setswana** have no voice at Azure, Google or
  ElevenLabs. The options are the South African specialists: **Lelapa AI's
  Vulavula** (API, says it offers text-to-speech; 100 free calls per key),
  **Qfrency** (CSIR, all 11 official languages, sold business-to-business
  through a licensing partner, no self-serve) and **Botlhale AI** (enterprise
  call-centre focus). Confirm each one's language list and whether advertising
  use is covered.
- **Open source:** Meta's MMS covers nearly every language here (isiZulu
  `zul`, isiXhosa `xho`, Sesotho `sot`, Setswana `tsn`, Afrikaans `afr`,
  Swahili `swh`, Nigerian Pidgin `pcm`) but is **non-commercial**
  (CC-BY-NC 4.0): good for the internal voice check, never for a published
  video. No open-source voice with a commercial licence was found for any
  South African language other than English. Kokoro (Apache 2.0) is English
  and a few European and Asian languages; Piper has no Afrikaans or Bantu
  voices. The NCHLT speech corpora (about 56 hours each of isiZulu, isiXhosa
  and Sesotho, CC-BY 3.0) could train one, but that's a project, not a tool.
- **Nigeria:** **9jaLingo** sells Nigerian Pidgin, Yoruba, Igbo and Hausa
  voices (240+ speakers) in naira, commercial use allowed, with a free starter
  allowance. **Spitch** covers Yoruba, Hausa, Igbo and Amharic. **YarnGPT** is
  an open model for Nigerian-accented English, Yoruba, Igbo, Hausa and Pidgin
  whose licence wasn't stated in what was found: check before any commercial
  use.

## By language

Publishable = a licence that allows use in FluxMuse's own or a customer's
advertising. Check-only = internal voice check only.

| Language | Publishable options found | Check-only | Suggested first try |
|---|---|---|---|
| South African English | Azure `en-ZA` (Leah, Luke); Google; ElevenLabs (no SA accent); Kokoro (British `bf_emma`, Apache 2.0) | — | Azure `en-ZA`, or Kokoro if staying open source |
| Afrikaans | Azure `af-ZA` (Adri, Willem); Google `af-ZA` Standard; ElevenLabs v3 | MMS `afr` | Azure or Google `af-ZA` (both cheap; Google has a free tier) |
| isiZulu | Azure `zu-ZA` (Thando, Themba); Vulavula (verify); Qfrency (B2B) | MMS `zul` | Azure `zu-ZA` |
| isiXhosa | Vulavula (verify); Qfrency (B2B); Botlhale (enterprise) | MMS `xho` | Vulavula trial (100 free calls) |
| Sesotho | Vulavula (verify); Qfrency (B2B); Botlhale (enterprise) | MMS `sot` | Vulavula trial |
| Setswana | Qfrency (B2B); Botlhale (enterprise); Vulavula (verify) | MMS `tsn` | Ask Lelapa and CSIR |
| Swahili | Azure `sw-KE`; Google `sw-KE` (Chirp 3 HD); ElevenLabs v3 | MMS `swh` | Google `sw-KE` (free tier) |
| Nigerian Pidgin | 9jaLingo | MMS `pcm`; YarnGPT (licence unclear) | 9jaLingo starter allowance |
| Yoruba, Igbo, Hausa | 9jaLingo; Spitch; ElevenLabs v3 (Hausa only) | YarnGPT (licence unclear) | 9jaLingo |

## What this means for the test

- **Now (SA English + Afrikaans):** the Colab notebook's Kokoro voice is fine
  for English. For a publishable Afrikaans voiceover use Google (`af-ZA`,
  free tier) or Azure (`af-ZA`). MMS `afr` in the notebook is for the voice
  check only.
- **When isiZulu comes in:** Azure `zu-ZA` is the simplest route, and the same
  account then covers English and Afrikaans. Put a fluent isiZulu speaker on
  the voice check before trusting it.
- **isiXhosa, Sesotho, Setswana:** expect to work with a South African
  specialist. Start a Vulavula trial early, because its 100 free calls and
  90-day key expiry mean the check has to be planned.
- **Every voice, every language:** the quality bar in the kit still applies
  (brand name said the same way every time, "R149" read as rand, no voice
  drift between clips), and a fluent speaker rates naturalness.

## Sources

Search results, not the vendors' pages, which were blocked here.

- Azure Zulu voices: [Themba (zu-ZA-ThembaNeural)](https://json2video.com/ai-voices/azure/voices/zu-za-thembaneural), [Thando](https://json2video.com/ai-voices/azure/voices/zu-za-thandoneural), [Azure Zulu list](https://json2video.com/ai-voices/azure/languages/zulu/); Afrikaans [Adri](https://json2video.com/ai-voices/azure/voices/af-za-adrineural/), [Willem](https://json2video.com/ai-voices/azure/voices/af-za-willemneural/); [Azure language support](https://learn.microsoft.com/en-nz/azure/cognitive-services/speech-service/supported-languages)
- Google: [Chirp 3 HD voices](https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd), [voices list](https://docs.cloud.google.com/text-to-speech/docs/voices), [release notes (af-ZA added 2021)](https://docs.cloud.google.com/text-to-speech/docs/release-notes), [pricing and free tier summary](https://costbench.com/software/ai-voice-tools/google-cloud-text-to-speech/free-plan/)
- ElevenLabs: [languages supported](https://help.elevenlabs.io/hc/en-us/articles/32445761644433-What-languages-does-ElevenLabs-support-for-AI-narration), [v3 language expansion](https://alternativeto.net/news/2025/6/elevenlabs-v3-alpha-expands-text-to-speech-to-41-new-languages)
- Lelapa AI Vulavula: [docs](https://docs.lelapa.ai/), [language support](https://docs.lelapa.ai/overview/language-support), [product page](https://lelapa.ai/products/vulavula), [MIT Technology Review](https://www.technologyreview.com/2023/11/17/1083637/lelapa-ai-african-languages-vulavula/)
- Qfrency (CSIR): [CSIR overview](https://www.csir.co.za/converting-text-automated-south-african-languages), [commercialisation partner offer](https://innoget.com/technology-offers/9897/qfrency-text-to-speech-tts), [SA voices](http://www.inclusivesolutions.co.za/savoices)
- Botlhale AI: [company](https://botlhale.ai/), [profile](https://dabafinance.com/en/news/south-africas-botlhale-ai-builds-speech-tech-for-african-languages)
- Meta MMS: [model card](https://huggingface.co/facebook/mms-tts), [Swahili model](https://huggingface.co/facebook/mms-tts-swh)
- Nigeria: [9jaLingo pricing](https://naijalingo-frontend-dev.eastus.cloudapp.azure.com/pricing), [9jaLingo API docs](https://naijalingo-frontend-dev.eastus.cloudapp.azure.com/api-documentation), [Spitch interview](https://thecable.ng/interview-we-can-keep-nigerias-endangered-languages-alive-through-ai-says-temi-babalola), [YarnGPT](https://techpoint.africa/2025/02/04/how-unilag-student-created-yarngpt-ai/)
- Open corpora: [NCHLT speech corpus](https://www.isca-archive.org/sltu_2014/barnard14_sltu.pdf), [Coqui open speech corpora list](https://github.com/coqui-ai/open-speech-corpora), [Piper voices](https://raw.githubusercontent.com/rhasspy/piper/master/VOICES.md)
