# jon-lange.github.io

Jon Lange’s personal portfolio, led by
[Botbench](https://botbenchhq.github.io/) as the flagship independent product.
The page shows real product screens, the design system behind them, one small
reproducible experiment, and current writing. Other work is deliberately kept
in a compact archive.

## Build

One static page with system fonts, local assets, and no framework or runtime
package dependencies. A small inline script progressively enhances the gallery,
image viewer, and constructed logging example.

```bash
python3 build.py            # write index.html
python3 build.py --check    # fail if index.html is not current
```

Edit `template.html` for content, metadata, layout, styles, and interactions.
`build.py` escapes and renders historical records from `register.json` into the
template. Commit the source changes and generated `index.html` together.
GitHub Pages serves the committed file. The existing check workflow continues
to reject generated-output drift and validate the archive’s row count and
verdict vocabulary.

## Positioning and scope

The personal promise is **“I build AI products and the systems that help teams
ship them.”** Career context is separate from the independent projects.

Botbench leads with **“Put your agents to work. Together.”** Engineering and
macOS are the current starting point. The peer-question image demonstrates
owner-approved interaction; the copy identifies more autonomous cross-developer
coordination as a direction that still requires development and validation.

The design system is described as draft, with Botbench as its current consumer.
The experiment is a small, constructed demonstration. None of the research is
presented as validation of Botbench, prevalence data, or universal AI rules.

## Interaction and fallback behavior

- **Product explorer:** three real image panels. Tabs support Left/Right, Home,
  and End, with roving tab focus and one selected panel. Without JavaScript,
  all panels are readable in document order.
- **Image viewer:** screenshot links progressively open a native modal dialog.
  The Close button and Escape dismiss it; focus returns to the originating link.
  Without native dialog support, the original image link still works.
- **Constructed example:** three radio choices and a reversible redaction toggle
  reproduce the published example’s six combinations. The outcome is calculated
  locally, with no model, request, stored data, or external action. A polite
  live region explains each result. Without JavaScript, a static explanation
  and source link remain available.
- **Archive:** native `details` elements retain access to historical records.
- Motion is limited to a short image fade and control color changes, enabled
  only when the reader has not requested reduced motion.

## Assets and provenance

All four screenshots are unchanged copies of repository images. Their exact
Git blob identities and file SHA-256 hashes are recorded in
[`assets/provenance.json`](assets/provenance.json).

| Local image | Source repository path |
|---|---|
| `assets/botbench-workbench.png` | `botbenchhq/botbench:docs/images/hero-workbench.png` |
| `assets/botbench-review.png` | `botbenchhq/botbench:docs/images/ready-for-review-proof.png` |
| `assets/botbench-peers.png` | `botbenchhq/botbench:docs/images/paired-question.png` |
| `assets/design-system-timeline.png` | `botbenchhq/design-system:test/visual/screenshots/run-timeline-1280-dark-botbench.png` |

The design-system image is cropped by CSS in the page and opens at full size;
the underlying image bytes are unchanged. Product images are contained in full.
Gallery screenshots contain example activity and are not customer testimonials
or portfolio performance metrics.

`assets/social-card.svg` is the editable code-native social-card source;
`assets/social-card.png` is the 1200 × 630 export used by Open Graph and Twitter.
`assets/favicon.svg` is the personal mark. All page assets are served locally.
The old `og.png` is no longer referenced.

## The constructed example

The interactive logging illustration is based on:

- [Specimen 11: methods, results, and scope](https://github.com/jon-lange/not-evidence/blob/main/specimens/11-mutation-check/RESULTS.md)
- [The standalone mutation helper and demonstration](https://github.com/jon-lange/not-evidence/blob/main/tools/mutcheck.py)

The same substring-absence assertion is used in every case. On the normal
logging path it passes with working redaction and fails with redaction replaced
by a no-op. With logging disabled or the secret field removed, it passes in both
states. Those latter cases are constructed coverage gaps, not live leaks. The
mutation is hand-chosen; this is not a mutation-testing framework or a measure
of how frequently the problem occurs.

## Historical archive

`register.json` remains the original catalogue snapshot. Visible record titles
describe what was examined; each disclosure retains its original title,
verdict, measured setup, result, and link. Original categorical titles are not
used as new recommendations. There is no headline success/failure count.
The archive is explicitly dated and distinguishes these bounded experiments
from current-model benchmarks.

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

The page uses an oversized editorial identity, full-width product imagery, and
different compositions for the product, design system, experiment, and writing.
Supporting projects are not a grid of equal product claims. Dark neutrals and
restrained cyan/blue accents keep the main product visually dominant.

Semantic landmarks, one main heading, visible focus, a skip link, native
controls, meaningful image alternatives, and responsive rules down to 360px are
included. The actual product images can be enlarged rather than requiring the
visitor to read small screenshot text. Use the gallery controls, image dialog, and each experiment path when reviewing
changes to the page.
