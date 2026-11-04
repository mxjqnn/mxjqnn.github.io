# Breakwater: launch checklist

Written 19 October 2026 from a pass over staging (behind the site password) with Lighthouse 12 and a page-by-page crawl. Re-checked on 4 November 2026 against staging, the Webflow page settings and the build sheet: ticked items are done, and each open item says what is still missing. Tick things off here as they are done.

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

Phases run roughly in order. Each line says who can do it: **C** the connector from this repo, **D** the Webflow Designer or dashboard (Max), **B** Breakwater (content, accounts, legal). Findings from the 19 October pass are folded in where they belong; the 4 November re-check is noted in italics.

## 1. Content and copy (B, with D for entry)

- [x] Placeholder copy replaced. *The 4 November crawl finds no "placeholder" text on any page; the final copy went in on 2 and 3 November.*
- [ ] People collection complete. *The core team is real (eight people, Eilis Klein without a photo yet). The fellows and advisors are still the placeholder people: real names, roles, photos, bios and links needed, then the placeholders deleted. No one has a LinkedIn link yet.*
- [x] Posts: launch set in place. *Six posts: three Ideas pieces by Molly Kinder, three Press & media items (New York Times, CNN, Platformer). "Our policy agenda" is deleted, so nothing is Featured on Insights or pinned to Our Work; both slots hide themselves until a post is marked.*
- [ ] Decide whether a post should be Featured on Insights and one pinned to Our Work at launch. *Both are a tick box on the post.*
- [x] Big Questions: cut to three real questions on 3 November, all three pinned to Home.
- [x] Hidden FAQ blocks on Our People and Join Us: stay hidden (decided 15 October).
- [ ] Footer: the LinkedIn and X links are still `#`. *The legal line and the Privacy and Accessibility links are done.*
- [x] Nav and drawer: the phone drawer's first link reads Home and goes to the home page (4 November).
- [x] Join Us page copy and the email address (hello@breakwaterinitiative.org).
- [ ] A full read-through of every page by someone who has not seen it before; spelling, capitalisation of Breakwater Initiative, consistent author names, date formats.
- [ ] Image rights. *Final photos are in for Our Work, Our People, Join Us, the approach slides, the home team photo and the second Big Question. The home hero slides and the tailor photo are still placeholders. Licences and consents for the final photos to be confirmed; the hero captions are empty slots at the moment.*
- [x] Font licence: ABC Arizona Flare files stay out of the public repo. *Still to confirm with Breakwater that the licence covers the live domain and expected page views.*

## 2. Design QA (D)

- [ ] Compare every page against the design files at 1440 px; check spacing, type sizes, colours, line breaks in headlines. *Headlines were reworded and restaggered on 2 and 3 November; worth one more pass.*
- [ ] Breakpoints: 1920, 1440, 1280, 1024, 768, 390 and 360 px widths, plus a short 1280 x 650 window; nothing overflows horizontally, nothing is cut off.
- [ ] Phone details: 100svh hero with browser chrome open and closed, drawer menu, tap targets at least 44 px, the sticky nav over light and dark sections.
- [ ] Hover, focus and active states on every link, card, tile and button; the yellow wipes do not leave hairlines.
- [ ] Motion: every intro and scroll reveal plays once, nothing replays on resize, nothing is stuck invisible when a section is scrolled past quickly.
- [ ] Reduced motion: System settings > Accessibility > Reduce motion, then every page is readable with the motion off.
- [ ] Page transitions: crossfade with the nav held still in Chrome, Edge and Safari; plain loads in Firefox; back and forward buttons restore pages cleanly; arriving from a tile glides to the right group.
- [ ] Images: nothing stretched, correct crops and focal points on phones, no missing images on CMS items. *A person with no photo now shows the grey placeholder.*
- [ ] 404 page: still Webflow's default (plain "Page not found"). *Design it in Pages > Utility pages > 404, and style the password page while the password is on.*
- [ ] Favicon and webclip: both files are set (favicon.ico and webclip.png). *Check they are Breakwater's mark in a tab and on a phone home screen.*
- [ ] Browser matrix: Safari (macOS, iOS), Chrome (macOS, Windows, Android), Firefox, Edge; iPad both orientations.

## 3. Accessibility (D for fixes, anyone to test)

- [x] Keyboard: Escape closes the drawer and the person pop-up, Tab stays inside the open pop-up, focus returns to the card that opened it (29 October). *Still to walk every page with Tab alone and check the order and the focus ring.*
- [ ] Screen reader pass (VoiceOver on Safari): split-line headlines, images' alt text, the drawer and pop-up announcing as dialogs, the cycling hero caption.
- [x] One H1 per page. *Every page has exactly one: a real h1 on Home, Insights (visually hidden) and posts, and the main headline marked level 1 on Our Work, Our People and Join Us.*
- [ ] Colour contrast: body greys on the dark sections and the grey meta text on the beige card against WCAG AA 4.5:1; text over photographs.
- [ ] Forms: visible labels or readable placeholders, error and success states announced, submit button reachable. *Each form has an aria-label; the fields show their names as placeholders.*
- [ ] Zoom to 200 percent in the browser: layout still works, no clipped text.
- [x] Language attribute: `lang="en"` on every page.
- [x] axe audit on staging, 29 October: no A or AA failures; the four best-practice items were fixed (main landmark, Insights h1, form names, pop-up focus trap). *Re-run once the remaining content is in.*

## 4. SEO (D, some C)

- [x] Page titles: every page has one. *Home is "Breakwater Initiative"; the post template's title is bound to the post's Title (4 November).*
- [ ] Meta descriptions: Privacy policy and Accessibility have one, and posts take theirs from the Excerpt (4 November). *Home, Our Work, Our People, Our Insights and Join Us need copy; C can set them once supplied.*
- [x] Collection templates: the People, Big Questions, FAQs and Authors templates all return 404 on staging (none of their item pages is reachable), and each carries a noindex tag in its page head code as a safeguard (4 November); Webflow will not draft a template through the API. *D: delete the Authors collection in the Designer, which removes its template.*
- [ ] Open Graph: nothing set. *Only Our Work copies its title; no page has a share image and there is no default share image in Site settings. Add a default image and per-page titles and descriptions; test with the LinkedIn Post Inspector and X card validator after launch.*
- [ ] Crawlable internal links: the Insights rows, the post page's Read more rows, the press cards and the agenda card are `#` in the HTML until the script fills them. *D: the connector cannot set a Current Post link (it only writes a literal slug), so in the Designer select each of the four link blocks (`.jrow` on Our Insights, `.jrow` in the Read more list on the Posts template, `.pcard` and `.agenda` on Our Work), open Link settings and choose Collection page > Current Post; the script leaves a real link alone. The Featured card on Insights is static and stays `#` until the script fills it.*
- [ ] No remaining `#` links: the footer's LinkedIn and X (see section 1). *The filter buttons, Load more and the approach tabs are `#` by design as the script handles them; they could become buttons.*
- [x] Heading structure sensible on every page; no empty headings. *Checked 4 November.*
- [x] Alt text: no image on any page is missing an alt attribute. *The press and post images carry alt text from the CMS; decorative images are marked empty.*
- [ ] Sitemap and robots: every static page is flagged for the sitemap, but the sitemap is not generated (returns 404) because the Auto-generate sitemap toggle in Site settings > SEO is off; the API cannot reach it. *D: turn it on. robots.txt disallows everything, which is right while the password is on; at launch, "Disable Webflow subdomain indexing" on so the webflow.io copy is never indexed, and confirm robots.txt allows the live domain.*
- [ ] Canonical domain: no custom domain is connected yet. *Choose `www` or bare, redirect the other, SSL on.*
- [ ] 301 redirects for any old URLs if Breakwater had a previous site (Site settings > Publishing > 301 redirects).
- [ ] Structured data: none yet. *Organization JSON-LD on Home (name, logo, URL, sameAs); Article JSON-LD on posts if wanted. C can write both.*
- [x] Post slugs final. *The three press posts were renamed to the outlet names on 4 November (`new-york-times`, `cnn`, `platformer`); the Ideas slugs are the titles.*
- [ ] After launch: Google Search Console and Bing Webmaster verified, sitemap submitted, live URL inspected and indexed.

## 5. Performance (D, some C)

- [ ] Hero intro versus LCP: decide whether to keep the 1.55 s hold before the hero words (mobile LCP 5.5 s on 19 October) or show the first photo immediately.
- [ ] Responsive images: the connector-placed hero photos load at their full 2400 px width (three on Our Work, one each on Our People and Join Us). *Switch them to Webflow's responsive variants or upload smaller sources.*
- [x] Lazy loading below the fold: 8 of 10 images on Our Work, 29 of 31 on Our People, 9 of 11 on Home.
- [x] Fonts: Regular and Bold are preloaded from the site head (4 November); Italic is not used above the fold and is not preloaded.
- [ ] Site settings > Publishing: minify HTML, CSS and JS on.
- [ ] Re-run Lighthouse mobile and desktop on Home, Our Work, Our People and a post; target 85+ mobile with the intro kept as designed.
- [ ] Check total page weight on Our People once the fellows' and advisors' real photos are in (31 images today).

## 6. Forms, integrations and tracking (B decides, D sets)

- [ ] Contact form: notification recipients in Site settings > Forms, reply-to set, success and error messages read well, test submission from the live domain lands in the inbox.
- [ ] Newsletter form: connect to the mailing tool or confirm the submissions inbox is watched; test a signup.
- [ ] Spam protection on both forms once they are live.
- [ ] Analytics: nothing connected (no Google tag on the site, data collection off). *Add GA4 or Plausible via Site settings > Custom code. Hover prerendering is on, so wrap the snippet to wait for `document.prerendering` to become false; otherwise prerendered pages inflate visits. The privacy policy already describes Google Analytics cookies, so the two should match.*
- [ ] Search Console and analytics linked; conversion events for form submits if wanted.
- [ ] Cookie consent if the chosen analytics or any embeds need it for the audience's jurisdiction.
- [ ] Third-party embeds: the three press posts embed YouTube and New York Times video players. *Check them for performance and consent.*

## 7. Legal and privacy (B)

- [x] Privacy policy written and linked from the footer (`/privacy-policy`, final copy 2 November). *Terms & conditions were dropped on purpose; the Accessibility page (`/accessibility`) is live.*
- [ ] Cookie notice if required; data retention for form submissions agreed. *The privacy policy states retention periods; confirm they are what Breakwater wants.*
- [ ] Company details in the footer or an imprint page if required where Breakwater is registered. *RF Catalytic Capital is named in the privacy policy.*
- [x] Accessibility statement: the Accessibility page.

## 8. Webflow housekeeping (D)

- [ ] Delete the orphan Authors collection and its template (Designer only); delete the "Field notes" option from the Posts Category field; remove unused classes (Style manager > Clean up) and unused assets (the old studio hero and the first person placeholder are no longer used). *The draft Terms and Company pages are already gone.*
- [ ] Check the Navigator on every page for stray empty elements or hidden test blocks.
- [ ] Components: Styles, Header, Footer, Wave CTA and Newsletter are single components; no page has a detached copy.
- [x] CMS: field help text filled in; Photo on People is optional (grey placeholder when empty); no empty required values on published items.
- [ ] Editor and collaborator access set up for whoever will edit content; a short CMS guide (BUILD-SHEET.md has one) handed over.
- [ ] Workspace and site ownership transferred or shared with Breakwater; billing on their card; two-factor authentication on the Webflow accounts.
- [ ] Site plan: CMS plan (the site uses collections), bandwidth and form limits adequate.
- [ ] Backups: Webflow keeps versions; note the pre-launch version in Site settings > Backups and restore test once.
- [ ] Site settings reviewed: time zone (America/New_York today), site name, custom code head and footer reviewed line by line, no leftover test scripts.

## 9. Domain, DNS and hosting (D with B's registrar access)

- [ ] Registrar access confirmed; who owns the domain and where the DNS is hosted. *No custom domain is connected to the site yet.*
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
- [ ] One month: Lighthouse re-run, content cadence for Insights, people updates, review any spam on the forms.
- [ ] Maintenance: who publishes, how changes are made (this repo's BUILD-SHEET.md is the manual), and how to reach the developer.

## 12. Handover pack

- [ ] BUILD-SHEET.md and this checklist, with the staging URL and password held by Breakwater.
- [ ] Logins: Webflow workspace, domain registrar, analytics, mailing tool, form inbox.
- [ ] A short recorded walkthrough of editing a post, a person and a big question in the Editor.
- [ ] Source files: the design, the font licence, the photo licences.
