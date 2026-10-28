# LeepX website

Static site. No build step. Open `index.html` or serve the folder.

```bash
python3 -m http.server 4601 --directory site
```

| File | What |
|---|---|
| `index.html` | Landing page. Story-first (numbered sections alternating with learner case studies, Ali Abdaal / LBA rhythm). No course catalogue. Every CTA goes to the assessment. |
| `assess.html` | 14-question self-assessment → result card → email capture (WhatsApp field only for warm/hot leads) → tier-specific thank-you. |
| `js/leepx-logic.js` | Questions, reflections, track scoring, readiness stage, intent/tier, lead submit. Mirrors `../docs/Assessment-Logic.md`. |
| `css/leepx.css` | Brand tokens + shared components (buttons, stickers, WhatsApp-style chat cards, nav, footer). |
| `assets/` | Brand marks, Shreya photos, compressed testimonial video (18 MB, 720p) + poster. |

## Before launch — fill in `js/leepx-logic.js` → `CONFIG`

- `LEAD_ENDPOINT` — where leads POST as JSON (Google Apps Script → Sheet, Formspree, Make webhook). Empty = leads only saved to the visitor's `localStorage` (dev mode; the thank-you screen says so).
- `BOOKING_URL` — Calendly / Cal.com for the 15-min Clarity Call.
- `WHATSAPP_URL` — `https://wa.me/91XXXXXXXXXX?text=...`
- `CHECKOUT` — TagMango checkout URL per track (used in the email, not on the page).
- Set `TRACKS.pm.available` / `TRACKS.fo.available` to `false` to hide tracks not yet sellable.

Also: footer Contact / Terms / Privacy links, OG image, Google Analytics if wanted.

## Testing personas

`assess.html?a=<url-encoded JSON of answers>` jumps straight to the result. Example (senior ops, unsure direction → PM + Clarity Call, hot):

```
assess.html?a=%7B%22situation%22%3A%22job_stuck%22%2C%22blockers%22%3A%5B%22no_direction%22%5D%2C%22experience%22%3A%223_6%22%2C%22industry%22%3A%22ops_admin%22%2C%22roles_done%22%3A%5B%22admin_ea%22%2C%22project_coord%22%5D%2C%22tools%22%3A%5B%22notion%22%2C%22gworkspace%22%5D%2C%22income%22%3A%2230_50%22%2C%22dream_income%22%3A%2280%22%2C%22leap%22%3A%22unsure%22%2C%22roles_interest%22%3A%5B%22unsure%22%5D%2C%22intl%22%3A%22no%22%2C%22interviews%22%3A%22some_calls%22%2C%22hours%22%3A%226_10%22%2C%22budget%22%3A%225_10k%22%7D
```

Leads captured locally: run `JSON.parse(localStorage.leepx_leads)` in the console.

## Content notes

- All quotes are verbatim from the cohort-1 graduation recording (`../Testimonials/LeepX_Learner_Quotes.md`). Srishti's deals are described as "in talks", never "signed". Keep it that way.
- Verify names "Bharathi" and "Ayushi" before publishing (Zoom labels).
- Income bands on the result card are placeholders marked "typical learner range, not a guarantee". Replace with real numbers once you have them.
