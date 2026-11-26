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
not a measured claim. LangSpan v0.1.0 is available for macOS and Linux; the
portfolio's local coordination walkthrough is an authored illustration.
Link to the [product story](https://langspan.dev/), [semantic example](https://langspan.dev/#why),
[parallel-work illustration](https://langspan.dev/#scale) and
[canonical positioning](https://github.com/Langspan/LangSpan.dev/blob/main/docs/positioning.md).

Botbench remains a supporting project. Its recorded tour
identifies it as an early, open-source macOS product. Its coordination example
was recorded with two installations on one Mac; the receiving owner chooses
how to handle an incoming question. The source-build guide is the next step.

The work view also links to Botbench’s design system. The lab’s five-day
feedback schedule is explicitly an illustration, not measured results.
Historical experiments remain separately dated and qualified. They are not
presented as validation of Botbench, prevalence data, or universal AI rules.

## Interaction and fallback behavior

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
  shareable route is `#langspan`. The About action and no-JavaScript fallback
  link directly to the product website when scripts are unavailable. The
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
- **Motion:** reduced-motion preferences disable the command animation and
  tour transitions. Focus indicators, semantic landmarks, and skip links
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

`assets/social-card.svg` is the editable code-native social-card source;
`assets/social-card.png` is the 1200 × 630 export used by Open Graph and Twitter.
`assets/favicon.svg` is the personal mark, retained for the homepage and archive.
The product tour uses `assets/botbench-favicon.svg`, copied unchanged from
[`botbenchhq/botbench:web/src/brand/favicon.svg`](https://github.com/botbenchhq/botbench/blob/ff02c33ad152ddfe113236e87ee10449b793ea6f/web/src/brand/favicon.svg)
(Git blob `8fc7019e6aa69342139eb1ed1ceda24cc851034d`). The Botbench tour retains
its Shared Seam mark. The About action uses LangSpan's approved icon instead.
Recorded screenshots remain unchanged.

Images, scripts, and stylesheets are
served locally. The terminal and tour request their web fonts from Google Fonts
and retain system-font fallbacks. The archive uses system fonts only. The old
`og.png` is no longer referenced.

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

The homepage keeps the interactive command palette and hash-backed skills. The LangSpan view includes an authored, clearly labelled React Stageshow scene compiled to static GitHub Pages JavaScript and CSS; it illustrates a second coding-agent session noticing overlapping file intent and redirecting independent work. The original illustrated workflow remains linked. The LangSpan stages are not a live product recording and make no collision-prevention guarantee.

- **Stageshow by Benji Taylor** — original kit, pinned to commit 299140fafd08df55a9c234e610c3f64af3f45531, loaded from its upstream source at CI build time. See [stageshow/](https://github.com/benjitaylor/skills/tree/299140fafd08df55a9c234e610c3f64af3f45531/stageshow).
- **Living Canvas** — the [accessible SVG story](assets/langspan-living-canvas.svg) follows the upstream [Living Canvas authoring skill](https://github.com/shouvik12/living-canvas/blob/14a4a4f160d951d9745090a8c7f4822edd32bb18/SKILL.md): the concrete conflict, shared signal, and independent progress, with animated focus and static reduced-motion path.
- **Impeccable** — design-mode decisions in [DESIGN.md](DESIGN.md), source critique and detector in CI; see [Impeccable](https://github.com/pbakaus/impeccable/tree/9e460a87ef338ee9d12c7beed8fedc597a5af5f7).

The [motion build workflow](.github/workflows/build-motion.yml) downloads and pins Stageshow, compiles into /assets/langspan-stage.{js,css}, builds the static HTML, checks generator parity, performs desktop/mobile browser interaction tests with Playwright, captures motion-sequence stills and reduced-motion screenshots as a CI artifact, and commits the distributable asset bundle only after browser validation. The original [check workflow](.github/workflows/check.yml) continues verifying the historical research archive and generated-pages invariants.

To build locally:

    git clone https://github.com/benjitaylor/skills.git /tmp/benji-skills
    git -C /tmp/benji-skills checkout 299140fafd08df55a9c234e610c3f64af3f45531
    cp -r /tmp/benji-skills/stageshow/kit motion-src/kit
    npm install --prefix motion-src
    npm run --prefix motion-src build
    python3 build.py && python3 build.py --check

**Important:** the React kit is source-bundled; do not add a runtime CDN dependency or silently replace its motion system with a CSS approximation.
