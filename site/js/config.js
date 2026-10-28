/* LeepX launch settings. This is the only file that needs editing to connect the site to the outside world.
   Leave a value empty ('') to switch that feature off. */
window.LEEPX_CONFIG = {
  // Google Sheet web-app link (from Apps Script → Deploy). Every form answer is sent here.
  LEAD_ENDPOINT: 'https://script.google.com/macros/s/AKfycbwpsiXxLNCS8UlhtQyKeBFOeZOTmh7M17AnQwctaiOisj6Gjh8-SxwsAE08mc1wHTLJ/exec',

  // Where the "Join the cohort" buttons on the result page go.
  CHECKOUT: {
    launchpad: 'https://academy.theleepx.com/l/84561c3c5b',   // Remote Launchpad (Remote Career Launchpad Plus)
    linkedin: 'https://academy.theleepx.com/l/e44abed2fc',    // Attract inbound via LinkedIn
    smm: 'https://academy.theleepx.com/web/checkout/6a7739472e3b4113124f0600',   // Become a Social Media Manager
    va: 'https://academy.theleepx.com/web/checkout/6a1b333e808d71fed1f65298?purchaseNow=true',
    pm: 'https://academy.theleepx.com/l/c48219926c',          // Become a Virtual Assistant
  },

  // Team WhatsApp number: country code + number, digits only.
  WHATSAPP_NUMBER: '918264599906',
  // Waitlist cohorts (Freelancing, AI-powered Project Manager). Empty = open WhatsApp with a ready-made waitlist message.
  WAITLIST_URL: '',
  // Floating "Upcoming Masterclass" button. Hidden automatically from MASTERCLASS_UNTIL (YYYY-MM-DD, India time). Empty URL = no button.
  MASTERCLASS_URL: 'masterclass.html',
  MASTERCLASS_UNTIL: '2026-11-14',
  COMMUNITY_URL: 'https://academy.theleepx.com/l/ad00303ec0',

  // Visitor tracking. Empty = off.
  GA_ID: '',        // Google Analytics Measurement ID, looks like G-XXXXXXXXXX
  CLARITY_ID: '',   // Microsoft Clarity Project ID, looks like abcd1234ef
};
