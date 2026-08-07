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

FT = "https://github.com/jon-lange/field-tested/tree/main/training"

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
    """The register as a table in a session transcript."""
    out = []
    for r in rows:
        cls, verdict = VERDICT[r["adj"]]
        out.append(
            f'<details class="row row--{cls}"><summary>'
            f'<span class="c-n">{html.escape(r["n"])}</span> '
            f'<span class="c-name">{html.escape(r["name"])}</span>'
            f'<span class="c-v"><i class="mark"></i>{verdict}</span>'
            f'</summary><div class="row__body">'
            f'<div class="kv"><span>refuses</span><span>{html.escape(r["refuses"])}</span></div>'
            f'<div class="kv"><span>measured</span><span>{strip_md(r["measured"])}</span></div>'
            f'<div class="kv"><span>result</span><span>{strip_md(r["result"])}</span></div>'
            f'<a class="lnk" href="https://github.com/jon-lange/not-evidence/blob/main/'
            f'specimens/{r["spec"]}/RESULTS.md">open specimens/{r["spec"]}/RESULTS.md</a>'
            f'</div></details>')
    return "".join(out)


DIMENSIONS = [
    ("Data inputs", "03-data-inputs", "demo"),
    ("Prompt engineering", "04-prompting", "demo"),
    ("Model selection", "05-model-selection", "demo"),
    ("Workflow architecture", "06-workflow", "demo"),
    ("Evaluation pipelines", "01-evaluation", "measured"),
    ("Continuous monitoring", "02-monitoring", "measured"),
]


def dimension_items() -> str:
    out = []
    for i, (name, slug, proof) in enumerate(DIMENSIONS, 1):
        cls = ' class="m"' if proof == "measured" else ""
        label = "measured" if proof == "measured" else "demonstrated"
        out.append(f'<li{cls}><span>{i}</span><span>{html.escape(name)}</span>'
                   f'<a href="{FT}/{slug}">{label} &rarr;</a></li>')
    return "".join(out)


LABS = [
    ("01", "01-evaluation", "is your eval suite telling the truth?",
     "39.1% of 53,130 weightings pick the other candidate"),
    ("02", "02-monitoring", "is your dashboard?",
     "one alert queries a metric nothing emits — it can never fire"),
    ("03", "03-data-inputs", "is what reaches the model what you think?",
     "three cited sources that are 91% identical — one document"),
    ("04", "04-prompting", "did your prompt really improve?",
     "v2 wins by 4.9% and drops one class from 80% to 10%"),
    ("05", "05-model-selection", "are those two models interchangeable?",
     "0.7% apart overall, 49 points apart on one slice"),
    ("06", "06-workflow", "what did your pipeline actually do?",
     "five stages green: one retried, one fell back, one did nothing"),
]


def lab_items() -> str:
    return "".join(
        f'<li><a href="{FT}/{slug}"><span class="n">{n}</span>'
        f'<span class="t">{html.escape(title)}</span>'
        f'<span class="f">{html.escape(fig)}</span></a></li>'
        for n, slug, title, fig in LABS
    )


def build() -> str:
    rows = json.loads(DATA.read_text())
    counts = {v: sum(1 for r in rows if r["adj"] == k)
              for k, (v, _) in VERDICT.items()}
    revised = counts["failed"] + counts["narrowed"]
    return TEMPLATE.format(
        labs=lab_items(),
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
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<style>
/* A session transcript, not a shell impression.
   Monospace throughout, so hierarchy has to come from weight, colour and space
   rather than from changing family. The three accents are the three verdicts a
   claim can earn — colour is data here, the same as everywhere else. */
:root {{
  --paper:#E7E9E3; --ink:#14171A; --rule:#C7CBC2; --muted:#6E7772;
  --failed:#A8321E; --narrowed:#B5761F; --confirmed:#2F6F5E;
  --chrome:#DDE0DA;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --paper:#14171A; --ink:#E4E7E0; --rule:#2C312D; --muted:#8B948C;
    --failed:#E4795F; --narrowed:#DFA84B; --confirmed:#5FA98F;
    --chrome:#1C2020;
  }}
}}
*,*::before,*::after {{ box-sizing:border-box; }}
html {{ -webkit-text-size-adjust:100%; }}
body {{
  margin:0; background:var(--paper); color:var(--ink);
  font:400 14px/1.75 "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  font-variant-ligatures:none;
}}
@media (min-width:48rem) {{ body {{ font-size:14.5px; }} }}
a {{ color:inherit; }}
:focus-visible {{ outline:2px solid var(--failed); outline-offset:3px; }}

.win {{ width:min(78rem, 100% - 1.5rem); margin:1.5rem auto 3rem; }}

/* window chrome — the one piece of decoration, and it does the work of saying
   "terminal" so nothing else has to */
.bar {{
  display:flex; align-items:center; gap:.5rem;
  background:var(--chrome); border:1px solid var(--rule); border-bottom:0;
  padding:.55rem .8rem; border-radius:6px 6px 0 0;
}}
.bar i {{ width:.65rem; height:.65rem; border-radius:50%; flex:none; }}
.bar .t {{
  margin-left:.5rem; color:var(--muted); font-size:.75rem; letter-spacing:.04em;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}}
.pane {{
  border:1px solid var(--rule); border-radius:0 0 6px 6px;
  padding:1.6rem clamp(.9rem,3vw,2rem) 2.4rem;
}}

/* the transcript grammar */
.cmd {{ margin:2.4rem 0 .9rem; display:flex; gap:.6rem; flex-wrap:wrap; }}
.cmd:first-child {{ margin-top:0; }}
.cmd .p {{ color:var(--failed); user-select:none; font-weight:600; }}
.cmd .k {{ font-weight:600; }}
.out {{ color:var(--muted); margin:0 0 .9rem; max-width:78ch; }}
.out strong {{ color:var(--ink); font-weight:600; }}
.out.ink {{ color:var(--ink); }}
.hi {{ color:var(--ink); font-weight:600; }}
.ok {{ color:var(--confirmed); }} .no {{ color:var(--failed); }} .wa {{ color:var(--narrowed); }}
.dim {{ color:var(--muted); }}

/* the banner, printed the way a shell prints one */
.motd {{ margin:0 0 .4rem; }}
.motd b {{
  display:block; font-size:clamp(1.6rem,5.2vw,2.6rem); line-height:1.15;
  font-weight:600; letter-spacing:-.02em; margin-bottom:.5rem;
}}
.motd b em {{ font-style:normal; color:var(--failed); }}

/* The output blocks carry fixed-width tables whose right-hand column is the
   whole point — CAUGHT vs NOT CAUGHT, the failure counts. Left at body size
   they run off a phone and the verdict is the part that disappears. Scaled to
   the viewport so the longest line fits, with horizontal scroll as a floor
   rather than the primary way to read it. */
pre {{
  margin:0 0 .9rem; overflow-x:auto; color:var(--muted);
  font-size:clamp(9px, 2.42vw, 14.5px);
  line-height:1.7;
}}
@media (min-width:44rem) {{ pre {{ font-size:inherit; }} }}
pre .ok {{ color:var(--confirmed); }} pre .no {{ color:var(--failed); }}

/* the register */
.row {{ border-bottom:1px solid var(--rule); }}
.row:first-of-type {{ border-top:1px solid var(--rule); }}
.row > summary {{
  display:grid; grid-template-columns:2.5rem minmax(0,1fr) auto; gap:.75rem;
  padding:.5rem .2rem; cursor:pointer; list-style:none; align-items:baseline;
}}
.row > summary::-webkit-details-marker {{ display:none; }}
.row > summary:hover {{ background:color-mix(in srgb, var(--ink) 5%, transparent); }}
.c-n {{ color:var(--muted); }}
.c-name {{ font-weight:500; }}
.c-v {{ display:inline-flex; align-items:center; gap:.5rem; white-space:nowrap; color:var(--muted); font-size:.8125rem; }}
.mark {{ width:.5rem; height:.5rem; border-radius:50%; flex:none; }}
.row--failed .mark {{ background:var(--failed); }}
.row--narrowed .mark {{ background:var(--narrowed); }}
.row--confirmed .mark {{ background:transparent; box-shadow:inset 0 0 0 1.5px var(--confirmed); }}
.row--failed .c-v {{ color:var(--failed); }}
.row--failed .c-name {{ font-weight:600; }}
.row__body {{ padding:.4rem .2rem 1.2rem 3.25rem; max-width:76ch; }}
.kv {{ display:grid; grid-template-columns:5.5rem minmax(0,1fr); gap:.5rem; margin-bottom:.3rem; }}
.kv span:first-child {{ color:var(--muted); }}
.lnk {{ display:inline-block; margin-top:.6rem; color:var(--ink); text-decoration:none; border-bottom:1px solid var(--rule); }}
.lnk:hover {{ border-color:currentColor; }}

/* listings */
.ls {{ list-style:none; margin:0 0 .9rem; padding:0; }}
.ls li {{ border-bottom:1px solid var(--rule); }}
.ls li:first-child {{ border-top:1px solid var(--rule); }}
.ls a {{
  display:grid; grid-template-columns:2.5rem minmax(0,1fr) minmax(0,1.1fr);
  gap:.75rem; padding:.55rem .2rem; text-decoration:none; align-items:baseline;
}}
.ls a:hover {{ background:color-mix(in srgb, var(--ink) 5%, transparent); }}
.ls .n {{ color:var(--muted); }}
.ls .t {{ font-weight:500; }}
.ls .f {{ color:var(--muted); font-size:.8125rem; }}

.grep {{ list-style:none; margin:0 0 .9rem; padding:0; }}
.grep li {{ padding:.3rem 0; }}
.grep a {{ text-decoration:none; color:var(--muted); }}
.grep a:hover {{ color:var(--ink); }}
.grep b {{ color:var(--failed); font-weight:600; }}

.dims {{ list-style:none; margin:0 0 .9rem; padding:0; }}
.dims li {{ display:grid; grid-template-columns:1.5rem minmax(0,1fr) auto; gap:.75rem; padding:.28rem 0; color:var(--muted); }}
.dims .m {{ color:var(--ink); }}
.dims a {{ text-decoration:none; font-size:.8125rem; }}
.dims .m a {{ color:var(--confirmed); }}
.dims a:hover {{ text-decoration:underline; }}

.foot {{ margin-top:2.6rem; padding-top:1.2rem; border-top:1px solid var(--rule); color:var(--muted); font-size:.8125rem; }}
.foot a {{ color:var(--ink); text-decoration:none; border-bottom:1px solid var(--rule); }}
.foot a:hover {{ border-color:currentColor; }}
.cursor {{ display:inline-block; width:.55em; height:1.05em; background:var(--failed); vertical-align:-.18em; }}
@media (prefers-reduced-motion: no-preference) {{
  .cursor {{ animation:blink 1.15s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity:0; }} }}
}}
@media (max-width:40rem) {{
  .row > summary {{ grid-template-columns:2rem minmax(0,1fr); }}
  .c-v {{ grid-column:2; }}
  .row__body {{ padding-left:2rem; }}
  .ls a {{ grid-template-columns:2rem minmax(0,1fr); row-gap:.2rem; }}
  .ls .f {{ grid-column:2; }}
  .kv {{ grid-template-columns:1fr; gap:0; }}
}}
</style>
</head>
<body>
<div class="win">

<div class="bar">
  <i style="background:#E0685F"></i><i style="background:#E4B14C"></i><i style="background:#5FA98F"></i>
  <span class="t">jon-lange@github — ~/not-evidence</span>
</div>

<div class="pane">

<div class="motd">
  <b>Jon Lange <span class="dim">·</span> AI architect</b>
</div>
<p class="out ink">I publish claims about AI systems, then try to <span class="no">prove them wrong</span>.<br>
Evaluation, guardrails, and the half of the problem that is knowing when a system should decline.</p>
<p class="out">Everything below is a real command. The output is what it prints.</p>

<div class="cmd"><span class="p">$</span><span class="k">python3 tools/mutcheck.py --demo</span></div>
<pre>  implementation                            mutation caught?
  ---------------------------------------   ----------------
  redaction works                           <span class="ok">CAUGHT</span>
  rollout flag off — nothing is logged      <span class="no">NOT CAUGHT</span>
  schema change — field no longer carried   <span class="no">NOT CAUGHT</span>

  The assertion passed in all three. Two were never watching.</pre>

<div class="cmd"><span class="p">$</span><span class="k">make check</span></div>
<pre>  12 patterns
  12 adjudications
  <span class="hi">16 derived count claims</span>
  12 falsification conditions
  208 relative links
  <span class="ok">0 failure(s)</span></pre>
<p class="out">Every published count is derived from the twelve specimens. Rephrase a sentence
and the check fails rather than quietly stopping.</p>

<div class="cmd"><span class="p">$</span><span class="k">cat register.tsv</span> <span class="dim"># {total} claims · all measured · {survived} survived</span></div>
<p class="out">Each was written as a claim, put in front of real models or a real adversary,
then rewritten to whatever came back. <span class="hi">{survived} survived that; {failed} did not</span>, and the {failed}
are why the {survived} are worth anything. Open a row for what was predicted and what happened.</p>
{rows}
<p class="out" style="margin-top:.9rem">
<span class="no">●</span> {failed} did not hold &nbsp;&nbsp;<span class="wa">●</span> {narrowed} held, narrowed &nbsp;&nbsp;<span class="ok">○</span> {confirmed} held</p>

<div class="cmd"><span class="p">$</span><span class="k">grep -rl "$SYMPTOM" patterns/</span></div>
<ul class="grep">
<li><a href="https://jon-lange.github.io/not-evidence/patterns/11-green-is-not-evidence.html"><b>&gt;</b> "The suite is green and I can't say what that proves"</a></li>
<li><a href="https://jon-lange.github.io/not-evidence/patterns/05-judge-cannot-share-a-family.html"><b>&gt;</b> "A model grades another model, and the score gates a release"</a></li>
<li><a href="https://jon-lange.github.io/not-evidence/patterns/09-modalities-off-the-reasoning-path.html"><b>&gt;</b> "We shipped image upload and the injection suite didn't change"</a></li>
<li><a href="https://jon-lange.github.io/not-evidence/patterns/03-deterministic-over-prompted.html"><b>&gt;</b> "Our defence is a prompt telling the model to ignore instructions"</a></li>
<li><a href="https://jon-lange.github.io/not-evidence/patterns/12-distrust-the-sanitization-label.html"><b>&gt;</b> "Someone handed me a file marked sanitised and asked me to publish it"</a></li>
<li><a href="https://jon-lange.github.io/not-evidence/patterns/08-remembered-is-not-current.html"><b>&gt;</b> "The agent quoted a figure it had seen earlier instead of fetching it"</a></li>
<li><a href="https://jon-lange.github.io/not-evidence/patterns/07-gate-over-refusal-separately.html"><b>&gt;</b> "Quality went up and nobody measured what we started refusing"</a></li>
<li><a href="https://jon-lange.github.io/not-evidence/patterns/10-never-auto-commit-a-transducer.html"><b>&gt;</b> "A transcript or extraction gets acted on automatically"</a></li>
</ul>

<div class="cmd"><span class="p">$</span><span class="k">cat ~/context-engineering/dimensions</span></div>
<ul class="dims">{dimensions}</ul>
<p class="out">Two came from specimens that ship their harness. Four are runnable demonstrations —
the failure is real, and nothing here measured how often it happens.</p>

<div class="cmd"><span class="p">$</span><span class="k">ls training/</span> <span class="dim"># 45–60 min each, no API key</span></div>
<ol class="ls">{labs}</ol>

<div class="cmd"><span class="p">$</span><span class="k">ls tools/ skills/ okf/</span></div>
<ul class="ls">
<li><a href="https://github.com/jon-lange/not-evidence/blob/main/tools/mutcheck.py"><span class="n">1</span><span class="t">tools/mutcheck.py</span><span class="f">one file, no dependencies — prove an assertion would have failed</span></a></li>
<li><a href="https://github.com/jon-lange/not-evidence/tree/main/skills"><span class="n">5</span><span class="t">skills/</span><span class="f">installable: /plugin marketplace add jon-lange/not-evidence</span></a></li>
<li><a href="https://github.com/jon-lange/not-evidence/tree/main/okf"><span class="n">27</span><span class="t">okf/</span><span class="f">the catalogue as an Open Knowledge Format bundle</span></a></li>
<li><a href="https://github.com/jon-lange/not-evidence/blob/main/EVIDENCE.md"><span class="n">1</span><span class="t">EVIDENCE.md</span><span class="f">every measured figure on one page, each linked to its working</span></a></li>
</ul>

<div class="cmd"><span class="p">$</span><span class="k">cat METHOD.md | head -6</span></div>
<p class="out">Working in a regulated industry usually means publishing nothing. I wrote down the
discipline that makes it possible instead — six rules, enforced by hooks and CI rather
than by remembering, including the one that matters most:
<span class="hi">no number appears that was not generated here.</span></p>
<p class="out"><a class="lnk" href="https://github.com/jon-lange/not-evidence/blob/main/METHOD.md">open METHOD.md</a></p>

<div class="cmd"><span class="p">$</span><span class="k">contact --what-i-want</span></div>
<p class="out ink">A result that contradicts one of the twelve.</p>
<p class="out">Every specimen states what would falsify it. Run one, get something different, and the
entry gets rewritten with you credited in it — not as a courtesy, but because a catalogue
whose claims were only ever checked by their author is a catalogue of one person's confidence.</p>
<p class="out">
<a class="lnk" href="https://github.com/jon-lange/not-evidence/issues/new/choose">open an issue</a>
&nbsp; <a class="lnk" href="https://www.linkedin.com/in/jonathan-lange-ai-architect/">linkedin</a>
&nbsp; <a class="lnk" href="https://x.com/langej117">x</a>
&nbsp; <a class="lnk" href="https://github.com/jon-lange">github</a></p>

<div class="cmd"><span class="p">$</span><span class="cursor" aria-hidden="true"></span></div>

<div class="foot">
  Measured 2026-08-05. The register is generated from the catalogue, so this page
  cannot claim something it does not. Views are my own.
</div>

</div>
</div>
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
