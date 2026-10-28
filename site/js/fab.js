// Floating "Upcoming Masterclass" button. Set MASTERCLASS_URL and MASTERCLASS_UNTIL in js/config.js.
// The button disappears on its own from the MASTERCLASS_UNTIL date (India time). Empty URL = no button.
(function(){
  var cfg = window.LEEPX_CONFIG || {};
  var url = cfg.MASTERCLASS_URL, until = cfg.MASTERCLASS_UNTIL;
  if (!url) return;
  // Not on the masterclass page itself: the visitor is already there.
  var page = document.body && document.body.getAttribute('data-page');
  var here = (location.pathname.split('/').pop() || '').toLowerCase();
  if (page === 'masterclass' || (here && url.toLowerCase().indexOf(here) === 0)) return;
  if (until && new Date() >= new Date(until + 'T00:00:00+05:30')) return;
  var a = document.createElement('a');
  a.className = 'fab'; a.href = url; if (/^https?:/.test(url)) { a.target = '_blank'; a.rel = 'noopener'; }
  a.innerHTML = '<i></i><span><small>Upcoming</small><b>Masterclass \u2192</b></span>';
  a.addEventListener('click', function(){ window.lxTrack && lxTrack('masterclass_click'); });
  document.body.appendChild(a);
})();
