# KCA website, everything a new Claude needs

Written 7 Nov 2026. This file is auto loaded by Claude Code whenever you work in this
folder. Read it fully before the first edit. Facts here were verified live on 7 Nov 2026,
not recalled from memory. If something below contradicts what you observe, trust what you
observe and correct this file.

---

## 1. What this is

The public website for **Kids' Cerebral Academy (KCA India)**, Nagpur. Run by
**Dr. Gurupreet Kaur Saluja**, child psychologist. KCA has been running national art
competitions since 2008. The site is plain static HTML and CSS. No build step, no
framework, no npm, no node. You edit `.html` and `.css` files and push.

**Live:** https://kcaindia.com

**Owner of content:** Yash's mother (referred to as mumma in chat). She sends changes by
WhatsApp as screenshots, marked up images, PDFs, videos of a mockup, or short text notes.
Yash relays them.

---

## 2. Hosting, domain, DNS

| Thing | Value |
|---|---|
| Host | GitHub Pages, legacy build, branch `main`, path `/` |
| Repo | `https://github.com/kcaindia/kcaindia.github.io` |
| GitHub account that owns it | **kcaindia** (mumma's), email kcaindia.com@gmail.com |
| Custom domain | `kcaindia.com`, set in the repo `CNAME` file |
| HTTPS | enforced, cert covers **both** `kcaindia.com` and `www.kcaindia.com` |
| Cert expiry | 2027-01-18, renews automatically |
| Registrar | GoDaddy |
| Domain expiry | **2027-09-27** (renewed, confirmed by whois) |
| Nameservers | `ns19.domaincontrol.com`, `ns20.domaincontrol.com` (GoDaddy) |
| Apex A records | 185.199.108.153 / .109.153 / .110.153 / .111.153 (all end `.153`) |
| www | CNAME to `kcaindia.github.io`, 301s to the apex. **Working.** |

Both apex and www return 200 and http redirects to https. DNS is settled. Do not touch it
unless something is actually broken.

---

## 3. How to deploy

There are two GitHub accounts on this machine. The active one is **not** the one that owns
this repo, so you must pass the kcaindia token explicitly on every push.

```bash
cd /path/to/kca-website
git add -A
git commit -m "your message"
GH_TOKEN=$(gh auth token --user kcaindia) \
  git -c credential.helper='!f(){ echo username=kcaindia; echo password=$GH_TOKEN; };f' \
  push origin HEAD
```

Do **not** run `gh auth switch`. It changes the global active account and affects Yash's
other work. The inline credential helper above leaves the global state alone.

GitHub Pages rebuilds automatically on push. It usually goes live in 1 to 3 minutes.

---

## 4. New Mac setup

```bash
# 1. clone
cd ~/Desktop/agents
git clone https://github.com/kcaindia/kcaindia.github.io.git kca-website

# 2. GitHub CLI, log in as BOTH accounts
gh auth login          # yashlondee-star
gh auth login          # kcaindia   (this one owns the site)
gh auth status         # confirm both are listed

# 3. python helpers used for brochures and QR codes
pip3 install --user pymupdf segno
```

Google Chrome must be installed. It is used headless to render HTML to PDF and to take
screenshots. Nothing else is needed.

---

## 5. Repo layout

```
index.html                        home page
grand-indian-art-contest.html     contest page, has the 13 page flipbook
rising-colours.html               school competition page
kca-international-art-club.html   art club page
blog.html + 3 blog-*.html         articles
faq.html  previous-events.html
privacy-policy.html  terms.html  refund-policy.html  user-deletion.html

style.css      site wide: topbar, nav, dropdown, hero, cards, footer, lightbox
contest.css    the three programme pages: gc-* components, flipbook, KIAC, Rising variant

CNAME          kcaindia.com
.nojekyll      REQUIRED, see traps
robots.txt  sitemap.xml
images/kca-logo.png
images/events/        15 past event posters, 2008 to 2025
images/brochure/      13 JPGs, the Grand contest flipbook pages
brochure/             the two downloadable PDFs
```

**Redirect stubs.** These are tiny files that bounce to a real page. They exist so old
printed URLs and short share links keep working. Never delete them.

| Stub | Goes to |
|---|---|
| `contest.html` → `/contest` | grand-indian-art-contest.html |
| `club.html` → `/club` | kca-international-art-club.html |
| `rising.html` → `/rising` | rising-colours.html |
| `register.html` → `/register` | NOT a stub since 10 Nov 2026: the Register chooser page (all three programmes, each with its own button or a closed notice). Every nav Register Now and footer Register Now points here |
| `national.html` `about.html` `about-us.html` `gallery.html` `global.html` `previous_events.html` `privacy_policy.html` `terms_and_condition.html` `refund_and_cancellation.html` `user_deletion.html` | old site URLs from before the 2026 rebuild |

GitHub Pages serves `/contest` from `contest.html`, so the short links work without any
server config.

---

## 6. The programmes

### The Grand Indian Art Contest 2026, individual entry
- Page: `/grand-indian-art-contest.html`, short link `/contest`
- Registration form: `https://forms.gle/iWaxGnuNpZi9wHgM6`, short link `/register`
- Email: thegrandindianart@gmail.com
- 10 categories A to J. A to G use **A3** sheets, H, I and J use canvas 18 × 18 inch.
- Fees ₹199 to ₹599. Grand winner prizes ₹4,000 / ₹6,000 / ₹11,000 / ₹21,000.
- Dates: register by 30 Oct 2026, artwork upload by 15 Nov 2026, shortlist 15 Dec 2026,
  originals by 30 Dec 2026, results 15 Jan 2027, awards and certificates before 30 Jan 2027.
- **Registration CLOSED since 10 Nov 2026** (Yash's instruction): every button reads *Registration opens June 2027*, the form link appears nowhere. Artwork upload and later dates still stand for people already registered.
- Has a hand built **flipbook** of the 13 page brochure, see section 8.

### Rising Colours 2026, school entry, 16th edition
- Page: `/rising-colours.html`, short link `/rising`
- Email: kcarisingcolours@gmail.com
- **Registration is CLOSED.** Everywhere it appears it must read
  *School Registration opens June 2027*. Mumma's exact instruction, 23 Aug 2026:
  "Close registration form of National Talent search from everywhere and show School
  Registration will open on June 2027."
- The old form `https://forms.gle/CwWsuruPVywwZugW8` is dead. It must not appear anywhere.
- 7 age categories, Nursery to Class 10. Competition runs in September at each school.

### KCA International Art Club, global membership
- Page: `/kca-international-art-club.html`, short link `/club`
- Membership form: `https://forms.gle/8Bmg7mxJtpuujmbo7`, **registration CLOSED since 10 Nov 2026**, every button reads *Membership Registration opens June 2027*, form link appears nowhere
- Email: kcainternationalartclub@gmail.com
- Membership ₹499 India, AED 25 UAE, US$8 other countries, per year.
- 7 categories A to G. Monthly theme of the member's own choice.
- **Submission deadline is the 30th of every month.** It was the 20th until 13 Oct 2026.
- Brochure PDF at `brochure/KCA-International-Art-Club-Brochure.pdf`, linked from every
  Read the Brochure button.

### KCA National Art Excellence Awards Ceremony 2027, Kala Ratna Samman (added 10 Nov 2026)
- Page: `/national-art-excellence-awards.html`, short link `/awards`
- Source: mumma's 4 page brochure, `brochure/KCA-National-Art-Excellence-Awards-2027-Brochure.pdf`, page JPGs at `images/awards-brochure/page-01.jpg` to `page-04.jpg`
- Ceremony 14 March 2027, Sunday, 11 AM to 2.30 PM, 5 star hotel in Nagpur (to be informed). Exhibition 11 AM to 8 PM.
- 9 categories (Class 1 and 2 up to Professional Artists), 25 awardees each, 225 total, one time fee Rs 2500 non refundable.
- WhatsApp community: https://chat.whatsapp.com/BQgHsGOWsWu6Rku9VicChp (printed in the brochure)
- **NO REGISTRATION FORM YET.** Yash will send a Google Form. Until then every button reads *Registration opens soon* (awards page hero and closing, homepage card, register.html card). When the form arrives, swap those locked spans for links.
- Homepage headline changed from "Three Ways to Join" to "Four Ways to Join" when this was added.

### Shared contacts and socials
```
Facebook   https://www.facebook.com/share/1JeERH8wxB/
Instagram  https://www.instagram.com/kcakidscerebralacademy?igsh=MTZ5bTBxNmRzd2Fhbw==
Telegram   https://t.me/KCAcontests          (the winners gallery)
WhatsApp   https://wa.me/917770016545  and  https://wa.me/917796613273
Phones     77700 16545 · 77966 13273 · 90673 55412
Address    44 Farmland, Ramdaspeth, Nagpur 440010, Maharashtra
Emails     thegrandindianart@gmail.com · kcaindia.com@gmail.com
           kcainternationalartclub@gmail.com · kcarisingcolours@gmail.com
```

---

## 7. Content rules, non negotiable

1. **No hyphens or dashes in visible text. Ever.** No `-`, no en dash, no em dash. This is a
   hard standing rule from Yash. Rewrite as two words, one word, or use commas, or "to" for
   ranges. "Two level jury" not the hyphenated form. and write "Grades 1 to 2" rather than joining them with a dash.
   Hyphens inside code, file names, CSS class names and URLs are fine, they are syntax.
2. **Never invent content.** Every fact on this site comes from a brochure, a poster or a
   message from mumma. An earlier session invented category labels and prize amounts and
   got it badly wrong. If a fact is missing, ask. Do not fill the gap.
3. **Mumma's wording wins.** When she sends copy, use her words. If her wording creates a
   factual problem, for example the headline said "Two Ways to Join" after a third option
   was added, flag it and offer the fix. Do not silently rewrite her copy.
4. When a screenshot or markup is ambiguous, ask one focused question rather than guessing.
   Do the unambiguous parts first so the question is not blocking.

---

## 8. Brochures and the flipbook

### Grand Indian Art Contest brochure
13 A4 pages at `brochure/The-Grand-Indian-Art-Contest-2026-Brochure.pdf`, plus 13 JPGs at
`images/brochure/page-01.jpg` to `page-13.jpg` at 120 dpi that feed the flipbook.

**The HTML and CSS source for this PDF no longer exists.** It was built in a session
scratchpad that has since been cleared. The PDF keeps a full text layer, so the content can
be read back with PyMuPDF, but editing means rebuilding the layout. **If you ever rebuild
it, commit the source into this repo so this does not happen again.**

The original recipe, worth reusing:

```bash
# HTML with @page { size:A4; margin:0 } and mm units, one <section class="page"> per page
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=16000 \
  --print-to-pdf=raw.pdf brochure.html

python3 -c "
import fitz
d=fitz.open('raw.pdf'); d.save('slim.pdf', garbage=4, deflate=True, clean=True)
d2=fitz.open('slim.pdf')
for i in range(d2.page_count):
    d2[i].get_pixmap(dpi=120).save(f'page-{i+1:02d}.jpg', jpg_quality=78)"
```

QR codes were made with `segno`.

### Art Club brochure
A single tall page PDF that mumma produces herself. When she sends a new version, just
replace `brochure/KCA-International-Art-Club-Brochure.pdf` and update the page text to
match. **Always diff the new PDF against the live page**, she changes details quietly.
Extract its text with PyMuPDF and compare line by line.

### The flipbook
Hand built, no library. Lives at the bottom of `grand-indian-art-contest.html`.
7 leaves, each with a front and a back face, `backface-visibility:hidden`, and
`z-index = flipped ? i : n - i`. Two page spread above 980px, single page below.
Click either half to turn, arrow keys, swipe, fullscreen.

**When you replace any page image, bump the cache version** in the `src` builder in that
page's script, `?v=3` today. Otherwise visitors keep seeing the old page from cache.

---

## 9. How to verify your work

**This machine cannot preview localhost.** The sandbox blocks loopback, so
`preview_start` dev servers and `curl 127.0.0.1` both fail. Two things that do work:

**Local, before pushing.** Headless Chrome on a `file://` URL. Relative paths resolve, so
CSS and images load.

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --window-size=1440,11000 --virtual-time-budget=15000 \
  --allow-file-access-from-files --screenshot=out.png \
  "file:///path/to/kca-website/index.html"
```

Screenshots of **scrolled** content come out blank. To shoot a section lower down, make a
temporary copy of the page with the sections above it set to `display:none`, shoot that,
then delete the copy. Slice tall screenshots with PyMuPDF to read them.

**After pushing, always verify on the live site.** A green build is not proof. Wait for the
deploy, then assert on real bytes:

```bash
until curl -s https://kcaindia.com/ | grep -q "your new text"; do sleep 10; done
echo "LIVE $(date)"
```

Check the thing you changed **and** that the old wording is gone, count should be 0. For
PDFs, download and read the text layer back rather than trusting the file size.

Before every commit, check tag balance on any page you restructured:

```bash
python3 -c "
import re
s=open('index.html').read(); b=s[s.index('<body'):]
for t in ('div','section','a','ul','li','span','p','h1','h2'):
    o=len(re.findall(r'<%s[\s>]'%t,b)); c=len(re.findall(r'</%s>'%t,b))
    print(t,o,c,'OK' if o==c else 'MISMATCH')"
```

---

## 10. Traps, learned the hard way

1. **Never remove or toggle the Pages custom domain through the API.** Doing it once served
   a GitHub 404 to every visitor until it was re added, and GitHub silently deleted the
   `CNAME` file from the repo. Recovery was restoring `CNAME` on main and posting a build.
2. **`.nojekyll` must stay.** Without it Jekyll processes the site and fails with an opaque
   "Page build failed". The file is empty, that is correct.
3. **Deploys can wedge.** On 2 Jul 2026 every deploy sat in `deployment_queued` for exactly
   10 minutes then aborted. The build passed, the deploy timed out. It was not content and
   not a GitHub incident. The live site kept serving the last good version. It cleared on
   its own. Do not start deleting things.
4. **The kcaindia token has no `workflow` scope.** You cannot push anything under
   `.github/workflows/`. Keep `build_type` on `legacy`.
5. **Every GoDaddy DNS write sends an SMS code** to a phone ending 29850. Claude cannot
   enter it. Any DNS change needs the owner present.
6. **macOS can revoke Desktop folder access** and then every tool, including Bash with the
   sandbox disabled, gets `Operation not permitted` on the whole project. Fix is
   System Settings → Privacy & Security → Files and Folders → enable **Desktop Folder** for
   the app, then restart the session. This happened on 25 Aug 2026.
7. **Invisible characters break WhatsApp links.** Long URLs copied from some sources carry a
   zero width character, and WhatsApp then linkifies only half the URL so the tap goes
   nowhere and reads as "invalid link". The short links in section 5 exist for this reason.
   Tell people to share `kcaindia.com/contest`, not the long URL.
8. **Git identity can come back empty** after a session restart. If a commit fails with
   "Author identity unknown", restore it from history:
   `git config user.name "$(git log -1 --format='%an')"` and the same for `user.email`.
9. **Browsers keep style.css for 10 minutes** (GitHub sends max-age=600). If you add new CSS classes and the HTML that uses them, returning visitors see the new HTML unstyled until the cache expires. index.html and register.html link `style.css?v=20261110`; bump that value whenever you add CSS a page depends on.
10. **Homepage hero slide** (`.ks-hero`, 10 Nov 2026): poster mosaic background `images/hero/kca-hero-posters.jpg`, top line **DISCOVER THE ARTIST WITHIN YOU** (Yash's wording), gold strip button EXPLORE OUR COMPETITIONS, line NATIONAL ART COMPETITIONS SINCE 2008, stats row below. One slide, no arrows. Yash wants THIS banner; a colour rings hero was tried and rejected. CSS cache tag `style.css?v=20261110c`.

---

## 11. Watch list

| When | What |
|---|---|
| Done 10 Nov 2026 | Grand contest and Art Club registration closed until June 2027, Register chooser page added |
| 15 Nov 2026 | Artwork upload closes for the Grand contest |
| 15 Dec 2026 | Shortlist announced, all 10 categories |
| 30 Dec 2026 | Original artworks due from shortlisted participants |
| 15 Jan 2027 | Final results |
| 18 Jan 2027 | HTTPS cert renews, automatic, no action unless it fails |
| 30 Jan 2027 | Awards and digital certificates sent |
| June 2027 | All three registrations reopen: Rising Colours 17th edition, Grand contest, Art Club. Swap the locked buttons on register.html, index.html and each programme page back to forms |
| 27 Sep 2027 | Domain renewal at GoDaddy |

There is also one known inconsistency left alone on purpose: the Grand contest stat strip
says **50 top winners** per category, taken from mumma's poster, while the brochure says
**top 49**. She reviewed the brochure and said the rest was fine, so both stand. Do not
"fix" it without asking.

---

## 12. Working rhythm

Yash wants speed. When mumma sends a change:

1. Read what she actually sent. Open the PDF, extract the video frames, zoom the screenshot.
2. Diff it against what is live before editing. She often changes small details silently.
3. Do the unambiguous parts immediately. Ask at most one question about the rest.
4. Push, then verify on the live site and report with the real numbers.
5. Report what changed and what you deliberately did not touch.

Keep changes surgical. Every edited line should trace to something she asked for.
