#!/usr/bin/env python3
"""Bundle site/ into one shareable HTML file: CSS, JS, images, video inlined; assessment embedded as an overlay iframe (srcdoc)."""
import base64, html, mimetypes, pathlib, re
ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent / 'LeepX-site.html'
mimetypes.add_type('image/png', '.png'); mimetypes.add_type('video/mp4', '.mp4')

def data_uri(rel):
    p = ROOT / rel
    mt = mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
    return f"data:{mt};base64,{base64.b64encode(p.read_bytes()).decode()}"

def inline_css(css, base='assets/'):
    return re.sub(r"url\((?:\.\./)?assets/([^)]+)\)", lambda m: f"url({data_uri('assets/' + m.group(1))})", css)

def inline_page(name, video=None):
    s = (ROOT / name).read_text()
    css = inline_css((ROOT / 'css/leepx.css').read_text())
    s = s.replace('<link rel="stylesheet" href="css/leepx.css" />', f'<style>{css}</style>')
    s = s.replace('<link rel="stylesheet" href="css/course.css" />', f'<style>{inline_css((ROOT / "css/course.css").read_text())}</style>')
    s = re.sub(r'<script src="(js/[^"]+)"></script>', lambda m: '<script>' + (ROOT / m.group(1)).read_text() + '</script>', s)
    if video:
        s = s.replace('src="assets/hero.mp4"', f'src="{data_uri(video)}"')
    # remaining asset refs in src/href/url()
    s = re.sub(r'(src|href|poster)="assets/([^"]+)"', lambda m: f'{m.group(1)}="{data_uri("assets/" + m.group(2))}"', s)
    s = s.replace('href="favicon.ico"', f'href="{data_uri("favicon.ico")}"')
    s = inline_css(s)
    return s

import json
# Script added to every embedded page: links that would leave the file talk to the outer page instead.
BRIDGE = """<script>
if (window.parent !== window) document.addEventListener('click', function (e) {
  var a = e.target.closest ? e.target.closest('a') : null; if (!a) return;
  var h = a.getAttribute('href') || '', m = h.match(/^(privacy|terms)\\.html(?:#(.*))?/), c = h.match(/^(remote-launchpad|social-media-manager|virtual-assistant|ai-project-manager|masterclass)\\.html/);
  if (m) { e.preventDefault(); parent.postMessage({ leepx: 'legal', page: m[1], hash: m[2] || '' }, '*'); }
  else if (c) { e.preventDefault(); parent.postMessage({ leepx: 'page', page: c[1] }, '*'); }
  else if (h.indexOf('assess.html') === 0) { e.preventDefault(); parent.postMessage({ leepx: 'assess' }, '*'); }
  else if (h.indexOf('index.html') === 0) { e.preventDefault(); parent.postMessage({ leepx: 'close', hash: h.split('#')[1] || '' }, '*'); }
});
</script></body>"""

# --- assessment and legal pages → standalone docs shown in overlays ---
assess = inline_page('assess.html').replace('</body>', BRIDGE)
legal = {name: inline_page(name + '.html').replace('</body>', BRIDGE) for name in ('privacy', 'terms')}
legal_json = json.dumps(legal).replace('</', '<\\/')
COURSE_PAGES = ('remote-launchpad', 'social-media-manager', 'virtual-assistant', 'ai-project-manager', 'masterclass')
pages = {name: inline_page(name + '.html').replace('</body>', BRIDGE) for name in COURSE_PAGES}
pages_json = json.dumps(pages).replace('</', '<\\/')

# --- landing ---
index = inline_page('index.html', video='assets/hero-sm.mp4')
index = index.replace('href="assess.html"', 'href="#assess"')
overlay = f"""
<style>
  #lxOverlay,#lxLegal,#lxPage{{position:fixed;inset:0;z-index:1000;background:#fff;display:none}}
  #lxPage{{z-index:999}} #lxLegal{{z-index:1001}}
  #lxOverlay.open,#lxLegal.open,#lxPage.open{{display:block}}
  #lxOverlay iframe,#lxLegal iframe,#lxPage iframe{{width:100%;height:100%;border:0}}
  body.lx-locked{{overflow:hidden}}
</style>
<div id="lxOverlay" aria-label="LeepX self-assessment"><iframe id="lxFrame" title="LeepX self-assessment" srcdoc="{html.escape(assess, quote=True)}"></iframe></div>
<div id="lxLegal"><iframe id="lxLegalFrame" title="LeepX policies"></iframe></div>
<div id="lxPage"><iframe id="lxPageFrame" title="LeepX course page"></iframe></div>
<script type="application/json" id="lxLegalData">{legal_json}</script>
<script type="application/json" id="lxPageData">{pages_json}</script>
<script>
(function(){{
  const ov=document.getElementById('lxOverlay'), lg=document.getElementById('lxLegal'), lf=document.getElementById('lxLegalFrame');
  const LEGAL=JSON.parse(document.getElementById('lxLegalData').textContent);
  const PAGES=JSON.parse(document.getElementById('lxPageData').textContent), pg=document.getElementById('lxPage'), pf=document.getElementById('lxPageFrame');
  function lock(){{ document.body.classList.toggle('lx-locked', ov.classList.contains('open')||lg.classList.contains('open')||pg.classList.contains('open')); }}
  function openPage(name,noPush){{ if(!PAGES[name]) return; pf.srcdoc=PAGES[name]; pg.classList.add('open'); lock(); if(!noPush && location.hash!=='#'+name) history.pushState(null,'','#'+name); }}
  function closePage(){{ pg.classList.remove('open'); pf.srcdoc=''; lock(); if(PAGES[location.hash.slice(1)]) history.replaceState(null,'',location.pathname+location.search); }}
  function open(){{ ov.classList.add('open'); lock(); }}
  function close(hash){{ ov.classList.remove('open'); lock(); history.replaceState(null,'',location.pathname+location.search+(hash?'#'+hash:'')); if(hash){{ const el=document.getElementById(hash); if(el) el.scrollIntoView(); }} }}
  function openLegal(page,hash){{ lf.onload=function(){{ if(hash){{ const el=lf.contentDocument.getElementById(hash); if(el) el.scrollIntoView(); }} }}; lf.srcdoc=LEGAL[page]; lg.classList.add('open'); lock(); }}
  function closeLegal(){{ lg.classList.remove('open'); lf.srcdoc=''; lock(); }}
  document.querySelectorAll('a[href="#assess"]').forEach(a=>a.addEventListener('click',e=>{{e.preventDefault();history.pushState(null,'','#assess');open();}}));
  document.addEventListener('click',e=>{{ const a=e.target.closest('a'); if(!a) return; const h=a.getAttribute('href')||''; const m=h.match(/^(privacy|terms)\\.html(?:#(.*))?/); if(m){{ e.preventDefault(); openLegal(m[1],m[2]||''); return; }} const c=h.match(/^(remote-launchpad|social-media-manager|virtual-assistant|ai-project-manager|masterclass)\\.html/); if(c){{ e.preventDefault(); openPage(c[1]); }} }});
  window.addEventListener('message',e=>{{ const d=e.data||{{}}; if(d.leepx==='legal') openLegal(d.page,d.hash); else if(d.leepx==='page') openPage(d.page); else if(d.leepx==='assess'){{ history.pushState(null,'','#assess'); open(); }} else if(d.leepx==='close'){{ if(lg.classList.contains('open')) closeLegal(); else if(ov.classList.contains('open')) close(d.hash); else {{ closePage(); if(d.hash){{ const el=document.getElementById(d.hash); if(el) el.scrollIntoView(); }} }} }} }});
  function route(){{ const h=location.hash.slice(1); if(h==='assess'){{ if(pg.classList.contains('open')) closePage(); open(); }} else if(PAGES[h]){{ if(ov.classList.contains('open')) ov.classList.remove('open'); openPage(h,true); }} else {{ if(pg.classList.contains('open')) closePage(); if(ov.classList.contains('open')) close(h); }} }}
  window.addEventListener('popstate',route);
  route();
}})();
</script>
</body>"""
index = index.replace('</body>', overlay)
OUT.write_text(index)
print(OUT, f"{OUT.stat().st_size/1e6:.1f} MB")
