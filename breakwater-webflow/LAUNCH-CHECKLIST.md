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

## Performance

- [ ] **Hero intro versus LCP.** Lighthouse's LCP element is the first hero headline word, which by design is hidden until the fonts are in and then wiped on after 1.55 s. That intro is what makes mobile LCP 5.5 s. Options: keep it and accept the number (Google's threshold is 2.5 s), shorten the hold before the hero text appears, or show the first hero photo immediately and keep the delay only for the words. Max's call.
- [ ] **Responsive photos.** Lighthouse flags the home page photos as larger than their rendered size (photo-tailor, photo-team, the hero photos; 90 to 160 KB each). These `<img>`s were set through the connector, so they do not carry Webflow's `srcset`. In the Designer select each image and make sure "Responsive image" is on and the asset is the Webflow-processed one, or upload smaller sources. Expect roughly 100 to 130 KB saved per page.
- [ ] **Eager-load the hero and nav images.** The three hero photos and the two logo images are `loading="lazy"` (9 lazy images on the home page). Set them to Eager in Image settings > Load so the first frame is not waiting on them.
- [ ] **Fonts.** Four Arizona Flare files load; Regular and Bold do the work, Italic is only used for captions. Consider preloading Regular (Site settings > Custom code > Head: `<link rel="preload" as="font" type="font/woff2" crossorigin href="...">` with the Webflow font URL) and checking the italic is really needed in the hero's first paint. Lighthouse estimates 60 to 210 ms from `font-display`.
- [ ] **Webflow minification.** Site settings > Publishing: minify HTML, CSS and JS on. Our own stylesheet and script are already minified.
- [ ] **Re-run Lighthouse** after the above, mobile and desktop, home and one post.

## SEO

- [ ] **Titles and meta descriptions on every page.** Today Home, Contact and the post template still carry the site name as their title and no page has a description or share image. Set in each page's Settings > SEO and Open Graph: Home, What we do, Who we are, Journal, Contact, the Posts template (bind title to the post Title and description to the Excerpt), and the Big Questions and People templates if they stay reachable.
- [ ] **Open Graph image** per page (and a default one in Site settings) so links shared on LinkedIn and X show a card.
- [ ] **Crawlable links to posts.** The Journal rows, the featured card and the What we do agenda card render as `href="#"` in the HTML; the script fills in the real post URL on load. Google does run scripts, but it is safer to set the link in the Designer: select the row's link block inside the Collection List > Link settings > Collection page > "Current Post". Same for the featured card and the agenda card. Keep `data-slug`, the script leaves a real link alone.
- [ ] **Placeholder links.** Still `#`: drawer "Why we exist", footer "Company setup", LinkedIn, X, Terms, Privacy policy. Point them somewhere or remove them.
- [ ] **One H1 per page.** Home and posts have one; What we do, Who we are, Journal and Contact have none (their headlines are divs with `role="heading"`). Give each page's main headline `aria-level="1"` or make it an H1 element.
- [ ] **Sitemap and robots.** Staging currently serves `Disallow: /` and no sitemap, which is right while it is unindexed. In Site settings > SEO turn on auto-generated sitemap and keep "Disable Webflow subdomain indexing" on so the webflow.io copy never competes with the live domain.
- [ ] **Canonical / www.** Decide `www` or bare domain, set the other to redirect in Site settings > Publishing, and enable SSL.
- [ ] **Structured data.** Add Organization JSON-LD on the home page (name, logo, sameAs for LinkedIn and X) via page custom code or the connector's schema tool.
- [ ] **After launch:** add the live domain to Google Search Console, submit the sitemap, and check "Indexing" a week later.

## Content

- [ ] **Placeholder copy.** The crawl finds "placeholder" text on every page: 165 hits on Who we are (the people cards: "Team member 2", "Role placeholder", bios), 21 on What we do (prong paragraphs, agenda standfirst), and the posts' bodies. Replace or unpublish before launch.
- [ ] **People.** Replace the placeholder team members in the People collection, add real photos, roles, bios and LinkedIn links, and check the group order values.
- [ ] **Posts.** Replace the placeholder bodies, decide which posts go live, confirm Featured (Journal) and Pin to What we do are set as wanted, and that dates and authors are right.
- [ ] **Big Questions.** Real answers for the six questions; confirm the three pinned to the home page.
- [ ] **Hidden FAQ blocks** on Who we are and Contact: leave hidden, or restore and fill in.
- [ ] **Footer**: legal text, newsletter wording, social links.
- [ ] **Delete the orphan Authors collection and its template** in the Designer (the connector cannot).
- [ ] **Spell-check and read every page once in full.**

## Forms and services

- [ ] **Contact form.** Site settings > Forms: notification email recipients, reply-to, and a test submission on the live domain. Decide whether submissions should also go to a CRM or sheet (Webflow Logic, Zapier or Make).
- [ ] **Newsletter form.** Today it only lands in Webflow's form submissions. Connect it to the mailing tool (Mailchimp, Substack, Beehiiv or similar) or confirm someone reads the submissions.
- [ ] **Spam.** Turn on reCAPTCHA or Webflow's form spam filtering if junk arrives.
- [ ] **Analytics.** Add GA4 or Plausible in Site settings > Custom code. Note that hover prerendering is on: wrap the analytics snippet so it runs after `document.prerendering` becomes false (listen for `prerenderingchange`), otherwise prerendered pages count as visits.
- [ ] **Cookie consent** if the analytics tool needs it for the audience's jurisdiction.

## Function and motion

- [ ] Click every nav, drawer, footer, tile, card and button link on every page (desktop and phone).
- [ ] Journal: filters, search, Load more, category links from a post, Read more picks.
- [ ] Who we are: person pop-ups open and close with mouse, keyboard (Tab, Enter, Escape) and the backdrop.
- [ ] What we do: the pinned three-pronged section scrolls correctly on a real phone and at a short desktop window.
- [ ] Arrivals: home tiles glide to the right group on Who we are; home question cards glide to the questions section on What we do.
- [ ] Page transitions: Chrome and Safari crossfade with the nav held still; Firefox loads plainly; the browser back button restores the page cleanly.
- [ ] Reduced motion (System settings > Accessibility): pages read correctly with the motion off.
- [ ] Password page off, then test the 404 page (Webflow default unless a custom one is designed).

## Browsers and devices

- [ ] Safari (macOS and iOS), Chrome, Firefox, Edge; an Android phone; an iPad in both orientations.
- [ ] Phone checks: the 100svh hero with the browser chrome showing and hidden, the drawer menu, the contact form, long titles wrapping.
- [ ] A very wide (2560 px) and a short (1280 x 650) desktop window.
- [ ] Dark-mode system setting (the site is fixed-palette; just confirm nothing inverts).

## Webflow settings and launch day

- [ ] Site plan: a CMS plan (the site uses collections) on the Breakwater workspace, billing in the client's name.
- [ ] Custom domain added, DNS records set (A records or CNAME per Webflow's panel), SSL on, default domain chosen.
- [ ] **Turn the site password off** before the first live publish, since it covers every domain.
- [ ] Favicon and webclip icons in Site settings > General.
- [ ] Publish to the custom domain, then crawl it once (every page 200, no `#` links, no staging URLs in content).
- [ ] Run PageSpeed Insights and the Rich Results test on the live domain.
- [ ] Remove the Webflow MCP app from the Designer if it is no longer needed, and the `?state=after` debugging hook can stay (harmless).
- [ ] Hand over: this repo's `BUILD-SHEET.md` explains how every section is built and how to change it.

## After launch

- [ ] Search Console: sitemap submitted, no coverage errors after a week.
- [ ] Analytics receiving data; forms tested from the live domain.
- [ ] Re-run Lighthouse on the live domain and keep the report.
- [ ] Schedule a content pass in a month: journal cadence, people updates.
