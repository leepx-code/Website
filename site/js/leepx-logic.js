/* LeepX Self-Assessment — questions, scoring, routing.
   Mirrors docs/Assessment-Logic.md. Keep both in sync. */
(function (global) {
  'use strict';

  // Launch settings live in js/config.js (window.LEEPX_CONFIG). These are the fallbacks.
  const CONFIG = Object.assign({
    LEAD_ENDPOINT: '',
    WHATSAPP_NUMBER: '',
    WAITLIST_URL: '',
    MASTERCLASS_URL: '', MASTERCLASS_UNTIL: '',
    COMMUNITY_URL: '',
    CHECKOUT: {},
  }, global.LEEPX_CONFIG || {});
  // WhatsApp link with a ready-made message. Falls back to '#' until a number is set.
  CONFIG.wa = function (text) { return CONFIG.WHATSAPP_NUMBER ? 'https://wa.me/' + CONFIG.WHATSAPP_NUMBER + '?text=' + encodeURIComponent(text) : '#whatsapp'; };

  /* ---------------- Questions ---------------- */
  const Q = [
    { id: 'situation', block: 'A', type: 'single',
      title: 'First things first. What does work feel like right now?',
      sub: 'No wrong answer. We just want to know where you are.',
      options: [
        ['job_stuck','briefcase', 'In a job, but stuck or underpaid'],
        ['job_ok_bored','trending-up', 'Job is fine. I want more: money, freedom, remote'],
        ['freelance_unstable','activity', 'Freelancing, but income is a rollercoaster'],
        ['student','graduation-cap', 'Student or fresh graduate'],
        ['break','sprout', 'On a break (parenting, health, moving, life)'],
        ['unemployed','search', 'Between jobs, actively looking'],
      ] },
    { id: 'blockers', block: 'A', type: 'multi', max: 3,
      title: 'Where do you usually get stuck?',
      sub: 'Pick up to three. Be honest, this is the useful bit.',
      options: [
        ['no_direction','compass', "I don't know which path fits me"],
        ['no_skills','wrench', 'I know the direction, not the skills'],
        ['no_portfolio','folder', 'I have skills but nothing to show'],
        ['no_interviews','inbox', 'I apply, nobody replies'],
        ['fail_interviews','mic', 'I reach interviews, then it fizzles'],
        ['no_clients','handshake', "I can't find or price clients"],
        ['no_where','map-pin', "I don't know where to apply (I know the role, tools, skills)"],
        ['no_time','clock', "I can't find the time"],
      ] },
    { id: 'experience', block: 'B', type: 'single',
      title: 'How many years have you worked professionally?',
      sub: 'Internships count as half.',
      options: [['0','sprout','None yet'],['lt1','hourglass','Under a year'],['1_3','calendar','1 to 3'],['3_6','flame','3 to 6'],['6_10','building','6 to 10'],['10p','award','10+']] },
    { id: 'industry', block: 'B', type: 'multi', layout: 'picker', noun: 'industries',
      title: 'Which industries have you worked in?',
      sub: 'Pick all that apply. Search, or browse by category.',
      none: ['none', 'No industry yet'],
      groups: [
        { label: 'Marketing, media & creative', cat: 'creative', items: ['Marketing / advertising', 'Digital marketing agency', 'Media / entertainment', 'Publishing / journalism', 'PR / communications', 'Design / creative', 'Fashion / beauty', 'E-commerce / D2C', 'Gaming / esports', 'Events / weddings', 'Film / production', 'Music / audio'] },
        { label: 'Tech & product', cat: 'corp', items: ['IT services', 'Software / SaaS', 'Startups', 'Fintech', 'AI / data', 'Telecom', 'Cybersecurity', 'Hardware / electronics'] },
        { label: 'Business & finance', cat: 'corp', items: ['Banking', 'Financial services', 'Insurance', 'Accounting / audit', 'Consulting', 'Legal', 'Real estate', 'Construction', 'Manufacturing', 'Engineering', 'Automobile', 'Energy / oil & gas', 'Import / export'] },
        { label: 'Services & people', cat: 'service', items: ['Education', 'Edtech', 'Healthcare', 'Pharma', 'Hospitality', 'Travel / tourism', 'Aviation', 'Retail', 'FMCG', 'Food & beverage', 'HR / staffing', 'BPO / KPO', 'Customer service', 'Logistics / supply chain', 'Admin / operations', 'Wellness / fitness', 'Beauty / salon'] },
        { label: 'Public & social', cat: 'other', items: ['Government / public sector', 'Non-profit / NGO', 'Defence', 'Agriculture', 'Research / academia', 'Religious / community organisations'] },
      ] },
    { id: 'roles_done', block: 'B', type: 'multi', layout: 'picker', noun: 'kinds of work',
      title: 'What kind of work have you actually done?',
      sub: 'Pick everything that applies. Internships and freelance gigs count.',
      none: ['none', 'Nothing professional yet'],
      groups: [
        { label: 'Marketing & content', cat: 'social', items: ['Social media management', 'Content creation', 'Copywriting', 'Content writing / blogging', 'Marketing (general)', 'SEO', 'Performance marketing / ads', 'Email marketing', 'Influencer marketing', 'Community management', 'PR / communications', 'Brand management', 'Market research'] },
        { label: 'Design & creative', cat: 'social', items: ['Graphic design', 'Video editing', 'UI / UX design', 'Photography', 'Videography', 'Motion graphics', 'Illustration', 'Podcast / audio editing'] },
        { label: 'Operations & support', cat: 'ops', items: ['Admin / office management', 'Executive assistant', 'Virtual assistance', 'Customer support', 'Customer success', 'Operations', 'Project coordination', 'Event management', 'Data entry', 'Bookkeeping', 'Procurement / vendor management', 'Travel coordination', 'Inbox / calendar management', 'Transcription', 'Back-office processing'] },
        { label: 'Product, tech & data', cat: 'pm', items: ['Project management', 'Product management', 'Program management', 'Scrum master / agile', 'Business analysis', 'Data analysis', 'Software development', 'Web development', 'QA / testing', 'IT support', 'No-code / automation building', 'Research'] },
        { label: 'Sales & business', cat: 'biz', items: ['Sales', 'Business development', 'Lead generation', 'Account management', 'Partnerships', 'Consulting', 'Founder / ran my own business', 'Fundraising', 'Strategy'] },
        { label: 'People, finance & teaching', cat: 'people', items: ['HR / recruiting', 'Training / L&D', 'Teaching / tutoring', 'Coaching / mentoring', 'Finance / accounting', 'Legal / compliance', 'Healthcare / clinical', 'Hospitality / front desk', 'Retail / store', 'Translation'] },
      ] },
    { id: 'tools', block: 'B', type: 'multi', layout: 'picker', noun: 'tools',
      title: 'Which tools could you open right now without panicking?',
      sub: 'Pick all that apply. Search, or browse by category.',
      none: ['none', 'None of these'],
      groups: [
        { label: 'Design', cat: 'design', items: ['Canva', 'Figma', 'Adobe Photoshop', 'Adobe Illustrator', 'Adobe InDesign', 'Adobe Express', 'Adobe Lightroom', 'Adobe XD', 'Sketch', 'Procreate', 'CorelDRAW', 'Miro', 'FigJam'] },
        { label: 'Video & audio', cat: 'video', items: ['CapCut', 'Premiere Pro', 'After Effects', 'DaVinci Resolve', 'Final Cut Pro', 'InShot', 'VN Editor', 'Filmora', 'Descript', 'Audacity', 'OBS Studio', 'Loom', 'Riverside'] },
        { label: 'Social media', cat: 'social', items: ['Instagram Insights', 'Meta Business Suite', 'LinkedIn analytics', 'YouTube Studio', 'TikTok', 'X / Twitter', 'Pinterest', 'Threads', 'Buffer', 'Hootsuite', 'Later', 'Sprout Social', 'Metricool', 'Linktree', 'ManyChat'] },
        { label: 'Ads & analytics', cat: 'ads', items: ['Meta Ads', 'Google Ads', 'LinkedIn Ads', 'Google Analytics', 'Google Search Console', 'Google Tag Manager', 'Looker Studio', 'Hotjar', 'Microsoft Clarity'] },
        { label: 'SEO & writing', cat: 'seo', items: ['SEMrush', 'Ahrefs', 'Ubersuggest', 'Yoast SEO', 'Grammarly', 'Hemingway', 'Surfer SEO', 'Medium / Substack'] },
        { label: 'Email & CRM', cat: 'crm', items: ['Mailchimp', 'Klaviyo', 'Kit (ConvertKit)', 'Brevo', 'HubSpot', 'Zoho CRM', 'Salesforce', 'Pipedrive', 'Freshsales', 'Apollo', 'LinkedIn Sales Navigator', 'Lemlist'] },
        { label: 'Project management', cat: 'pm', items: ['Notion', 'Asana', 'ClickUp', 'Trello', 'Monday.com', 'Jira', 'Confluence', 'Basecamp', 'Airtable', 'Smartsheet', 'Linear', 'Microsoft Project', 'Todoist'] },
        { label: 'Communication & scheduling', cat: 'comms', items: ['Slack', 'Microsoft Teams', 'Zoom', 'Google Meet', 'Calendly', 'Google Calendar', 'Outlook', 'Discord', 'WhatsApp Business', 'Telegram'] },
        { label: 'Docs & spreadsheets', cat: 'docs', items: ['Google Docs', 'Google Sheets', 'Google Slides', 'Google Forms', 'Google Drive', 'Microsoft Word', 'Excel', 'Excel (pivots, formulas)', 'PowerPoint', 'Dropbox', 'Typeform'] },
        { label: 'Data', cat: 'data', items: ['SQL', 'Power BI', 'Tableau', 'Python', 'R', 'Google BigQuery'] },
        { label: 'AI tools', cat: 'ai', items: ['ChatGPT', 'Claude', 'Gemini', 'Perplexity', 'Microsoft Copilot', 'Notion AI', 'Midjourney', 'DALL·E / AI image tools', 'ElevenLabs', 'HeyGen / AI video', 'Gamma', 'Otter / Fireflies'] },
        { label: 'Automation', cat: 'automation', items: ['Zapier', 'Make', 'n8n', 'IFTTT', 'Google Apps Script'] },
        { label: 'Customer support', cat: 'support', items: ['Zendesk', 'Freshdesk', 'Intercom', 'Zoho Desk', 'Tidio'] },
        { label: 'Websites & e-commerce', cat: 'web', items: ['WordPress', 'Webflow', 'Wix', 'Framer', 'Squarespace', 'Shopify', 'WooCommerce', 'Carrd', 'Amazon Seller Central'] },
        { label: 'Finance & admin', cat: 'finance', items: ['QuickBooks', 'Zoho Books', 'Tally', 'Xero', 'Razorpay / Stripe', 'DocuSign', 'LastPass / 1Password'] },
        { label: 'Freelance platforms', cat: 'freelance', items: ['Upwork', 'Fiverr', 'Freelancer.com', 'Toptal', 'Contra', 'LinkedIn job search'] },
        { label: 'Development', cat: 'dev', items: ['GitHub', 'VS Code', 'HTML / CSS', 'JavaScript', 'Postman', 'Bubble'] },
      ] },
    { id: 'income', block: 'B', type: 'single',
      title: 'What do you earn a month right now (or last did)?',
      sub: 'Monthly, in US dollars. Stays private. We use it to keep our advice realistic.',
      options: [['0','wallet','Nothing right now'],['lt15','wallet','Under $200'],['15_30','wallet','$200 to $400'],['30_50','wallet','$400 to $600'],['50_80','wallet','$600 to $1,000'],['80_150','wallet','$1,000 to $1,800'],['150p','wallet','$1,800+']] },
    { id: 'dream_income', block: 'B', type: 'single',
      title: 'And what would feel like a real win, monthly?',
      sub: 'In US dollars. Dream a little. Then we will get practical.',
      options: [['600','sparkles','$600'],['1000','sparkles','$1,000'],['1500','sparkles','$1,500'],['2500','sparkles','$2,500'],['4000p','dollar-sign','$4,000+']] },
    { id: 'leap', block: 'C', type: 'multi',
      title: 'What kind of leap are you after?',
      sub: 'Pick all that apply.',
      options: [
        ['job_to_freelance','plane','Job → freelancing / remote clients'],['freelance_to_job','house','Freelancing → a stable remote job'],
        ['switch_role','refresh-cw','Same industry, new role'],['switch_industry','globe','New industry entirely'],
        ['first_job','target','My first real role'],['side_income','moon','Keep my job, add a side income'],['unsure','circle-question-mark','Honestly, not sure yet'],
      ] },
    { id: 'roles_interest', block: 'C', type: 'multi',
      title: 'Do any of our cohorts interest you?',
      sub: 'Pick any that sound right. "Not sure" is a perfectly good answer.',
      options: [
        ['launchpad','rocket','Remote Launchpad','Start here if you are new to remote work. We will help you pick a role. Then you learn the tools, build a complete portfolio and send your first applications.'],
        ['smm','smartphone','Become a Social Media Manager','For people who enjoy content and brands. Learn strategy, content and analytics, build a portfolio on a real brand, and pitch it with a deck and outreach plan.'],
        ['va','user','Become a Virtual Assistant','12 weeks. For organised people who like running things. Manage inboxes, calendars, research and operations for founders abroad, with work samples and a first paid trial.'],
        ['linkedin','link','Attract inbound via LinkedIn','For professionals who want opportunities to come to them. Rework your headline and story, build a content system, and get recruiters and clients messaging you first.'],
        ['freelance','trending-up','Scale your freelancing career','Waitlist open. For people already freelancing or taking side clients. Find better clients, raise your rates, package your services and build steady monthly income.'],
        ['pm','puzzle','Become an AI-powered Project Manager','16 weeks. For people with some work experience who coordinate teams. Learn planning, sprints and stakeholder communication with AI tools, plus case studies and interview prep.'],
        ['unsure','circle-question-mark','Not sure yet','No problem. Tell us about yourself and we will suggest the cohort that fits.'],
      ] },
    { id: 'intl', block: 'C', type: 'single',
      title: 'Ever worked with an international client or company?',
      options: [['yes_paid','globe','Yes, paid work directly with them'],['via_indian','building','Yes, international clients but via an Indian company'],['yes_unpaid','graduation-cap','Only internships or volunteering'],['no','circle-off','Not yet']] },
    { id: 'interviews', block: 'C', type: 'single',
      title: 'Interviews in the last six months?',
      options: [['none_applied','armchair',"Haven't applied"],['applied_no_calls','inbox','Applied, no calls'],['some_calls','mic','A few interviews, no offer'],['offers','circle-question-mark','Offers, but not what I want']] },
    { id: 'hours', block: 'D', type: 'single',
      title: 'Realistically, how many hours a week can you give this?',
      sub: 'Realistic beats ambitious. We plan around this.',
      options: [['lt3','clock','Under 3'],['3_6','timer','3 to 6'],['6_10','zap','6 to 10'],['10p','rocket','10+']] },
    { id: 'budget', block: 'D', type: 'single',
      title: 'If the right path were clear, what could you invest in it?',
      sub: 'One-time, in US dollars. EMI is available. So we only recommend what fits your life.',
      options: [['0','gift','Not right now. FREE resources please'],['200_300','wallet','$200 to $300'],['300_400','wallet','$300 to $400'],['400_500','package','$400 to $500'],['500_600','zap','$500 to $600'],['600_700','rocket','$600 to $700']] },
  ];

  const slug = l => l.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
  const CAT = {}; // question id -> { option key -> category }
  Q.forEach(q => { if (!q.groups) return; CAT[q.id] = {};
    q.groups.forEach(g => { g.options = g.items.map(l => [slug(l), '', l]); g.options.forEach(o => { CAT[q.id][o[0]] = g.cat; }); });
    q.options = q.groups.flatMap(g => g.options); if (q.none) q.options.push([q.none[0], '', q.none[1]]); });
  // keys used before the lists were expanded (old leads, saved test links)
  Object.assign(CAT.roles_done, { social_content: 'social', marketing: 'social', design: 'social', content_writing: 'social', seo_perf: 'social', community: 'social', pr_comms: 'social', admin_ea: 'ops', virtual_assist: 'ops', customer_support: 'ops', ops: 'ops', project_coord: 'ops', event: 'ops', hr_recruit: 'people', product: 'pm', dev: 'pm', data_analysis: 'pm', qa: 'pm', founder: 'biz', sales: 'biz', consulting: 'biz' });
  Object.assign(CAT.tools, { canva: 'design', figma: 'design', adobe: 'design', capcut_premiere: 'video', ig_native: 'social', scheduling: 'social', meta_ads: 'ads', google_ads: 'ads', ga: 'ads', notion: 'pm', asana_clickup_trello: 'pm', monday: 'pm', jira: 'pm', slack_teams: 'comms', calendly: 'comms', gworkspace: 'docs', excel_adv: 'docs', powerbi: 'data', sql: 'data', chatgpt_ai: 'ai', midjourney: 'ai', zapier_make: 'automation', hubspot_crm: 'crm' });
  Object.assign(CAT.industry, { marketing_media: 'creative', design_creative: 'creative', media_ent: 'creative', ecommerce: 'creative', ops_admin: 'service', hospitality_retail: 'service', hospitality: 'service', retail: 'service', education: 'service', bpo: 'service', hr: 'service', tech_product: 'corp', finance: 'corp', consulting: 'corp', manufacturing: 'corp', telecom: 'corp' });

  /* ---------------- Reflections ---------------- */
  const REFLECT = {
    no_direction: "Not knowing <em>which</em> door to knock on is more tiring than knocking. Let's fix that first.",
    no_skills: "You've picked a direction. That's the hard part most people skip.",
    no_portfolio: "Skills without proof read as 'no skills' to a recruiter. Fixable in weeks, not years.",
    no_interviews: "Applying into a void isn't a you problem. It's a positioning problem.",
    fail_interviews: "Getting to the final round means you're good. Converting is a separate skill.",
    no_clients: "Finding clients is a system, not luck. We'll show you ours.",
    no_where: "You've done the hard part. Knowing <em>where</em> to apply is the quickest gap to close.",
    no_time: "Then we design around 5 focused hours a week, not 15.",
    break: "A break isn't a gap. It's the reason remote work exists.",
    unemployed: "Job hunts are lonely. You've got company now.",
    intl_no: "Most of our learners hadn't either. International clients care about proof, not passports.",
  };

  /* ---------------- Tracks ---------------- */
  const TRACKS = {
    smm: { name: 'Social Media Manager', short: 'SMM', available: true, icon: 'smartphone',
      tagline: 'Run brand accounts that grow. Remote, freelance-friendly, in demand.',
      program: 'SMM Accelerator · 8 weeks · 11 modules · portfolio built on a real target brand',
      income: { Explorer: '$200–500/month within 4–6 months', Builder: '$400–700/month within 3–5 months', Launcher: '$600–1,200+/month within 2–4 months' },
      timeline: { Explorer: '8 weeks to a pitch-ready portfolio', Builder: '6–8 weeks to first pitches', Launcher: '3–4 weeks to first client conversations' },
      steps: {
        Explorer: ['Pick one niche you already consume content in (fitness, D2C, finance, food).', 'Audit three brand accounts in it: what they post, how often, what gets saved.', 'Rebuild one of their posts in Canva. That is portfolio piece #1.'],
        Builder: ['Choose one target brand and write a 30-day content strategy for it.', 'Turn it into a 6-slide pitch deck (we will show you the structure).', 'DM 10 small brands this week with one useful observation each.'],
        Launcher: ['Package what you have into a one-page SMM profile with 2–3 pricing tiers.', 'Send 20 personalised DMs to brands in one niche over 5 days.', 'Follow up twice. Most yeses arrive on follow-up two.'],
      } },
    va: { name: 'Virtual Assistant / Online Business Manager', short: 'VA', available: true, icon: 'user',
      tagline: 'Be the right hand founders pay to offload to. Global clients, flexible hours.',
      program: 'VA Accelerator · 13 modules · from workspace setup to Upwork proposals',
      income: { Explorer: '$250–550/month within 4–6 months', Builder: '$400–850/month within 3–5 months', Launcher: '$700–1,500+/month within 2–4 months' },
      timeline: { Explorer: '8–10 weeks to a services page and work samples', Builder: '5–7 weeks to first proposals', Launcher: '2–4 weeks to first paid trial' },
      steps: {
        Explorer: ['List the 10 tasks you already do that someone would pay to offload (inbox, calendar, research, sheets).', 'Set up a clean Google Workspace + Notion dashboard for yourself. That is your first sample.', 'Write one SOP for a task you do weekly.'],
        Builder: ['Pick a niche (coaches, D2C founders, agencies) and write your 3 starter services.', 'Create 2 work samples: a project tracker and a client onboarding doc.', 'Draft a 5-line outreach script and send it to 5 founders you already follow.'],
        Launcher: ['Rewrite your Upwork / LinkedIn headline around outcomes, not tasks.', 'Send 15 proposals this week using the pain → plan → proof structure.', 'Offer a paid 2-week trial instead of a free one.'],
      } },
    pm: { name: 'Project Manager', short: 'PM', available: true, icon: 'puzzle',
      tagline: 'Plan, unblock and ship with teams. The high-growth remote path.',
      program: 'PM track · planning, sprints, stakeholder comms, Notion / Asana / ClickUp / Jira',
      income: { Explorer: '$500–850/month within 5–7 months', Builder: '$700–1,200/month within 3–5 months', Launcher: '$1,200–2,200+/month within 2–4 months' },
      timeline: { Explorer: '10–12 weeks to a PM portfolio', Builder: '6–8 weeks to interview-ready', Launcher: '3–5 weeks to targeted applications' },
      steps: {
        Explorer: ['Take one messy thing you coordinate today and turn it into a project plan with owners and dates.', 'Learn one tool deeply (Notion or Asana). Rebuild that plan in it.', 'Write a one-paragraph retrospective: what slipped and why.'],
        Builder: ['Document 2 past projects as case studies: goal, plan, risks, outcome.', 'Run a mock sprint on a personal project for 2 weeks.', 'Rewrite your CV bullets as outcomes with numbers.'],
        Launcher: ['Shortlist 20 remote-first companies hiring PMs / program coordinators.', 'Prepare 3 STAR stories around conflict, slippage and stakeholder pushback.', 'Reach out to one PM at each company before applying.'],
      } },
    fo: { name: "Founder's Office / Chief of Staff", short: 'FO', available: false, icon: 'brain',
      tagline: 'The generalist right hand to a founder. Ops, strategy, execution. High leverage.',
      program: "Founder's Office track · ops, strategy decks, hiring, metrics, execution rhythm",
      income: { Explorer: '$600–1,000/month within 5–7 months', Builder: '$1,000–1,800/month within 3–5 months', Launcher: '$1,800–3,000+/month within 2–4 months' },
      timeline: { Explorer: '10–12 weeks to a strategy + ops portfolio', Builder: '6–8 weeks to targeted outreach', Launcher: '3–5 weeks to founder conversations' },
      steps: {
        Explorer: ['Pick one startup you admire and write a one-page teardown: model, metrics, next 3 bets.', 'Build a simple weekly-metrics dashboard in Sheets for a made-up business.', 'Read three founder investor updates and note what they track.'],
        Builder: ['Turn a past project into a strategy memo (problem, options, recommendation).', 'Write 3 SOPs you would hand a new hire on day one.', 'Reach out to 5 founders with a specific observation about their business.'],
        Launcher: ['Position yourself around one stage (seed / Series A) and one function you are strongest in.', 'Send 10 tailored notes to founders and CoS on LinkedIn this week.', 'Prepare a 90-day plan template you can adapt in any conversation.'],
      } },
  };

  /* ---------------- Scoring ---------------- */
  const EXP = { '0': 0, lt1: 0.5, '1_3': 2, '3_6': 4.5, '6_10': 8, '10p': 12 };
  const INC = { '0': 0, lt15: 100, '15_30': 300, '30_50': 500, '50_80': 800, '80_150': 1400, '150p': 2200 }; // USD / month
  const GOAL = { '600': 600, '1000': 1000, '1500': 1500, '2500': 2500, '4000p': 4000 }; // USD / month
  const has = (arr, ...vals) => Array.isArray(arr) && vals.some(v => arr.includes(v));

  function score(a) {
    a = a || {};
    const exp = EXP[a.experience] ?? 0;
    const incomeNow = INC[a.income] ?? 0;
    const incomeGoal = GOAL[a.dream_income] ?? 600;
    const incomeGap = Math.max(0, incomeGoal - incomeNow);
    const roles = a.roles_done || [], tools = a.tools || [], interest = a.roles_interest || [], blockers = a.blockers || [];
    const leap = Array.isArray(a.leap) ? a.leap : (a.leap ? [a.leap] : []);

    const cats = (arr, id) => new Set(arr.map(k => CAT[id][k]).filter(Boolean));
    const roleCats = cats(roles, 'roles_done'), toolCats = cats(tools, 'tools');
    const anyCat = (set, ...c) => c.some(x => set.has(x));
    const social = roleCats.has('social') || anyCat(toolCats, 'design', 'video', 'social', 'ads');
    const ops = roleCats.has('ops') || anyCat(toolCats, 'docs', 'comms', 'automation', 'support', 'finance');
    const pmx = roleCats.has('pm') || has(roles, 'project_coordination', 'project_coord') || anyCat(toolCats, 'pm', 'data');
    const fox = exp >= 3 && (roleCats.has('biz') || has(roles, 'product_management', 'operations', 'product', 'ops'));
    const ind = Array.isArray(a.industry) ? a.industry : (a.industry ? [a.industry] : []);
    const directionGap = has(blockers, 'no_direction') || has(leap, 'unsure') || has(interest, 'unsure');

    const s = { smm: 20, va: 20, pm: 20, fo: 20 };
    const add = (o) => { for (const k in o) s[k] += o[k]; };
    ['smm', 'va', 'pm', 'fo'].forEach(t => { if (interest.includes(t)) s[t] += 30; });
    if (interest.includes('launchpad')) add({ smm: 10, va: 12 });
    if (interest.includes('freelance')) add({ smm: 8, va: 8 });
    if (interest.includes('linkedin')) add({ pm: 4, fo: 4 });
    if (social) s.smm += 20;
    if (ops) add({ va: 20, pm: 8, fo: 8 });
    if (pmx) add({ pm: 20, fo: 8 });
    if (fox) add({ pm: 8, fo: 20 });
    const indCats = cats(ind, 'industry');
    if (indCats.has('creative')) s.smm += 10;
    if (indCats.has('service')) s.va += 10;
    if (indCats.has('corp')) add({ pm: 10, fo: 10 });
    if (exp < 1) add({ smm: 8, va: 12, pm: -10, fo: -15 });
    else if (exp < 3) add({ smm: 5, va: 8, pm: 5, fo: -5 });
    else if (exp < 6) add({ va: 2, pm: 12, fo: 10 });
    else add({ smm: -5, va: -5, pm: 12, fo: 15 });
    if (has(leap, 'job_to_freelance', 'side_income')) add({ smm: 10, va: 12, pm: -5, fo: -10 });
    if (has(leap, 'freelance_to_job')) add({ smm: -5, va: 5, pm: 10, fo: 10 });
    if (has(leap, 'first_job')) add({ smm: 8, va: 10, pm: -5, fo: -10 });
    if (a.situation === 'break') add({ smm: 5, va: 12 });
    if (a.situation === 'student') add({ smm: 8, va: 8, pm: -5, fo: -10 });
    if (a.intl === 'yes_paid') add({ va: 5, pm: 5, fo: 5 });
    if (incomeGoal >= 1500) add({ pm: 5, fo: 8 });
    if (toolCats.has('ai')) add({ smm: 3, va: 3, pm: 3, fo: 3 });
    for (const k in s) { s[k] = Math.max(0, Math.min(100, Math.round(s[k]))); if (!TRACKS[k].available) s[k] = -1; }

    const ranked = Object.keys(s).sort((x, y) => s[y] - s[x]);
    const primary = ranked[0], secondary = ranked[1];
    const twoPaths = s[primary] - s[secondary] <= 8 && directionGap;
    const showSecondary = s[primary] - s[secondary] <= 12;

    /* readiness */
    const relevantTools = { smm: ['design', 'video', 'social', 'ads', 'seo', 'ai'], va: ['docs', 'pm', 'comms', 'automation', 'crm', 'support', 'finance', 'ai'], pm: ['pm', 'docs', 'data', 'comms', 'ai'], fo: ['docs', 'data', 'pm', 'crm', 'ai'] }[primary];
    const adjacent = { smm: 'social', va: 'ops', pm: 'pm', fo: 'biz' }[primary];
    const nTools = tools.filter(t => relevantTools.includes(CAT.tools[t])).length;
    let readiness = 0;
    if (exp >= 1) readiness += 2;
    readiness += nTools >= 3 ? 2 : nTools >= 1 ? 1 : 0;
    if (roleCats.has(adjacent)) readiness += 2;
    if (['yes_paid', 'via_indian'].includes(a.intl)) readiness += 1;
    if (['some_calls', 'offers'].includes(a.interviews)) readiness += 1;
    if (!blockers.includes('no_portfolio')) readiness += 1;
    if (blockers.includes('no_where')) readiness += 1; // knows role, tools and skills
    const stage = readiness <= 3 ? 'Explorer' : readiness <= 6 ? 'Builder' : 'Launcher';

    /* fit */
    let fit = 'ok';
    if (a.budget === '0' && a.hours === 'lt3') fit = 'low';
    if (exp >= 10 && has(leap, 'switch_role') && leap.length === 1 && !has(interest, 'pm')) fit = 'low';

    /* intent */
    let intent = 0;
    intent += { '0': 0, '200_300': 26, '300_400': 30, '400_500': 34, '500_600': 37, '600_700': 40 }[a.budget] ?? 0;
    intent += { lt3: 0, '3_6': 10, '6_10': 18, '10p': 20 }[a.hours] ?? 0;
    intent += ['unemployed', 'freelance_unstable', 'job_stuck'].includes(a.situation) ? 15 : ['break', 'student'].includes(a.situation) ? 10 : 5;
    if (['applied_no_calls', 'some_calls'].includes(a.interviews)) intent += 10;
    if (blockers.length >= 2) intent += 5;
    if (incomeGap >= 500) intent += 5;
    if (a.dream_text && a.dream_text.trim()) intent += 3;
    if (a.linkedin && a.linkedin.trim()) intent += 2;

    let tier;
    if (fit === 'low') tier = 'redirect';
    else if (intent >= 65 && a.budget && a.budget !== '0') tier = 'hot';
    else if (intent >= 40) tier = 'warm';
    else tier = 'nurture';

    const clarityCall = ['hot', 'warm'].includes(tier) && (directionGap || twoPaths);

    /* why line */
    const why = [];
    if (interest.includes(primary)) why.push('you said this role is already on your mind');
    if (primary === 'smm' && social) why.push('you already live in content tools');
    if (primary === 'va' && ops) why.push('you already run the ops other people avoid');
    if (primary === 'pm' && pmx) why.push('you already coordinate people and timelines');
    if (primary === 'fo' && fox) why.push('you have the years and the generalist range founders look for');
    if (has(leap, 'job_to_freelance', 'side_income') && ['smm', 'va'].includes(primary)) why.push('it fits a freelance-first leap');
    if (a.situation === 'break' && primary === 'va') why.push('it is the most break-friendly way back in');
    if (!why.length) why.push('it is the fastest realistic path from where you are to what you want');

    return { directionGap, trackScores: s, primary, secondary: showSecondary ? secondary : null, twoPaths, readiness, stage, fit, intent, tier, clarityCall, incomeGap, incomeNow, incomeGoal, exp, why: why.slice(0, 2).join(' and ') };
  }

  /* ---------------- Lead submit ---------------- */
  // Sends one row to the Google Sheet. kind = 'lead' (finished) or 'progress' (after each question).
  function send(kind, row) {
    if (!CONFIG.LEAD_ENDPOINT) return Promise.resolve({ ok: true, stored: 'local' });
    return fetch(CONFIG.LEAD_ENDPOINT, { method: 'POST', mode: 'no-cors', keepalive: true, headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify({ kind: kind, row: row }) })
      .then(function () { return { ok: true, stored: 'remote' }; })
      .catch(function (e) { return { ok: false, error: String(e) }; });
  }
  function submitLead(payload, row) {
    try { const arr = JSON.parse(localStorage.getItem('leepx_leads') || '[]'); arr.push(payload); localStorage.setItem('leepx_leads', JSON.stringify(arr)); } catch (e) {}
    return send('lead', row || payload);
  }

  global.LeepX = { CONFIG, CAT, QUESTIONS: Q, REFLECT, TRACKS, score, submitLead, send };
})(window);
