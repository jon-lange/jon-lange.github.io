# jon-lange.github.io

Jon Lange’s personal portfolio, led by
[Botbench](https://botbenchhq.github.io/) as the flagship independent product.
One terminal is the front door: `/about` is already typed, and choosing a skill
retypes the command before showing its output. A recorded product tour and a
separate historical research archive provide the deeper paths.

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

Botbench leads with **“Put your coding agents to work. Together.”** The tour
identifies it as an early, open-source macOS product. Its coordination example
was recorded with two installations on one Mac; the receiving owner chooses
how to handle an incoming question. The source-build guide is the next step.

The work view also links to Botbench’s design system. The lab’s five-day
feedback schedule is explicitly an illustration, not measured results.
Historical experiments remain separately dated and qualified. They are not
presented as validation of Botbench, prevalence data, or universal AI rules.

## Interaction and fallback behavior

- **Skill picker:** click the pretyped command or use `/` or Command/Ctrl+K.
  The native dialog offers `/about`, `/work`, `/botbench`, `/writing`, `/lab`,
  `/contact`, and `/duck`; `/help` explains the paths. Search, Tab, and Enter
  work from the keyboard. Escape dismisses the picker and restores focus.
  On narrow screens, opening it does not immediately summon the soft keyboard.
- **Output:** commands erase and retype before their curated content appears.
  Direct hash links and browser history work. The terminal does not execute
  shell commands or call an AI model. About content and ordinary fallback
  links are present in the delivered HTML.
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

All five screenshots are unchanged copies of repository images. Their exact
Git blob identities and file SHA-256 hashes are recorded in
[`assets/provenance.json`](assets/provenance.json).

| Local image | Source repository path |
|---|---|
| `assets/botbench-workbench.png` | `botbenchhq/botbench:docs/images/hero-workbench.png` |
| `assets/botbench-review.png` | `botbenchhq/botbench:docs/images/ready-for-review-proof.png` |
| `assets/botbench-peers.png` | `botbenchhq/botbench:docs/images/paired-question.png` |
| `assets/permissions-check.png` | `botbenchhq/botbench:docs/images/permissions-check.png` |
| `assets/design-system-timeline.png` | `botbenchhq/design-system:test/visual/screenshots/run-timeline-1280-dark-botbench.png` |

Image fitting is controlled by CSS; the underlying image bytes are unchanged.
Product screenshots are contained in full, and the tour offers an enlarged
view. Screenshots contain example activity and are not customer testimonials
or portfolio performance metrics. The tour keeps a project’s recorded check
separate from a model’s review and explicitly labels the coordination setup.

`assets/social-card.svg` is the editable code-native social-card source;
`assets/social-card.png` is the 1200 × 630 export used by Open Graph and Twitter.
`assets/favicon.svg` is the personal mark. Images, scripts, and stylesheets are
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

