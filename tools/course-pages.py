#!/usr/bin/env python3
"""Generates the course pages (site/remote-launchpad.html, site/social-media-manager.html).

Edit the data below, then run:  python3 tools/course-pages.py
The pages share css/course.css and the main site's tokens (css/leepx.css).
Each section uses a different layout on purpose (timeline, dark steps, checklist panel,
tickets, carousel, chat thread, tiers) so the page reads as distinct blocks.
"""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / 'site'

def esc(t): return html.escape(t, quote=False)
def ic(name): return f'<i class="ic" data-ic="{name}"></i>'
def chips(items): return ''.join(f'<span class="chip">{ic(i)}{esc(t)}</span>' for i, t in items)
def ul(items, icon='check'): return '<ul>' + ''.join(f'<li>{ic(icon)}<span>{esc(x)}</span></li>' for x in items) + '</ul>'
def faq(items): return '<div class="faq">' + ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in items) + '</div>'

def steps(items):
    return '<div class="steps">' + ''.join(
        f'<div class="step reveal"><span class="num">{i+1:02d}</span><b>{esc(t)}</b><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(items)) + '</div>'

def ticks(items):
    return '<ul class="ticks">' + ''.join(f'<li>{ic("check")}<div><b>{esc(t)}</b>' + (f'<p>{esc(d)}</p>' if d else '') + '</div></li>' for t, d in items) + '</ul>'

def inc(items):
    return '<div class="inc reveal">' + ''.join(
        f'<div>{ic(i)}<div><b>{esc(t)}</b><small>{esc(d)}</small></div></div>' for i, t, d in items) + '</div>'

def rail(items):
    return '<ul class="ticks two reveal">' + ''.join(
        f'<li>{ic("check")}<div><b>{esc(t)}</b><p>{esc(d)}</p></div></li>' for i, t, d in items) + '</ul>'

def thread(items):
    return '<div class="thread">' + ''.join(
        f'<div class="qa reveal"><div class="ask">{esc(q)}</div><div class="ans"><small>Straight answer</small>{esc(a)}</div></div>' for q, a in items) + '</div>'

def quotes(items):
    cards = []
    for src, text, name, role, tag in items:
        ini = ''.join(w[0] for w in name.split()[:2]).upper()
        cards.append(f'<div class="q"><span class="src">{esc(src)}</span><q>{esc(text)}</q>'
                     + (f'<span class="tag">{esc(tag)}</span>' if tag else '')
                     + f'<div class="who"><span class="av">{ini}</span><div><b>{esc(name)}</b><small>{esc(role)}</small></div></div></div>')
    track = ''.join(cards)
    return f'<div class="carousel"><div class="car-track">{track}{track}</div></div>'

def timeline(groups, l1='Live with Shreya', l2='Recorded, at your pace'):
    out = ['<div class="weeks">']
    for g in groups:
        phase, items = g[0], g[1]
        note = g[2] if len(g) > 2 else ''
        if phase: out.append(f'<div class="phase">{esc(phase)}</div>')
        for row in items:
            n, title, live, lessons = row[:4]
            tags = row[4] if len(row) > 4 else None
            outcome = row[5] if len(row) > 5 else None
            label = row[6] if len(row) > 6 else l1
            tag_html = (f'<div class="tags">{"".join(f"<span>{esc(x)}</span>" for x in tags)}</div>') if tags else ''
            out_html = (f'<p class="out">{ic("target")}<span><b>Outcome</b> {esc(outcome)}</span></p>') if outcome else ''
            out.append(f'<div class="wk reveal"><span class="n">{esc(n)}</span><div><b>{esc(title)}</b>'
                       f'<div style="margin-top:10px"><div class="l live">{esc(label)}</div><p>{esc(live)}</p>{out_html}</div></div>'
                       f'<div><div class="l">{esc(l2)}</div><ul>{"".join(f"<li>{esc(x)}</li>" for x in lessons)}</ul>{tag_html}</div></div>')
        if note: out.append(f'<div class="cap reveal">{ic("trophy")}<span>{esc(note)}</span></div>')
    out.append('</div>')
    return ''.join(out)

LOGOS = {'chatgpt':'ChatGPT','claude':'Claude','sheets':'Google Sheets','jira':'Jira','confluence':'Confluence','zapier':'Zapier',
         'make':'Make','copilot':'Copilot','gemini':'Gemini','n8n':'n8n','notion':'Notion AI','power-automate':'Power Automate'}
def logo(key, label=None):
    return f'<span class="lg"><img src="assets/logos/{key}.svg" alt="" loading="lazy">{esc(label or LOGOS[key])}</span>'
def toolcards(rows):
    out = []
    for when, module, tools, task in rows:
        out.append(f'<div class="tcard reveal"><div class="tc-when"><span class="wkn">{esc(when)}</span><b>{esc(module)}</b></div>'
                   f'<div class="tc-logos">{"".join(logo(*t) if isinstance(t, tuple) else logo(t) for t in tools)}</div>'
                   f'<p>{esc(task)}</p></div>')
    return '<div class="tcards">' + ''.join(out) + '</div>'

def ticket(tag, title, worth, items):
    worth_html = (f'<span class="worth"><s>Worth {esc(worth)}</s><em>Included</em></span>' if worth
                  else '<span class="worth"><em>Included</em></span>')
    return (f'<div class="ticket reveal"><span class="tag">{esc(tag)}</span><h3>{esc(title)}</h3>'
            f'{worth_html}{ul(items)}</div>')

def buy(href, label, tier, cls='btn btn-primary'):
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener" data-buy="{tier}">{esc(label)}</a>'

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:image" content="https://theleepx.com/assets/hero-poster.jpg" />
<link rel="icon" href="favicon.ico" sizes="any" />
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png" />
<link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-192.png" />
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="css/leepx.css" />
<link rel="stylesheet" href="css/course.css" />
</head>
<body data-page="{slug}">
<header class="ctop">
  <div class="in">
    <a class="back" href="index.html#outcomes">{back_ic}<span>Back to all cohorts</span></a>
    <a class="logo" href="index.html" aria-label="LeepX home"><img src="assets/logo-primary.png" alt="LeepX" /></a>
    <a class="btn btn-primary btn-sm nav-enrol" href="{cta_href}"{cta_attrs}>{cta_short}</a>
  </div>
</header>

{body}

<section class="cfinal" id="enrol">
  <div class="blob"></div>
  <div class="wrap">
    <span class="eyebrow light">Enrolment open</span>
    <h2>{final_h}</h2>
    <p>{final_p}</p>
    <a class="btn btn-lime" href="{final_href}" {final_attrs}>{final_cta}</a>
  </div>
</section>

<div class="cfoot"><span>© 2026 LeepX · Job-ready, not job-guaranteed.</span><span><a href="index.html">Home</a><a href="assess.html">Free assessment</a><a href="terms.html">Terms</a><a href="privacy.html">Privacy</a></span></div>
<div class="mcta"><small>{mcta_small}</small><a class="btn btn-primary btn-sm" href="{cta_href}"{cta_attrs}>{cta_short}</a></div>

<script src="js/config.js"></script>
<script src="js/track.js"></script>
<script src="js/icons.js"></script>
<script src="js/fab.js"></script>
<script>
  document.querySelectorAll('[data-ic]').forEach(e=>{{ e.innerHTML=LX.icon(e.dataset.ic,20); }});
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce||!('IntersectionObserver' in window)) document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));
  else {{ const io=new IntersectionObserver(es=>es.forEach(e=>{{ if(!e.isIntersecting) return; e.target.classList.add('in'); io.unobserve(e.target); }}),{{threshold:.12}}); document.querySelectorAll('.reveal').forEach(e=>io.observe(e)); }}
  document.querySelectorAll('a[data-buy]').forEach(a=>a.addEventListener('click',()=>{{ window.lxTrack&&lxTrack('checkout_click',{{course:'{slug}',tier:a.dataset.buy}}); }}));
  window.lxTrack&&lxTrack('course_page_view',{{course:'{slug}'}});
  const bar=document.querySelector('.ctop'); const stick=()=>bar.classList.toggle('stuck',scrollY>12||!document.querySelector('.chero')); addEventListener('scroll',stick,{{passive:true}}); stick();
  document.addEventListener('click',e=>{{ const a=e.target.closest('a[href^="#"]'); if(!a) return; const t=document.querySelector(a.getAttribute('href')); if(!t) return; e.preventDefault(); const y=t.getBoundingClientRect().top+scrollY-76; const y0=scrollY; window.scrollTo({{top:y,behavior:reduce?'auto':'smooth'}}); setTimeout(()=>{{ if(Math.abs(scrollY-y0)<4&&Math.abs(y-y0)>4) window.scrollTo(0,y); }},450); history.replaceState(null,'',a.getAttribute('href')); }});
</script>
</body>
</html>
"""

BACK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>'
ASSESS = '<a href="assess.html" style="color:var(--purple);font-weight:700">Take the free 3-minute assessment</a>'

# ===================================================================== REMOTE LAUNCHPAD
LP_SEAT = 'https://academy.theleepx.com/web/checkout/6a9aa91e3e4aa855e2067682?purchaseNow=true'
LP_PLUS = 'https://academy.theleepx.com/web/checkout/6a9aa9fc5c8117f87d961146?purchaseNow=true'

launchpad_body = f"""
<section class="chero compact" id="top">
  <div class="wrap">
    <span class="eyebrow">The Remote Career Launchpad · 8 weeks</span>
    <h1>Get hired by companies that <span class="hl">pay in dollars.</span></h1>
    <p class="lead">Hybrid setup: self-paced lessons you watch whenever you like, live Q&amp;As with Shreya for accountability and progress tracking, and two live bonus sessions.</p>
    <div class="acts"><a class="btn btn-primary" href="#seats">Lock your seat →</a><a class="btn btn-ghost" href="#schedule">See the eight weeks</a></div>
  </div>
</section>

<section class="sec" id="schedule">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Your eight weeks</span><h2>What you learn, and what you ask about.</h2><p>Modules drop weekly. Every Sunday Q&amp;A is recorded too, so a missed Sunday is never a missed week.</p></div>
    {timeline([('', [
      ('WEEK 1','Career Clarity','Your strategy doc and where to start',['Profile Personalisation','Profile Asset Mapping','Niche Discovery','Strategy Doc Walkthrough']),
      ('WEEK 2','Remote Skills & Setup','Stack, workspace, payments and invoicing',['Async Work Skills','Global Communication','Payments & Invoicing','Leo 101']),
      ('WEEK 3','Projects & Case Studies','Portfolio, projects and the self internship',['The Self Internship','Portfolio Building','The Global CV']),
      ('WEEK 4','Applications & Outreach','LinkedIn, messages and what to actually say',['LinkedIn Optimisation','Outreach Messages']),
      ('WEEK 5','Momentum Check','What is landing and what to change',['Outreach Strategy','Finding Remote Jobs']),
      ('WEEK 6','Interview Prep','Answers, assignments and negotiation',['Interview Answers','Assignments & Trials','Salary Negotiation']),
      ('WEEK 7','Live Applications','Where to apply and how to follow up',['The Follow Up Formula']),
      ('WEEK 8','Graduation','Your certificate and what comes after your first role',['After Your First Role'])])])}
  </div>
</section>

<section class="sec dark" id="how">
  <div class="wrap">
    <div class="head"><span class="eyebrow light">How the Launchpad works</span><h2>Eight weeks. Two things happen every week.</h2><p>Nothing here needs you free at a fixed hour to learn. You only need one Sunday a week to get unstuck.</p></div>
    {steps([
      ('Learn: 4+ hrs of recorded content','Released weekly. Watch at 6 AM or 11 PM, rewatch as often as you need. Nothing to attend, nothing to miss, no falling behind because of a meeting that ran late.'),
      ('Ask: 8 Sunday live Q&As','Every Sunday for eight weeks, live with Shreya. Bring your profile, your outreach messages, your blockers. Ask anything about that week’s material and leave with an answer.'),
      ('Plus: 2 live bonus sessions','A fireside with a US hiring manager who hires from India, and a live session with Shreya on starting freelancing and side hustles alongside your job.')])}
    <p class="note">The teaching is on your schedule. The answers are live. That is the whole design.</p>
  </div>
</section>

<section class="sec" id="outcome">
  <div class="wrap split">
    <div class="head"><span class="eyebrow">By the end of week eight</span><h2>You do not leave with notes. Here is what you walk out with.</h2><p>Three assets built and reviewed during the cohort, and five things you carry with you long after week eight.</p></div>
    <div>
      <div class="assets">
        <div class="card reveal"><span class="eyebrow num-tag">Asset 01</span><h3>The Global CV</h3><p>Written for one role, not for everyone, with impact lines a recruiter can scan in six seconds.</p></div>
        <div class="card reveal"><span class="eyebrow num-tag">Asset 02</span><h3>A LinkedIn that gets found</h3><p>Rewritten so the right recruiter searching the right words actually lands on you.</p></div>
        <div class="card reveal"><span class="eyebrow num-tag">Asset 03</span><h3>Outreach that gets replies</h3><p>Built from the templates inside. You write your own version in week four and get it reviewed.</p></div>
      </div>
      {ticks([
        ('A portfolio with real project samples','Two or three pieces built during the self internship, reviewed before they go anywhere near an application.'),
        ('Tool fluency for global remote work','Async communication, documentation, project tools, AI in your workflow, invoicing and payments.'),
        ('Confidence walking into interviews','Your answers, your assignment approach and your negotiation position worked out in advance.'),
        ('Clarity on demand, and on your packaging','Which roles are actually being hired for, in which geographies, and how to package your experience for one of them.'),
        ('Your LeepX graduation certificate','Plus a long term career plan you keep using after your first global role.')])}
    </div>
  </div>
</section>

<section class="sec lilac" id="inside">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">What your seat includes</span><h2>Everything inside the Launchpad.</h2></div>
    {inc([
      ('book-open','4+ hrs of recorded content','Released weekly, from your CV all the way to interviews'),
      ('calendar','8 Sunday live Q&As','Every Sunday for eight weeks, live with Shreya'),
      ('wrench','The Resource Hub','Templates, prompts and swipe files, yours to keep forever'),
      ('mic','Interview Prep Track','Answers, assignments and salary negotiation, module by module'),
      ('notebook','Assignment Training','How to win the take home rounds instead of dreading them'),
      ('briefcase','Ready to Market Portfolio','Built hands on across the eight weeks, with review'),
      ('pen-line','Your Strategy Doc','A guided one page plan, questions answered on Sunday 1'),
      ('bot','Full access to Leo','Your AI career agent, for all eight weeks'),
      ('user','Community Access','Your cohort plus alumni who refer opportunities forward'),
      ('zap','24 hr Q&A','Every question answered within a day, all eight weeks'),
      ('map-pin','Opportunity Board','Curated global openings, posted weekly'),
      ('graduation-cap','LeepX Graduation','Certificate plus a long term career plan you keep using')])}
    <p class="note center">Plus an optional mini cohort on LinkedIn, Medium, Substack and newsletters, for the ones who want inbound.</p>
  </div>
</section>

<section class="sec warm" id="bonus">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">On top of the eight weeks</span><h2>Two live sessions you cannot buy anywhere else.</h2><p>₹21,000 of live sessions, included in your seat.</p></div>
    <div class="tickets">
      {ticket('Bonus 1','Fireside chat with a US hiring manager','₹9,000',['What US recruiters screen for in the first 30 seconds','Contractor versus employee: how US companies actually hire from India','Live Q&A, ask them anything, unfiltered'])}
      {ticket('Bonus 2','Freelancing and side hustles, live with Shreya','₹12,000',['Landing your first three international clients','Pricing in USD without underselling yourself','Turning one off gigs into monthly retainers'])}
    </div>
  </div>
</section>

<section class="sec" id="hub">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Yours to keep, forever</span><h2>The Resource Hub.</h2><p>You keep every one of these after the cohort ends, and they keep working long after week eight.</p></div>
    {rail([
    ('mail-check','20+ outreach messages','And follow ups. The ones that actually get replies.'),
    ('pen-line','10+ CV templates','By geography and profile type'),
    ('sparkles','200+ prompts','For the entire LeepX workflow'),
    ('notebook','20+ cover letters that work','Their problem, your proof'),
    ('briefcase','10+ portfolio templates','Real ones, ready to copy and use'),
    ('brain','100+ interview questions','Behavioural and case study, with practice'),
    ('book-open','Medium and Substack guide','Step by step, so global opportunities come to you')])}
  </div>
</section>

<section class="sec soft" id="fit">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Read this before you buy</span><h2>This is built for one kind of person. See if it is you.</h2></div>
    <div class="fornot">
      <div class="fn yes reveal"><h3>{ic('check')} This is for you if</h3>{ul([
        'You are already working, or job hunting, and the applications are going nowhere',
        'You want to work with companies outside India and get paid accordingly',
        'You are willing to put in a few focused hours a week for eight weeks',
        'You are switching careers, or coming back after a break, and need a route that is written down',
        'You would rather build one strong profile than send a hundred weak applications'])}</div>
      <div class="fn no reveal"><h3>{ic('circle-off')} This is not for you if</h3>{ul([
        'You want a guaranteed job handed to you at the end of eight weeks',
        'You are looking for quick money without building any proof of work',
        'You already work confidently with global companies and have a full pipeline',
        'You will not open the modules or turn up on a single Sunday'],'circle-off')}</div>
    </div>
  </div>
</section>

<section class="sec" id="honest">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">The honest bit</span><h2>What is actually stopping you.</h2><p>Every one of these has come up in a cohort before. Here is the straight answer.</p></div>
    {thread([
      ('I do not have a tech background.','Neither did Shreya. Global remote work is not a tech-only market. Operations, marketing, design, content, support, project management and admin roles are all hired remotely from India. What matters is proof, not pedigree.'),
      ('I have no time, I already have a job.','That is precisely why there are no live classes. Everything is recorded and released weekly. The only fixed commitment is one Sunday Q&A a week, and even that is recorded if you cannot make it.'),
      ('I have applied to hundreds of jobs already.','Volume without positioning is the problem, not the solution. Weeks 1 to 3 exist to fix what you are sending before week 4 asks you to send anything at all.'),
      ('I do not have anything to put in a portfolio.','Week 3 is the self internship. You build two or three real samples during the cohort, reviewed before they go anywhere near an application. Nobody starts with a portfolio, they leave with one.')])}
  </div>
</section>

<section class="sec soft" id="pricing">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Which seat is yours?</span><h2>Two seats. Three questions to pick the right one.</h2><p>Launchpad and Launchpad Plus are the same eight weeks. The only difference: Plus adds a 1:1 call with Shreya before you start, to lock the role or client you are going after. Answer these three honestly to know whether you need that call.</p></div>
    <div class="qs">
      <div class="card reveal"><span class="num">1</span><div><p>Can you name the exact role, or the exact kind of client, you are going after, in one sentence?</p><span class="yn">Yes or no?</span></div></div>
      <div class="card reveal"><span class="num">2</span><div><p>Are your CV and LinkedIn already written for that one role, not for everyone?</p><span class="yn">Yes or no?</span></div></div>
      <div class="card reveal"><span class="num">3</span><div><p>Have you sent applications or outreach for it in the last 30 days?</p><span class="yn">Yes or no?</span></div></div>
    </div>
    <div class="verdict">
      <div class="card pick reveal"><b>Yes to all three</b><h3>Take the Launchpad</h3><p>You already know your direction. You need the system, not the diagnosis.</p><a href="#seats">See the seat ↓</a></div>
      <div class="card pick hot reveal"><b>Even one no</b><h3>Take Launchpad Plus</h3><p>Most people land here. The 1:1 with Shreya fixes your direction before week one, so you do not spend eight weeks pointing at the wrong role.</p><a href="#seats">See the seat ↓</a></div>
    </div>
    <p class="note">A no is not a failure, it is the actual starting line. Not sure of your answers? {ASSESS}.</p>

    <div class="head" style="margin-top:72px"><span class="eyebrow">The two seats</span><h2>Pick the seat that matches your answers.</h2><p>Bought piece by piece, everything inside comes to ₹98,000. You are not buying it piece by piece.</p></div>
    <div class="tiers" id="seats">
      <div class="tier reveal">
        <h3>Launchpad</h3><p class="for">For you if you already know the role or client you are going after.</p>
        {ul(['4+ hrs of recorded content, released weekly','8 Sunday live Q&As with Shreya','2 live bonus sessions','Resource Hub, Leo and the Opportunity Board','Community, 24 hr Q&A and certificate'])}
        <div class="price"><s>₹98,000</s><b>₹37,000 <small>+ GST</small></b></div>
        {buy(LP_SEAT,'Lock my seat →','launchpad')}
      </div>
      <div class="tier hot reveal">
        <span class="pop">Most people start here</span>
        <h3>Launchpad Plus</h3><p class="for">For you if any answer to those three questions was a no.</p>
        {ul(['Everything in Launchpad, plus:','A 1:1 clarity call with Shreya to lock your niche and positioning','Your roadmap built with you in that call, not from a template','Your profile reviewed against that roadmap','Community, 24 hr Q&A and certificate'])}
        <div class="price"><s>₹1,13,000</s><b>₹42,000 <small>+ GST</small></b></div>
        {buy(LP_PLUS,'Lock my seat →','launchpad_plus')}
      </div>
    </div>
  </div>
</section>

<section class="sec" id="voices">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">What our learners say</span><h2>Real people. Real turning points.</h2></div>
  </div>
  {quotes([
    ('LinkedIn post','At some point Shreya put up a table. Roles in demand, mapped to geographies. And somehow it did something that a lot of searching on your own can’t, it cut through the noise.','Shinjini Shah','Integrated Marketing Manager, B2B SaaS & AI',''),
    ('LinkedIn post','Went in thinking it would be interesting. Did not expect to walk out actually believing I could work from whichever country I want. She did not speak in theory.','Palak Seth','Equity Research & Investment Banking',''),
    ('Message','I just signed my first client. Some time ago I was 8+ years deep into a career in HR Compensation. Today I am building personal brands for people who want to show up authentically.','Smitha Dhanya','Personal Branding & Social Media Manager','First client'),
    ('LinkedIn post','I focused so much on what skills I have that I forgot the value I create from them. It has changed my perspective on positioning myself in the global market.','Nikita Chandola','Content Writer & Strategist, SaaS',''),
    ('LinkedIn post','Today’s opportunities aren’t limited by where you live, they’re defined by the value you create, the skills you build and the consistency you show.','Poonam Koul','Marketing Head, Brand Strategy',''),
    ('LinkedIn post','I have been working remotely for 5+ years myself, but learning never really stops. AI can do a lot of things, but it cannot replace real experiences and personal stories.','Gargi Dey','Digital Marketer',''),
  ])}
  <div class="wrap"><p class="swipe center">Straight from LinkedIn and the DMs · swipe →</p></div>
  <div class="shots">{''.join(f'<img src="assets/course/launchpad-shot-{i}.jpg" alt="LinkedIn post or message about the session" loading="lazy" />' for i in range(1,10))}</div>
  <div class="wrap"><p class="note center">Unedited screenshots. Public posts and messages, shared with permission. Personal details hidden. Individual results depend on individual effort. This programme does not guarantee a job.</p></div>
</section>

<section class="sec soft" id="faq">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Before you ask</span><h2>Questions about the Launchpad.</h2><p>General questions about LeepX, refunds and payments are answered on the <a href="index.html#faq" style="color:var(--purple);font-weight:700">main FAQ</a>.</p></div>
    {faq([
      ('Are there live classes I have to attend?','No. All the teaching is recorded and released weekly, so you learn whenever it suits you. The only live commitments are the eight Sunday Q&As and the two bonus sessions, and every one of those is recorded as well.'),
      ('What actually happens in a Sunday Q&A?','You bring questions from that week’s lessons and from your own work in progress: your CV, your LinkedIn, an outreach message that got no reply, a role you are unsure about. Shreya answers them live. It is a working session, not a lecture.'),
      ('What if I miss a Sunday?','The recording goes up the same day, and you can drop your question into the 24 hour Q&A channel instead. You will not be behind.'),
      ('Launchpad or Launchpad Plus: which one should I choose?','Both are the same eight weeks. Plus adds a 1:1 call with Shreya before you start. If you can already name your target role, your CV and LinkedIn are written for it, and you have been applying for it, Launchpad is enough. If any of those is a no, take Plus: the call fixes your direction before you spend eight weeks in the wrong one.'),
      ('Do I keep access after eight weeks?','Yes. The Resource Hub, the templates and the recordings stay with you, and you stay in the alumni community where opportunities get referred forward.')])}
  </div>
</section>
"""

# ===================================================================== SOCIAL MEDIA MANAGER
SMM_BUY = 'https://academy.theleepx.com/web/checkout/6a7739472e3b4113124f0600?purchaseNow=true'

smm_body = f"""
<section class="chero compact" id="top">
  <div class="wrap">
    <span class="eyebrow">The SMM Cohort · 10 weeks · limited seats</span>
    <h1>Become a Remote <span class="hl">Social Media</span> Manager.</h1>
    <p class="lead">Seven live sessions with Shreya, 40+ recorded lessons and 10+ real projects. You leave with a portfolio, case studies and an AI workflow you have already used.</p>
    <div class="acts"><a class="btn btn-primary" href="#pricing">Join the cohort →</a><a class="btn btn-ghost" href="#schedule">See the 10 modules</a></div>
  </div>
</section>

<section class="sec" id="schedule">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Your 10-week schedule</span><h2>Ten modules. Five to build, five to launch.</h2><p>One live session a week with Shreya, recorded the same day, plus lessons you take at your own pace.</p></div>
    {timeline([
      ('Modules 1 to 5 · the build phase', [
        ('MODULE 1','Kickoff: Welcome to Social Media Management','Meet the cohort, map your starting point, and install the SMM mindset: five jobs, one career',['What an SMM actually does','The 5 pillars of the job','Your 10-week roadmap','Goal setting + niche shortlist']),
        ('MODULE 2','Operations: Tools, Planning & Scheduling','Set up your working system hands-on: boards, calendars, schedulers and the content dashboard',['The SMM tool stack','Content calendars that stick','Batching + scheduling workflows','Your content dashboard setup']),
        ('MODULE 3','Content Creation: Planning & Production','Plan, script, shoot and edit a real batch of content in one week, the professional way',['Scripts, hooks + retention','Editing: bare minimum to advanced','Captions + design systems','Batch day, done right']),
        ('MODULE 4','Understanding Content Strategy','The full strategy framework installed on real brands: goal, audience, voice, format, rhythm',['The Content OS in depth','Format-to-job mapping','Platform currencies + algorithms','Strategy docs clients sign off']),
        ('MODULE 5','Research, Discovery, Social Listening & Analytics','Audit real brands and their competitors, then read the analytics and decide what you would change',['Brand + competitor analysis','Content research + swipe files','Social listening + trends','The 5 KPIs and the one-page report'])]),
      ('Modules 6 to 10 · the launch phase', [
        ('MODULE 6','How to Work with Clients','Onboarding, expectations, approvals, feedback and the conversations nobody prepares you for',['Client onboarding kit','Revenue language + reporting','Scope, pricing + boundaries','Handling feedback + escalations']),
        ('MODULE 7','AI for Social Media Management','Build your AI-powered production line: one person shipping the volume of three',['The AI stack for SMMs','Prompt systems for content','AI dashboards + automations','Where AI stops and you begin']),
        ('MODULE 8','Package Your SMM Profile','Define your role, your niche and your one-sentence pitch, then package it everywhere',['Positioning + niche lock','Your SMM CV + LinkedIn','The 4-line pitch, personalised','Rate cards + packages']),
        ('MODULE 9','SMM Portfolio','Assemble your one-link portfolio from nine weeks of real work, then get it reviewed',['Case studies that convert','The one-link portfolio','Before/after proof packaging','Portfolio teardowns']),
        ('MODULE 10','Finding Clients, Jobs & Launch Week','Application, pitching and outreach strategies shared with the whole cohort, plus graduation and your 90-day plan',['The three client doors','Outreach strategies + scripts','Job boards + platforms','Graduation + what’s next'])])])}
    <p class="note">10 modules · 40+ lessons · 10+ real projects · hands-on practice every week, with feedback on your actual work.</p>
  </div>
</section>

<section class="sec dark" id="build">
  <div class="wrap">
    <div class="head"><span class="eyebrow light">Practice, not theory</span><h2>You will not just watch. You will build.</h2><p>Every module ends with work you actually do, on real brands, reviewed by us. By Week 10 the proof is yours, not a certificate saying you attended.</p></div>
    {steps([
      ('Practise every single week','Hands-on assignments from Module 1: calendars, hooks, scripts, batches and reports. Not quizzes.'),
      ('Analyse real brands','Audit live accounts and competitors: what they post, what is working, what you would change, and why.'),
      ('10+ real projects','Strategy docs, content batches, dashboards and monthly reports, all produced by your own hands.'),
      ('Case studies clients read','Every project written up properly: the brief, what you did, and the numbers that moved.'),
      ('A one-link portfolio','Assembled in Module 9 from ten weeks of real work, and torn down live so it is client-ready.'),
      ('Social media with AI','Build an AI production line for research, scripting, repurposing and reporting, and know where AI stops.')])}
    <p class="note">You leave with a portfolio, case studies and an AI workflow you have already used. That is what gets you hired.</p>
  </div>
</section>

<section class="sec lilac" id="inside">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">What your seat includes</span><h2>Everything inside the cohort.</h2></div>
    {inc([
      ('map-pin','Live cohort kickoff call','One live kickoff call to map your starting point and the 10 weeks ahead'),
      ('video','7 live sessions','Weekly live coaching with Shreya, recorded if you miss one'),
      ('book-open','40+ recorded lessons','Watch at your pace, structured module by module'),
      ('pen-line','Feedback on real work','Your calendars, content, brand audits and reports reviewed, not just graded'),
      ('folder','10+ projects, not notes','You graduate with 10+ real projects, case studies, a dashboard and a one-link portfolio'),
      ('bot','AI workflows','The complete AI production line for one-person volume'),
      ('message-circle','Private community','Cohort-mates, accountability and 24-hr Q&A'),
      ('rocket','Launch Week','Application, pitch and outreach strategies, shared live in Week 10'),
      ('award','Certificate + lifetime access','Completion certificate, plus every module, template and recording kept for life'),
      ('calendar','Built around real life','Every session recorded the same day, structured weekly modules, 4 to 6 hours a week')])}
  </div>
</section>

<section class="sec" id="vault">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Yours to keep, forever</span><h2>The SMM Resource Vault.</h2><p>Every template we use with real clients, handed over and yours for life.</p></div>
    {rail([
    ('mail-check','Outreach message pack','Warm, cold and follow-up scripts that get replies'),
    ('folder','Portfolio templates','Case-study and one-link portfolio formats, plug and fill'),
    ('pen-line','SMM CV templates','Positioning-first CVs for in-house and agency roles'),
    ('sparkles','The 1000-Hooks swipe file','Researched hooks for IG, Shorts, titles and thumbnails'),
    ('pen-tool','Caption guide','Caption structures, CTAs and keyword-DM setups'),
    ('wrench','Tools guidance','The bare-minimum vs advanced stack, per platform'),
    ('chart-bar','Content dashboard template','The Notion dashboard clients love, ready to duplicate'),
    ('notebook','One-page report template','The monthly report that renews retainers'),
    ('calendar','Content calendar template','The 80/20 week, pre-built for any brand'),
    ('book-open','The Content OS one-pager','Install the full strategy system on any brand, tonight')])}
  </div>
</section>

<section class="sec dark" id="system">
  <div class="wrap">
    <div class="head"><span class="eyebrow light">The system</span><h2>The LEEPX framework, built for SMM.</h2><p>Four moves that build a paid social media manager, and an X that accelerates all of them.</p></div>
    <div class="letters">
      <div class="letter reveal"><span class="big">L</span><b>Learn</b><p>Social + Media + Management: platforms, engagement, the 5 KPIs and content strategy.</p></div>
      <div class="letter reveal"><span class="big">E</span><b>Equip</b><p>The tool stacks, the 80/20 calendar, dashboards and AI workflows, set up hands-on.</p></div>
      <div class="letter reveal"><span class="big">E</span><b>Evidence</b><p>10+ real projects, case studies and a one-link portfolio built during the cohort.</p></div>
      <div class="letter reveal"><span class="big">P</span><b>Promote</b><p>Positioning, packages, pitching and outreach: turning your proof into paying clients.</p></div>
      <div class="letter reveal"><span class="big">X</span><b>Accelerate</b><p>Live feedback, mentors and community multiplying all four, every week.</p></div>
    </div>
  </div>
</section>

<section class="sec" id="honest">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Objections, handled</span><h2>Every fear you have? We handle it, module by module.</h2></div>
    {thread([
      ('I’m a complete fresher.','Perfect. From Module 3 you’re producing real work, and by Module 9 you hold a portfolio of 10+ projects. You enter through proof, not years of experience.'),
      ('I have a full-time job. No time.','7 live sessions, all recorded the same day, lessons at your own pace, and a clear plan for every week. Built to fit around your 9-to-5 in 4 to 6 hours a week.'),
      ('I’m not good at design or video.','You don’t have to be. Templates and the bare-minimum stack cover 90% of client work. Clients hire you for the system, not for being a designer.'),
      ('I’ve been posting. Nothing happens.','Posting without a system is just noise. By Week 4 you’ll know what to post, when, why, and how to report what it earned, the part that gets you paid.')])}
  </div>
</section>

<section class="sec soft" id="pricing">
  <div class="wrap">
    <div class="head"><span class="eyebrow">The investment</span><h2>Piece it together yourself, and here’s your receipt.</h2><p>Every part of the cohort, priced on its own on the left. One seat with all of it on the right.</p></div>
    <div class="price2">
    <div class="receipt reveal">
      <div><span>Live kickoff call + roadmap</span><b>₹6,000</b></div>
      <div><span>7 live sessions with Shreya</span><b>₹25,000</b></div>
      <div><span>40+ recorded lessons, all 10 modules</span><b>₹20,000</b></div>
      <div><span>Portfolio, CV & outreach template vault</span><b>₹10,000</b></div>
      <div><span>1000-Hooks file + caption guide</span><b>₹5,000</b></div>
      <div><span>AI workflows + tools guidance</span><b>₹8,000</b></div>
      <div><span>Community, feedback & launch week</span><b>₹10,000</b></div>
      <div class="tot"><span>Total, done alone</span><b>₹84,000</b></div>
    </div>
    <div class="tiers single">
      <div class="tier hot reveal">
        <span class="pop">Seats are capped</span>
        <h3>The SMM Cohort, complete</h3><p class="for">Everything above, in one seat, with Shreya and the cohort around you.</p>
        {ul(['Kickoff call, 7 live sessions and 40+ recorded lessons','10+ real projects with feedback, case studies and a one-link portfolio','AI workflows, the Resource Vault and lifetime access','Private community, 24-hr Q&A and Launch Week'])}
        <div class="price"><s>₹84,000</s><b>₹25,000 <small>+ GST</small></b></div>
        {buy(SMM_BUY,'Lock your seat →','smm')}
      </div>
    </div>
    </div>
    <p class="note"><b style="color:var(--ink)">One retainer client covers this in your first month or two.</b> Not sure this is your role? {ASSESS}.</p>
  </div>
</section>

<section class="sec warm" id="bonus">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Enrol and unlock</span><h2>₹10,000 in free bonuses.</h2><p>Stacked on top of your seat.</p></div>
    <div class="tickets">
      {ticket('Bonus 1','Live portfolio and pitch teardowns','₹6,000',['Real cohort portfolios reviewed on screen','Your 4-line pitch, rewritten live','What makes a client actually reply'])}
      {ticket('Bonus 2','The Opportunity Board','₹4,000',['SMM openings and client leads shared weekly','First access for cohort members','Alumni referrals as the community grows'])}
    </div>
  </div>
</section>

<section class="sec" id="voices">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Straight from our cohort</span><h2>What our previous cohort members have to say.</h2></div>
  </div>
  {quotes([
    ('Instagram DM','Well I learned all the tools that you talked about and what was needed for that role. That helped me grab 22 LPA in my own company from 8 LPA and couldn’t thank you more for it. Being 23 and getting this good really is a big thing for me.','A.','Community member, 23','8 LPA → 22 LPA'),
    ('WhatsApp · community group','Thanks a lot Shreya! If it weren’t for you, I probably wouldn’t have this right now! Really appreciate you making this community and sharing great resources! Really excited to get started with this new role!','F.','Community member','Cracked a new role'),
    ('Instagram DM','You are the best creator over internet. I have cracked my first international client because of you, so keep going. The first and IG best mentors I have.','R.','Follower turned freelancer','First international client'),
    ('WhatsApp','I just heard back from them! I got the job! Thanks again for everything! Sharing that opportunity, conducting the crash course!','S.','Learner','Placed via a shared opportunity'),
    ('WhatsApp','Hi Shreya, your course session was really very insightful and valuable, am glad that I joined and enrolled in. Appreciate how you put this much of efforts to help others gain clarity and direction through your rich experiences in this domain.','P.','Enrolled learner','On the course sessions'),
  ])}
  <div class="wrap"><p class="note center">Messages shared with permission. Names hidden for privacy. Individual results depend on individual effort.</p></div>
</section>

<section class="sec soft" id="faq">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Questions, answered</span><h2>Questions about the SMM cohort.</h2><p>General questions about LeepX, refunds and payments are answered on the <a href="index.html#faq" style="color:var(--purple);font-weight:700">main FAQ</a>.</p></div>
    {faq([
      ('I’m a fresher with no experience. Can I join?','Yes. The cohort is built around manufacturing proof: from Module 3 you’re producing real content, and by Module 9 you have a portfolio made from your own work. Freshers enter through proof, not years of experience.'),
      ('Will I actually get to practise, or is it just lessons?','You practise every week. Every module ends with hands-on work on real brands: content calendars, hooks and scripts, a full content batch, a strategy doc, a brand audit and a monthly report. You submit it, we give feedback on it. Nothing here is a quiz.'),
      ('Will I have a portfolio and case studies by the end?','Yes, and that is the point of the ten weeks. You produce 10+ real projects during the cohort, write each one up as a case study, and assemble them into a one-link portfolio in Module 9, which gets reviewed live before you send it anywhere.'),
      ('Will I learn to use AI for social media?','Yes. Module 7 is a full AI module: the tool stack, prompt systems for research, scripting and repurposing, AI-assisted dashboards and automations, and a clear line on where AI stops and your judgement starts.'),
      ('Do I need to be good at design or video editing?','No. Modules 2 and 3 teach the bare-minimum stack (Canva templates, CapCut, native editors) that covers 90% of client work. You’re hired for the system, not for being a designer.'),
      ('Will you help me find clients or a job?','We do not commit a job. What we commit to: by Module 10 you are job-ready, with a portfolio, a positioned CV and a practised pitch. Launch Week is where we share the strategies for applying, pitching and outreach, live, and you keep the outreach pack, the Opportunity Board and feedback on every application asset you build.')])}
  </div>
</section>
"""


# ===================================================================== VIRTUAL ASSISTANT
VA_BUY = 'https://academy.theleepx.com/web/checkout/6a1b333e808d71fed1f65298?purchaseNow=true'

va_body = f"""
<section class="chero compact" id="top">
  <div class="wrap">
    <span class="eyebrow">The VA Program · ongoing cohort · join any day</span>
    <h1>Become a <span class="hl">Global Virtual Assistant.</span></h1>
    <p class="lead">Learn the systems, tools and AI workflows that founders, creators and agencies around the world pay for. Build a portfolio that proves it. Pitch your first international client.</p>
    <div class="acts"><a class="btn btn-primary" href="#pricing">Join the cohort →</a><a class="btn btn-ghost" href="#schedule">See the 13 modules</a></div>
  </div>
</section>

<section class="sec" id="schedule">
  <div class="wrap">
    <div class="head"><span class="eyebrow">The full curriculum</span><h2>Thirteen modules. Seven to build, six to launch.</h2><p>Recorded lessons at your own pace, about 5 to 7 hours a week. One module a week finishes in about 12 weeks. Seven live sessions with Shreya along the way, all recorded.</p></div>
    {timeline([
      ('Modules 1 to 7 · the build phase', [
        ('MODULE 1','VA as an Industry & Career','Understand what a VA actually does, how the career ladder works, and where you fit',['What modern VA work looks like','Admin, specialist and operations VAs','The ladder from VA to Chief of Staff','What global clients actually hire for']),
        ('MODULE 2','Niche Discovery & Role Clarity','Pick the niche you will pitch and build your first service menu',['Choosing a niche from your background','Client types: founders, creators, agencies','Your starting services','Niche worksheet + service menu']),
        ('MODULE 3','Setting Intentions & Systems','Enter your manager’s world and build the systems that make you indispensable',['Reading a manager’s priorities','Four prioritisation frameworks','Writing your first SOP','Cadence: check-ins and updates']),
        ('MODULE 4','Workspace Setup','Build the digital workspace of a professional VA',['A lean three to five tool stack','Project tracking system','File hygiene and folder structure','Status updates, traffic-light style']),
        ('MODULE 5','Your First VA Tech Stack, with AI','Master the tools, then multiply your speed with AI',['Advanced Google Workspace','Trello, Notion and Loom','ChatGPT for everyday VA tasks','Finding AI tools for your manager']),
        ('MODULE 6','Client Communication & Boundaries','The soft skills that separate junior VAs from senior ones',['Boundaries without losing the client','Understanding your client deeply','Document harbouring','SLAs and conflict management']),
        ('MODULE 7','SOPs & Documentation','Turn how you work into a repeatable system clients can rely on',['Planning documentation','Structuring a multi-stage SOP','Checklists, screenshots and Loom','The full professional SOP Pack'])]),
      ('Modules 8 to 13 · the launch phase', [
        ('MODULE 8','Coordination & Scheduling','Project management fundamentals for handling multiple clients',['Project management basics','Overlapping timelines and task juggling','Multi-client scheduling','Clean cross-team handoffs']),
        ('MODULE 9','Portfolio Building & Work Samples','Turn everything you have built into proof',['What a strong portfolio contains','Work samples from mock projects','Portfolio templates, Notion and Canva','Ship your first work sample']),
        ('MODULE 10','Personal Branding & Packaging','Show up online like a senior operator',['How to present yourself as a VA','Copy for every application document','Building your portfolio page','Your finished VA portfolio']),
        ('MODULE 11','The CV','A CV that reads in under 90 seconds',['The six sections of a VA CV','An outcome-led profile summary','Grouping skills and tools','Presenting mock projects honestly']),
        ('MODULE 12','Client Outreach','Apply the right way and pitch with proof',['Finding and researching clients','The personalised cover pitch','Vetting clients with the BJ Check','Attaching tangible value']),
        ('MODULE 13','Finding Jobs on Freelance Platforms','Where international remote roles actually live',['Upwork, Contra, Pearl Talent, Wishup, Toptal','Reading a client scorecard','The rate ladder across platforms','Optimising your profile + graduation'])])])}
    <p class="note">13 modules · 65+ lessons · 14 portfolio-grade assignments · every one submitted and reviewed, not graded.</p>
  </div>
</section>

<section class="sec dark" id="build">
  <div class="wrap">
    <div class="head"><span class="eyebrow light">Practice, not theory</span><h2>You will not just watch. You will build.</h2><p>Every module ends with an assignment you actually submit, and every one doubles as a portfolio piece. You finish with proof, not a certificate saying you attended.</p></div>
    {steps([
      ('A clear niche and service menu','The niche you will pitch and the services you sell, packaged so you can say it in one sentence.'),
      ('A client-ready portfolio','Built from real-shaped assignments: SOPs, trackers, dashboards and AI tool briefs.'),
      ('A VA CV that reads in 90 seconds','Outcome-led, grouped by skill and tool, formatted the way global clients expect.'),
      ('A professional SOP Pack','An eight-component pack for an agency campaign launch, your portfolio centrepiece.'),
      ('An AI-first workflow','A prompt library and tool stack that makes you three to five times faster on client work.'),
      ('An outreach kit that works','Cover pitch, the BJ Check for vetting clients, SLA templates and pricing logic for your first retainer.')])}
    <p class="note">You leave with a niche, a portfolio, a CV and an outreach system you have already used. That is what gets you hired.</p>
  </div>
</section>

<section class="sec" id="ai">
  <div class="wrap">
    <div class="head"><span class="eyebrow">The real differentiator</span><h2>Learn to work like an AI-first VA.</h2><p>Clients do not want someone who types fast. They want someone who gets the outcome faster and smarter. A VA who uses AI well delivers more in fewer hours, which is how you charge for outcomes instead of time. AI runs through this whole program, not one bonus lesson at the end.</p></div>
    {inc([
      ('pen-line','Prompting like a professional','A structured brief format covering role, audience, goal, tone, must include, length and what to avoid, so the first output is already client-ready'),
      ('message-circle','ChatGPT and Claude, daily','Drafting client emails, summarising meeting notes, brainstorming outreach variations and writing SOPs in minutes instead of hours'),
      ('chart-bar','AI inside Docs and Sheets','Faster reports, cleaner data and smarter templates, applied to the client work you are actually paid for'),
      ('wrench','AI tools for your manager','How to pick, pitch and implement Motion, Fathom, Reclaim and Notion AI, with a full implementation plan your client can sign off'),
      ('search','Editing AI output','Spotting robotic phrasing, fixing tone, and making sure nothing reaches a client sounding machine-written'),
      ('book-open','Your reusable prompt library','The prompts you save once and run on every client after that, yours to keep for life')])}
    <p class="note"><b style="color:var(--ink)">Two AI assignments, both portfolio pieces.</b> Finding AI tools for your manager: two tool briefs with implementation plans. Using ChatGPT to write, summarise and brainstorm: a client email, a meeting recap and three outreach variations. This is the gap between a VA who gets replaced by AI and a VA who gets hired because of it.</p>
  </div>
</section>

<section class="sec lilac" id="inside">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">What your seat includes</span><h2>Everything inside the cohort.</h2></div>
    {inc([
      ('map-pin','Live onboarding kickoff','How the program works, your first week, and three activities to get you thinking like a VA'),
      ('video','7 live sessions with Shreya','Kickoff, five live Q&As where your questions are answered on screen, and a graduation session'),
      ('book-open','65+ lessons, 13 modules','Recorded lessons, assignments and resources, watched at your own pace'),
      ('pen-line','Assignments, submitted and reviewed','Every assignment submitted on the LeepX platform, with a brief, a template and a worked example'),
      ('folder','14 portfolio-grade deliverables','SOPs, trackers, a manager persona, an SOP Pack, your CV, your portfolio and an outreach pitch'),
      ('bot','AI-first workflows','Prompt systems, AI in Docs and Sheets, AI tool briefs and your own reusable prompt library'),
      ('message-circle','Cohort community chat','An active chat where students share wins, questions, leads and feedback'),
      ('rocket','Graduation session','Freelance platforms, your outreach plan, and exactly what to do in your first 30 days after'),
      ('award','Lifetime access','Every module, template and recording kept for life, including future curriculum updates'),
      ('calendar','Join any day, start today','An ongoing cohort: you get every module the day you enrol, at 5 to 7 hours a week, every live session recorded')])}
  </div>
</section>

<section class="sec" id="vault">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Yours to keep, forever</span><h2>The VA Resource Vault.</h2><p>Every template we use with real clients, handed over and yours for life.</p></div>
    {rail([
      ('notebook','Prioritisation frameworks','Eisenhower Matrix, Impact vs Effort, the Daily 3-Task Rule and Visibility vs Background work'),
      ('folder','Doc harbouring system','How to store, name and structure client documents so nothing is ever lost'),
      ('handshake','Conflict management guide','Handling difficult feedback, scope creep and awkward client conversations'),
      ('notebook','SLA templates and formats','The service agreements that set expectations before the work starts'),
      ('mail-check','Outreach Pro Toolkit','A Notion pack: pitch structures, the BJ Check and tangible value attachments'),
      ('pen-line','VA CV template','The one-page, outcome-led CV that reads in under 90 seconds'),
      ('briefcase','Portfolio templates','Notion and Canva formats, ready to fill with your own assignments'),
      ('chart-bar','Project tracker and SOP formats','Trackers, upkeep SOPs and the status update system clients rely on'),
      ('bot','AI prompt library','The structured brief format and prompts you save once and reuse on every client'),
      ('book-open','The SOP Pack walkthrough','Step by step: build the portfolio piece clients ask to see, this week')])}
  </div>
</section>

<section class="sec dark" id="system">
  <div class="wrap">
    <div class="head"><span class="eyebrow light">The system</span><h2>The LEEPX framework, built for VA work.</h2><p>Four moves that build a paid VA, and an X that accelerates all of them.</p></div>
    <div class="letters">
      <div class="letter reveal"><span class="big">L</span><b>Learn</b><p>What modern VA work actually is, the client types, the career ladder, and the niche you will own.</p></div>
      <div class="letter reveal"><span class="big">E</span><b>Equip</b><p>The workspace, the lean tool stack, prioritisation frameworks and AI workflows, set up hands-on.</p></div>
      <div class="letter reveal"><span class="big">E</span><b>Evidence</b><p>SOPs, trackers, dashboards and an SOP Pack, built as assignments and kept as portfolio pieces.</p></div>
      <div class="letter reveal"><span class="big">P</span><b>Promote</b><p>Positioning, your CV, your portfolio, pricing and outreach: turning proof into paying clients.</p></div>
      <div class="letter reveal"><span class="big">X</span><b>Accelerate</b><p>Live Q&amp;As with Shreya, assignment reviews and a community where leads circulate.</p></div>
    </div>
  </div>
</section>

<section class="sec" id="honest">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Objections, handled</span><h2>Every fear you have? We handle it, module by module.</h2></div>
    {thread([
      ('I have no VA experience.','Most students start from zero. From Module 3 you are producing real work, and by Module 10 you hold a portfolio built from your own assignments. You enter through proof, not years of experience.'),
      ('I have a full-time job. No time.','The cohort is self-paced and needs about 5 to 7 hours a week. Every live session is recorded. Join any day, start the same day, and move at whatever speed your week allows.'),
      ('Isn’t VA work just data entry?','No. Modern VAs run inboxes for seven-figure founders, manage launches for creators and coordinate teams across time zones. Data entry is the bottom rung. We teach you to skip it.'),
      ('Will I have to work night shifts?','No. Most VA work is async over Slack, email and Notion. 7 to 9 AM or 9 to 11 PM IST overlaps comfortably with the US East Coast, and plenty of clients never need live hours at all.')])}
  </div>
</section>

<section class="sec soft" id="pricing">
  <div class="wrap">
    <div class="head"><span class="eyebrow">The investment</span><h2>Piece it together yourself, and here’s your receipt.</h2><p>Every part of the program, priced on its own on the left. One seat with all of it on the right.</p></div>
    <div class="price2">
    <div class="receipt reveal">
      <div><span>Live onboarding kickoff + roadmap</span><b>₹5,000</b></div>
      <div><span>7 live sessions with Shreya</span><b>₹25,000</b></div>
      <div><span>65+ lessons across 13 modules</span><b>₹22,000</b></div>
      <div><span>SOP, SLA & tracker template library</span><b>₹9,000</b></div>
      <div><span>CV + portfolio templates</span><b>₹6,000</b></div>
      <div><span>Outreach Pro Toolkit</span><b>₹6,000</b></div>
      <div><span>AI workflows + prompt library</span><b>₹8,000</b></div>
      <div><span>Community + assignment reviews</span><b>₹10,000</b></div>
      <div class="tot"><span>Total, done alone</span><b>₹91,000</b></div>
    </div>
    <div class="tiers single">
      <div class="tier hot reveal">
        <span class="pop">Ongoing cohort · join any day</span>
        <h3>The VA Program, complete</h3><p class="for">Everything above, in one seat, with Shreya and the cohort around you.</p>
        {ul(['Onboarding kickoff, 7 live sessions and 65+ recorded lessons','14 portfolio-grade assignments, submitted and reviewed','AI-first workflows, the Resource Vault and lifetime access','Cohort community chat and the graduation session'])}
        <div class="price"><s>₹91,000</s><b>₹24,999 <small>+ GST</small></b></div>
        {buy(VA_BUY,'Join the cohort →','va')}
      </div>
    </div>
    </div>
    <p class="note"><b style="color:var(--ink)">One international retainer client covers this in your first month.</b> Not sure this is your role? {ASSESS}.</p>
  </div>
</section>

<section class="sec warm" id="bonus">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Enrol and unlock</span><h2>₹15,000 in free bonuses.</h2><p>Stacked on top of your seat.</p></div>
    <div class="tickets three">
      {ticket('Bonus 1','Live portfolio review','₹6,000',['Your finished portfolio reviewed on screen','What a client sees in the first 60 seconds','The fixes to make before you send it anywhere'])}
      {ticket('Bonus 2','Live application session','₹5,000',['We open real listings and apply together, live','Your pitch written and sent in the session','Feedback on your application before you hit send'])}
      {ticket('Bonus 3','The Opportunity Board','₹4,000',['Remote VA and ops openings shared weekly','First access for cohort members','Referrals circulating inside the community'])}
    </div>
  </div>
</section>

<section class="sec" id="voices">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Straight from our community</span><h2>Real messages. Real wins.</h2><p>These are the messages that land in our DMs from people who followed the system.</p></div>
  </div>
  {quotes([
    ('Instagram DM','Well I learned all the tools that you talked about and what was needed for that role. That helped me grab 22 LPA in my own company from 8 LPA and couldn’t thank you more for it. Being 23 and getting this good really is a big thing for me.','A.','Community member, 23','8 LPA → 22 LPA'),
    ('WhatsApp · community group','Thanks a lot Shreya! If it weren’t for you, I probably wouldn’t have this right now! Really appreciate you making this community and sharing great resources! Really excited to get started with this new role!','F.','Community member','Cracked a new role'),
    ('Instagram DM','You are the best creator over internet. I have cracked my first international client because of you, so keep going. The first and IG best mentors I have.','R.','Follower turned freelancer','First international client'),
    ('WhatsApp','I just heard back from them! I got the job! Thanks again for everything! Sharing that opportunity, conducting the crash course!','S.','Learner','Placed via a shared opportunity'),
    ('WhatsApp','Hi Shreya, your course session was really very insightful and valuable, am glad that I joined and enrolled in. Appreciate how you put this much of efforts to help others gain clarity and direction through your rich experiences in this domain.','P.','Enrolled learner','On the course sessions'),
  ])}
  <div class="wrap"><p class="note center">Messages shared with permission. Names hidden for privacy. Individual results depend on individual effort.</p></div>
</section>

<section class="sec soft" id="faq">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Questions, answered</span><h2>Questions about the VA program.</h2><p>General questions about LeepX, refunds and payments are answered on the <a href="index.html#faq" style="color:var(--purple);font-weight:700">main FAQ</a>.</p></div>
    {faq([
      ('When does the cohort start?','It is an ongoing cohort. You can join any day and start immediately, with access to every module from day one.'),
      ('Do I need prior experience?','No. Many students start from zero. If you have done admin, ops, HR, customer service or project work, you are further ahead than you think.'),
      ('Will I actually practise, or is it just lessons?','You submit 14 assignments, each with a brief, a template and a fully worked example: a manager persona, SOPs, a project tracker, AI tool briefs, your CV, your portfolio and a real outreach pitch. Every one doubles as a portfolio piece.'),
      ('How many live sessions are there?','Seven with Shreya: an onboarding kickoff, five live Q&As where your submitted questions are answered on screen, and a graduation session. All recorded.'),
      ('How much AI is in the course?','AI runs through the whole program, with a dedicated block in Module 5: ChatGPT and Claude for daily work, AI in Docs and Sheets, choosing and pitching AI tools for clients, and building your own prompt library.'),
      ('Do I have to work US night shifts?','No. Most VA work is async over Slack, email and Notion. Early mornings between 7 and 9 AM IST, or evenings between 9 and 11 PM IST, overlap comfortably with the US East Coast.'),
      ('I am already a VA. Is this for me?','If you are stuck at ₹15,000 to ₹25,000 a month and want international clients and premium positioning, yes. If you are already earning ₹50,000 and above from international clients, the early modules may feel basic.'),
      ('What is the difference between the VA and SMM programs?','SMM is running social media for clients: strategy, content and analytics. VA is running operations for clients: inbox, calendar, projects, research and executive support. Organised and process-minded suits VA. Creative and content-driven suits SMM.'),
      ('Do I need a Mac?','No. Any working laptop with reliable internet is fine, Windows included. All the tools are cloud-based.')])}
  </div>
</section>
"""


# ===================================================================== AI PROJECT MANAGEMENT
PM_BUY = 'https://academy.theleepx.com/l/c48219926c'

pm_body = f"""
<section class="chero compact" id="top">
  <div class="wrap">
    <span class="eyebrow">AI Project Management · 16 weeks</span>
    <h1>Learn <span class="hl">AI Project Management</span> in 16 weeks.</h1>
    <p class="lead">Manage projects the modern way with AI and unlock in-demand project management roles, with the skills, confidence and portfolio to land them.</p>
    <div class="acts">{buy(PM_BUY,'Join the program →','pm')}<a class="btn btn-ghost" href="#schedule">See the 16 weeks</a></div>
    <div class="chips">{chips([('calendar','16 weeks'),('video','8 weekend live sessions'),('handshake','Dedicated mentor'),('mic','2 expert guest sessions'),('wrench','Live project with Shreya'),('notebook','Job-ready portfolio'),('award','Certificate'),('clock','4 weeks post-program support')])}</div>
  </div>
</section>

<section class="sec" id="schedule">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Your 16-week schedule</span><h2>Four phases. One capstone playbook.</h2><p>A project every week, a capstone milestone every phase, so your portfolio grows as you go. In phase 3 you choose the track that matches your career goal. Live Q&amp;As happen on weekends, so your weekday schedule stays untouched.</p></div>
    <div class="skills reveal"><span class="l">What you’ll master</span>{chips([('bot','Gen AI'),('brain','Agentic AI'),('chart-bar','Gantt charts'),('folder','WBS'),('trending-up','Earned Value Management'),('refresh-cw','Scrum & Kanban'),('settings','Lean Six Sigma'),('target','DMAIC'),('activity','Predictive risk modelling'),('wrench','Jira · Asana · Notion · MS Project')])}</div>
    {timeline([
      ('Phase 1 · weeks 1 to 4 · initiation and scoping', [
        ('WEEK 1','The Modern PM Mindset','Turn a chaotic client chat thread into a clean, professional project summary.',['PM frameworks and lifecycles','Structured thinking','Async communication'],['Waterfall','Agile','Hybrid','PMO setup'],'A client-ready project update that proves you communicate with clarity.'),
        ('WEEK 2','Scoping the Brief','Turn a messy 3-page email chain into a structured requirements document (PRD).',['Project discovery','AI as your PM assistant','Requirement documents'],['Gen AI','Prompt engineering','PRD','Scope definition'],'Your first PRD, a core artefact every PM hiring manager looks for.'),
        ('WEEK 3','Visual Scoping','Create a working landing page mockup from a written brief.',['Visual scoping','Rapid prototyping','Wireframes'],['Gen AI prototyping','Wireframing','UX scoping'],'A visual prototype that aligns the team before execution starts.'),
        ('WEEK 4','Project Gating & Kickoff','Capstone milestone 1: build your project vision, process map and official project charter.',['Workflow mapping','Budgets and baselines','Stakeholder alignment'],['WBS','Gantt charts','Cost baselines','Earned Value Management'],'The first chapter of your capstone portfolio.')],
       'Capstone milestone 1: project vision, process map and official project charter.'),
      ('Phase 2 · weeks 5 to 8 · agile delivery and execution', [
        ('WEEK 5','Your Project Command Center','Break a full project roadmap into 15 structured task tickets inside a real PM tool.',['Backlogs','Workspace setup','Agile boards'],['Jira','Asana','Product backlog','User stories'],'A live project board you can walk any recruiter through.'),
        ('WEEK 6','Agile Ceremonies & Delivery','Write a formal change-request response for a client pushing scope creep.',['Agile rituals','Scope creep','Team friction'],['Scrum','Kanban','Sprint planning','Change control'],'Proof you can protect timelines and handle difficult stakeholders.'),
        ('WEEK 7','Agentic AI & Quality Control','Build a step-by-step quality checklist for a marketing or software deliverable.',['AI agents in workflows','Human review checkpoints','QA templates'],['Agentic AI','Human-in-the-loop','Lean Six Sigma','DMAIC','Root cause analysis'],'A reusable QA framework that shows you ship work right the first time.'),
        ('WEEK 8','Presenting Your Work','Capstone milestone 2: build a full agile backlog board and present it in a 5-minute video walkthrough.',['Async updates','Video walkthroughs','Stakeholder reporting'],['Stakeholder mapping','Async reporting','Milestone reviews'],'A recorded presentation that proves your delivery and communication skills.')],
       'Capstone milestone 2: a full agile backlog board and a 5-minute video walkthrough.'),
      ('Phase 3 · weeks 9 to 12 · choose your track', [
        ('TRACK A','Creative, Agency & Operations','For PMs who want to run content, marketing and agency operations.',['Wk 9 · Workflow automation: build an automation that turns client brief forms into structured tasks','Wk 10 · Creative pipelines: map how 50 ad variations get produced, reviewed and catalogued','Wk 11 · Brand governance: create a master guideline sheet for a multi-client agency','Wk 12 · Capstone milestone 3: agency automation blueprint, operational budget and a live workflow prototype'],['Agentic AI','No-code automation','AI prompt libraries','Brand governance'],'A portfolio built for agency, content and operations roles.','Who this track is for'),
        ('TRACK B','Technical, Corporate & SaaS','For PMs who want to work with software and product teams.',['Wk 9 · Budget modelling: build a dynamic cost-tracking sheet that scales with users','Wk 10 · Translating tech: turn developer release notes into a plain-English feature update','Wk 11 · Launches and releases: design a launch checklist with go/no-go criteria and rollback steps','Wk 12 · Capstone milestone 3: project budget engine, risk and failure matrix and a technical handover manual'],['Agentic AI','FinOps','CI/CD pipelines','Predictive risk modelling','SLAs'],'A portfolio built for tech, SaaS and corporate PM roles.','Who this track is for')],
       'Capstone milestone 3: Track A ships an agency automation blueprint, operational budget and a live workflow prototype. Track B ships a project budget engine, risk and failure matrix and technical handover manual.'),
      ('Phase 4 · weeks 13 to 16 · presentation and career placement', [
        ('WEEK 13','Executive Presentation','Record a 3-minute executive update explaining a major project delay and your recovery plan.',['Leadership presentations','Data storytelling','Handling tough questions'],['Executive dashboards','Data storytelling','Risk mitigation'],'Proof you can face leadership and own the room.'),
        ('WEEK 14','Portfolio & LinkedIn','Publish your public portfolio and submit your updated LinkedIn profile for review.',['Portfolio building','Resume rewrite','LinkedIn optimisation'],['Notion portfolio','ATS-ready CV','LinkedIn SEO'],'A live portfolio link and a recruiter-ready profile.'),
        ('WEEK 15','Applications & Networking','Reach out to 3 project directors or team heads at companies in your track.',['Reading job specs','Tailored applications','Outreach'],['AI-powered job search','Outbound networking'],'Real conversations started with people who hire PMs.'),
        ('WEEK 16','Interviews & Negotiation','Capstone milestone 4: final portfolio audit, job application launch and graduation.',['Behavioural interviews','Mock interviews','Negotiation'],['STAR method','Mock interviews','Salary negotiation'],'You graduate job-ready, with a verified portfolio and applications live.')],
       'Capstone milestone 4: final portfolio audit, job application launch and graduation. Then four more weeks of post-program support.')],
      l1='This week’s project', l2='What you learn')}
    <p class="note">16 weeks · a project every week · 4 capstone milestones · 2 specialised tracks, plus 4 weeks of post-program support.</p>
  </div>
</section>

<section class="sec lilac" id="aitools">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Built into the curriculum</span><h2>AI tools, week by week.</h2><p>Not a separate module. Each week’s project is done with the tool a working PM would reach for.</p></div>
    {toolcards([
      ('Week 2','Scoping the Brief',['chatgpt','claude'],'A PRD from a messy brief'),
      ('Week 4','Gating & Kickoff',['chatgpt','claude','sheets'],'Budget and risk drafts'),
      ('Weeks 5 to 6','Command Center, Agile',[('jira','Jira AI / Rovo'),('confluence','Confluence AI')],'Backlog, tickets and docs with AI inside the tools'),
      ('Week 7','Agentic AI & QC',['zapier','make'],'Your first agent workflow with a human checkpoint'),
      ('Week 8','Presenting',['copilot','gemini'],'Status decks and summaries'),
      ('Track A · weeks 9 to 12','Creative, Agency & Operations',['n8n','make','zapier','notion'],'Automations for content and client operations'),
      ('Track B · weeks 9 to 12','Technical, Corporate & SaaS',['n8n',('chatgpt','LLM APIs'),'power-automate'],'Automation with LLM APIs (concepts) and Power Automate'),
      ('Weeks 13 to 15','Career',['chatgpt','claude'],'Tailored CVs, cover letters and outreach')])}
  </div>
</section>

<section class="sec dark" id="build">
  <div class="wrap">
    <div class="head"><span class="eyebrow light">Practice, not theory</span><h2>What you walk away with.</h2></div>
    {steps([
      ('A job-ready portfolio','Real-world case studies and project artefacts built throughout the program, ready to show employers or clients.'),
      ('Practical mastery, step by step','Complex frameworks broken into manageable, actionable milestones, so you always know what to learn and apply next.'),
      ('Certificate of completion','From The LeepX Academy, to show your learning journey and newly acquired skills.'),
      ('Modern tools and AI proficiency','Hands-on fluency in the project management tools and AI workflows professionals use globally.'),
      ('Four capstone milestones','A charter, a backlog board, a track-specific build and a verified portfolio, one per phase.'),
      ('Four weeks of post-program support','Guidance continues after the core lessons end, while you apply and interview.')])}
  </div>
</section>

<section class="sec soft" id="fit">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Who it is for</span><h2>Built for four kinds of people. See if you are one.</h2></div>
    <div class="fornot">
      <div class="fn yes reveal"><h3>{ic('check')} This is for you if</h3>{ul([
        'You are a fresher or student looking to break into tech or corporate roles without prior project management experience',
        'You are switching from non-tech roles, customer support, sales or operations into project management',
        'You are returning after a career gap and want to refresh your skills, learn modern tools and re-enter with confidence',
        'You already manage projects or lead a team and want to upgrade to AI-driven workflows and modern tools'])}</div>
      <div class="fn no reveal"><h3>{ic('circle-off')} This is not for you if</h3>{ul([
        'You are looking for a shortcut to a high-paying job',
        'You cannot commit time consistently over the 16-week core curriculum',
        'You expect overnight results without putting in the work'],'circle-off')}</div>
    </div>
    <p class="note">Not sure this is your role? {ASSESS}.</p>
  </div>
</section>

<section class="sec lilac" id="inside">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">What your seat includes</span><h2>Everything inside the program.</h2></div>
    {inc([
      ('calendar','16-week core curriculum + 4 weeks of support','A comprehensive learning journey with continued guidance after the core lessons end'),
      ('video','8 weekend live Q&A sessions','Interact directly with experts and clear your doubts without disrupting your weekday schedule'),
      ('handshake','Dedicated mentor support','Personalised guidance through learning challenges, practical assignments and project milestones'),
      ('message-circle','Community Q&A and peer support','Asynchronous answers, exchanged ideas, and learning alongside mentors and fellow learners'),
      ('zap','Lifetime access to the portal','Revisit lessons, templates and frameworks whenever you need a refresher'),
      ('map-pin','LeepX community and Opportunity Board','Connect with peers, grow your network and explore relevant career opportunities'),
      ('pen-line','Advanced application and CV strategies','Position your skills, strengthen your CV and refine your portfolio to stand out'),
      ('award','Certificate of completion','From The LeepX Academy, on finishing the program'),
      ('book-open','Recorded sessions','Every live session is recorded, so a missed weekend is never a missed week')])}
  </div>
</section>

<section class="sec warm" id="bonus">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Bonuses inside the program</span><h2>Two guest sessions with industry experts, and a live build with Shreya.</h2><p>Learn straight from people doing the work: how AI is changing project management, and what teams look for when they hire.</p></div>
    <div class="tickets three">
      {ticket('Guest session 1','AI in Project Management','',['Industry expert, revealed to enrolled learners','How AI is reshaping the way projects are planned, run and delivered','How PMs can stay ahead of the change'])}
      {ticket('Guest session 2','PM Careers in the AI Era','',['Industry expert, revealed to enrolled learners','Modern PM roles and the skills teams hire for today','How to grow your career from here'])}
      {ticket('Bonus · live','Live project session with Shreya','',['Work through a real project live with Shreya, step by step','Apply the frameworks and tools from the program as you go','Questions answered on the spot'])}
    </div>
    <p class="note center">Speakers are revealed only inside the program. Join to find out who’s coming.</p>
  </div>
</section>

<section class="sec" id="roles">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Where this leads</span><h2>High-value roles you can work towards.</h2></div>
    {inc([
      ('notebook','Project Manager / Associate Project Manager','Manage cross-functional execution and deliver projects efficiently with AI-powered workflows'),
      ('refresh-cw','Agile Scrum Master / Project Coordinator','Facilitate collaboration, support agile delivery and help teams execute projects effectively'),
      ('settings','Operations & Process Excellence Specialist','Optimise workflows, identify inefficiencies and apply AI-driven approaches to process improvement'),
      ('briefcase','Freelance Consultant / Strategy Specialist','Apply your project management skills to independent client projects and consulting engagements')])}
  </div>
</section>

<section class="sec dark" id="system">
  <div class="wrap">
    <div class="head"><span class="eyebrow light">How the program works</span><h2>Four phases, then four weeks of support.</h2></div>
    <div class="letters">
      <div class="letter reveal"><span class="big">1</span><b>Initiation &amp; scoping</b><p>Weeks 1 to 4. Shift from worker to manager mindset, master structured thinking, and scope projects clearly.</p></div>
      <div class="letter reveal"><span class="big">2</span><b>Agile delivery</b><p>Weeks 5 to 8. Set up your digital command center, run agile ceremonies, and manage day-to-day delivery.</p></div>
      <div class="letter reveal"><span class="big">3</span><b>Specialised tracks</b><p>Weeks 9 to 12. Track A: creative, agency and operations. Track B: technical, corporate and SaaS.</p></div>
      <div class="letter reveal"><span class="big">4</span><b>Presentation &amp; placement</b><p>Weeks 13 to 16. Package your capstone into a portfolio, sharpen your CV and LinkedIn, and prepare for interviews.</p></div>
      <div class="letter reveal"><span class="big">+4</span><b>Post-program support</b><p>Four more weeks of guidance and support, even after the core lessons end.</p></div>
    </div>
  </div>
</section>


<section class="sec" id="voices">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Straight from our community</span><h2>What our learners have to say.</h2><p>Messages that landed in our DMs and community groups.</p></div>
  </div>
  {quotes([
    ('Learner review','The level of handholding in this program is unreal. Whenever I got stuck, Shreya was right there to guide me through it. It’s worth the investment.','Krushnal','Operations Analyst',''),
    ('Instagram DM','Well I learned all the tools that you talked about and what was needed for that role. That helped me grab 22 LPA in my own company from 8 LPA and couldn’t thank you more for it. Being 23 and getting this good really is a big thing for me.','A.','Community member, 23','8 LPA → 22 LPA'),
    ('Learner review','Before joining, I felt totally overwhelmed trying to learn everything on my own. The step-by-step structure changed everything for me. Building my own capstone project and creating portfolio assets gave me the confidence I needed to transition into a PM role.','Aiyesha','Social Media Operations','Moved into a PM role'),
    ('WhatsApp · community group','Thanks a lot Shreya! If it weren’t for you, I probably wouldn’t have this right now! Really appreciate you making this community and sharing great resources! Really excited to get started with this new role!','F.','Community member','Cracked a new role'),
    ('Instagram DM','You are the best creator over internet. I have cracked my first international client because of you, so keep going. The first and IG best mentors I have. Keep going.','R.','Follower turned freelancer','First international client'),
    ('WhatsApp','I just heard back from them! I got the job! Thanks again for everything! Sharing that opportunity, conducting the crash course!','S.','Learner','Placed via a shared opportunity'),
    ('WhatsApp','Hi Shreya, your course session was really very insightful and valuable, am glad that I joined and enrolled in. Appreciate how you put this much of efforts to help others gain clarity and direction through your rich experiences in this domain.','P.','Enrolled learner','On the course sessions'),
  ])}
  <div class="wrap"><p class="note center">Messages shared with permission. Some names hidden for privacy. Individual results depend on individual effort.</p></div>
</section>

<section class="sec soft" id="faq">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Questions, answered</span><h2>Questions about AI Project Management.</h2><p>General questions about LeepX, refunds and payments are answered on the <a href="index.html#faq" style="color:var(--purple);font-weight:700">main FAQ</a>.</p></div>
    {faq([
      ('Do I need prior project management or tech experience?','No. The program starts with the fundamentals and is designed for freshers, career switchers and working professionals alike.'),
      ('When are the live sessions? What if I miss one?','On weekends, eight of them across the 16 weeks, so your weekday schedule stays untouched. Every session is recorded, so if you miss one you can watch it later and the community Q&A keeps you on track.'),
      ('What happens in weeks 9 to 12?','You pick a track. Track A is creative, agency and operations: workflow automation, creative pipelines and brand governance. Track B is technical, corporate and SaaS: budget modelling, translating tech, launches and releases. Both end in capstone milestone 3.'),
      ('Will this program help me get a job?','We do not guarantee job placement. The program equips you with practical frameworks, modern tools, portfolio projects and CV strategies to prepare for and apply to relevant project management roles.'),
      ('What is the post-program support?','Four extra weeks of guidance after the 16-week curriculum ends, while you apply, network and interview.'),
      ('Will I have access to the materials after the program ends?','Yes. You get lifetime access to the portal, lessons, templates and frameworks.'),
      ('Can I pay in instalments?','Yes. An instalment payment option is available at checkout.')])}
  </div>
</section>
"""


# ===================================================================== MASTERCLASS (free live session)
MC_URL = 'https://academy.theleepx.com/l/145f740193'

mc_body = f"""
<section class="chero compact" id="top">
  <div class="wrap">
    <span class="eyebrow">Saturday, 14 November · 4 to 6 PM · live</span>
    <h1>Unlock <span class="hl">Global Remote Careers.</span></h1>
    <p class="lead">Learn how to stand out, get shortlisted, and land opportunities with global companies. Two live hours on building an industry-ready profile, applying strategically, and unlocking roles worldwide. No generic advice, just practical steps you can use the same night.</p>
    <div class="acts"><a class="btn btn-primary" href="{MC_URL}" target="_blank" rel="noopener" data-buy="masterclass">Reserve my spot →</a><a class="btn btn-ghost" href="#learn">See what you learn</a></div>
    <div class="chips">{chips([('hourglass','2 hours, live'),('gift','Freebies included'),('video','Recording for 3 days')])}</div>
  </div>
</section>

<section class="sec" id="learn">
  <div class="wrap">
    <div class="head"><span class="eyebrow">What you will learn</span><h2>Two hours. Everything that actually moves the needle.</h2><p>This live masterclass shows you exactly how to build an industry-ready profile, apply strategically, and unlock opportunities with global companies.</p></div>
    {rail([
      ('sparkles','Application techniques that get you noticed','Step-by-step, for global companies'),
      ('pen-line','A CV that works for remote and international companies','With real examples'),
      ('briefcase','What global remote employers actually look for','And how to match their expectations'),
      ('puzzle','Key skills you can prepare in weeks','How to stand out and show them even with no experience'),
      ('plane','Real stories of remote workers who cracked global roles','Without tech backgrounds, including Shreya'),
      ('search','Where to look','Top job boards, communities and the hidden sources of legit remote jobs'),
      ('eye-off','How to stay safe from job scams','And avoid shady platforms'),
      ('trending-up','Inbound opportunities through LinkedIn','And other platforms, so roles come to you'),
      ('bot','Use AI to speed up your job search','And stand out in a crowded pile'),
      ('wallet','Receive international payments','And manage finances and accounts')])}
  </div>
</section>

<section class="sec soft" id="video">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Watch this first</span><h2>A quick word from Shreya.</h2><p>Two minutes on what this masterclass covers and who it is really for.</p></div>
    <div class="vidbox reveal"><iframe src="https://www.youtube.com/embed/0J7XbOgDz_Q" title="A quick word from Shreya" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>
  </div>
</section>

<section class="sec lilac" id="freebies">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Yours the moment you show up</span><h2>Your freebies.</h2><p>Everything below is included free with your seat, no upsell at the end.</p></div>
    {inc([
      ('map-pin','Remote job portals','The vetted list of where global roles are actually posted'),
      ('wrench','Skills and tools to focus on','So you know exactly what to learn first'),
      ('bot','Leo AI Career Compass','Our in-house AI career agent'),
      ('pen-line','Remote-work optimised CV templates','ATS friendly and ready to fill'),
      ('user','LinkedIn profile setup','The full walkthrough so recruiters find you'),
      ('sparkles','Bonus strategies','Shared only inside the session'),
      ('mail-check','Outreach templates','Cold emails and LinkedIn DMs that actually get responses'),
      ('graduation-cap','Lifetime access to the global opportunities pool','On LeepX Academy, free')])}
  </div>
</section>

<section class="sec" id="fit">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Be honest with yourself</span><h2>Who this masterclass is and is not for.</h2></div>
    <div class="fornot">
      <div class="fn yes reveal"><h3>{ic('check')} This is for you if</h3>{ul([
        'You are a student or a fresh graduate',
        'You are a working professional eyeing global roles',
        'You are a career switcher starting a new lane',
        'You want global work as a side hustle, part-time or full-time',
        'You are willing to do the work over the next few weeks'])}</div>
      <div class="fn no reveal"><h3>{ic('circle-off')} This is not for you if</h3>{ul([
        'You are looking for a shortcut to a high-paying job',
        'You already work confidently with global companies',
        'You expect overnight results or easy money'],'circle-off')}</div>
    </div>
  </div>
</section>

<section class="sec soft" id="voices">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">What our learners say</span><h2>Real people. Real turning points.</h2></div>
  </div>
  {quotes([
    ('Learner','I always wanted to work with global companies, but I didn’t know where to start. Shreya gave me the right guidance, and today I feel confident applying for international opportunities.','Ananya','Masterclass attendee',''),
    ('Learner','The session was incredibly insightful and well-structured. Shreya’s teaching style is calm, patient and highly engaging, she addressed all our questions with clarity and care. I highly recommend this workshop to anyone actively seeking a job switch or upgrade.','Krushali','Masterclass attendee',''),
    ('Learner','I finally understood what recruiters are looking for. The feedback and mentorship helped me improve my profile and apply with confidence.','Jannet S.','Masterclass attendee',''),
    ('Learner','Thank you Shreya for all your insights and valuable feedback. Appreciate how you respected our time as well and were very careful and kind about every feedback you provided. Thanks again.','Karanpreet','Masterclass attendee',''),
  ])}
  <div class="wrap"><p class="swipe center">Straight from the DMs · swipe →</p></div>
  <div class="shots">{''.join(f'<img src="assets/course/mc-shot-{i}.jpg" alt="Learner message" loading="lazy" />' for i in range(1,6))}</div>
  <div class="wrap"><p class="note center">Unedited screenshots, shared with permission. Names hidden for privacy. Individual results depend on individual effort. This masterclass does not guarantee a job.</p></div>
</section>

<section class="sec" id="host">
  <div class="wrap host">
    <img class="reveal" src="assets/course/mc-shreya.jpg" alt="Shreya Mahendru" />
    <div>
      <div class="head"><span class="eyebrow">Your host</span><h2>Taught by Shreya Mahendru.</h2></div>
      {ticks([
        ('TEDx speaker and remote work evangelist',''),
        ('10+ years working with teams across the US, EU and UK',''),
        ('Built a global remote career starting from a ₹5,000 stipend',''),
        ('Has guided 1,000+ professionals toward global remote roles',''),
        ('Founder of LeepX, where the whole map got written down','')])}
      <p class="note">She did not have a tech background either. That is exactly why the path is teachable.</p>
    </div>
  </div>
</section>

<section class="sec lilac" id="keep">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Yours to keep</span><h2>What you walk away with.</h2></div>
    {inc([
      ('map-pin','A clear roadmap','The exact path from where you are today to global remote opportunities'),
      ('plane','Every pathway','Freelancing, part-time, full-time, contracts: which one fits you first'),
      ('trophy','Practical strategies','Application, outreach and positioning tactics you can use tomorrow'),
      ('bot','AI tools','The stack that makes searching and applying dramatically faster'),
      ('package','Resources you keep','Templates and guides you can start using immediately'),
      ('pen-line','Your templates','CV, outreach messages and profile formats, ready to fill')])}
  </div>
</section>

<section class="sec soft" id="faq">
  <div class="wrap">
    <div class="head c"><span class="eyebrow">Questions, answered</span><h2>Questions about the masterclass.</h2></div>
    {faq([
      ('Do I need prior experience?','No. The session is beginner-friendly and designed for anyone who wants to build a global career, whether you are a student, a fresher or switching lanes after years in another field.'),
      ('Will I get the recording?','Yes. The recording stays available for 3 days after the session, so you can revisit anything you missed. That said, attending live is where the real value sits: you can ask questions and get answers in the room.'),
      ('Will this masterclass help me get a job?','This masterclass will not guarantee a job, but it will give you the roadmap, tools and strategies to build an industry-ready profile and confidently apply for global opportunities.'),
      ('What exactly do I need on the day?','Two uninterrupted hours, a notebook, and your current CV or LinkedIn open so you can apply things as we go.')])}
  </div>
</section>
"""

COURSES = [
    dict(file='remote-launchpad.html', slug='launchpad',
         title='Remote Launchpad · 8 weeks to a global remote career · LeepX',
         desc='Eight weeks, recorded lessons plus a live Q&A with Shreya every Sunday. Build a global CV, a LinkedIn that gets found and outreach that gets replies.',
         cta_short='Lock your seat →', mcta_small='8 weeks · from ₹37,000',
         final_h='Eight weeks from now, you are either applying differently, or applying the same way.',
         final_p='The modules are recorded so your calendar is not the reason you stop. The Sundays are live so you are never stuck alone with a question. The rest is you.',
         final_cta='Lock your seat →', final_href='#seats', final_attrs='', cta_href='#seats', body=launchpad_body),
    dict(file='social-media-manager.html', slug='smm',
         title='Become a Remote Social Media Manager in 10 weeks · LeepX',
         desc='Ten weeks, seven live sessions, 40+ recorded lessons and 10+ real projects. Leave with a portfolio, case studies and an AI workflow you have already used.',
         cta_short='Join the cohort →', mcta_small='10 weeks · ₹25,000 + GST',
         final_h='Your leap starts here.',
         final_p='Seats are capped, so it stays personal. One of them is yours if you take it.',
         final_cta='Lock your seat →', final_href=SMM_BUY, final_attrs='target="_blank" rel="noopener" data-buy="smm"', cta_href='#pricing', body=smm_body),
    dict(file='virtual-assistant.html', slug='va',
         title='Become a Global Virtual Assistant · ongoing cohort · LeepX',
         desc='Thirteen modules, seven live sessions with Shreya, 65+ lessons and 14 portfolio-grade assignments. AI-first workflows, lifetime access, join any day.',
         cta_short='Join the cohort →', mcta_small='Join any day · ₹24,999 + GST',
         final_h='Your remote career starts the day you join.',
         final_p='Ongoing cohort. 13 modules. 7 live sessions. AI-first. Lifetime access.',
         final_cta='Join the cohort →', final_href=VA_BUY, final_attrs='target="_blank" rel="noopener" data-buy="va"', cta_href='#pricing', body=va_body),
    dict(file='ai-project-manager.html', slug='pm',
         title='AI Project Management · 16 weeks · LeepX',
         desc='Sixteen weeks, eight weekend live sessions, a dedicated mentor and four capstone milestones. Two specialised tracks, a job-ready portfolio and four weeks of post-program support.',
         cta_short='Join the program →', mcta_small='16 weeks · instalments available',
         final_h='Ready to manage projects the modern way?',
         final_p='Join AI Project Management by The LeepX Academy: practical skills, AI-powered workflows and a portfolio that gets you into the room.',
         final_cta='Join the program →', final_href=PM_BUY, final_attrs='target="_blank" rel="noopener" data-buy="pm"', cta_href=PM_BUY, body=pm_body),
    dict(file='masterclass.html', slug='masterclass',
         title='Unlock Global Remote Careers · live masterclass with Shreya Mahendru · LeepX',
         desc='Saturday, 14 November, 4 to 6 PM, live. Two hours on building an industry-ready profile, applying strategically and unlocking roles with global companies. Freebies included, recording for 3 days.',
         cta_short='Reserve my spot →', mcta_small='Sat 14 Nov · 4 to 6 PM · live',
         final_h='Your global career starts with one decision.',
         final_p='Join Unlock Global Remote Careers and take the first step towards working with companies across the world. Live session, recording for 3 days, freebies included.',
         final_cta='Reserve my spot →', final_href=MC_URL, final_attrs='target="_blank" rel="noopener" data-buy="masterclass"', cta_href=MC_URL, body=mc_body),
]

for c in COURSES:
    out = PAGE.format(
        title=esc(c['title']), desc=esc(c['desc']), slug=c['slug'],
        back_ic=BACK, cta_short=esc(c['cta_short']), cta_href=c['cta_href'], cta_attrs=(' target="_blank" rel="noopener"' if c['cta_href'].startswith('http') else ''), mcta_small=esc(c['mcta_small']),
        final_h=esc(c['final_h']), final_p=esc(c['final_p']), final_cta=esc(c['final_cta']),
        final_href=c['final_href'], final_attrs=c['final_attrs'], body=c['body'])
    (ROOT / c['file']).write_text(out)
    print('wrote', c['file'], len(out), 'chars')
