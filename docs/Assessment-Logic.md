# LeepX Self-Assessment — Questions, Scoring & Routing Logic

**Purpose (internal):** market-qualify leads (MQL) and route them to the right LeepX product, while the learner experiences it as "someone finally listened and told me what to do next".

**Purpose (as the learner sees it):** *"Tell us where you're stuck. We'll map your next leap and send you a personal assessment."*

The same logic lives in code at `site/js/leepx-logic.js`. Change it there and here together.

---

## 0. Design principles (why it doesn't feel salesy)

1. **Listen before you ask facts.** First question is emotional ("what's going on at work right now?"), not "years of experience".
2. **Reflect back.** After key answers the screen shows a one-line reflection ("3 years in and still applying into a void. That's exhausting."). This is the "feeling heard" moment and costs nothing.
3. **Give before you take.** The learner sees a real result (their profile card + recommended path + first 3 steps) *before* we ask for email. Email unlocks the *full* written assessment; it is not a paywall on the answer.
4. **Progressive contact capture.** Email always. Phone/WhatsApp only when the lead is Warm or Hot (see §5). Nurture-tier leads are never asked for a phone number.
5. **Honest outcomes.** We say "job-ready, not job-guaranteed" inside the flow. Trust converts better for a premium ticket.
6. **≤ 3 minutes.** 14 tap-based questions, 2 optional text fields. Never more than one free-text question on a screen.

---

## 1. Question set (in order shown)

Codes in `[brackets]` are field names stored on the lead. All single-select unless marked.

### Block A — "What's going on?" (emotion first)

**Q1. What best describes where you are right now?** `[situation]`
- `job_stuck` — In a full-time job, feeling stuck / underpaid
- `job_ok_bored` — In a job that's fine, but I want more (income, freedom, remote)
- `freelance_unstable` — Freelancing, but income is unstable
- `student` — Student / recent graduate
- `break` — On a career break (parenting, health, relocation, etc.)
- `unemployed` — Between jobs, actively searching

**Q2. Where do you usually get stuck?** *(multi-select, max 3)* `[blockers]`
- `no_direction` — I don't know which role/path fits me
- `no_skills` — I know the direction but not the skills
- `no_portfolio` — I have skills but nothing to show
- `no_interviews` — I apply but never hear back
- `fail_interviews` — I reach interviews but don't convert
- `no_clients` — I can't find (or price) clients
- `no_confidence` — I don't feel confident enough to start
- `no_time` — I can't find the time

> Reflection screen after Q2 (picked by first blocker chosen; see §6 copy table).

### Block B — "Tell us about you" (facts, fast)

**Q3. Years of professional experience** `[experience]`
- `0` — None yet · `lt1` — Less than 1 · `1_3` — 1–3 · `3_6` — 3–6 · `6_10` — 6–10 · `10p` — 10+

**Q4. Industry you're in (or last worked in)** `[industry]`
- `marketing_media`, `tech_product`, `sales_bd`, `ops_admin`, `finance`, `education`, `healthcare`, `design_creative`, `hospitality_retail`, `other`, `none`

**Q5. Roles you've done so far** *(multi-select)* `[roles_done]`
- `social_content` — Social media / content
- `marketing` — Marketing (any)
- `admin_ea` — Admin / EA / office coordination
- `customer_support` — Customer support / success
- `project_coord` — Project or program coordination
- `product` — Product
- `sales` — Sales / BD
- `ops` — Operations
- `teaching` — Teaching / training
- `design` — Design / video
- `dev` — Engineering / data
- `founder` — Ran my own thing
- `none` — No professional role yet

**Q6. Tools you're comfortable with** *(multi-select)* `[tools]`
- `canva`, `figma`, `capcut_premiere` (video editing), `ig_native` (Instagram/LinkedIn analytics), `meta_ads`, `notion`, `asana_clickup_trello`, `gworkspace` (Sheets/Docs/Calendar), `excel_adv` (pivots, formulas), `chatgpt_ai`, `zapier_make`, `hubspot_crm`, `jira`, `none`

**Q7. Current (or last drawn) monthly income** `[income]`
- `0` — None · `lt15` — < ₹15k · `15_30` — ₹15–30k · `30_50` — ₹30–50k · `50_80` — ₹50–80k · `80_150` — ₹80k–1.5L · `150p` — ₹1.5L+

**Q8. What would feel like a real win, monthly?** `[dream_income]`
- `30` — ₹30k · `50` — ₹50k · `80` — ₹80k · `120` — ₹1.2L · `200` — ₹2L · `200p` — ₹2L+ / earn in dollars

### Block C — "Where do you want to go?"

**Q9. What kind of leap are you after?** `[leap]`
- `job_to_freelance` — Job → freelancing / remote clients
- `freelance_to_job` — Freelancing → stable remote job
- `switch_role` — Same industry, new role
- `switch_industry` — New industry entirely
- `first_job` — My first real role
- `side_income` — Keep my job, add a side income
- `unsure` — Honestly, not sure yet

**Q10. Any of these roles on your mind?** *(multi-select, incl. "not sure")* `[roles_interest]`
- `smm` — Social Media Manager
- `va` — Virtual Assistant / Online Business Manager
- `pm` — Project Manager
- `fo` — Founder's Office / Chief of Staff
- `content` — Content creator
- `unsure` — Not sure, that's why I'm here

**Q11. Have you ever worked with an international client or company?** `[intl]`
- `yes_paid` — Yes, paid work
- `yes_unpaid` — Only internships / volunteer
- `no` — Not yet

**Q12. Interviews in the last 6 months?** `[interviews]`
- `none_applied` — Haven't applied
- `applied_no_calls` — Applied, no calls
- `some_calls` — A few interviews, no offer
- `offers` — Got offers, but not what I want

### Block D — "How much can you put in?" (commitment)

**Q13. Hours per week you can realistically give for the next 10 weeks** `[hours]`
- `lt3` — < 3 · `3_6` — 3–6 · `6_10` — 6–10 · `10p` — 10+

**Q14. If the right path were clear, what could you invest in it per month?** `[budget]`
- `0` — Nothing right now, free resources only
- `lt2k` — Under ₹2,000
- `2_5k` — ₹2,000–5,000
- `5_10k` — ₹5,000–10,000
- `10k_p` — ₹10,000+ / one-time payment is fine

Framed as *"so we only recommend what actually fits your life"*, never as "budget".

### Block E — Optional (skippable, one screen)

- **LinkedIn URL** `[linkedin]` — "Want us to look at your profile in the assessment? Drop your LinkedIn."
- **One line: what does your ideal Tuesday look like a year from now?** `[dream_text]` — used verbatim in the email; extremely high engagement signal if filled.

### Block F — Contact (after the result preview)

- **Email** `[email]` — required to send the full assessment.
- **First name** `[name]` — required.
- **WhatsApp number** `[phone]` — shown only if tier ∈ {Warm, Hot} (§5). Copy: *"Want Shreya's team to walk you through this on WhatsApp? Optional."*
- **Consent checkbox** — "Send me the assessment and follow-ups. Unsubscribe anytime."

---

## 2. Derived signals

| Signal | Rule |
|---|---|
| `exp_years` | midpoint of Q3: 0 / 0.5 / 2 / 4.5 / 8 / 12 |
| `income_now` | midpoint of Q7 in ₹k: 0 / 10 / 22 / 40 / 65 / 115 / 180 |
| `income_goal` | Q8 in ₹k |
| `income_gap` | `income_goal − income_now` (₹k). Used for copy ("You're asking for a ₹40k/month jump. Realistic in 6–9 months on this path.") |
| `has_social_exposure` | any of `social_content`, `marketing`, `design`, `content` interest, tools ∈ {canva, capcut_premiere, ig_native, meta_ads} |
| `has_ops_exposure` | any of `admin_ea`, `customer_support`, `ops`, `project_coord`, tools ∈ {gworkspace, notion, asana_clickup_trello, excel_adv} |
| `has_pm_exposure` | any of `project_coord`, `product`, `dev`, tools ∈ {jira, asana_clickup_trello, notion} |
| `has_fo_exposure` | `founder`, `sales`, `product`, `ops` with exp ≥ 3 |
| `has_portfolio_gap` | blockers ∋ `no_portfolio` or interviews ∈ {applied_no_calls} |
| `has_interview_gap` | interviews = `some_calls` or blockers ∋ `fail_interviews` |
| `direction_gap` | blockers ∋ `no_direction` or leap = `unsure` or roles_interest ∋ `unsure` |

---

## 3. Track recommendation (which product)

Four tracks: **SMM** (Social Media Manager Accelerator), **VA** (Virtual Assistant Accelerator), **PM** (Project Management track), **FO** (Founder's Office track). Score each 0–100, recommend top; show runner-up if within 12 points.

Start every track at 20. Add:

| Evidence | SMM | VA | PM | FO |
|---|---|---|---|---|
| roles_interest includes the track | +30 | +30 | +30 | +30 |
| roles_interest = `content` | +15 | | | |
| roles_interest = `unsure` (no penalty; rely on fit) | 0 | 0 | 0 | 0 |
| has_social_exposure | +20 | | | |
| has_ops_exposure | | +20 | +8 | +8 |
| has_pm_exposure | | | +20 | +8 |
| has_fo_exposure | | | +8 | +20 |
| industry ∈ {marketing_media, design_creative} | +10 | | | |
| industry ∈ {ops_admin, hospitality_retail, education} | | +10 | | |
| industry ∈ {tech_product, finance} | | | +10 | +10 |
| exp_years = 0–1 | +8 | +12 | −10 | −15 |
| exp_years = 1–3 | +5 | +8 | +5 | −5 |
| exp_years = 3–6 | 0 | +2 | +12 | +10 |
| exp_years ≥ 6 | −5 | −5 | +12 | +15 |
| leap = `job_to_freelance` or `side_income` | +10 | +12 | −5 | −10 |
| leap = `freelance_to_job` | −5 | +5 | +10 | +10 |
| leap = `first_job` | +8 | +10 | −5 | −10 |
| situation = `break` | +5 | +12 | | |
| situation = `student` | +8 | +8 | −5 | −10 |
| intl = `yes_paid` | | +5 | +5 | +5 |
| dream_income ≥ 1.2L | | | +5 | +8 |
| tools ∋ `chatgpt_ai` | +3 | +3 | +3 | +3 |

**Tie-break:** explicit interest > exposure > experience band. If `direction_gap` and top two tracks within 8 points, label the result **"Two paths fit you"** and recommend the *Clarity Call* (see §5) before a purchase.

**Rationale:** SMM and VA are entry-friendly, freelance-friendly and match the current audience (freshers, 0–2 yrs, remote-seekers). PM and FO need professional maturity; recommending them to a fresher hurts trust and completion.

---

## 4. Readiness stage (what to tell them to do first)

Compute `readiness` 0–10:

| Factor | Points |
|---|---|
| exp_years ≥ 1 | +2 |
| ≥ 3 relevant tools for the recommended track | +2 (1 if 1–2 tools) |
| roles_done includes a role adjacent to the track | +2 |
| intl = `yes_paid` | +1 |
| interviews ∈ {some_calls, offers} | +1 |
| blockers ∌ `no_portfolio` | +1 |
| blockers ∌ `no_confidence` | +1 |

| Score | Stage | What we say | Product emphasis |
|---|---|---|---|
| 0–3 | **Explorer** | "You need clarity and a foundation, not more free videos." | Full Accelerator (Modules 1→end), community |
| 4–6 | **Builder** | "You know enough. You're missing proof." | Accelerator with focus on portfolio modules + live sprint |
| 7–10 | **Launcher** | "You're closer than you think. This is a packaging & outreach problem." | Portfolio/profile review + outreach modules; 1:1 call upsell |

The stage also picks the **first 3 steps** shown on the result card (copy table in `leepx-logic.js`).

---

## 5. Lead tier (MQL) and routing

### 5a. Fit gate (from the "Not ideal for" list)

Mark `fit = low` if **any**:
- budget = `0` **and** hours = `lt3`
- exp_years ≥ 10 **and** leap ∈ {switch_role} **and** roles_interest ∌ {fo, pm} (rigid senior corporate, no stated interest)
- roles_interest = `content` only **and** leap = `side_income` **and** hours = `lt3`

Low-fit leads still get a result and the email assessment (free resources + masterclass invite). They do **not** get a phone field or sales follow-up.

### 5b. Intent score (0–100)

| Factor | Points |
|---|---|
| budget: `0`→0 · `lt2k`→10 · `2_5k`→25 · `5_10k`→35 · `10k_p`→40 | 0–40 |
| hours: `lt3`→0 · `3_6`→10 · `6_10`→18 · `10p`→20 | 0–20 |
| urgency: situation ∈ {unemployed, freelance_unstable, job_stuck}→15 · {break, student}→10 · {job_ok_bored}→5 | 5–15 |
| pain clarity: interviews ∈ {applied_no_calls, some_calls}→10 · blockers count ≥ 2→+5 | 0–15 |
| income_gap ≥ 40k→5 · dream_text filled→+3 · linkedin filled→+2 | 0–10 |

### 5c. Tier

| Tier | Rule | Route |
|---|---|---|
| **Hot** | fit ≠ low **and** intent ≥ 65 **and** budget ∈ {5_10k, 10k_p} | Result → email → **WhatsApp field shown** → "Book a 15-min call with Shreya's team" CTA. Lead pushed to sales sheet/CRM with tag `hot`. Email assessment includes cohort date + EMI + checkout link. WhatsApp message within 24h. |
| **Warm** | fit ≠ low **and** intent 40–64, or intent ≥ 65 with budget `2_5k` | Result → email → **WhatsApp field shown (optional)**. Email assessment includes recommended track, EMI framing, free masterclass invite. 3-email sequence over 7 days; WhatsApp nudge only if number given. |
| **Nurture** | fit ≠ low **and** intent < 40 | Result → email only. Assessment includes free resources, free masterclass, "reply to this email" prompt. Monthly newsletter. Re-assess prompt after 60 days. |
| **Redirect** | fit = low | Result (honest: "LeepX programs may not be the best fit right now, here's what we'd do instead") → email with free resources. No sales follow-up. |

### 5d. Recommended offer per tier × stage

| | Explorer | Builder | Launcher |
|---|---|---|---|
| **Hot** | Full Accelerator (one-time) + community. Call to confirm track. | Full Accelerator, emphasise live sprint. Call. | Accelerator *or* 1:1 Portfolio & Outreach Review (if track already landed). Call. |
| **Warm** | Accelerator on EMI. Masterclass first. | Accelerator on EMI. Masterclass first. | Portfolio/profile review (lower ticket) → Accelerator. |
| **Nurture** | Free masterclass + starter guide for the track. | Free portfolio checklist for the track. | Free outreach scripts + job board. |

### 5e. Clarity Call trigger
Offer "15-min Clarity Call" (free, human) whenever: tier ∈ {Hot, Warm} **and** (`direction_gap` **or** two tracks within 8 points). This is the highest-converting moment for confused-but-committed leads and looks like help, because it is.

---

## 6. Reflection copy (shown between blocks)

| Trigger | Line |
|---|---|
| blocker `no_direction` | "Not knowing *which* door to knock on is more tiring than knocking. Let's fix that first." |
| blocker `no_skills` | "You've picked a direction. That's the hard part most people skip." |
| blocker `no_portfolio` | "Skills without proof read as 'no skills' to a recruiter. Fixable in weeks, not years." |
| blocker `no_interviews` | "Applying into a void isn't a you problem. It's a positioning problem." |
| blocker `fail_interviews` | "Getting to the final round means you're good. Converting is a separate skill." |
| blocker `no_clients` | "Finding clients is a system, not luck. We'll show you ours." |
| blocker `no_confidence` | "Confidence usually shows up *after* the first small win, not before." |
| blocker `no_time` | "Then we'll design around 5 focused hours a week, not 15." |
| situation `break` | "A break isn't a gap. It's a reason employers are remote-friendly now." |
| situation `unemployed` | "Job hunts are lonely. You've got company now." |
| Q8 answered | "So we're talking about a ₹{gap}k/month jump. Noted. Let's see what gets you there fastest." |
| Q11 = `no` | "Most of our learners hadn't either. International clients care about proof, not passports." |

---

## 7. Result card (shown before contact capture)

1. **Headline:** "{Name or 'Okay'}, here's what we're seeing." (name asked later; use "Okay" first time)
2. **Profile chip row:** experience band · situation · leap type
3. **Recommended path:** track name + one-line why ("because you already live in Canva and Instagram, and you want to freelance").
4. **Stage badge:** Explorer / Builder / Launcher + one-line meaning.
5. **First 3 steps** (stage-specific, actionable, free-to-start).
6. **Realistic timeline & income band** (from track + stage; conservative ranges, labelled "typical learner range, not a guarantee").
7. **Soft CTA:** "Get the full assessment by email" → contact form.
8. After submit: tier-specific next step (call booking / WhatsApp / "check your inbox").

---

## 8. Data captured per lead (schema)

```
lead_id, created_at, source(utm_*), 
situation, blockers[], experience, industry, roles_done[], tools[], income, dream_income,
leap, roles_interest[], intl, interviews, hours, budget, linkedin, dream_text,
name, email, phone(optional), consent,
derived: track_primary, track_secondary, track_scores{}, readiness, stage, intent, fit, tier, clarity_call(bool)
```

Client posts JSON to `LEAD_ENDPOINT` (Google Apps Script → Sheet, or Formspree/Make webhook). Config is at the top of `site/js/leepx-logic.js`.

---

## 9. Email assessment (auto-generated outline)

Subject: *"{Name}, your LeepX leap map (the {Track} one)"*

1. What you told us (3 bullets, their words)
2. What we're seeing (stage + why)
3. Your recommended path (track) and what the first 10 weeks look like
4. Realistic numbers (timeline, income band, "not a guarantee")
5. First 3 free steps this week
6. Tier-specific block: Hot → cohort date, price, EMI, checkout, book-a-call · Warm → masterclass invite + EMI · Nurture → free resources · Redirect → honest alternatives
7. One learner story that matches their situation (Srishti / Keerthana / Shreeya / Smitha)
8. "Reply to this email, a human reads it."

---

## 10. Open decisions for Shreya / Sambhav

- Confirm PM and Founder's Office tracks are sellable now, or hide them and route to a waitlist (logic supports `TRACKS.pm.available=false`).
- Price points & EMI to show in Hot/Warm emails.
- Where leads go: Google Sheet vs CRM. Endpoint URL.
- Booking link for Clarity Call (Calendly/Cal.com).
- Whether to ask LinkedIn (adds a field, ~10% drop-off; high value for manual review).

---

## Changelog — 2026-10-01 (supersedes the sections above where they differ)

- **Currency:** all money in US dollars (reference rate $1 ≈ ₹83). Q7 income, Q8 dream income, Q14 budget, result income bands.
- **Q2 blockers:** option 7 is now `no_where` — "I don't know where to apply (I know the role, tools, skills)". Replaces `no_confidence`. Adds +1 readiness.
- **Q7 income (USD/month):** none · <$200 · $200–400 · $400–600 · $600–1,000 · $1,000–1,800 · $1,800+.
- **Q8 dream income (USD/month):** starts at $600 (≈ ₹50k): $600 · $1,000 · $1,500 · $2,500 · $4,000+.
- **Q9 leap:** multi-select. Scoring treats it as a list.
- **Q10:** now "Do any of our cohorts interest you?" with a description per option: Remote Launchpad, Global Remote Accelerator, Become a SMM, Become a VA, Attract inbound via LinkedIn, Scale your freelancing career, Become an AI-powered PM, Not sure. Track weights: smm/va/pm +30 own track; launchpad → smm +10, va +12; accelerator → pm +12, fo +12; freelance → smm +8, va +8; linkedin → pm +4, fo +4. Saved on the lead as `cohort_interest`.
- **Q11 international:** new option `via_indian` — international clients via an Indian company. Counts for readiness, not for the direct-international track bonus.
- **Q13 hours:** "for the next 10 weeks" removed.
- **Q14 budget (USD, one-time, EMI available):** not right now · $250–400 (≈ ₹20k–35k) · $400–600 · $600–1,000 · $1,000+. Intent points 0 / 28 / 34 / 38 / 40.
- **Tiers:** Hot = fit ok, intent ≥ 65, any paid budget band. Warm = intent 40–64 (or ≥ 65 with no budget). Nurture < 40. Redirect = low fit.
- **Flow:** questions → optional → **contact gate (name, email, WhatsApp all required)** → result on screen + tier next-step. Full version goes by email. This replaces "result before email" and "phone only for warm/hot".

## Changelog — 2026-10-01 (round 2)

- **Q4 industry, Q5 roles, Q6 tools:** long chip lists, multi-select, with an "add your own" text field (saved as `industry_other`, `roles_done_other`, `tools_other`). Tools are grouped by category (design & video, social & marketing, productivity & PM, docs & data, AI & automation, CRM & sales, websites & no-code).
- **Q10:** "Global Remote Accelerator" option removed. Clearer definitions for Remote Launchpad and Scale your freelancing career.
- **Q14 budget:** not right now · $200–300 · $300–400 · $400–500 · $500–600 · $600–700. Intent points 0 / 26 / 30 / 34 / 37 / 40.
- **Currency hints:** the "$1 ≈ ₹83" conversion notes are removed.
- **WhatsApp:** country-code dropdown (default +91) plus number. Lead stores `phone` as "+CC number" and `phone_country_code`.

## Changelog — 2026-10-02

- **Q4, Q5, Q6 are now a searchable picker.** Search box, category list on the left, checkbox grid on the right, selected items in a tray, "add your own" box, and a separate "none" toggle. Industries: 56 options in 5 groups. Work done: 67 in 6 groups. Tools: 160 in 17 groups.
- **Scoring is category-based for these three.** Each option inherits its group's category (`CAT` in `leepx-logic.js`): roles → social / ops / pm / biz / people; tools → design, video, social, ads, seo, crm, pm, comms, docs, data, ai, automation, support, web, finance, freelance, dev; industries → creative / corp / service / other. Custom entries are saved as arrays in `industry_other`, `roles_done_other`, `tools_other` and do not affect scoring.
- **Q10:** every cohort has a two-sentence description. Remote Launchpad includes "We will help you pick a role."
- **Landing cohorts:** Global Remote Accelerator removed. Live: Remote Launchpad, Social Media Manager, Virtual Assistant. Waitlist: LinkedIn inbound, Freelancing, AI-powered Project Manager.

## Changelog — 2026-10-02 (result page)

- **Result page is a summary, not a plan.** It shows: an encouraging "where you stand" line, a table of what they told us, what they could earn (USD band for their path and stage), what is already working for them, and the recommended programs. First steps and timeline are no longer shown.
- **Recommendation = Remote Launchpad + one cohort.** Launchpad is recommended to everyone. The second cohort is the best-scoring track, unless they picked specific cohorts in Q10 that exclude it; then it is their highest-scoring pick (LinkedIn / Freelancing if those are all they picked). Lead field `cohort_recommended` is `['launchpad', <second>]`.
- **Founder's Office track is switched off** (`TRACKS.fo.available = false`); it is not a cohort.
- **CTAs:** "Join the cohort" (checkout link from `CONFIG.CHECKOUT`) and "Talk to our team on WhatsApp". The 15-minute call button is removed. If the second cohort is on waitlist, the join button is for Remote Launchpad and a note says they will be waitlisted for the other.

## Changelog — 2026-10-02 (result page, round 2)

- **New section "What you are missing"** (up to six gaps), read from blockers, interview status, international exposure and the leap they want: role clarity, skill path, proof of work, positioning, application strategy, interview framework, client system, global exposure, weekly plan, then outreach, networking and a step-by-step framework as defaults. It names the gap only; it never explains how to close it.
- **Three recommended programs, each with its own button:** Remote Launchpad (always), Attract inbound via LinkedIn (always), and a third from their selection (SMM, VA, AI-powered PM or Freelancing). Live cohorts get "Join the cohort" (`CONFIG.CHECKOUT[key]`); waitlist cohorts get "Join the waitlist" (`CONFIG.WAITLIST_URL`). Lead field `cohort_recommended` is `['launchpad','linkedin',<third>]`.
- **One shared "Talk to our team on WhatsApp" button** under the three cards, with the WhatsApp logo.

## Changelog — 2026-10-02 (result page, rebuilt)

Result page rebuilt for scanning, about 225 words in total. Order: (1) one-line headline by stage, with five profile chips; (2) one large "You could earn $X–Y/month" block with Today and Goal beside it; (3) "What is already working" as tick chips; (4) **"What you are missing"** as the main section: up to five rows, each a short title, a few words, and a tag naming the program that covers it; (5) three program cards (Remote Launchpad, LinkedIn, plus one from their selection), each with one line and its own Join button; (6) one WhatsApp button. The long answers table and the paragraph copy are removed.

## Changelog — 2026-10-02 (result page, final structure)

- **No earnings shown.** The "You could earn" block is removed; LeepX does not promise income. `TRACKS.*.income` stays in the logic file but is not displayed.
- **Bento structure restored:** where you stand → what you told us + what is already working → what you are missing → recommended programs.
- **Gaps are not tied to programs.** The "What you are missing" rows show the gap only. No program name appears next to a gap.

## Changelog — 2026-10-02 (result page, settled)

Result page is back to the earlier layout: purple "Where you stand" header → "What you told us" (full list of their selections) beside "What is already working for you" → "What you are missing" → "Your recommended programs". The programs block is now soft purple with white cards (was black). Still no earnings shown, and no program names next to gaps.

## Changelog — 2026-10-02 (result page order)

Order is now: Where you stand → What you told us (left) with What you are missing and How much you can earn stacked on the right → What is already working for you → Your recommended programs. The earnings card is back at the client's request, with the "typical range, not a guarantee" line. Program cards: live cohorts first, waitlist cohort last; the small tag line above each program name is removed.

## Changelog — 2026-10-02 (earnings rule)

"How much you can earn" = **60% above the income range they chose in Q7**, rounded to the nearest $10: under $200 → up to $320 · $200–400 → $320–640 · $400–600 → $640–960 · $600–1,000 → $960–1,600 · $1,000–1,800 → $1,600–2,880 · $1,800+ → $2,880+. If they earn nothing today, there is no base, so the card shows the path's starting range from `TRACKS.*.income` (placeholder figures). The card says "About 60% above what you earn today" and "An estimate, not a guarantee."

## Changelog 2026-10-05

- Result page: if Q14 (budget) is "Not right now. FREE resources please", the WhatsApp row is replaced by "Want to start for free?" with a "Join the Free Community →" button that opens `COMMUNITY_URL` from `site/js/config.js` (https://academy.theleepx.com/l/ad00303ec0). Everyone else still sees the WhatsApp button. The three program cards are unchanged.
- Landing page: the hero video autoplays muted and loops while on screen. Tapping "Watch with sound" restarts it from the beginning with sound and controls.

## Changelog 2026-10-09

- Landing page: Remote Launchpad and Social Media Manager cards got a primary "Enrol now →" button (the assessment link stays as the secondary link). Virtual Assistant and LinkedIn cards get theirs once their pages exist.
- New course pages inside the site: `site/remote-launchpad.html` and `site/social-media-manager.html` (live at theleepx.com/remote-launchpad and theleepx.com/social-media-manager). Built from the old Netlify landing pages, restyled to the site theme, with the founders section, Shreya's story block and the general FAQs removed because the main site already has them. Buy buttons go straight to the academy checkout (Launchpad ₹37,000, Launchpad Plus ₹42,000, SMM ₹25,000, all + GST).
- The pages are generated: edit `tools/course-pages.py`, then run `python3 tools/course-pages.py`. Styles live in `site/css/course.css`.
- Result page "Join the cohort" buttons still go straight to checkout (unchanged).

## Changelog 2026-10-09 (later)

- Third course page: `site/virtual-assistant.html` (theleepx.com/virtual-assistant), built from `LeepX_VA_Program.html`. Ongoing cohort, 13 modules, ₹22,999 + GST, checkout `academy.theleepx.com/web/checkout/6a1b333e808d71fed1f65298`. Founders, "built around real life" block and general FAQs dropped like the other pages.
- The Virtual Assistant card on the home page now has the "Enrol now →" button too. Only the LinkedIn card still lacks one.
- Course pages now: short centred hero, slim top bar (back · logo · CTA), week/module cards, dark numbered steps, AI boxes (VA only), lilac "included" boxes, tick-list vault, framework letters, objection thread, receipt + seat side by side, tilted bonus tickets, testimonial carousel, course FAQs.

## Changelog 2026-10-22

- VA price: ₹22,999 → ₹24,999 + GST (course page tier and sticky bar).
- Floating "Upcoming Masterclass" button on the home page and all course pages (`js/fab.js`, styles in `css/leepx.css`). Link and end date live in `js/config.js`: `MASTERCLASS_URL` and `MASTERCLASS_UNTIL: '2026-11-14'`. The button hides itself from that date (India time); set the URL to '' to remove it earlier, or change the date for the next masterclass.
- AI Project Management is now a live cohort: new page `site/ai-project-manager.html` (theleepx.com/ai-project-manager, 16 weeks, ₹34,999, checkout `academy.theleepx.com/l/c48219926c`). Home card moved from the waitlist row to the live row with "Enrol now →"; result page marks it Live and `CHECKOUT.pm` points to the same link; Q10 description no longer says "Waitlist open". Only "Scale your freelancing career" remains on the waitlist.
- Masterclass page in the site theme: `site/masterclass.html` (theleepx.com/masterclass), content copied one-to-one from leepxremotemasterclass.netlify.app (14 Nov, 4 to 6 PM; reserve link `academy.theleepx.com/l/145f740193`). The floating button now opens this page (`MASTERCLASS_URL: 'masterclass.html'`). For the next masterclass, update the date/time text in `tools/course-pages.py` (mc_body), the reserve link, and `MASTERCLASS_UNTIL`.

## 2026-10-25
- AI PM page synced with the updated leepxaipm.netlify.app content: hero fact chips, "What you'll master" skills strip, per-week project + outcome + skill tags, track rows labelled "Who this track is for", new bonus section (2 expert guest sessions + live project session with Shreya), two extra testimonials (R., P.), job-placement FAQ. Price unchanged at ₹34,999 (checkout page is JS-rendered; confirm if it changed).
- Generator: `timeline()` rows accept optional tags (5th), outcome (6th) and label override (7th); `ticket()` accepts an empty worth.
- Home: live cohort cards reordered to Launchpad, AI PM, SMM, VA, LinkedIn.
- 2026-10-25 later: pricing section removed from AI PM page only; hero, top bar and mobile CTAs go straight to checkout.
- 2026-10-26: live site was the single-file bundle (course pages = overlays, one URL). Fix: deploy LeepX-website-upload/ folder. Added site/_redirects (clean URLs: /ai-project-manager serves the .html, .html redirects to clean) and hash deep links in the bundle (#ai-project-manager, #masterclass, #assess open the overlay on load; back closes).
- 2026-10-27: AI PM page gains an "AI tools, week by week" table (section #aitools, lilac, after the schedule). Generator helper tooltable(); CSS .tbl.
- 2026-10-27 later: AI tools section rebuilt as logo cards (toolcards() helper, .tcards/.tcard/.lg CSS). Brand marks in site/assets/logos/ (simple-icons CC0 + Wikimedia Commons: chatgpt, claude, sheets, jira, confluence, zapier, make, copilot, gemini, n8n, notion, power-automate). make-upload.sh now copies assets/logos.
- 2026-10-28: moved hosting to GitHub Pages (repo leepx-code/Website). All internal links extension-less (/ai-project-manager, /assess, ./). tools/serve.py = local preview with clean URLs. _redirects removed (Netlify only).
- 2026-10-28: index.html redirects #slug hash links (from the old single-file deploy) to the real page.
- 2026-10-31: VA checkout link changed to https://academy.theleepx.com/l/f8d6f79725 (course page buttons + config CHECKOUT.va for the result page).
