# LeepX website — go-live guide (no technical knowledge needed)

Do the parts in order. Each part says how long it takes. Whenever a step says "send it to Claude", paste it in the chat and the site gets updated for you.

---

## Part 1 — Create the lead spreadsheet (10 minutes)

This is where every form answer will land.

1. Log in to the Google account that should own the leads.
2. Open **sheets.new** in your browser. A blank sheet opens. Name it **LeepX Leads** (click "Untitled spreadsheet" at the top left).
3. In the menu, click **Extensions → Apps Script**. A new tab opens with a few lines of code.
4. Select everything in that code box and delete it.
5. Open the file **lead-sheet-script.gs** (in the `docs` folder, also sent in the chat). Copy all of it and paste it into the empty code box.
6. Click the **save** icon (the floppy disk).
7. Click **Deploy** (top right) → **New deployment**.
8. Click the **gear icon** next to "Select type" and choose **Web app**.
9. Set **Execute as: Me** and **Who has access: Anyone**. Click **Deploy**.
10. Google asks for permission. Click **Authorize access** → pick your account → **Advanced** → **Go to (project name)** → **Allow**. This warning is normal for your own script.
11. Copy the **Web app URL**. It starts with `https://script.google.com/macros/s/` and ends with `/exec`.
12. **Send that URL to Claude.**

What you will see later in this sheet:
- **Leads** tab: one row per person who finished the form. Name, email, WhatsApp, every answer in plain words, the recommended programs, a lead rating (hot / warm / nurture / redirect), and where they came from.
- **Progress** tab: one row per person who started the form, updated after every question. The "Last step reached" column shows where people stop.

---

## Part 2 — Collect your links (5 minutes)

Send these to Claude in one message:
- **WhatsApp number** for the team, with country code.
- **Checkout link** for each live cohort: Remote Launchpad, Become a Social Media Manager, Become a Virtual Assistant.
- **Waitlist link** for the three waitlist cohorts. A Google Form link works, or say "use WhatsApp".

---

## Part 3 — Switch on visitor tracking (10 minutes, optional but recommended)

**Google Analytics** shows how many people visit, where they come from, and how far they get.
1. Go to **analytics.google.com** and sign in.
2. Click **Start measuring**. Account name: LeepX. Property name: LeepX website. Pick India and your time zone. Click through to **Create**.
3. Choose **Web**, type your domain, and click **Create stream**.
4. Copy the **Measurement ID**. It looks like `G-XXXXXXXXXX`.

**Microsoft Clarity** records how visitors move, click and scroll.
1. Go to **clarity.microsoft.com** and sign in with Google.
2. Click **New project**, give it a name, type your domain, and create it.
3. Go to **Settings → Overview** and copy the **Project ID**.

**Send both IDs to Claude.**

---

## Part 4 — Publish the site (10 minutes)

Wait until Claude confirms "the upload folder is ready" (after Parts 1–3 are filled in).

1. Go to **app.netlify.com** and sign up with Google. It is free.
2. Go to **app.netlify.com/drop**.
3. Open Finder → Desktop → LeepX. Drag the folder **LeepX-website-upload** onto the Netlify page.
4. In about a minute Netlify gives you a link like `something.netlify.app`. Open it.
5. Fill the assessment once with your own details. Then open your Google Sheet and check that a row appeared in **Leads**.

---

## Part 5 — Connect your domain (15 minutes, then waiting)

1. In Netlify, open your site → **Domain management** → **Add a domain**. Type your domain and confirm.
2. Netlify now shows the **DNS records** you need to add. Keep this tab open.
3. In another tab, log in to the company where you bought the domain (GoDaddy, Namecheap, Hostinger and so on). Open **DNS** or **Manage DNS** for the domain.
4. Add the records exactly as Netlify shows them, and save. If there is an old record with the same name pointing to a "parked" page, delete it.
5. Wait. It usually takes 10 to 60 minutes, sometimes up to 24 hours. Netlify shows a green tick when it is done and switches on the secure padlock (HTTPS) by itself.

If you get stuck here, send Claude a screenshot of the Netlify records and of your domain's DNS page.

---

## Part 6 — Updating the site later

1. Tell Claude what to change.
2. Claude edits the site and rebuilds the **LeepX-website-upload** folder.
3. In Netlify, open your site → **Deploys**. Drag the new **LeepX-website-upload** folder into the upload box on that page.
4. The live site updates in about a minute.

Every upload stays in the Deploys list. To undo a change, open an older one and click **Publish deploy**.

---

## Before you announce the site

- [ ] A test lead appears in the Google Sheet.
- [ ] "Join the cohort", "Join the waitlist" and the WhatsApp button open the right links.
- [ ] Privacy Policy and Terms pages have their blanks filled: business name, registered address, contact email, grievance officer, payment platform, how long data is kept, refund request window, and court city. A lawyer has looked them over.
- [ ] Numbers on the page are ones you can stand behind.
- [ ] The site looks right on your phone.
