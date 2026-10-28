#!/bin/bash
# Builds the folder you upload to the web host: only the files the live site needs.
set -e
cd "$(dirname "$0")/.."
OUT="LeepX-website-upload"
rm -rf "$OUT"; mkdir -p "$OUT/css" "$OUT/js" "$OUT/assets"
cp site/index.html site/assess.html site/privacy.html site/terms.html site/remote-launchpad.html site/social-media-manager.html site/virtual-assistant.html site/ai-project-manager.html site/masterclass.html site/favicon.ico site/_redirects "$OUT/"
cp site/css/leepx.css site/css/course.css "$OUT/css/"
cp site/js/config.js site/js/track.js site/js/icons.js site/js/leepx-logic.js site/js/fab.js "$OUT/js/"
for f in favicon-32.png favicon-192.png favicon-512.png apple-touch-icon.png spark-mask.png logo-primary.png logo-white.png logo-black.png shreya-portrait.jpg riya.jpg cohort-call.jpg hero.mp4 hero-poster.jpg; do cp "site/assets/$f" "$OUT/assets/"; done
mkdir -p "$OUT/assets/course" "$OUT/assets/logos" && cp site/assets/course/* "$OUT/assets/course/" && cp site/assets/logos/*.svg "$OUT/assets/logos/"
echo "Ready: $OUT ($(du -sh "$OUT" | cut -f1))"
