# How to change the LeepX website

No coding needed. Two ways, pick whichever you like.

## Way 1: ask Claude (recommended)
1. Go to claude.ai/code, pick the `leepx-code/Website` repository.
2. Say what you want in plain words. Examples:
   - "Change the VA price to 26,999 and the checkout link to ..."
   - "Add a new FAQ to the AI PM page: ..."
   - "Make a page for the LinkedIn cohort, same style as the others, content below: ..."
   - "Replace the masterclass date with 12 December, 5 to 7 PM, link ..."
3. Claude edits, shows you a preview, and opens a "pull request" (a proposed change).
4. Open the pull request on GitHub, read the summary, press **Merge**. The live site updates in about one minute.

## Way 2: edit the text yourself on GitHub
1. Open github.com/leepx-code/Website, go to `tools/course-pages.py` (course text) or `site/index.html` (home page).
2. Press the pencil icon, change the words, press **Commit changes**.
3. Wait a minute, refresh theleepx.com.

Only for small word changes. For anything structural use Way 1.

## Where things live
| Want to change | File |
|---|---|
| Course page text, weeks, price, bonuses, FAQ | `tools/course-pages.py` (one block per course) |
| Checkout links, WhatsApp number, community link, masterclass link and end date | `site/js/config.js` |
| Home page | `site/index.html` |
| Assessment questions and results | `site/js/leepx-logic.js` and `docs/Assessment-Logic.md` |
| Screenshots and photos | `site/assets/course/` |
| Tool logos | `site/assets/logos/` |

## Checking the live site
Every publish shows under the **Actions** tab on GitHub. Green tick = live. Red cross = open it, copy the error, paste to Claude.

## Rules everyone follows
- Never touch the `academy.theleepx.com` DNS record at GoDaddy.
- Prices appear in two places (course page and config). Change both.
- Keep the brand: purple and lime, Lucide icons, no emoji except faces.
