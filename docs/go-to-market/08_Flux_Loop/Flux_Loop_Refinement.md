# Flux Loop refinement: ideas from HubSpot's "Loop" talk

Working notes, September 2026. Internal only.

**Source:** a conference talk by HubSpot's Kieran Flanagan and Kipp Bodnar on
their "Loop" marketing playbook (Express → Tailor → Amplify → Evolve). This doc
picks the ideas worth taking for the **Flux Loop** (Plan → Create → Publish →
Sell → Learn), maps each one to an agent or feature, and marks what's already
shipped and what's a proposal.

**Scope:** the loop product itself lives in `embizo/foundation-zero-point`
(React/Supabase). Every "Proposal" below is a product change to that repo, and
none of it is live. Claims rules from `00_FACTS_AND_ASSUMPTIONS.md` §4 still
apply: don't put any of the proposals in external materials until they ship.

---

## 1. The big shift, and why it favours FluxMuse

HubSpot's story in one line: **traffic volume fell sharply while leads grew,
because the visits they kept were worth more.** In their words, marketing has
moved from *volume of visits* to *value of visits*. Their funnel is now an
hourglass. Awareness is spread across many platforms, each of which works hard
to stop people leaving, so getting clicks is harder than ever. But AI makes
personalisation cheap, so conversion keeps getting easier.

The FluxMuse version of this:

- African SMB buyers already skip the website. They go **ad or post →
  WhatsApp chat → pay**. The narrow middle of the hourglass is a conversation,
  and that's where FluxMuse lives.
- HubSpot's loop stops at marketing. **The Flux Loop has a Sell stage**:
  catalog, cart and payment on 5 rails inside the chat. We don't have to
  estimate "closed-won" value, because we record it. That's the strongest line
  we can take from this talk.

**Proposal: change the north-star metrics from volume to value.** The Analyst
and all pilot reporting should lead with *conversations started, orders, GMV,
revenue per conversation*, and treat reach and followers as secondary. That
already matches the pilot KPI list in `00_FACTS` §6, so this is only a change
of emphasis.

Don't reuse HubSpot's own numbers (traffic drop, lead growth, ROAS uplift) in
our materials. They're HubSpot's claims about HubSpot, we haven't checked them,
and the talk's own ROAS maths doesn't add up (see §7).

---

## 2. How the two loops line up

| HubSpot Loop | Flux Loop | Agent | What to take |
|---|---|---|---|
| **Express**: put your taste and judgment into AI | **Plan** | Strategist | A living **Taste Profile** that every agent reads before it works (§3) |
| **Tailor**: fit content to audience and channel | **Create** | Creator | "Start short, double down on winners" plus one-to-many repurposing (§4) |
| **Amplify**: get it into the channels where buyers are | **Publish** | Publisher, Flux Ads | Creative volume is the new targeting; optimise ads for paid orders (§5) |
| *(no equivalent)* | **Sell** | WhatsApp commerce | Our edge: first-party order data closes the loop |
| **Evolve**: learn in real time, compound | **Learn** | Analyst | Two-week **Loop Sprints** with an auto-written sprint report (§6) |

**Naming recommendation:** keep "Plan. Create. Publish. Sell. Learn." It's
already on the brand kit, decks and infographics, and adding Sell is what makes
it ours. Put the taste idea *inside* Plan (it's what the Strategist plans
*from*) rather than adding a sixth step. A supporting line for copy:
*"Every loop learns. Every loop sells."*

---

## 3. Plan: the Taste Profile

**The idea.** Everyone has the same models and prompts, so AI output drifts
towards a "sea of sameness". When making content costs almost nothing,
*choosing* what to make is the valuable skill. You don't hand your taste to AI;
you write it down and teach it. HubSpot calls the written version a **taste
profile**. Unlike a brand style guide that sits in a folder, it's a living
document that changes as you learn, and AI reads it before making anything.

It has two parts:

1. **Customer taste.** Who the customer is, how they talk, what earns their
   trust, and what makes them stop scrolling.
2. **Brand taste.** The brand's stories: brand story, product story, "why
   you", "why now".

**Why it fits FluxMuse especially well:**

- "How they talk" is the multilingual Creator's home ground: isiZulu, Pidgin,
  Swahili, Afrikaans, code-switching and township slang, not textbook
  translation.
- Our customers' best voice-of-customer data is already in FluxMuse: their
  **WhatsApp conversations and orders**. Frequent questions, objections,
  compliments and the words buyers use can all feed the customer-taste half,
  with consent and within POPIA/NDPR.
- For a solo braiding studio, the "why you" story is usually the owner. Taste
  gives a one-person business an edge over generic AI content.

**Proposals (product):**

- **Onboarding interview → Taste Profile v1.** The Onboarding agent asks about
  10 questions, in the owner's language, by WhatsApp voice note or text, then
  drafts the profile. Pull in the business's existing posts and chats if they
  connect them.
- **One profile per brand, read by every agent.** It sits alongside the RAG
  memory the Analyst already has. The Creator, Flux Ads and the chatbot all use
  it, so the tone in posts, ads and chat replies matches.
- **The Analyst updates it.** After each sprint (§6), the Analyst suggests
  changes ("hooks about price did badly; before/after photos did well") and the
  owner approves or rejects them. That approval step is where the human's taste
  and judgment stay in charge.
- **Taste check before publishing.** The Creator scores each draft against the
  profile and marks anything that "could belong to any business" for rewriting.

**Proposal (GTM):** make the Taste Profile the first deliverable of every
pilot brand's onboarding call, and use it in case studies as a before/after
("generic AI post" vs "post written with this studio's taste profile"). That's
a clear, honest demo that doesn't need any results numbers.

---

## 4. Create: remarkable and relentless

**The idea.** AI-assisted content has multiplied, but attention hasn't, and
content now fades fast (a LinkedIn post is mostly done within a day; an email
gets half its opens in the first couple of hours). Picture a 2×2 of quality
against volume:

|  | **Low volume** | **High volume** |
|---|---|---|
| **Remarkable** | Invisible excellence | **Remarkable and relentless** ← aim here |
| **Generic** | Dead zone | Slop factory |

"Remarkable" means content built on things a generic model can't produce:
unique data, real customer stories, real examples. "Relentless" means doing it
at volume, which is now affordable with AI.

HubSpot's example was a solo creator who grew a large following alone, using two
moves:

- **Start short:** test 20–30 quick ideas (short videos, short posts) over a week
  or two, find the few that take off, then make longer, richer versions of those.
- **Start long:** make one long piece (video, newsletter), then cut it into
  pieces for each channel, rewriting the hook for each audience.

**For our segments, start short is the default.** Solo and SME owners rarely
have a long-form asset. They do have a phone full of product photos and a
steady stream of customer chats.

**Proposals (product):**

- **Idea sprint in the Creator.** Each week, generate a batch of short variants
  (several hooks, languages and formats) from the Taste Profile, and publish
  across the connected channels.
- **Double-down button.** When the Analyst marks a winner, one action turns it
  into bigger assets: a carousel, a longer caption or short video script, a
  WhatsApp broadcast to opted-in customers, a catalog highlight, or a
  landing-page section. This is "start short, then go long".
- **Repurpose with per-channel hooks.** From one piece, produce the Facebook
  post, WhatsApp status/broadcast, email and SMS versions, each with its own
  opening hook and length limit, not the same text pasted everywhere. Only
  target channels that are live (see Meta approvals in `00_FACTS` §1).
- **"Remarkable" inputs first.** The Creator should draw on the business's own
  material before generic copy: customer photos and reviews (with permission),
  real prices and stock, local events, common questions from chats.
- **Content quadrant in the Analyst.** Show each brand where it sits on the 2×2
  (posting volume against engagement or conversation rate), and the one change
  that would move it towards "remarkable and relentless".

---

## 5. Publish (and Amplify): creative is the new targeting

**The idea.** Paid ads are having a comeback because AI makes creative cheap.
Meta and Google now find audiences better than manual targeting does, so the
advertiser's job is to supply **many creatives**, covering different
jobs-to-be-done, and let the algorithm find the buyers. HubSpot quotes about 20
new creatives a month as a new baseline. Then **optimise for quality, not
quantity**: tell the platform what a *good* result is (paid orders, not form
fills) by sending it first-party conversion data from your CRM.

**Why it fits FluxMuse:** step two is hard for HubSpot's customers, because
they need to connect a CRM to find closed-won deals. For us it's built in: an
order paid inside WhatsApp is the closed-won event.

**Proposals (product), in dependency order:**

1. **Creative batches from Flux Ads + Creator.** For each campaign, generate a
   set of ad variants from the Taste Profile across different angles (price,
   social proof, urgency, product demo, founder story), and refresh them on a
   regular schedule. The monthly count should be set by tier and AI credits.
   `[[PRODUCT: credits per ad creative, and a sensible default count per tier]]`.
2. **Broad targeting by default.** Default to Meta's automated audiences
   (Advantage+) for SMB campaigns rather than detailed interest targeting. Keep
   manual targeting as an advanced option.
3. **Click-to-WhatsApp as the default ad destination**, landing in a chatbot
   flow that knows the ad it came from.
4. **Send paid orders back to Meta.** Report in-chat purchases (value and
   currency) as conversion events so campaigns optimise for orders and
   revenue, not clicks or messages started.

**Blocked on:** Meta ads permissions and `business_management`, which are
roadmap item 1 and **not approved**. Until then, this section is roadmap
material only. Don't promise it to pilot brands.

---

## 6. Learn: Loop Sprints

**The idea.** Learning speed beats budget. HubSpot used the Wright brothers
(cheap gliders, fast fixes) against Samuel Langley (well funded, one big
attempt, crashed twice). Swap quarterly campaigns for **sprints**: two-week
sprints give 26 chances to learn a year, where a quarterly plan gives 4.
AI now handles the admin (pulling data, writing the report), so sprints are
realistic even for a one-person business.

**Fit:** SMBs are the Wright brothers, with small budgets and nothing to lose by
testing quickly. The Analyst already has RAG memory, cohort analysis and
auto-optimisation; sprints give those features a regular rhythm the owner can
see.

**Proposal (product): Loop Sprint mode**, run by the Strategist and Analyst:

- **Sprint length:** 2 weeks by default (6-week option for bigger campaigns).
- **Start of sprint:** the Strategist proposes 1–3 hypotheses in plain
  language ("posts in isiZulu will get more DMs than English ones"), each with
  a single metric that decides it.
- **End of sprint:** the Analyst writes a one-page **Sprint Report**, sent
  on WhatsApp and email:
  1. What we tried (hypotheses and content/ads published)
  2. What happened (conversations, orders, GMV, revenue per conversation,
     then reach)
  3. What we learned (kept, dropped, surprises)
  4. Suggested Taste Profile changes (owner approves)
  5. The next sprint's plan (owner approves, or one tap to "run it")
- **Compounding:** each report is saved to the brand's memory, so later
  sprints build on earlier ones. That's the "every loop gets smarter" promise,
  and it makes switching away costly.

**Proposal (pilot, now):** the Gauteng pilot runs until 30 November 2026,
roughly five two-week sprints. Run each pilot brand in sprints now (a manual
sprint report is fine) so that:

- the case studies in `07_Case_Studies/` can be written as "sprint 1 → sprint 5"
  stories showing learning, not only end results;
- the pilot tests the sprint report format before it becomes a product feature.

`[[FOUNDER DECISION: adopt two-week sprints for the remaining pilot weeks]]`

---

## 7. Things not to copy

- **HubSpot's figures** (traffic loss, lead growth, the ROAS uplift from more
  creatives, their Advantage+/Performance Max results). They're from one
  company's talk and we haven't verified them. Don't quote them as industry
  facts or as FluxMuse results.
- **The talk's ROAS maths.** It says doubling creatives lifts ROAS by 65%, then
  says 10 → 20 creatives takes $3 back to $6 (a 100% lift), and 100 creatives
  gives $30. Those don't agree. Don't repeat them.
- **Brand anecdotes** (Red Bull, Liquid Death, Hathaway, the Jaguar sales-drop
  figure) are fine as inspiration in internal training. Check any figure before
  it goes on a slide.
- **Their four step names.** Our loop's Sell step is the difference; keep our
  names.

---

## 8. Suggested order of work

| # | Item | Stage | Depends on | Size |
|---|---|---|---|---|
| 1 | Run the pilot in two-week sprints with a manual sprint report | Learn | Founder decision | Small, ops only |
| 2 | Taste Profile v1 as the first onboarding deliverable (`Taste_Profile_Template.md`) | Plan | Nothing | Small, ops only |
| 3 | Value-first metrics in Analyst dashboards and reports | Learn | Nothing | Small |
| 4 | Taste Profile stored per brand and read by Creator, Ads and chatbot | Plan/Create | Nothing | Medium |
| 5 | Idea sprint + double-down + per-channel repurposing in Creator | Create | 4 | Medium |
| 6 | Loop Sprint mode with auto Sprint Report | Learn | 3, 4 | Medium |
| 7 | Creative batches + broad targeting + Click-to-WhatsApp default | Publish | Meta ads permissions | Medium |
| 8 | Send paid WhatsApp orders back to Meta as conversions | Publish/Sell | 7 | Medium |

Items 1–2 can start this week with no code. Items 3–6 are product work in
`embizo/foundation-zero-point`. Items 7–8 wait for Meta approval.
