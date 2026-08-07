#!/usr/bin/env python3
"""Build index.html from register.json.

The register on the front page is the twelve entries of not-evidence, with the
verdict each one earned. It is generated rather than typed so this site cannot
claim something the catalogue does not — the same reason the catalogue derives
its own counts instead of asserting them.

    python3 build.py            # write index.html
    python3 build.py --check    # fail if index.html is not current

Refresh register.json from the catalogue with:
    (cd ../not-evidence && python3 - <<'EOF' ... )   # see README
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "register.json"
OUT = HERE / "index.html"

VERDICT = {
    "central-claim-failed": ("failed", "did not hold"),
    "narrowed": ("narrowed", "held, narrowed"),
    "confirmed": ("confirmed", "held"),
}


def strip_md(text: str) -> str:
    """RESULTS prose carries markdown emphasis and code ticks. Keep the code
    ticks as real markup — those are the measured figures, and they should not
    read as prose."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    parts, out = re.split(r"`([^`]+)`", text), []
    for i, part in enumerate(parts):
        out.append(f"<b>{html.escape(part)}</b>" if i % 2 else html.escape(part))
    return "".join(out)


def register_rows(rows: list[dict]) -> str:
    out = []
    for i, r in enumerate(rows):
        cls, verdict = VERDICT[r["adj"]]
        out.append(f"""
      <details class="row row--{cls}" style="--i:{i}">
        <summary>
          <span class="row__n">{html.escape(r['n'])}</span>
          <span class="row__name">{html.escape(r['name'])}</span>
          <span class="row__verdict"><i class="mark"></i>{verdict}</span>
        </summary>
        <div class="row__body">
          <p class="row__claim">Refuses {html.escape(r['refuses'])}.</p>
          <dl class="row__data">
            <dt>measured</dt><dd>{strip_md(r['measured'])}</dd>
            <dt>result</dt><dd>{strip_md(r['result'])}</dd>
          </dl>
          <a class="row__link"
             href="https://github.com/jon-lange/not-evidence/blob/main/specimens/{r['spec']}/RESULTS.md">
            the working &rarr;</a>
        </div>
      </details>""")
    return "".join(out)


FT = "https://github.com/jon-lange/field-tested/tree/main/training"

DIMENSIONS = [
    ("Data inputs", None), ("Prompt engineering", None),
    ("Model selection", None), ("Workflow architecture", None),
    ("Evaluation pipelines", f"{FT}/01-evaluation"),
    ("Continuous monitoring", f"{FT}/02-monitoring"),
]


def dimension_items() -> str:
    out = []
    for name, href in DIMENSIONS:
        if href:
            out.append(
                f'<li class="has-evidence">{html.escape(name)}'
                f'<a class="tag" href="{href}">measured &middot; module &rarr;</a></li>')
        else:
            out.append(f"<li>{html.escape(name)}</li>")
    return "".join(out)


def build() -> str:
    rows = json.loads(DATA.read_text())
    counts = {v: sum(1 for r in rows if r["adj"] == k)
              for k, (v, _) in VERDICT.items()}
    revised = counts["failed"] + counts["narrowed"]
    return TEMPLATE.format(
        rows=register_rows(rows),
        total=len(rows),
        revised=revised,
        failed=counts["failed"],
        narrowed=counts["narrowed"],
        confirmed=counts["confirmed"],
        survived=counts["narrowed"] + counts["confirmed"],
        dimensions=dimension_items(),
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jon Lange — AI architecture, and the evidence for it</title>
<meta name="description" content="I publish claims about AI systems and then try to prove them wrong. Twelve claims, all twelve measured, seven survived — and the five that did not are why the seven are worth anything.">
<link rel="canonical" href="https://jon-lange.github.io/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23E7E9E3'/%3E%3Ccircle cx='16' cy='16' r='7' fill='%23A8321E'/%3E%3C/svg%3E">
<meta property="og:type" content="website">
<meta property="og:title" content="Jon Lange — AI architecture, and the evidence for it">
<meta property="og:description" content="I publish claims about AI systems and then try to prove them wrong. Twelve claims, all twelve measured, seven survived — and the five that did not are why the seven are worth anything.">
<meta property="og:url" content="https://jon-lange.github.io/">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:image" content="https://jon-lange.github.io/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="I publish claims, then try to prove them wrong. Twelve dots showing each entry's verdict: five failed, five narrowed, two confirmed.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&display=swap" rel="stylesheet">
<style>
/* Field register. Paper is a pale sage-grey, not cream; the accents are the
   three verdicts a claim can earn, so colour here is data rather than trim. */
:root {{
  --paper:#E7E9E3; --ink:#14171A; --rule:#C7CBC2; --muted:#6E7772;
  --failed:#A8321E; --narrowed:#B5761F; --confirmed:#2F6F5E;
  --measure:34rem;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --paper:#14171A; --ink:#E4E7E0; --rule:#2E332F; --muted:#8B948C;
    --failed:#E4795F; --narrowed:#DFA84B; --confirmed:#5FA98F;
  }}
}}
*,*::before,*::after {{ box-sizing:border-box; }}
html {{ -webkit-text-size-adjust:100%; }}
body {{
  margin:0; background:var(--paper); color:var(--ink);
  font:300 1.0625rem/1.65 Newsreader, Georgia, serif;
  font-synthesis-weight:none;
}}
.wrap {{ width:min(72rem, 100% - 2.5rem); margin-inline:auto; }}
a {{ color:inherit; }}
:focus-visible {{ outline:2px solid var(--failed); outline-offset:3px; }}

/* label = the utility voice: mono, tracked, small caps energy */
.label {{
  font:500 .6875rem/1 "IBM Plex Mono", ui-monospace, monospace;
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted);
}}

/* ---------- masthead ---------- */
.masthead {{
  display:flex; justify-content:space-between; align-items:baseline; gap:1.5rem;
  padding:1.75rem 0 1.25rem; flex-wrap:wrap;
}}
.masthead__name {{
  font:600 1.0625rem/1 Archivo, system-ui, sans-serif;
  letter-spacing:-.01em; text-decoration:none;
}}
/* Wraps. Adding two nav items pushed this 43px past a 390px viewport and gave
   the whole page a horizontal scrollbar — the one layout failure that is never
   acceptable. */
.masthead nav {{ display:flex; gap:1.5rem; flex-wrap:wrap; row-gap:.5rem; }}
@media (max-width:30rem) {{ .masthead nav {{ gap:1rem; row-gap:.5rem; }} }}
.masthead nav a {{ text-decoration:none; }}
.masthead nav a:hover {{ color:var(--ink); }}

/* ---------- hero ---------- */
.hero {{ padding:clamp(3rem,11vw,7.5rem) 0 clamp(2.5rem,6vw,4rem); }}
.hero__thesis {{
  font:600 clamp(2.1rem,6.2vw,4.25rem)/1.04 Archivo, system-ui, sans-serif;
  letter-spacing:-.032em; margin:0 0 1.75rem; max-width:20ch;
  font-stretch:105%;
}}
.hero__thesis em {{ font-style:normal; color:var(--failed); }}
.hero__sub {{ max-width:var(--measure); margin:0 0 2rem; font-size:1.1875rem; }}
.hero__meta {{ display:flex; gap:2rem; flex-wrap:wrap; align-items:baseline; }}

/* ---------- section scaffolding ---------- */
.section {{ padding-block:clamp(3rem,7vw,5rem); border-top:1px solid var(--rule); }}
.section__head {{
  display:flex; justify-content:space-between; align-items:baseline;
  gap:1rem; margin-bottom:2rem; flex-wrap:wrap;
}}
.section__title {{
  font:600 clamp(1.35rem,3vw,1.9rem)/1.1 Archivo, system-ui, sans-serif;
  letter-spacing:-.02em; margin:0;
}}
.section__note {{ max-width:var(--measure); color:var(--muted); margin:0; }}

/* ---------- the register: the signature ---------- */
/* A ledger only reads as one if the eye can get from the name to the verdict.
   Full-width rows on a large screen put 800px between them and the pairing
   breaks. */
.register {{ border-top:1px solid var(--rule); max-width:56rem; }}
.tally {{ max-width:56rem; }}
.row {{ border-bottom:1px solid var(--rule); }}
.row > summary {{
  display:grid; grid-template-columns:2.75rem 1fr auto; gap:1rem;
  align-items:baseline; padding:.95rem .25rem; cursor:pointer;
  list-style:none; transition:background .18s ease;
}}
.row > summary::-webkit-details-marker {{ display:none; }}
.row > summary:hover {{ background:color-mix(in srgb, var(--ink) 4%, transparent); }}
.row__n {{
  font:500 .8125rem/1.5 "IBM Plex Mono", monospace; color:var(--muted);
}}
.row__name {{
  font:500 1.0625rem/1.35 Archivo, system-ui, sans-serif; letter-spacing:-.011em;
}}
.row__verdict {{
  display:inline-flex; align-items:center; gap:.55rem; white-space:nowrap;
  font:400 .75rem/1 "IBM Plex Mono", monospace; letter-spacing:.06em;
  color:var(--muted);
}}
.mark {{ width:.5rem; height:.5rem; border-radius:50%; flex:none; }}
.row--failed    .mark {{ background:var(--failed); }}
.row--narrowed  .mark {{ background:var(--narrowed); }}
.row--confirmed .mark {{ background:transparent; box-shadow:inset 0 0 0 1.5px var(--confirmed); }}
/* the five that did not hold carry the weight */
.row--failed .row__name {{ font-weight:600; }}
.row--failed .row__verdict {{ color:var(--failed); }}

.row__body {{
  padding:.25rem .25rem 1.6rem 3.75rem; max-width:var(--measure);
}}
.row__claim {{ margin:0 0 1rem; }}
.row__data {{ margin:0 0 1rem; display:grid; grid-template-columns:auto 1fr; gap:.3rem 1rem; }}
.row__data dt {{
  font:500 .6875rem/1.7 "IBM Plex Mono", monospace; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted);
}}
.row__data dd {{ margin:0; font-size:.9875rem; }}
.row__data b {{ font:500 .875rem/1.6 "IBM Plex Mono", monospace; font-weight:500; }}
.row__link {{ font:500 .8125rem/1 Archivo, sans-serif; text-decoration:none; border-bottom:1px solid var(--rule); }}
.row__link:hover {{ border-color:currentColor; }}

.tally {{ display:flex; gap:1.75rem; flex-wrap:wrap; margin-top:1.75rem; }}
.tally div {{ display:flex; align-items:center; gap:.5rem; }}

/* ---------- dimensions ---------- */
.dims {{ list-style:none; margin:0; padding:0; max-width:44rem; }}
.dims li {{
  display:flex; justify-content:space-between; align-items:baseline; gap:1rem;
  padding:.7rem 0; border-bottom:1px solid var(--rule);
  font:400 1.0625rem/1.4 Archivo, system-ui, sans-serif; color:var(--muted);
}}
.dims .has-evidence {{ color:var(--ink); font-weight:500; }}
.tag {{
  font:500 .625rem/1 "IBM Plex Mono", monospace; letter-spacing:.11em;
  text-transform:uppercase; color:var(--confirmed); white-space:nowrap;
  text-decoration:none; border-bottom:1px solid transparent;
}}
a.tag:hover {{ border-bottom-color:currentColor; }}
.card code {{
  display:block; margin-top:.55rem; color:var(--ink);
  font-size:.6875rem; line-height:1.5;
  /* Break between path segments, never inside "jon-lange". */
  /* The break is placed by hand above; never split a name. */
  overflow-wrap:normal; word-break:keep-all;
}}

/* ---------- cards ---------- */
.cards {{ display:grid; gap:1.25rem; grid-template-columns:repeat(auto-fit,minmax(17rem,1fr)); }}
.card {{ border:1px solid var(--rule); padding:1.4rem; text-decoration:none; display:block; }}
.card:hover {{ border-color:var(--ink); }}
.card h3 {{
  font:600 1.0625rem/1.3 Archivo, sans-serif; margin:.6rem 0 .5rem; letter-spacing:-.01em;
}}
.card p {{ margin:0; font-size:.9375rem; color:var(--muted); }}
.card code {{ font:400 .8125rem/1 "IBM Plex Mono", monospace; }}

/* ---------- honest volume ---------- */
.stats {{ border-top:1px solid var(--rule); padding-block:2.25rem; }}
.stats dl {{
  margin:0; display:grid; gap:1.75rem 2.5rem;
  grid-template-columns:repeat(auto-fit,minmax(9rem,1fr));
}}
.stats dt {{
  font:500 .625rem/1.4 "IBM Plex Mono",monospace; letter-spacing:.13em;
  text-transform:uppercase; color:var(--muted);
}}
.stats dd {{
  margin:.3rem 0 0; font:600 2rem/1 Archivo,sans-serif; letter-spacing:-.03em;
}}
.stats dd span {{ font:400 .875rem/1 "IBM Plex Mono",monospace; color:var(--muted); }}

/* ---------- symptom router ---------- */
.triage {{ list-style:none; margin:0; padding:0; columns:2; column-gap:2.5rem; }}
.triage li {{ break-inside:avoid; margin:0 0 .1rem; }}
.triage a {{
  display:block; padding:.6rem 0; border-bottom:1px solid var(--rule);
  text-decoration:none; font-size:1.0125rem;
}}
.triage a:hover {{ color:var(--failed); }}
@media (max-width:44rem) {{ .triage {{ columns:1; }} }}

/* ---------- close ---------- */
.close {{ border-top:1px solid var(--rule); padding-block:clamp(3rem,7vw,5rem); }}
.close h2 {{
  font:600 clamp(1.5rem,3.4vw,2.25rem)/1.15 Archivo,sans-serif;
  letter-spacing:-.025em; margin:0 0 1.25rem; max-width:22ch;
}}

/* ---------- prose + footer ---------- */
.prose {{ max-width:var(--measure); }}
.prose p {{ margin:0 0 1.15rem; }}
.prose a {{ text-decoration-thickness:1px; text-underline-offset:.18em; }}
footer {{ border-top:1px solid var(--rule); padding:2.5rem 0 3.5rem; }}
footer .links {{ display:flex; gap:1.5rem; flex-wrap:wrap; margin-bottom:1.25rem; }}
footer a {{ font:500 .9375rem/1 Archivo, sans-serif; text-decoration:none; border-bottom:1px solid var(--rule); }}
footer a:hover {{ border-color:currentColor; }}
footer small {{ color:var(--muted); font-size:.8125rem; }}

/* ---------- one orchestrated moment: results arriving ---------- */
@media (prefers-reduced-motion: no-preference) {{
  .js .row {{ opacity:0; transform:translateY(6px); }}
  .js .row.in {{
    opacity:1; transform:none;
    transition:opacity .5s ease calc(var(--i) * 45ms), transform .5s ease calc(var(--i) * 45ms);
  }}
  .js .row .mark {{ transform:scale(0); }}
  .js .row.in .mark {{ transform:scale(1); transition:transform .32s cubic-bezier(.2,1.4,.4,1) calc(var(--i) * 45ms + 260ms); }}
}}
@media (max-width:34rem) {{
  .row > summary {{ grid-template-columns:2rem 1fr; row-gap:.3rem; }}
  .row__verdict {{ grid-column:2; }}
  .row__body {{ padding-left:2rem; }}
}}
</style>
</head>
<body>
<div class="wrap">

<header class="masthead">
  <a class="masthead__name" href="/">Jon Lange</a>
  <nav class="label">
    <a href="#register">register</a>
    <a href="#start">start here</a>
    <a href="#work">work</a>
    <a href="#learn">learn</a>
    <a href="#method">method</a>
    <a href="https://www.linkedin.com/in/jonathan-lange-ai-architect/">linkedin</a>
  </nav>
</header>

<main>
<section class="hero">
  <h1 class="hero__thesis">I publish claims about AI systems, then try to <em>prove them wrong</em>.</h1>
  <p class="hero__sub">
    I work on AI platforms for a living — evaluation, guardrails, and the half of
    the problem that is knowing when a system should decline. What I publish comes
    with the measurement that tested it, including the measurements that went
    against me.
  </p>
  <div class="hero__meta label">
    <span>AI architect</span>
    <span>Enterprise platforms · LLMOps · Evaluation</span>
  </div>
</section>

<section class="stats">
  <dl>
    <div><dt>patterns</dt><dd>12</dd></div>
    <div><dt>specimens</dt><dd>12</dd></div>
    <div><dt>models measured</dt><dd>11</dd></div>
    <div><dt>vendors</dt><dd>2</dd></div>
    <div><dt>citations verified</dt><dd>24</dd></div>
    <div><dt>claims that survived</dt><dd>7 <span>of 12</span></dd></div>
  </dl>
</section>

<section class="section" id="register">
  <div class="section__head">
    <h2 class="section__title">The register</h2>
    <span class="label">{total} claims · all measured · {survived} survived</span>
  </div>
  <p class="section__note">
    Every entry in <a href="https://github.com/jon-lange/not-evidence">not-evidence</a>
    was written as a claim, put in front of real models or a real adversary, and
    then rewritten to whatever came back. {survived} survived that; {failed} did not, and
    the {failed} are why the {survived} are worth anything. Open a row to see what was
    predicted and what happened.
  </p>

  <div class="register">{rows}
  </div>

  <div class="tally label">
    <div><i class="mark" style="background:var(--failed)"></i>{failed} did not hold</div>
    <div><i class="mark" style="background:var(--narrowed)"></i>{narrowed} held, narrowed</div>
    <div><i class="mark" style="box-shadow:inset 0 0 0 1.5px var(--confirmed)"></i>{confirmed} held</div>
  </div>
</section>

<section class="section" id="start">
  <div class="section__head">
    <h2 class="section__title">Start with what you recognise</h2>
    <span class="label">symptom &rarr; entry</span>
  </div>
  <ul class="triage">
    <li><a href="https://jon-lange.github.io/not-evidence/patterns/11-green-is-not-evidence.html">&ldquo;The suite is green and I can&rsquo;t say what that proves&rdquo;</a></li>
    <li><a href="https://jon-lange.github.io/not-evidence/patterns/05-judge-cannot-share-a-family.html">&ldquo;A model grades another model, and the score gates a release&rdquo;</a></li>
    <li><a href="https://jon-lange.github.io/not-evidence/patterns/09-modalities-off-the-reasoning-path.html">&ldquo;We shipped image upload and the injection suite didn&rsquo;t change&rdquo;</a></li>
    <li><a href="https://jon-lange.github.io/not-evidence/patterns/03-deterministic-over-prompted.html">&ldquo;Our defence is a prompt telling the model to ignore instructions&rdquo;</a></li>
    <li><a href="https://jon-lange.github.io/not-evidence/patterns/12-distrust-the-sanitization-label.html">&ldquo;Someone handed me a file marked <i>sanitised</i> and asked me to publish it&rdquo;</a></li>
    <li><a href="https://jon-lange.github.io/not-evidence/patterns/08-remembered-is-not-current.html">&ldquo;The agent quoted a figure it had seen earlier instead of fetching it&rdquo;</a></li>
    <li><a href="https://jon-lange.github.io/not-evidence/patterns/07-gate-over-refusal-separately.html">&ldquo;Quality went up and nobody measured what we started refusing&rdquo;</a></li>
    <li><a href="https://jon-lange.github.io/not-evidence/patterns/10-never-auto-commit-a-transducer.html">&ldquo;A transcript or extraction gets acted on automatically&rdquo;</a></li>
  </ul>
</section>

<section class="section" id="work">
  <div class="section__head">
    <h2 class="section__title">What I work on</h2>
    <span class="label">six dimensions · two with published evidence</span>
  </div>
  <p class="section__note">
    Context engineering, as the framework I use to separate production AI from an
    impressive demo. Two of the six have measurements I can show you.
  </p>
  <ul class="dims">{dimensions}</ul>
</section>

<section class="section" id="learn">
  <div class="section__head">
    <h2 class="section__title">Two things you can work through</h2>
    <span class="label">about an hour each &middot; no API key</span>
  </div>
  <p class="section__note">
    Each hands you something green that is lying, and asks you to find out how
    before showing you. Standard library, nothing to install.
  </p>
  <div class="cards">
    <a class="card" href="https://github.com/jon-lange/field-tested/tree/main/training/01-evaluation">
      <span class="label">01 &middot; evaluation pipelines</span>
      <h3>Is your eval suite telling the truth?</h3>
      <p>A release gate with three green checks: a test that passes with the code
      broken, a judge that scores everything the same, and a scorecard where
      <b>39.1% of 53,130 weightings</b> pick the other candidate.</p>
    </a>
    <a class="card" href="https://github.com/jon-lange/field-tested/tree/main/training/02-monitoring">
      <span class="label">02 &middot; continuous monitoring</span>
      <h3>Is your dashboard?</h3>
      <p>Three panels, three alerts, nothing firing. One alert queries a metric
      nothing emits. A segment worth 3% of traffic fails 29% of the time. Refusals
      went up 9&times; on no panel.</p>
    </a>
  </div>
  <p class="section__note" style="margin-top:1.5rem">
    Both live in <a href="https://github.com/jon-lange/field-tested">field-tested</a>,
    where every block declares how you know it works — <code>measured</code>,
    <code>tested</code>, <code>demo</code>, or <code>unproven</code>. A script
    enforces it, and <code>unproven</code> is the one that makes the rest honest.
  </p>
</section>

<section class="section">
  <div class="section__head">
    <h2 class="section__title">Take these</h2>
  </div>
  <div class="cards">
    <a class="card" href="https://github.com/jon-lange/not-evidence/blob/main/tools/mutcheck.py">
      <span class="label">one file · no dependencies</span>
      <h3>mutcheck.py</h3>
      <p>Proves an assertion would have failed before you trust that it passed.
      Run <code>python3 mutcheck.py --demo</code> and watch a green test prove nothing.</p>
    </a>
    <a class="card" href="https://github.com/jon-lange/not-evidence/blob/main/EVIDENCE.md">
      <span class="label">one page</span>
      <h3>Every figure, with its working</h3>
      <p>What was measured, what came back, and a link to the harness that
      produced it. No number appears that was not generated there.</p>
    </a>
    <a class="card" href="https://github.com/jon-lange/not-evidence/tree/main/skills">
      <span class="label">five checks &middot; installable</span>
      <h3>Evaluation skills</h3>
      <p>Judge independence, injection-class coverage, scorecard weight
      sensitivity, re-identification, test liveness. Each ships its measurement.<br>
      <code>/plugin marketplace add<br>jon-lange/not-evidence</code></p>
    </a>
    <a class="card" href="https://github.com/jon-lange/not-evidence/tree/main/okf">
      <span class="label">27 concepts</span>
      <h3>As an OKF bundle</h3>
      <p>The catalogue in the Open Knowledge Format, readable by agents without an
      SDK. Each specimen is an <code>Attested Computation</code> — a sanctioned way
      to compute a value so a consumer can confirm it.</p>
    </a>
  </div>
</section>

<section class="section" id="method">
  <div class="section__head">
    <h2 class="section__title">How I publish</h2>
  </div>
  <div class="prose">
    <p>
      Working in a regulated industry usually means publishing nothing. I wrote
      down the discipline that makes it possible instead — six rules, enforced by
      hooks and CI rather than by remembering, including the one that matters
      most: <strong>no number appears that was not generated here.</strong>
    </p>
    <p>
      It is written down because a method you can inspect is worth more than an
      assurance you have to take on faith.
      <a href="https://github.com/jon-lange/not-evidence/blob/main/METHOD.md">Read the method &rarr;</a>
    </p>
  </div>
</section>
</main>

<section class="close">
  <h2>The thing I most want is a result that contradicts one of these.</h2>
  <div class="prose">
    <p>
      Every specimen states what would falsify it. If you run one and it comes
      out differently, that gets the entry rewritten and you credited in it —
      not as a courtesy, but because a catalogue whose claims were only ever
      checked by their author is a catalogue of one person&rsquo;s confidence.
    </p>
    <p>
      <a href="https://github.com/jon-lange/not-evidence/issues/new/choose">Open an issue &rarr;</a>
      &nbsp;·&nbsp;
      <a href="https://www.linkedin.com/in/jonathan-lange-ai-architect/">Or say hello on LinkedIn &rarr;</a>
    </p>
  </div>
</section>

<footer>
  <div class="links">
    <a href="https://github.com/jon-lange">GitHub</a>
    <a href="https://www.linkedin.com/in/jonathan-lange-ai-architect/">LinkedIn</a>
    <a href="https://jon-lange.github.io/not-evidence/">not-evidence</a>
  </div>
  <small>
    Measured 2026-08-05. The register is generated from the catalogue, so this
    page cannot claim something it does not. Views are my own.
  </small>
</footer>

</div>
<script>
document.documentElement.classList.add('js');
const rows = document.querySelectorAll('.row');
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {{
  rows.forEach(r => r.classList.add('in'));
}} else {{
  const io = new IntersectionObserver((es) => {{
    es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
  }}, {{ rootMargin: '0px 0px -8% 0px' }});
  rows.forEach(r => io.observe(r));
}}
</script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    page = build()
    if args.check:
        if not OUT.is_file() or OUT.read_text() != page:
            print("BLOCKED - index.html is not current. Run: python3 build.py")
            return 1
        print("  index.html current")
        return 0
    OUT.write_text(page)
    print(f"  index.html written ({len(page):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
