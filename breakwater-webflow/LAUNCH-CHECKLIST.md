# Breakwater: launch checklist

Written 19 October 2026 from a pass over staging (behind the site password) with Lighthouse 12 and a page-by-page crawl. Tick things off here as they are done.

## Speed checks while the password is on

Google PageSpeed Insights cannot get past the password page (staging returns 401 to it), so there are three ways to measure:

1. **Lighthouse in Chrome DevTools** (day to day). Open staging in Chrome, enter the password once, then DevTools > Lighthouse > Analyze. It uses your logged-in session. Test in an incognito window so extensions do not skew it, and run both Mobile and Desktop.
2. **Lighthouse from the terminal** (what the numbers below come from). `tools/cdp.py` can hand over the gate cookie; the command is `npx lighthouse@12 <url> --extra-headers='{"Cookie":"wf_auth=..."}'`. Ask Claude to rerun it after changes.
3. **PageSpeed Insights proper** once, just before launch: switch the password off in Site settings, publish, run PSI on the staging URL, then switch it back on and publish again. PSI's "field data" will stay empty until the live domain has had real visitors for about a month, so the lab numbers are the ones to read.

Baseline on 19 October (home page):

| | Mobile | Desktop |
|---|---|---|
| Performance | 72 | 84 |
| Largest Contentful Paint | 5.5 s | 2.0 s |
| First Contentful Paint | 2.6 s | 1.0 s |
| Cumulative Layout Shift | 0 | 0 |
| Total Blocking Time | 20 ms | 0 ms |
| Accessibility / Best practices | 100 / 100 | 100 / 100 |
| SEO | 58 | 58 |

The SEO score is low only because of the password (not crawlable) and missing meta descriptions; both are on the list below.

## How to use this list

Phases run roughly in order. Each line says who can do it: **C** the connector from this repo, **D** the Webflow Designer or dashboard (Max), **B** Breakwater (content, accounts, legal). Findings from the 19 October pass are folded in where they belong.

## 1. Content and copy (B, with D for entry)

- [ ] Every placeholder replaced. The crawl finds "placeholder" copy on every page: people cards on Who we are (names, roles, bios), the three-pronged paragraphs and agenda standfirst on What we do, post bodies, Big Question answers, footer legal line.
- [ ] People collection complete: real names, roles, photos (same crop, same lighting), bios, LinkedIn links, group and order set; placeholder members deleted.
- [ ] Posts: decide the launch set, finish bodies, check dates, authors, categories, excerpts; set Featured for the Journal and Pin to What we do for the agenda post; unpublish the rest rather than deleting if they are drafts.
- [ ] Big Questions: six real answers; the three pinned to Home confirmed.
- [ ] Hidden FAQ blocks on Who we are and Contact: stay hidden or come back with real questions.
- [ ] Footer: legal line, newsletter wording, social links, terms and privacy links.
- [ ] Nav and drawer: "Why we exist" link decided (it is `#` today).
- [ ] Contact page copy and the email address on it.
- [ ] A full read-through of every page by someone who has not seen it before; spelling, capitalisation of Breakwater Initiative, consistent author names, date formats.
- [ ] Image rights: the current photos are placeholders; final photos licensed for web use, people in them have consented, credits added where required (the hero captions name people).
- [ ] Font licence: ABC Arizona Flare is a licensed web font; confirm the licence covers the live domain and expected page views, and that the files stay out of the public repo (they do).

## 2. Design QA (D)

- [ ] Compare every page against the design files at 1440 px; check spacing, type sizes, colours, line breaks in headlines.
- [ ] Breakpoints: 1920, 1440, 1280, 1024, 768, 390 and 360 px widths, plus a short 1280 x 650 window; nothing overflows horizontally, nothing is cut off.
- [ ] Phone details: 100svh hero with browser chrome open and closed, drawer menu, tap targets at least 44 px, the sticky nav over light and dark sections.
- [ ] Hover, focus and active states on every link, card, tile and button; the yellow wipes do not leave hairlines (fixed on the headline blocks, check the rest).
- [ ] Motion: every intro and scroll reveal plays once, nothing replays on resize, nothing is stuck invisible when a section is scrolled past quickly.
- [ ] Reduced motion: System settings > Accessibility > Reduce motion, then every page is readable with the motion off.
- [ ] Page transitions: crossfade with the nav held still in Chrome, Edge and Safari; plain loads in Firefox; back and forward buttons restore pages cleanly; arriving from a tile glides to the right group.
- [ ] Images: nothing stretched, correct crops and focal points on phones, no missing images on CMS items.
- [ ] 404 page designed in the Breakwater style (Pages > Utility pages > 404), and the password page styled while the password is on.
- [ ] Favicon and webclip (Site settings > General) show in a tab and when saved to a phone home screen.
- [ ] Browser matrix: Safari (macOS, iOS), Chrome (macOS, Windows, Android), Firefox, Edge; iPad both orientations.

## 3. Accessibility (D for fixes, anyone to test)

- [ ] Keyboard only: Tab reaches every link, button, card and form field in a sensible order; focus is visible; Escape closes the drawer and the person pop-up; focus returns to the card that opened the pop-up.
- [ ] Screen reader pass (VoiceOver on Safari): headline divs announce as headings, images have meaningful alt text or are marked decorative, the drawer and pop-up announce as dialogs, the cycling hero caption is not disruptive.
- [ ] One H1 per page: Home and posts have one; What we do, Who we are, Journal and Contact need their main headline marked level 1 (today they are divs with `role="heading"` and level 2).
- [ ] Colour contrast: body greys on the dark sections (`rgba(238,237,236,.7)` and `.45`) against the dark background, and the grey meta text on the beige card; check against WCAG AA 4.5:1 for small text.
- [ ] Forms: labels or placeholders readable by assistive tech, error and success states announced, submit button reachable.
- [ ] Zoom to 200 percent in the browser: layout still works, no clipped text.
- [ ] Language attribute set (Webflow sets `lang` from the site locale; it is English).
- [ ] Run axe DevTools or Lighthouse accessibility on every page (home is 100 today).

## 4. SEO (D, some C)

- [ ] Page title and meta description on every static page: Home, What we do, Who we are, Journal, Contact. Home, Contact and the post template still use the site name as the title and no page has a description (C can set these if the copy is supplied).
- [ ] Collection templates: Posts title and description bound to Title and Excerpt; the Big Questions and People templates either given sensible SEO fields or set to noindex if they are not meant to be visited.
- [ ] Open Graph title, description and image per page, and a default share image in Site settings; test with the LinkedIn Post Inspector and X card validator after launch.
- [ ] Crawlable internal links: Journal rows, the featured card and the agenda card are `#` in the HTML until the script fills them. Set each link block to Collection page > Current Post in the Designer; the script leaves a real link alone.
- [ ] No remaining `#` links anywhere (footer and drawer today).
- [ ] Heading structure sensible on every page; no empty headings.
- [ ] Alt text on all images, including CMS images (bind People photos' alt to the Name field).
- [ ] Sitemap: Site settings > SEO > auto-generate sitemap on; robots.txt allows the live domain; "Disable Webflow subdomain indexing" on so the webflow.io copy is never indexed.
- [ ] Canonical domain: choose `www` or bare, redirect the other, SSL on.
- [ ] 301 redirects for any old URLs if Breakwater had a previous site (Site settings > Publishing > 301 redirects).
- [ ] Structured data: Organization JSON-LD on Home (name, logo, URL, sameAs); Article JSON-LD on posts if wanted.
- [ ] Journal post slugs are final (changing a slug later breaks shared links).
- [ ] After launch: Google Search Console and Bing Webmaster verified, sitemap submitted, live URL inspected and indexed.

## 5. Performance (D, some C)

- [ ] Hero intro versus LCP: decide whether to keep the 1.55 s hold before the hero words (mobile LCP 5.5 s today) or show the first photo immediately.
- [ ] Responsive images: switch the connector-placed images to Webflow's responsive variants or upload smaller sources (roughly 100 to 130 KB saved per page).
- [ ] Eager loading on the hero photos and nav logos; lazy everywhere below the fold (People photos are lazy already).
- [ ] Fonts: preload Regular; confirm Italic is needed above the fold.
- [ ] Site settings > Publishing: minify HTML, CSS and JS on.
- [ ] Re-run Lighthouse mobile and desktop on Home, What we do, Who we are and a post; target 85+ mobile with the intro kept as designed.
- [ ] Check total page weight on Who we are once real photos are in (23 people cards).

## 6. Forms, integrations and tracking (B decides, D sets)

- [ ] Contact form: notification recipients in Site settings > Forms, reply-to set, success and error messages read well, test submission from the live domain lands in the inbox.
- [ ] Newsletter form: connect to the mailing tool or confirm the submissions inbox is watched; test a signup.
- [ ] Spam protection on both forms once they are live.
- [ ] Analytics: GA4 or Plausible added via Site settings > Custom code. Hover prerendering is on, so wrap the snippet to wait for `document.prerendering` to become false; otherwise prerendered pages inflate visits.
- [ ] Search Console and analytics linked; conversion events for form submits if wanted.
- [ ] Cookie consent if the chosen analytics or any embeds need it for the audience's jurisdiction.
- [ ] Any third-party embeds (video, social) checked for performance and consent.

## 7. Legal and privacy (B)

- [ ] Privacy policy and terms pages written, linked from the footer (both links are `#` today).
- [ ] Cookie notice if required; data retention for form submissions agreed.
- [ ] Company details in the footer or an imprint page if required where Breakwater is registered.
- [ ] Accessibility statement if the organisation wants one.

## 8. Webflow housekeeping (D)

- [ ] Delete the orphan Authors collection and template, the test embeds are already gone, remove unused classes (Style manager > Clean up) and unused assets.
- [ ] Check the Navigator on every page for stray empty elements or hidden test blocks.
- [ ] Components: Styles, Header, Footer, Wave CTA and Newsletter are single components; no page has a detached copy.
- [ ] CMS: field help text filled in (done for Pin fields), required fields sensible, no empty required values on published items.
- [ ] Editor and collaborator access set up for whoever will edit content; a short CMS guide (BUILD-SHEET.md has one) handed over.
- [ ] Workspace and site ownership transferred or shared with Breakwater; billing on their card; two-factor authentication on the Webflow accounts.
- [ ] Site plan: CMS plan (the site uses collections), bandwidth and form limits adequate.
- [ ] Backups: Webflow keeps versions; note the pre-launch version in Site settings > Backups and restore test once.
- [ ] Site settings reviewed: time zone (America/New_York today), site name, custom code head and footer reviewed line by line, no leftover test scripts.

## 9. Domain, DNS and hosting (D with B's registrar access)

- [ ] Registrar access confirmed; who owns the domain and where the DNS is hosted.
- [ ] Lower the DNS TTL to 300 seconds a day before launch so the switch propagates fast.
- [ ] Note existing MX, SPF, DKIM and DMARC records and leave them untouched; email must keep working.
- [ ] Add the custom domain in Webflow, set the A records (or CNAME for www) exactly as the panel shows, wait for the checks to pass, enable SSL.
- [ ] Choose the default domain (www or bare) and confirm the redirect.
- [ ] If the domain currently points elsewhere, plan the cut-over time and who is watching.

## 10. Launch day runbook

1. Final content freeze and a last full read-through.
2. Password off in Site settings > General.
3. Confirm the custom domain and SSL are green; publish to the custom domain only (and staging if wanted).
4. Crawl the live domain: every page returns 200, no `#` links, no staging URLs, no mixed content, forms submit.
5. Run PageSpeed Insights, the Rich Results test and the LinkedIn and X share previews on the live URL.
6. Verify Search Console on the live domain and submit the sitemap; check analytics is receiving.
7. Put the DNS TTL back up a day later.
8. Keep the staging site password on; it is the review copy from now on.

## 11. After launch

- [ ] 24 hours: analytics and form submissions confirmed, SSL renewing, no errors in Search Console.
- [ ] One week: indexing coverage, Core Web Vitals in PSI field data starting to appear, broken link crawl (Screaming Frog or a free crawler).
- [ ] One month: Lighthouse re-run, content cadence for the Journal, people updates, review any spam on the forms.
- [ ] Maintenance: who publishes, how changes are made (this repo's BUILD-SHEET.md is the manual), and how to reach the developer.

## 12. Handover pack

- [ ] BUILD-SHEET.md and this checklist, with the staging URL and password held by Breakwater.
- [ ] Logins: Webflow workspace, domain registrar, analytics, mailing tool, form inbox.
- [ ] A short recorded walkthrough of editing a post, a person and a big question in the Editor.
- [ ] Source files: the design, the font licence, the photo licences.
