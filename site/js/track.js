/* Visitor tracking: loads Google Analytics and Microsoft Clarity only when their IDs are set in config.js.
   lxTrack('event_name', {details}) records a custom event in both. Safe to call when tracking is off. */
(function () {
  var C = window.LEEPX_CONFIG || {};
  window.lxTrack = function (name, data) {
    try { if (window.gtag) window.gtag('event', name, data || {}); } catch (e) {}
    try { if (window.clarity) window.clarity('event', name); } catch (e) {}
  };
  if (C.GA_ID) {
    var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=' + C.GA_ID; document.head.appendChild(g);
    window.dataLayer = window.dataLayer || []; window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date()); window.gtag('config', C.GA_ID);
  }
  if (C.CLARITY_ID) {
    (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); }; t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y); })(window, document, 'clarity', 'script', C.CLARITY_ID);
  }
  // one-time notice when tracking is on
  if ((C.GA_ID || C.CLARITY_ID) && window.self === window.top) {
    var seen = false; try { seen = localStorage.getItem('lx_cookie_ok') === '1'; } catch (e) {}
    if (!seen) document.addEventListener('DOMContentLoaded', function () {
      var b = document.createElement('div');
      b.setAttribute('style', 'position:fixed;left:16px;right:16px;bottom:16px;z-index:999;max-width:520px;margin:0 auto;background:#171618;color:#fff;border-radius:16px;padding:14px 16px;font:500 14px/1.45 "Plus Jakarta Sans",system-ui,sans-serif;display:flex;gap:12px;align-items:center;box-shadow:0 12px 40px rgba(0,0,0,.25)');
      b.innerHTML = '<span style="flex:1">We use cookies to understand how this site is used and to improve it.</span><button style="border:0;border-radius:99px;background:#C6F04A;color:#171618;font:800 13px inherit;padding:9px 16px;cursor:pointer">OK</button>';
      b.querySelector('button').onclick = function () { try { localStorage.setItem('lx_cookie_ok', '1'); } catch (e) {} b.remove(); };
      document.body.appendChild(b);
    });
  }
  // button clicks worth knowing about
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a,button') : null; if (!a) return;
    var href = a.getAttribute('href') || '', text = (a.textContent || '').trim().slice(0, 60);
    if (href.indexOf('assess') > -1) window.lxTrack('assessment_button_click', { label: text });
    if (a.classList.contains('wa')) window.lxTrack('whatsapp_click');
    if (/Join the cohort/.test(text)) window.lxTrack('join_cohort_click', { label: text });
    if (/Join the waitlist/.test(text)) window.lxTrack('join_waitlist_click', { label: text });
  });
})();
