# jon-lange.github.io

Jon Lange’s personal portfolio, led by
[LangSpan](https://langspan.dev/) as the flagship independent product.
One terminal is the front door: `/about` is already typed, and choosing a skill
retypes the command before showing its output. `/langspan` introduces the
current project. Botbench's recorded product tour and a separate historical
research archive remain available as supporting work.

## Build

Static HTML, CSS, and JavaScript with no framework or runtime package
dependencies. Python’s standard library generates the homepage and archive.

```bash
python3 build.py            # write index.html and archive.html
python3 build.py --check    # fail if either generated page is not current
```

Edit `template.html` for the homepage’s content, metadata, and skill templates;
`cli.css` and `cli.js` provide its presentation and interactions. The `$about`
placeholder is expanded from the `view-about` template so the initial output
is readable before JavaScript runs and the two copies cannot drift.

Edit `archive.template.html` and `archive.css` for the historical archive.
`build.py` escapes and renders every record from `register.json` into
`archive.html`. The register is not embedded in the homepage.

The five-stop product tour is maintained directly in `tour.html`, `tour.css`,
and `tour.js`. Commit source changes and both generated pages together.
GitHub Pages serves the committed files. CI checks both outputs, proves that
the drift check fails for each modified page independently, and retains the
twelve-record and verdict-vocabulary validation. It also rejects missing or
duplicated historical record identifiers.

## Positioning and scope

The personal promise is **“I build AI products and the systems that help teams
ship them.”** Career context is separate from the independent projects.

LangSpan leads with **“Run agents in parallel. Build as a team.”** Its brand
line remains **“Your agents. On the same page.”** The project is the open-source
coordination layer for parallel agentic development. Worktrees isolate files,
not intent; the product connects work through relevant briefings, supported
local edit checks, session-attributed commits and exact-tree integration
evidence. Opt-in Git metadata provides advisory awareness across machines.
Compatible parallel work with less repair and manual relay is a hypothesis,
not a measured claim. Link to the [product story](https://langspan.dev/),
[semantic example](https://langspan.dev/#why),
[parallel-work illustration](https://langspan.dev/#scale) and
[canonical positioning](https://github.com/Langspan/LangSpan.dev/blob/main/docs/positioning.md).
Version 0.1.0 is released for macOS and Linux, and the walkthrough is an
authored illustration of the product's real mechanism: for Claude Code and
Codex in one checkout, the hook refuses an edit that overlaps another session's
hold, and says why. Its refusal text is quoted from a recorded Codex run in
LangSpan's evidence. Adapters for Cursor, Gemini CLI and Antigravity are named
as unverified, as LangSpan's README does.

Botbench remains a supporting project, shown at 0.3.2: its real 25-second demo
recording (poster, controls, no autoplay), the four shipped team features
(issue claims, the overlap warning, checking two changes together, paired
questions) with their "early" caveat, and its own README card as a labelled
illustration. The recorded tour identifies it as an early, open-source macOS
product. Its coordination example was recorded with two installations on one
Mac.

The work view also links to Botbench’s design system. The lab’s five-day
feedback schedule is explicitly an illustration, not measured results.
Historical experiments remain separately dated and qualified. They are not
presented as validation of Botbench, prevalence data, or universal AI rules.

## Interaction and fallback behavior

- **Navigation:** the section bar is ordinary links (`#work`, `#langspan`, …),
  so they open in a new tab and can be copied; JavaScript intercepts a plain
  click to retype the command. Without JavaScript, `build.py` renders every
  view into a `<noscript>` block and each link shows its view by `:target`.
  On phones the bar keeps About, Work, LangSpan and Contact, with More for the
  rest.
- **Theme:** follows the operating system until the visitor chooses; the
  choice is stored in `localStorage` (`jl-theme`) and set before first paint
  on the homepage, the tour and the archive. Switching never animates colour.
- **Skill picker:** click the pretyped command or use `/` or Command/Ctrl+K.
  The native dialog offers `/about`, `/work`, `/langspan`, `/botbench`, `/writing`, `/lab`,
  `/contact`, and `/duck`; `/help` explains the paths. Search, Tab, and Enter
  work from the keyboard. Escape dismisses the picker and restores focus.
  On narrow screens, opening it does not immediately summon the soft keyboard.
- **Output:** commands erase and retype before their curated content appears.
  Direct hash links and browser history work. The terminal does not execute
  shell commands or call an AI model. About content and ordinary fallback
  links are present in the delivered HTML.
- **LangSpan:** the About action and first Work card open `/langspan`; the
  shareable route is `#langspan`. The Stageshow bundle
  (`assets/langspan-stage.{js,css}`) is loaded only when that view first opens;
  until then, and without JavaScript, LangSpan's own still card is shown. The
  generic `tour` alias opens LangSpan; `botbench tour` opens Botbench.
- **Product tour:** five stops use recorded screens to cover the task, boundaries, evidence,
  coordination, and source build. Chapter buttons and screen-detail controls
  work from the keyboard. Screens can be enlarged in a native modal dialog;
  Close and Escape dismiss it and return focus. Initial tour content and a
  concise no-JavaScript summary remain readable. Tour clicks do not run agents.
- **Lab:** a native range input adjusts an illustrative five-day schedule.
  A live result explains the first planned checkpoint. No network requests,
  stored data, or external actions are involved.
- **Archive:** every historical record uses native `details` and `summary`
  elements. It requires no JavaScript and links directly to the source results.
- **Motion:** two moments, both finite. On `/about` the three-step LangSpan
  illustration highlights each step once (about 3.7 s) and rests with all
  three visible. The LangSpan scene plays once when in view (about 9 s),
  pauses offscreen, has Pause/Play and Replay, and rests on its final frame.
  Beats use transform and opacity, 240 to 320 ms, `cubic-bezier(.2,0,0,1)`.
  Under reduced motion both show their final frame, and the command animation
  and tour transitions are off. Focus indicators, semantic landmarks, and skip links
  remain available throughout.

## Assets and provenance

All five Botbench/design-system screenshots are unchanged copies of repository images. Their exact
Git blob identities and file SHA-256 hashes are recorded in
[`assets/provenance.json`](assets/provenance.json).

LangSpan's two theme-specific icons and workflow illustration are also copied
unchanged from the public website, with source identities and hashes in the
same provenance file. The icons come from the supplied brand kit. The
illustration is labelled and is not a product screenshot. The current-build
action switches the approved icon with the homepage's light/dark theme.

| Local image | Source repository path |
|---|---|
| `assets/botbench-workbench.png` | `botbenchhq/botbench:docs/images/hero-workbench.png` |
| `assets/botbench-review.png` | `botbenchhq/botbench:docs/images/ready-for-review-proof.png` |
| `assets/botbench-peers.png` | `botbenchhq/botbench:docs/images/paired-question.png` |
| `assets/permissions-check.png` | `botbenchhq/botbench:docs/images/permissions-check.png` |
| `assets/design-system-timeline.png` | `botbenchhq/design-system:test/visual/screenshots/run-timeline-1280-dark-botbench.png` |

The four product screenshots use Botbench’s 0.3.0 interface and are pinned to
`botbenchhq/botbench` commit `32d41cdd4d99972e9119e6a55d8478c38c3c09ae`.
They show the billing-api example on studio-mac, with a paired office-mac
installation on the same Mac. The screens are captured from the product;
Claude Code’s build and Codex’s review are replayed from recorded tool sessions,
and the repository’s Python check really runs. Tour captions and hotspots refer
to those exact screens. The hero is 3200 × 1720; the three detail screens are
2880 × 1800.

The 1280 × 2387 design-system image is separate component-gallery evidence,
pinned to `botbenchhq/design-system` commit
`9457a46630f10c55a33682d80ee872e001a9a2a8`. It is not a product screenshot.

Image fitting is controlled by CSS; the underlying image bytes are unchanged.
Product screenshots are contained in full, and the tour offers an enlarged
view. Screenshots contain example activity and are not customer testimonials
or portfolio performance metrics. The tour keeps a project’s recorded check
separate from a model’s review and explicitly labels the coordination setup.

`assets/social-card.svg` is the editable code-native social-card source in the
site's charcoal and lilac with DM Sans and IBM Plex Mono;
`assets/social-card.png` is its 1200 × 630 export (rendered in Chromium with the
web fonts loaded), used by Open Graph and Twitter.

The Botbench demo recording and poster, Botbench's motionless README cards and
LangSpan's motionless product cards are unchanged copies; their sources,
commits, Git blob identities and SHA-256 hashes are in `assets/provenance.json`.
`assets/favicon.svg` is the personal mark, retained for the homepage and archive.
The product tour uses `assets/botbench-favicon.svg`, copied unchanged from
[`botbenchhq/botbench:web/src/brand/favicon.svg`](https://github.com/botbenchhq/botbench/blob/ff02c33ad152ddfe113236e87ee10449b793ea6f/web/src/brand/favicon.svg)
(Git blob `8fc7019e6aa69342139eb1ed1ceda24cc851034d`). The Botbench tour retains
its Shared Seam mark. The About action uses LangSpan's approved icon instead.
Recorded screenshots remain unchanged.

Images, scripts, and stylesheets are
served locally. The terminal and tour request their web fonts from Google Fonts
and retain system-font fallbacks. The archive uses system fonts only. 

## Historical archive

`archive.html` preserves the catalogue’s **August 5, 2026** experiments and
original outcomes. `register.json` remains the original catalogue snapshot.
Visible record titles
describe what was examined; each disclosure retains its original title,
verdict, measured setup, result, and link. Original categorical titles are not
used as new recommendations. There is no headline success/failure count.
The archive’s original qualifier is retained: cases are small and bounded,
some are deliberately constructed, and these records are not universal rules,
current-model benchmarks, or validation of Botbench. The former logging
illustration remains documented in [record 11’s methods and results](https://github.com/jon-lange/not-evidence/blob/main/specimens/11-mutation-check/RESULTS.md)
and [its standalone mutation helper](https://github.com/jon-lange/not-evidence/blob/main/tools/mutcheck.py).
It is not presented as a live homepage experiment.

Refresh the data from a checkout of the catalogue:

```bash
cd ../not-evidence && python3 - <<'EOF' > ../jon-lange.github.io/register.json
import re, json
from pathlib import Path
rows = []
for f in sorted(Path("patterns").glob("*.md")):
    _, block, _ = f.read_text().split("---", 2)
    m = {k.strip(): v.split("#")[0].strip().strip('"')
         for k, v in (l.split(":", 1) for l in block.strip().splitlines() if ":" in l)}
    results = (Path("specimens") / m["specimen"] / "RESULTS.md").read_text()
    adj = re.search(r"\*\*Adjudication:\s*([a-z-]+)\.\*\*", results).group(1)
    row = dict(n=m["pattern"], name=m["name"], refuses=m["refuses"],
               status=m["status"], adj=adj, slug=f.stem, spec=m["specimen"])
    for line in Path("EVIDENCE.md").read_text().splitlines():
        if line.startswith(f"| {row['n']} |"):
            c = [x.strip() for x in line.strip("|").split("|")]
            row["measured"], row["result"] = c[2], c[3]
    rows.append(row)
print(json.dumps(rows, indent=1))
EOF
cd ../jon-lange.github.io && python3 build.py
```

## Design and accessibility

Page and UI work uses [Impeccable](https://github.com/pbakaus/impeccable)
for design critique, focused refinement and final review.
[AGENTS.md](AGENTS.md) records that workflow alongside this portfolio's
existing identity, build process and product evidence.

The homepage is one restrained terminal, using charcoal surfaces and lilac
accents by default, with a light theme available. The archive shares that
palette and a simple route back to `/lab`. Skill outputs keep the flagship
product prominent without turning the landing page into a gallery of equal
claims.

When reviewing changes, exercise the skill picker, browser Back, direct skill
links, a narrow viewport, and reduced motion. Check the product tour’s chapters
and image dialog, and open an archive record with the keyboard and with
JavaScript disabled. Build drift is enforced by CI; visual and interaction
changes still need a focused browser review.



## Portfolio motion experience

The LangSpan view's scene is built with the original Stageshow React kit by
Benji Taylor, pinned to commit 299140fafd08df55a9c234e610c3f64af3f45531 and
fetched at build time ([stageshow/](https://github.com/benjitaylor/skills/tree/299140fafd08df55a9c234e610c3f64af3f45531/stageshow)).
It is labelled as an illustration: Claude Code holds `src/auth/session.ts`,
Codex's overlapping edit is refused by the hook with LangSpan's own wording,
Codex chooses `tests/session.test.ts`, and both continue. Its colours are the
site's tokens, so it follows the theme. Upstream defaults are overridden here:
no overshoot, beats at or under 450 ms, visible Pause/Play and Replay.

The `/about` illustration is plain HTML and CSS in the page, applying the
[Living Canvas](https://github.com/shouvik12/living-canvas/blob/14a4a4f160d951d9745090a8c7f4822edd32bb18/SKILL.md)
method (labelled stages that pass the still-frame test, each highlighted in
turn, every stage visible under reduced motion) without a loop.

The [motion build workflow](.github/workflows/build-motion.yml) fetches the kit,
compiles `assets/langspan-stage.{js,css}`, checks generator parity and runs
[`motion-src/visual-check.mjs`](motion-src/visual-check.mjs) on pull requests
and on `main`: every route at 1440, 390 and 358 in light and dark without
horizontal overflow, nav links and Back, the remembered theme, the lazy
bundle, Pause/Play/Replay, compact scene text of at least 12 px, reduced
motion, no-JavaScript routes, the tour and the archive.

To build locally:

    git clone https://github.com/benjitaylor/skills.git /tmp/benji-skills
    git -C /tmp/benji-skills checkout 299140fafd08df55a9c234e610c3f64af3f45531
    cp -r /tmp/benji-skills/stageshow/kit motion-src/kit
    npm install --prefix motion-src
    npm run --prefix motion-src build
    python3 build.py && python3 build.py --check
    python3 -m http.server 8123 --bind 127.0.0.1 &   # then:
    node motion-src/visual-check.mjs

**Important:** the React kit is source-bundled; do not add a runtime CDN dependency or silently replace its motion system with a CSS approximation.
