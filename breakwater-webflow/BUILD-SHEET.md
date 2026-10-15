# Breakwater homepage: Webflow build sheet

Build the page with native Webflow elements, give them the class names below, and paste in three snippets. The stylesheet and script do the layout and motion. You do not need to style anything in the Style panel, and no Webflow Interactions are used.

`reference.html` in this folder is the page built exactly this way. Open it through a local server and use it as the target.

## Status: built in Webflow on 5 October 2026 (What we do 7 October, Who we are, Journal and Contact 12 October)

Updated 6 October 2026: mobile menu drawer added (hamburger in `.menu.right`, `.drawer` after the nav), styles embed and footer script updated, published to staging.
Desktop alignment (6 October): the script now measures two font-dependent alignments on load and resize and writes them as inline variables: the "a plan" baseline sits exactly on the bottom edge of the tailor photo (`--bt` on `.big`), and the bottom of "More about us" sits on the baseline of "government" (`--ct`/`--cb` on `.bridge-copy`). The stylesheet fallbacks are exact while the headline sizes are uncapped. The footer Subscribe button gets a yellow hover wipe like the other buttons: the script wraps the submit input in `span.news-btn` (do not build it), and the label copy comes from the button's value.

Phone layout (6 October): the "Over the next decade" section has equal 9vw top and bottom padding with 9vw between the first paragraph and the photo; the photo (92vw wide) starts 29vw in and runs off the right edge; the headline (15.6vw, line-height 1.04) overlaps it so the baseline of "Right" sits exactly on the photo's bottom edge (the script measures the offset into `--ov`), its lines step right by 0 / 10 / 19.7 / 37.9 / 31vw, and it sits 4.4vw above the closing paragraph. The "Who" paragraphs are 1.4em apart with 2.1em before the button. The "We bridge" section keeps its two backgrounds on phones: light above, beige from the people block down (a pseudo-element on `.people-title`, nothing to build), and "More about us" becomes a padded 16px button 38px below the copy. In the wave section rows 1 and 3 are three-column grids with a 16vw hole, so the mark sits centred between "is coming" and "help us" and "The" sits centred over "is coming"; "breakwater" is right-aligned to the gutter, the headline rows touch (no margin between them, so the highlights stack), and the gap before the button is 6vw.

Headline sizes (6 October): the section headlines are `clamp(56px, 7.6vw, 120px)` on desktop; the hero keeps its own `clamp(40px, 6.1vw, 96px)` there (variable "Hero and wave headline size"). On phones every headline except the question cards and the wave section is 15vw, and the script keeps each hero word inside the 20px gutters by clamping its offset. The team photo in the "Who" section is positioned by the script so the mask's lower-left edge (74.93% down the box) sits on the baseline of "policy shop" (`--tt` on `.slot-team`). The wave mark on phones is 9vw wide.

Later on 6 October: the rotated hero caption now shows on phones (bottom left, 11px), and the yellow highlights in the "Who" headline wipe in from the left as the lines land, on every breakpoint, instead of showing from the start. The script copies each highlighted word into `data-text` for this, the same way it does for hover wipes.

The page described below has been built in the **Breakwater Initiative website** project through the Webflow connector, and published to staging at https://breakwater-initiative-website.webflow.io/. This sheet now documents how it was built and how to extend it.

What differs from a hand build:

- **Every class has one neutral style in Webflow**, `outline-offset: 0px`. Webflow's HTML import drops classes that have no styles, so each class carries this single no-op property to keep its name. It has no visual effect. Leave it in place, and still do not style these classes in the Style panel.
- **Section wrappers use semantic tags**: the nav is a `header`, sections are `section`, the footer is `footer`.
- **Head code holds one extra line**, a style rule that removes the default margin on the native form wrapper inside the footer newsletter. The same rule is in `breakwater.css`.
- **Footer code holds a comment-free copy** of `breakwater.js`. The logic is identical.
- **Images are set to Webflow's default lazy loading.** Switch the three hero images and the two nav logo images to Eager in the Designer (Image settings > Load).

## Design tokens: edit these in Webflow's Variables panel

Colours and key sizes are Webflow Variables in the **Breakwater** collection. Change a value there and the whole page follows, in the Designer canvas and on the published site.

| Variable | Default | Controls |
| --- | --- | --- |
| Dark | `#2B2929` | Off-black grounds, text, word boxes, buttons |
| Beige | `#DFD8D0` | The people band behind the tiles |
| Light | `#EEEDEC` | Off-white grounds, light text, question blocks, footer hairlines |
| Yellow | `#F6F675` | Highlights, hover wipes, tile overlay, the wave section |
| Body copy size (vw) | `1.95` | Paragraph text on desktop |
| Headline size (vw) | `7.6` | "Right now", "The Breakwater Initiative", "We bridge the gap" on desktop |
| Hero and wave headline size (vw) | `6.1` | The hero and wave headlines on desktop |
| Page gutter | `2.8vw` | Left and right page margin on desktop |

- **Sizes are in viewport-width units.** 1vw is 14.4px on the 1440px design, so 7.6 gives a 109px headline. Each keeps a minimum and a proportional maximum, so text stops growing on very wide screens exactly as before.
- **Phone sizes are not tokens.** Below 768px the headline sizes and gutter come from the mobile block in the stylesheet.
- **Positions don't follow the sizes.** The layout is placed in fixed viewport units, so a large change to a headline size can make it collide with a photo or paragraph. Small adjustments are safe.
- **The logo files have their colours baked in.** The yellow nav logo is an SVG, so it does not follow the Yellow variable.
- **How it's wired.** A second Code Embed, "Breakwater tokens", sits directly after the styles embed and maps each variable onto the stylesheet. It must stay after the styles embed. Its source is `webflow-2b-tokens-embed.html`.

## What's in this folder

| File | Use |
| --- | --- |
| `webflow-1-head.html` | Paste into Site settings > Custom code > Head code |
| `webflow-2-styles-embed.html` | Paste into a Code Embed element at the top of the page |
| `webflow-2b-tokens-embed.html` | Paste into a second Code Embed directly after the styles embed |
| `webflow-3-footer.html` | Paste into Site settings > Custom code > Footer code |
| `breakwater.css`, `breakwater.js` | Readable source of snippets 2 and 3. Edit these, not the snippets |
| `what-we-do.html` | Reference build of the What we do page, the Webflow way |
| `who-we-are.html`, `journal.html`, `post.html`, `contact.html` | Reference builds of the Who we are, Journal, post and Contact pages |
| `reference.html` | Working reference built the Webflow way |
| `assets/` | Photos, both logos and the font to upload |

The stylesheet is now about 52,000 characters, over Webflow's 50,000-character limit for one Code Embed, so the `Breakwater styles` component holds it in two embeds back to back (`tools/styles-a.min.css` and `tools/styles-b.min.css`, written by `tools/minify.py`, split at the `.wwa-hero` rule so a change in one half leaves the other untouched), followed by the tokens embed. The script is about 28,000 characters. If Webflow rejects the styles embed for length, split it across two embeds at any `}`.

## Set-up, in order

1. **Font.** Site settings > Fonts holds the four licensed ABC Arizona Flare woff2 files (Regular, Italic, Bold, Bold Italic) under the family name `Arizona Flare`. Done; see the Font section below.
2. **Assets.** Upload everything else in `assets/` to the Assets panel.
3. **Head code.** Paste `webflow-1-head.html`.
4. **Styles.** Add a Code Embed as the first element in the page body and paste `webflow-2-styles-embed.html`. An embed is used so the styles show on the Designer canvas. Turning it into a Component lets you reuse it on other pages.
5. **Footer code.** Paste `webflow-3-footer.html`.
6. **Build the elements** below, top to bottom.
7. **Publish to staging** to see motion. The Designer canvas shows the finished state of every section, because scripts do not run there.

Custom code needs a paid site plan or a paid Workspace.

## Rules of thumb while building

- **Classes only.** Type the class names exactly, lower case. Where two names are listed, add both. Webflow will show the second as a combo class, which is fine.
- **Leave the Style panel alone** for these classes. The stylesheet sets everything. Styles added in Webflow can override it.
- **Use plain elements.** Div Block, Link Block, Text Link, Text Block, Paragraph, Heading, Image. Do not use the Navbar, Slider, Grid or Container components.
- **Order matters** inside headlines, the hero image stack and the menus. Offsets and stagger delays are assigned by position.
- **Added by the script, so don't build them:** the arrows on the nav button, tiles and question blocks, the stepped mark on question blocks, the two wrappers inside masked photos, the hover label copies, the arrow on the drawer's "Get involved" link, and the wrapper around the footer Subscribe button.

## Element tree

Notation: `Element type .class .second-class`. Indentation means nesting. Text in quotes is the content.

### Nav

```
Div Block .nav                               (optional: set Tag to Header)
  Div Block .menu .left
    Text Link .wipe            "What we do"
    Text Link .wipe            "Who we are"
  Link Block .logo
    Div Block .lrow .ltop > Div Block .ltxt > Image   logo-yellow.svg     (the BREAKWATER block)
    Div Block .lrow .lbot > Div Block .ltxt > Image   logo-yellow.svg     (the INITIATIVE block; same file twice)
  Div Block .menu .right
    Text Link .wipe            "Journal"
    Text Link .nav-btn .wipe   "Get involved"
    Link Block .burger         (aria-label "Menu"; shown below 768px only)
      Div Block .burger-ico
```

### Mobile menu drawer (sibling of the nav, directly after it)

```
Div Block .drawer                            (yellow full-screen drawer, below 768px only)
  Div Block .drawer-top
    Div Block .drawer-mark                   (the dark stepped mark)
    Link Block .drawer-close                 (aria-label "Close menu"; the X is drawn by CSS)
  Div Block .drawer-links                    (optional: set Tag to Nav)
    Text Link .mlink           "Why we exist"
    Text Link .mlink           "What we do"
    Text Link .mlink           "Who we are"
    Text Link .mlink           "Journal"
    Text Link .mlink .mcta     "Get involved"
```

Below 768px the nav drops the text links and shows the wordmark on the left and the hamburger on the right; the scrolled dark bar keeps the hamburger. Tapping it opens the drawer: the yellow panel wipes in from the right with the links against the right edge, then each link slides left as its highlight wipes in from the left. Closing wipes the panel out to the right with the links drifting after it. The script measures the right-edge offsets, adds the arrow to "Get involved", closes on Escape and on any link tap, and locks page scroll while open. Above 767px the drawer and hamburger are `display: none`, so the desktop nav is unchanged.

The drawer's top padding (20px) puts the mark and the X on the same line as the nav's wordmark and hamburger.

In the Designer canvas (no script) the drawer shows as a yellow block at the top of the page on the mobile breakpoints, so its links can be edited; on the published site it is hidden until opened.

Set both logo images to load Eager, not Lazy.

### Hero

```
Div Block .hero                              (optional: Tag Section)
  Div Block .hero-mark
    Div Block .mark-shape
  Text Block .fig                            type the first caption; the script swaps it per photo
  Div Block .hero-img
    Image                      hero-sculptor.jpg
    Image                      hero-accountant.jpg
    Image                      hero-welder.jpg
  Heading H1 .hero-text        "The future of work is still ours to shape"
```

**Heading lines.** Inside the H1, select each line's words and wrap them in a span with class `word`. Five spans, in this order: `The`, `future`, `of work`, `is still ours`, `to shape`.

**Custom attributes on each hero Image** (Element settings > Custom attributes). Set all three images to load Eager.

| Image | data-fig | data-caption | data-x | data-pos |
| --- | --- | --- | --- | --- |
| hero-sculptor | `Fig 1.1` | `Chloe Bernardt, sculptor & clay modeller` | `-14.9,-26,-21,-7.4` | `0% 50%` |
| hero-accountant | `Fig 1.2` | `Mary Yan, accountant, New York` | `-9.3,-19.2,-15.7,-4.4` | `25% 50%` |
| hero-welder | `Fig 1.3` | `James Gray, industrial welder, Adelaide` | `-9.6,-1,-13.1,1.3` | `25% 50%` |

- `data-x` holds the horizontal offsets for lines 2 to 5, in viewport-width units measured from the page centre. Line 1 is always centred.
- `data-pos` is the photo's crop anchor.
- The first image is the one shown on load. Add or remove images freely. The cycle follows whatever is there.

### Why: "Right now, nobody has a plan"

```
Div Block .why                               (optional: Tag Section)
  Paragraph .para .p1          "Over the next decade, AI will upend work as we know it. Whole job..."
  Div Block .slot .slot-tailor .right
    Div Block .pic .from-right .mask-tailor
      Image                    photo-tailor.jpg
  Text Block .fig              "(Fig 2) Mark Klattenburgh, Atelier at Edwin Jeans Co."
  Div Block .big
    Text Block .line           "Right"
    Text Block .line           "now,"
    Text Block .line           "nobody"       wrap the word in a span with class hl
    Text Block .line           "has"
    Text Block .line           "a plan"
  Paragraph .para .p3          "The people closest to the technology are quietly, seriously worried..."
```

- Bold the first sentence of the first paragraph.
- Bold `(Fig 2)` in the caption.
- On `.big`, add custom attributes `role` = `heading`, `aria-level` = `2`, `aria-label` = `Right now, nobody has a plan`. The headline is built from separate lines so they can move independently, and these attributes make it read as one heading.

### Who: "The Breakwater Initiative is an action-oriented policy shop"

```
Div Block .who                               (optional: Tag Section)
  Div Block .who-title
    Text Block .line           "The"          wrap in span.hl
    Text Block .line           "Breakwater"   wrap in span.hl
    Text Block .line           "Initiative is"   wrap only "Initiative" in span.hl
    Text Block .line           "an action-"
    Text Block .line           "oriented"
    Text Block .line           "policy shop"
  Div Block .slot .slot-team .right
    Text Block .cap .cap-tr    "(Fig 5) Staff at Meredian Systems, Pittsburgh, reviewing how new automation tools will affect day to day operations"
    Div Block .pic .from-right
      Image                    photo-team.jpg
  Paragraph .para .p1          "Independent of industry and political tribe; pioneering the solutions..."
  Paragraph .para .p2          "We ask the hard questions and stay in the room for the answer..."
  Text Link .cta .wipe         "Our work & solutions"
  Div Block .qs
    Link Block .question
      Div Block .qtext
        Text Block .qline      "How do we"
        Text Block .qline      "manage the"
        Text Block .qline      "pace of job"
        Text Block .qline      "loss?"
    Link Block .question       "How can" / "and should" / "we share the" / "gains of AI?"
    Link Block .question       "How might" / "we reconcile" / "work and" / "purpose?"
```

- Bold `(Fig 5)` in the caption.
- On `.who-title`: `role` = `heading`, `aria-level` = `2`, `aria-label` = `The Breakwater Initiative is an action-oriented policy shop`.
- The three question blocks share one structure. Build one, then duplicate it.

### Bridge: "We bridge the gap between tech and big government"

```
Div Block .bridge                            (optional: Tag Section)
  Div Block .bridge-title
    Text Block .line           "We bridge"    wrap in span.hl
    Text Block .line           "the gap"      wrap in span.hl
    Text Block .line           "between tech"
    Text Block .line           "and big"
    Text Block .line           "government"
  Div Block .bridge-copy
    Paragraph .para            "Our organisation combines deep policy expertise and networks..."
    Text Link .more .wipe      "More about us"
  Text Block .people-title     "Meet our people"
  Div Block .tiles
    Link Block .tile
      Image                    people-core.jpg
      Div Block .tile-title
        Div Block .trow
          Text Block .tline    "Core"
        Div Block .trow
          Text Block .tline    "team"
    Link Block .tile           people-fellows.jpg, "Breakwater" / "fellows"
    Link Block .tile           people-advisors.jpg, "Our" / "advisors"
```

- On `.bridge-title`: `role` = `heading`, `aria-level` = `2`, `aria-label` = `We bridge the gap between tech and big government`.

### Wave: "The wave is coming, help us build the breakwater"

```
Div Block .wave                              (optional: Tag Section)
  Div Block .wave-mark
    Div Block .mark-shape
  Div Block .wave-text
    Div Block .wave-row
      Text Block .word         "The"
    Div Block .wave-row
      Text Block .word         "wave"
    Div Block .wave-row
      Text Block .word         "is coming"
      Text Block .word         "help us"
    Div Block .wave-row
      Text Block .word         "build the"
    Div Block .wave-row
      Text Block .word         "breakwater"
  Paragraph .para .p1          "Policy takes time. If we don't act now, we will miss the window..."
  Text Link .cta-dark .wipe    "Contact us"
```

- On `.wave-text`: `role` = `heading`, `aria-level` = `2`, `aria-label` = `The wave is coming. Help us build the breakwater`.

### Footer

```
Div Block .foot                              (optional: Tag Footer)
  Div Block .foot-top
    Div Block .foot-about
      Link Block .foot-logo
        Image                  logo-light.svg
      Paragraph                "An action-oriented policy shop — independent of industry..."
                               make "Company setup & legals" an inline link
    Form Block .news
      Label                    "The occasional briefing on the future of work. No noise."
      Div Block .news-row
        Email field .news-input      placeholder "Email address"
        Submit button .news-submit   "Subscribe"
  Div Block .foot-bottom
    Paragraph .legal           "© 2026 The Breakwater Initiative. All rights reserved..."
    Div Block .foot-links
      Text Link .wipe          "LinkedIn"
      Text Link .wipe          "X"
      Text Link .wipe          "Terms & conditions"
      Text Link .wipe          "Privacy policy"
```

- Put the class `news` on the Form Block wrapper, not on the inner form.
- The form uses Webflow's own submission and success message. The Subscribe button changes colour on hover instead of wiping, because form buttons can't carry the wipe.

## What we do page (built 7 October 2026)

Reference build: `what-we-do.html`. Page slug `/what-we-do`. The page is built from shared components plus four new sections; the stylesheet and script cover both pages.

**Components** (group "Breakwater" in the Components panel). Drop these on every new page in this order: `Breakwater styles` (first), `Site header` (nav plus the mobile drawer), then the page's sections, then `Wave CTA` and `Footer`. `Newsletter form` is nested in the footer and also used on its own in the "Coming soon" row.

**Nav on light pages.** Give the first section the class `light-top` and the menu text turns dark until the bar sticks (the script adds `.on-light`; a `:has()` rule covers the Designer canvas).

```
Section .wwd-hero .light-top
  Div Block .wwd-title .sec-title     lines: "An" / "action"(hl) / "oriented"(hl) / "policy" / "shop"
  Div Block .slot .slot-wwd .right > Div Block .pic .from-right .mask-tailor > Image   (wwd-hero-headphones.webp)
  Div Block .fig                      rotated caption in the mask's top-right notch
  Paragraph .para .p1 / .para .p2
  Div Block .wwd-mark                 the small stepped mark under the second paragraph

Section .prong                        "A three pronged approach"
  Div Block .prong-title .sec-title
  Div Block .prong-stage              300vh tall: the scroll distance that drives the tabs
    Div Block .prong-pin              sticky, fills the viewport
      Div Block .slot .prong-slot > Div Block .pic .from-right > Image x3   (one per tab, in tab order)
        Div Block .prong-tabs > Div Block .ptabs > Text Link .ptab x3 ("One", "Two", "Three")
                              > Div Block .ptitles > Div Block .ptitle x3 (one title per tab)
      Div Block .prong-paras > Div Block .pset x3 > Paragraph .ppara x2   (two paragraphs per tab)
  Link Block .agenda                  the policy agenda card (links to the post); 40px padding, columns meet on their last baselines
    Div Block .agenda-title > Div Block .line .wipe x3 ("Our" / "policy" / "agenda")
    Div Block .agenda-body > Paragraph, Div Block .agenda-meta (> .tag "Ideas", .sep "/", date, author)

Section .faq
  Div Block .faq-title .sec-title     lines: "Answering" / "the big" / "questions" / "with [hl]action,[/hl]" / "[hl]not words[/hl]"
  Div Block .faq-list > Collection List (FAQs, sorted by Order ascending)
    Collection Item > Div Block .faq-item
      Div Block .faq-q > Text Block (bound to Question), Div Block .faq-ico
      Div Block .faq-a > Rich Text .faq-rich (bound to Answer)

Section .start                        "We've made a start"
  Div Block .start-title .sec-title .dark-title   (first three lines wrapped in .hl)
  Div Block .slot .slot-start .right > Div Block .cap .cap-tr, Div Block .pic .from-right > Image (photo-team.jpg)
  Div Block .srows
    Link Block .srow > .snum "01", .srow-title .wipe "Early career lab", Paragraph .sdesc
    Link Block .srow > .snum "02", .srow-title .wipe "Invisible Disruption", Paragraph .sdesc
    Div Block .srow .soon > .snum, .srow-title "Coming soon...", Div Block .sdesc > Paragraph + Newsletter form component
```

**How the three-pronged section behaves.** The headline sits 40px above the photo. Scrolling through the stage pins the photo, tabs and paragraphs, and the photo grows to fill the viewport between 40px of padding top and bottom. The photo drifts slowly right to left inside its mask as you scroll, and each new shot slides in over the last one like the home hero. Progress is split evenly across the tabs: the active tab's yellow fill grows left to right, finished tabs stay filled, and the title, photo and paragraphs swap when a tab completes. Clicking a tab scrolls to it. Tabs Two and Three carry placeholder copy and borrowed photos until the real content arrives.

**FAQs** live in the "FAQs" collection (Question, Answer as rich text, Order). The script opens the first item and keeps one open at a time. In the Designer canvas every answer shows expanded so they can be edited. The Collection List currently has no sort set (the connector could not save one), so items show newest first; the six items were created in reverse so they read in order. Before adding more FAQs, open the Collection List settings in the Designer and set Sort to Order, ascending.

**Measured alignments on this page** (set by the script on load and resize, with stylesheet fallbacks): the hero is lifted so the photo's top edge sits as far below the logo as the logo sits below the top of the screen (`--up` on `.wwd-hero`); the hero's "shop" baseline sits on the photo's bottom edge and the mask's lower-left step on the "oriented" baseline (`--wt` on `.wwd-title`, `--notch` on `.slot-wwd`); the "made a start" photo's bottom edge sits on the "more to come" baseline (`--st` on `.slot-start`). FAQ dividers: one line above each item plus one under the list, because Webflow wraps each item in its own Collection Item. Type sizes on desktop: prong paragraphs, agenda copy and meta, and the start-row descriptions are 20px; FAQ answers 18px; prong tab titles 32px. Phones keep their own sizes.

Phone layout on this page (8 October): the hero and "made a start" photos start on the 20px text gutter and run off the right edge. The three-pronged block keeps 40px between the headline and the photo; the pinned block is at least one screen tall, the photo grows to fill whatever the tabs and copy leave (never under 40vw), the tab title stays 32px, and the paragraphs sit 20px below it, 20px apart (inactive titles are taken out of the flow so only the visible one sets that gap). The agenda meta line matches the paragraph size on every breakpoint (15px on phones). The "made a start" rows are a single column with the number or infinity sign above the title; the hover arrow is hidden on phones.

**Test tooling** lives in `tools/`: `cdp.py` drives headless Chrome (screenshots and measurements), `fullshot.py` takes full-page captures, and the `.js` files are measurement snippets.

**Placeholders to replace:** hero caption, tab Two and Three content, the policy agenda summary and link, FAQ answers two to six, the two "made a start" links.

## Who we are page (built 12 October 2026)

Reference build: `who-we-are.html`. Page slug `/who-we-are`. Same recipe as What we do: `Breakwater styles`, `Site header`, the page's sections, `Wave CTA`, `Footer`. The nav and drawer links for "What we do" and "Who we are" now point at their pages.

```
Section .wwa-hero .light-top
  Div Block .wwa-title .sec-title     lines: "Where" / "frontier" / "AI"(hl) / "knowledge meets"(hl) / "policy experience"(hl)
  Div Block .slot .slot-studio .right > .cap .cap-tr, .pic .from-right > Image (wwa-hero-studio.webp)
  Paragraph .para .p1
  Div Block .slot .slot-potter .right > .cap .cap-bl, .pic .from-right > Image (wwa-potter.webp)
  Paragraph .para .p2
  Div Block .slot .slot-headphones .left > .cap .cap-tr, .pic .from-left > Image (wwd-hero-headphones.webp)
  Paragraph .para .p3

Section .pgroup .pgroup-team      custom attribute data-group="Core team"        (beige)
Section .pgroup .pgroup-fellows   data-group="Breakwater fellows"                (light)
Section .pgroup .pgroup-advisors  data-group="Our advisors"                      (beige)
  each: Div Block .pgroup-title .sec-title (two lines, second wrapped in .hl), Paragraph .para .pgroup-intro,
        Div Block .pgrid .cols-3 (team) or .pgrid .cols-4 (fellows, advisors) > Collection List (People)   (the grid is styled on Webflow's .w-dyn-items; the reference page wraps its cards in .pcards for the same effect)
          Collection Item > Div Block .person
            Div Block .person-pic > Image (bound to Photo)
            Div Block .person-bar > Div .person-name .wipe (Name), Div .person-role (Role), Div .person-about > span "About", span .arr
            Div Block .person-data (hidden) > Div .person-cat (Category), Rich Text .person-bio (Bio), Text Link .person-link (LinkedIn)

Div Block .modal (the shared pop-up; hidden until a card is clicked)
  .modal-bg, .modal-panel > .modal-photo > Image, .modal-body > .modal-name, .modal-role, .modal-bio, Text Link .modal-link .wipe, Text Link .modal-close

Section .faq .faq-dark
  Div Block .faq-title .sec-title .dark-title   lines: "Frequently" / "asked" / "questions"(hl)
  Div Block .faq-list > Collection List (Who we are FAQs) > same item structure as What we do
```

**People** live in the "People" collection: Name, Category (Core team / Breakwater fellows / Our advisors), Photo, Role, Bio (rich text), LinkedIn, Order. All three grids read the whole collection; the script keeps only the cards whose Category matches the section's `data-group`, so no Collection List filter is needed (one can still be added in the Designer, which also tidies the canvas). Items show newest first because the connector cannot save a sort; the 23 placeholders were created in reverse so each group reads 1, 2, 3. Set Sort to Order ascending in the Designer before adding real people.

**Cards.** Hovering a card wipes a yellow highlight across the name, turns the About button yellow and slides in an arrow. Clicking anywhere on the card (or Enter/Space when focused) opens the pop-up: the script copies the photo, name, role, bio and LinkedIn link from that card's hidden `.person-data` into the single `.modal`, wipes the panel in from the left over a 90% dark overlay, and locks scroll. Escape, the X or the overlay closes it. The LinkedIn button is hidden when the field is empty.

**Who we are FAQs** is a second collection (Question, Answer, Order) so the two pages' accordions are edited separately. The existing "FAQs" collection is the What we do (big questions) one; the connector cannot rename collections, so rename it in the Designer if you want the names to match the pages.

**Hero alignment.** The hero is lifted so the photo's top edge sits as far below the logo as the logo sits below the top of the screen (`--up` on `.wwa-hero`; every top in the section subtracts it). "Where", "frontier" and "AI" share a right edge half an em left of the photo; "knowledge meets" starts on the gutter; "policy experience" ends half an em inside the photo's right edge. The highlights are exactly one line tall so they touch. The script sizes the photo so its bottom edge sits on the "knowledge meets" baseline, its lower-left step on the "AI" baseline, and the step's upright one gap right of the "knowledge meets" fill, where the gap is the one the font leaves between a baseline and the next line's fill, so the three gaps around the fills match (`--sh`, `--nx`, `--ny` on `.slot-studio`). The headline uses the hero size token (same as the What we do hero). The group intros are split into their wrapped lines by the script and slide in after the title lines: each line starts right-aligned to the shared edge and lands left-aligned, like the title.

**Phones.** Headline 11vw so "policy experience" fits; the studio photo starts on the gutter and bleeds right, the potter photo bleeds right, the headphones photo bleeds left; the two small captions are hidden. Groups are two columns; the About button drops under the role. The pop-up fills the screen with the photo on top and a light X over it.

**Placeholders to replace:** the three hero captions, the three group intros, every person except Molly Kinder (all use the same portrait and a one-line bio), and FAQ answers two to six.

## Journal and post pages (built 12 October 2026)

Reference builds: `journal.html` and `post.html`. Page slugs `/journal` and `/posts/<slug>` (the Posts collection page). Same recipe: `Breakwater styles`, `Site header`, the page's sections, `Wave CTA`, `Footer`. The nav and drawer "Journal" links point at the Journal page.

```
Section .journal .light-top
  Link Block .agenda .jfeat (href "#")                       the Featured card; the script fills it from the most recent featured post
    Div Block .jlabel "Featured", Div Block .agenda-title, Div Block .agenda-body > Paragraph .agenda-ex, Div Block .agenda-meta > .tag .jcat, .sep, .jdate, .sep, .jauthor
  Div Block .jfilter
    Link .jcat-btn .wipe .on  data-cat="All"      then one Link .jcat-btn .wipe per category (data-cat = the category name, exactly as in the CMS)
    Div Block .jsearch > Code Embed: <input class="jsearch-input" type="search" placeholder="Search" aria-label="Search posts" autocomplete="off">
  Div Block .jrows > Collection List (Posts)
    Collection Item > Link Block .jrow (custom attribute data-slug bound to Slug)
      Div Block .jrow-main > Div .jrow-title .wipe (Title), Div .jrow-ex (Excerpt)
      Div Block .jrow-meta > Div .tag .jcat (Category), span .sep "/", Div .jdate (Date), span .sep "/", Div .jauthor (Author)
      Div Block .jdata (hidden) > Div .jfeat-flag (Featured)
  Paragraph .jempty "No posts match that."
  Link .jmore .wipe "Load more"

Posts template page
Section .post .light-top
  Div Block .post-wrap > H1 .post-title (Title), Paragraph .post-ex (Excerpt),
    Div Block .post-meta > Link Block .tag .post-cat .wipe (href "/journal") > Div .post-cat-text (Category), span .sep, Div .post-date (Date), span .sep, Div .post-author (Author),
    Rich Text .post-body (Body)
Section .readmore
  Div Block .jlabel .readmore-label "Read more…"
  Div Block .jrows > Collection List (Posts) > the same .jrow item as the journal
```

**Posts** live in the "Posts" collection: Title, Slug, Category (News / Press & media / Ideas / Field notes), Author (plain text), Featured (Yes / No), Date, Excerpt, Body (rich text: headings, lists, links, images, video embeds). There are no featured images. Author started life as a reference to an "Authors" collection and Featured as a switch, but the connector cannot bind either kind of field to text, so they became a plain text field and a Yes/No option; the empty "Authors" collection can be deleted in the Designer. Twelve placeholder posts exist (two marked Yes).

**What the script does.** Both lists read the whole collection and the script does the rest, so no Designer filter, sort or limit is needed: it sorts rows newest first by Date, turns each row's `data-slug` into its page link, rewrites dates as "9th September 2026", moves the most recent post marked Yes into the Featured card (title split into lines so each wipes yellow on hover, yellow arrow bottom right) and drops it from the list, shows ten rows, adds ten per "Load more", filters by the clicked category (All by default; the active one holds the yellow highlight, the others wipe on hover), and searches title, excerpt, author and category as you type. Rows wipe their title yellow and show an arrow on hover; row columns sit on a shared bottom edge. Opening `/journal?cat=Ideas` starts with that category selected, which is where the post page's category tag links (the script builds the link from the tag's text). On a post, Read more shows three posts from the same category, topped up from the other categories when there are fewer than three, and hides itself if there are none. A Collection List shows at most 100 items; above that, add a second list or paginate in the Designer.

**Phones.** Featured card stacks; filters wrap with the search on its own line; each row stacks title, excerpt and meta; the post body runs gutter to gutter.

## Contact page (built 12 October 2026)

Reference build: `contact.html`. Page slug `/contact`. Recipe: `Breakwater styles`, `Site header`, the three sections, `Footer`. No `Wave CTA`, because this page is where that call to action leads: the nav and drawer "Get involved" buttons and the wave's "Contact us" all point here.

```
Section .chero
  Div Block .chero-img > Image (wwd-hero-headphones.webp)
  Div Block .ctitle .sec-title     lines: "Play" / "a part" / "in the" / "solution", each a dark block placed by --x
Section .contact
  Div Block .contact-copy > Paragraph .cpara, Paragraph .cpara (with Text Link .cmail .wipe to the email address)
  Div Block .cform-box > Form Block .cform (form name "Contact")
    Div Block .cform-row > Input .cfield (Name, required), Input .cfield (Email, required)
    Textarea .carea (Message, required), Submit .csubmit
    success and error messages (styled by .cform-box .w-form-done / .w-form-fail)
Section .faq .faq-dark   custom attribute data-location="Contact"
  Div Block .faq-title .sec-title .dark-title, Div Block .faq-list > Collection List (Who we are FAQs)
    Collection Item > Div Block .faq-item > Div .faq-loc (Location, hidden), Div .faq-q > Div (Question), Div .faq-ico; Div .faq-a > Rich Text .faq-rich (Answer)
```

**FAQ locations.** The "Who we are FAQs" collection has a **Location** option: "Who we are", "Contact" or "Who we are and Contact"; empty means both. Both pages' FAQ sections read the whole collection, carry a `data-location` attribute naming their page, and the script drops any question whose Location does not mention that page. The Who we are page's item gained the same hidden `.faq-loc` block. Submissions arrive in Webflow's Forms panel under "Contact" (the footer newsletter form is named "Newsletter" there); notification emails go to the addresses set in Site settings > Forms. The active field shows a yellow underline. The connector cannot set input placeholders, so the script fills each field's placeholder from its field name (Name, Email, Message).

**Headline size.** `.ctitle` is mapped in the tokens embed to the hero size variable at 1.08x, so it follows the same Webflow Variable as the other heroes.

**Phones.** Hero 110vw tall with the headline stacked at 13vw; copy above the form; form fields in one column.

## Font (updated 13 October 2026)

The full ABC Arizona Flare family replaced the variable trial font on 13 October. Site settings > Fonts holds four files under the one family name "Arizona Flare": Regular (400), Italic (400 italic), Bold (700) and Bold Italic (700 italic). The stylesheet uses weights 400 and 700 only; the semibold (575) and the slant axis the trial font offered no longer exist, so emphasis is true Bold and captions use the real Italic. The reference pages load the same four woff2 files from `assets/`, which `.gitignore` keeps out of the public repo because the font is licensed.

## Logo contraction (updated 13 October 2026)

The nav logo is two yellow blocks, one per row of the wordmark, each clipping its own copy of the logo SVG so only its row shows. When the nav sticks, each block's box contracts towards its own centre over 0.6s while the SVG stays put, so the lettering is cut off by the closing edges, and a mask on the text layer (`--fade`, animated through a registered custom property) greys the letters as the edge reaches them. The boxes land on the stepped mark's proportions (the same `--stepmask` geometry used elsewhere) and the last letters fade out as it settles. Scrolling back up plays the same motion in reverse. The box geometry is in percentages of `.logo`, so the phone size works from the same rules; the SVG's position inside each box is derived from `--logo-w`/`--logo-h`. Matches the reference clip `Breakwater-Logo-Condense.mp4`.

## Page to page (added 14 October 2026)

Moving between pages uses the browser's cross-document view transition. The head code (`webflow-1-head.html`) opts in with `@view-transition { navigation: auto }` and gives the header `view-transition-name: nav`, so the two pages crossfade and the header stays put. Those two rules have to live in the head: on a cold load the browser decides whether to run the transition before the body's stylesheet embed has been parsed, so the same rules in the stylesheet would be skipped. When the visitor came from another page of the site (checked by referrer), the head also holds the page's first frame until the end of the body has parsed (`<link rel="expect" href="#bw-foot" blocking="render">`, pointing at a hidden `#bw-foot` div that the footer custom code puts before the script), so the new page arrives complete instead of streaming in under the fade; first visits from outside paint as early as before. A page reached from another page of the site gets `html.vt` from the head script straight away (from the referrer, before any style is computed, so no transition can start from the clipped state); the `pagereveal` event then keeps the class when the browser ran a view transition and clears it when it did not. The stylesheet uses `html.vt` to show the nav links and logo blocks at once instead of wiping them in again; the hero and section motion still play as before. Chrome, Edge and Safari 18.2+ do this; other browsers load pages as they always did. The head script also adds a speculation-rules block so Chrome prerenders a page when its link is hovered, and the footer script holds a prerendered page's motion until it is actually shown (`document.prerendering` / `prerenderingchange`).

## Later on 14 October

- The nav logo and the footer logo link to the home page (`/`).
- The home hero always fills the window: `height: 100svh` (falls back to `100vh`) on every breakpoint, instead of the earlier width-based height.
- Journal intro: the dark featured card wipes in from the right (`clip-path` on `.jfeat`, released by `.journal.in`), the title's lines slide in from the centre of the screen to their place on the left (the script measures the offsets with `measureRightAligned(..., 0.5)`, the same mechanism as the section titles), and the "Featured" label, standfirst and meta fade and drift in a little later. The section is revealed on load like the others.

## Designer canvas (15 October 2026)

The canvas showed every page unstyled although the published site was right. The cause: an HTML Embed whose code contains a literal `<` inside the `<style>` block (here the `@property --fade { syntax: '<length-percentage>' }` rule) is not rendered on the Designer canvas at all, so the whole first stylesheet embed was dropped there. The `<` is now written as the CSS escape `\00003C` in the syntax string, which browsers read the same way, and the canvas styles the pages again. Keep this in mind for any future rule that needs a `<` inside an embed (there is no other one in the stylesheet today). Scripts still never run on the canvas, so the pages show their finished state there.

## Team tiles (15 October 2026)

The three tiles on the home page link to `/who-we-are#core-team`, `/who-we-are#fellows` and `/who-we-are#advisors`. On Who we are each people group section carries the matching name as a `data-anchor` attribute (not an `id`, so the browser does not jump on load); the script lands the page at the top and glides down to the group a moment later. If a group is renamed, keep the `data-anchor` value and the tile link in step.

## Home links and CMS-driven cards (15 October 2026)

- **Buttons.** "Our work & solutions" (`.cta`) links to `/what-we-do`; "More about us" (`.more`) links to `/who-we-are`.
- **Big question cards on Home** now come from the **Big Questions** collection. The collection has a new "Pin to home page" field (Yes / No): the Yes items show as the cards, lowest Order first, three at most. The grid holds one Collection List; each item is `.question > .qtext` (bound to Question) plus a hidden `.jdata` with the pin and order values. The script drops the unpinned items, splits each question into lines once the font has loaded (so the hover slide works as before) and links every card to `/what-we-do#questions`, where the big questions section carries `data-anchor="questions"` and the page glides down to it.
- **Policy agenda card on What we do** comes from the **Posts** collection. Posts have a new "Pin to What we do" field (Yes / No): the newest Yes post becomes the card and the card links to that post. The card is one Collection List (`.agenda-list`); each item is `.agenda` with the title, excerpt and meta bound to the post fields, and the script keeps only the pinned one, splits its title into wipe lines and formats the date. Change which post appears by moving the Yes to another post.

## FAQ blocks hidden (15 October 2026)

The FAQ sections on Who we are and Contact are hidden for now, not removed: in the Designer each section's Visibility is off (Element settings > Visibility), the Who we are FAQs collection and its Location field are untouched, and the reference pages carry the markup with a `hidden` attribute. To bring them back, switch the two sections visible again and remove the `hidden` attributes. The big questions on the home page and on What we do are a different collection and stay as they are.

## Where to change things later

Edit `breakwater.css` or `breakwater.js`, then re-create the snippets by pasting the file contents between the `<style>` or `<script>` tags.

| To change | Where |
| --- | --- |
| Colours, easing curves, text speed | The variables at the top of `breakwater.css` |
| Time between hero photos | `HERO_INTERVAL` at the top of `breakwater.js` |
| Hero captions, line positions, crop per photo | The custom attributes on each hero image |
| Which hero photo shows first | Order of the images inside `.hero-img` |
| Resting positions of the "Right now" lines | `.big .line:nth-child(n)` in the CSS |
| Resting positions of the wave words | `.wave-row:nth-child(n) .word` in the CSS |
| Section heights and element positions | Each section's block in the CSS. Values are in `vw`, where 1vw is 14.4px on the 1440px design |
| Where reveals trigger | The two `rootMargin` values in `start()` in the script |
| Phone layout | The `@media (max-width: 767px)` block. It matches Webflow's mobile landscape breakpoint |

## Things to know

- **Changing a headline's wording** is safe if the number of lines stays the same. Adding or removing a line needs its `nth-child` offset adding or removing in the CSS.
- **Tablet.** Between 768px and 991px the desktop layout scales down in proportion. It has not had its own design pass.
- **Other pages.** The styles set the page background, font and link colours globally. Pages that don't use these sections will inherit those.
- **Debugging.** Add `?state=after` to the published URL to skip all motion and see the finished layout.
- **If something looks unstyled,** check the class name for typos first, then check that no style was added to that class in the Style panel.
