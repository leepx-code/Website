# LeepX website (theleepx.com)

Static site, no framework. Live site is published automatically from the `main` branch by GitHub Pages.

- `site/` the website files (HTML, CSS, JS, images, video)
- `tools/course-pages.py` generates the five course pages from the content inside it
- `tools/make-upload.sh` builds the deploy folder (`LeepX-website-upload/`) that GitHub Pages serves
- `docs/` assessment logic, changelog
- `HOW-TO-EDIT.md` how anyone on the team makes a change
- `CLAUDE.md` rules Claude follows when editing this site

Preview locally:

```bash
python3 tools/serve.py
```
