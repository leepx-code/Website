#!/usr/bin/env python3
"""Local preview that behaves like GitHub Pages: /ai-project-manager serves ai-project-manager.html.
usage: python3 tools/serve.py  (then open http://localhost:4601)"""
import http.server, os, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'site'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4601
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(ROOT), **k)
    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and not p.endswith('/') and os.path.exists(p + '.html'): return p + '.html'
        return p
    def log_message(self, *a): pass
print(f'LeepX preview: http://localhost:{PORT}  (serving {ROOT})')
http.server.ThreadingHTTPServer(('', PORT), H).serve_forever()
