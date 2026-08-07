# jon-lange.github.io

Personal site. One page, no framework, no build step beyond a Python script and
no dependencies at runtime.

```bash
python3 build.py            # write index.html
python3 build.py --check    # fail if index.html is not current
```

## The register is generated, not written

The twelve rows on the front page are the entries of
[not-evidence](https://github.com/jon-lange/not-evidence) with the verdict each
one earned — `did not hold`, `held, narrowed`, or `held`. They come from
`register.json`, which is extracted from the catalogue rather than typed here.

That is deliberate. A page claiming "ten of twelve were revised by their own
evidence" should not be able to say that after it stops being true, and the
catalogue derives its own counts for the same reason. If the two ever disagree,
the catalogue is right.

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

## Design notes

Colour is data. The three accents are the three verdicts a claim can earn, so a
row's colour says what happened to it rather than decorating it — and the five
that did not hold are the loudest things on the page, which is the point.

Type carries the same split: claims are set in a serif, measurements in mono.
Prose argues; figures are measured. Keeping them visually distinct is the site's
whole argument in miniature.

Everything is one file. Fonts come from Google Fonts; nothing else is fetched.
