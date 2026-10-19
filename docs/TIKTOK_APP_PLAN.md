# Plan: Own TikTok API app (scheduler for creators)

Goal: a small, **public** web app that passes TikTok's app review, so videos can be posted through the official Content Posting API.

## The rule that shapes everything

TikTok rejects apps that are only for the owner:
> "Apps must not be for private or personal use."
> "Apps must not be limited to test use or to internal or private team accounts."
> "Apps that are still in development or testing will not be approved."

So this is a real product that any creator can sign up for, with free and paid plans.

## Decisions (19.10.)

| Topic | Decision |
|---|---|
| Name / domain | Jakob picks tomorrow. Free on 19.10.: kurzplan.app, slotpost.app, reelslot.app, cliptakt.de |
| Language | English |
| Platforms | TikTok first, built so Instagram can be added later |
| Plans | Free, Pro 9 EUR/month, Agency 29 EUR/month, Enterprise "Contact us" |
| Plan limits | By accounts, posts and features (draft below) |
| Payments | Stripe, real checkout from day 1 (account still to create) |
| Owner | Jakob (business or personal, see legal notes) |
| v1 features | Calendar scheduling, bulk upload via CSV, multiple TikTok accounts, send as draft to the TikTok app |
| Video source | Upload in the browser |
| Storage | Videos are deleted after posting |
| Design | Clean and minimal |
| Icon | Claude makes one, Jakob approves |
| Until approval | Try the calm browser script; if TikTok blocks again, post by hand in TikTok Studio |

### Plan limits (draft, adjust tomorrow)

| | Free | Pro 9 EUR | Agency 29 EUR | Enterprise |
|---|---|---|---|---|
| TikTok accounts | 1 | 5 | 25 | custom |
| Scheduled posts / month | 30 | 600 | 3,000 | custom |
| Calendar scheduling | yes | yes | yes | yes |
| Send as draft | yes | yes | yes | yes |
| Bulk upload (CSV) | no | yes | yes | yes |
| Team members | 1 | 1 | 5 | custom |

## Legal notes (check with your tax advisor, I'm not one)

- **Selling software subscriptions is usually a commercial activity (Gewerbe).** Your 34c Gewerbe covers real estate brokerage, and freelance AI consulting doesn't cover SaaS sales. Most likely you register an **extension of your Gewerbe** ("Entwicklung und Vertrieb von Software / SaaS"), usually online in a few minutes.
- **VAT on sales to consumers in other EU countries** (OSS procedure). Stripe can calculate it (Stripe Tax, extra fee). Alternative: Paddle or Lemon Squeezy act as the seller and handle VAT for you, at a higher fee.
- **Impressum + privacy policy + terms** must be on the website (German law + TikTok requirement). With a business address from the Gewerbe, that address can go in the Impressum.

## Your list for tomorrow (in this order)

### Before anything else (30 min)
- [ ] Pick the **name** (no "TikTok" in it) and **buy the domain** (send me the name, I can check availability)
- [ ] Set up an **email address on the domain** (e.g. hello@domain, forwarding to your Gmail is enough)
- [ ] Tell me which **address goes in the Impressum** (business or personal)

### Gewerbe extension (30 min, before the first real payment)
- [ ] Optional but quick: 5-minute call or mail to your **tax advisor**: "Ich verkaufe ab sofort Software-Abos (SaaS), reicht eine Gewerbe-Ummeldung?"
- [ ] **Gewerbe-Ummeldung** online at your city's Gewerbeamt (search "Gewerbeummeldung online [your city]"), fee usually around 20 to 40 EUR
  - Add activity: **"Entwicklung und Vertrieb von Software sowie Software as a Service (SaaS)"**
  - Start date: tomorrow's date
- [ ] **Finanzamt:** in ELSTER, submit the change of activity ("Fragebogen zur steuerlichen Erfassung, Änderung" / sonstige Nachricht), if your tax advisor doesn't do it
- [ ] Decide on **VAT for EU customers**: Stripe Tax (Stripe calculates it, extra fee) or a merchant of record (Paddle / Lemon Squeezy handle it fully)
- [ ] Use the **business address** in the Impressum and the **business details** in Stripe

### Accounts (30 min)
- [ ] Create a **TikTok developer account** at developers.tiktok.com (with the new email)
- [ ] Create an **app** there: name, short description, category (icon comes from me)
- [ ] Create a **Stripe account** (test mode is enough to start)
- [ ] Add the **TikTok client key + secret** and **Stripe keys** as environment variables in Vercel (never paste them in the chat; I tell you the variable names)

### While I build (2 to 3 h, you're free)
I build: website (home, features, pricing, FAQ), Terms, Privacy, Impressum, login with TikTok, posting screen with all TikTok UX rules, calendar, CSV bulk upload, multiple accounts, draft mode, Stripe checkout and plans, Supabase database and storage, automatic posting at the scheduled time, deletion after posting, app icon.

Meanwhile, test the calm browser script **once** with a draft: `python scripts/tiktok_upload.py test a14 --account akhmachtkrach19`

### Go live (30 min)
- [ ] Connect the domain to the Vercel project (I guide you)
- [ ] In the TikTok portal: **verify the domain** (DNS entry or file, I prepare it)
- [ ] Add products: **Login Kit** (redirect URI from me) + **Content Posting API** (Direct Post on)
- [ ] Add scopes: `user.info.basic`, `video.publish`, `video.upload`
- [ ] Create a **sandbox** and add your TikTok account as a target user

### Test + demo (1 h)
- [ ] Set your TikTok account to **private** (required while unaudited)
- [ ] Run through the app once: log in, upload, schedule, send a draft. Report any errors to me
- [ ] Record the **demo video** (Cmd + Shift + 5), following my shot list
- [ ] Set the account back to public afterwards

### Submit (15 min)
- [ ] Paste my texts (description, why each scope is needed), upload the icon + demo video
- [ ] **Submit for review**

## What to expect

- Review: no official timeline, reports say 1 to 3 weeks, often one rejection with feedback first
- Until approval: posts are private only, max 5 users per 24 h
- After approval: public posting, about 15 posts per account per day
- TikTok sounds are not possible via the API even after approval; the draft mode covers that

## TikTok's required posting screen (for reference)

- Load creator info every time, show the account nickname, stop if the account can't post right now
- Check video length against `max_video_post_duration_sec`
- Editable title/caption and hashtags
- Privacy as a dropdown **without a default**, options from `privacy_level_options`
- Comment / Duet / Stitch checkboxes, **none ticked by default**, greyed out if disabled in the account
- Commercial content toggle (off), then "Your brand" / "Branded content" with TikTok's exact texts; branded content can't be private
- AI-generated content label
- Video preview
- Consent text before the button (Music Usage Confirmation, Branded Content Policy when relevant)
- Upload only after the user clicks to confirm
- "May take a few minutes" note and a live status
- No watermarks, logos or links added to the video
