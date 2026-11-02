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
<title>Jon Lange — All in on AI, mostly in fintech</title>
<meta name="description" content="While everyone argues doom vs. hype, I'm building. All in on AI, mostly in fintech. Personal projects: claims about AI systems I try to prove wrong, and Settleview — a research tool for BTC Up/Down markets with no edge after fees.">
<link rel="canonical" href="https://jon-lange.github.io/">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%2314171A'/><rect x='11.5' y='7' width='9' height='17' fill='%23E4795F'/></svg>">
<meta property="og:type" content="website">
<meta property="og:title" content="Jon Lange — All in on AI, mostly in fintech">
<meta property="og:description" content="While everyone argues doom vs. hype, I'm building. All in on AI, mostly in fintech. Personal projects: claims about AI systems I try to prove wrong, and Settleview — a research tool for BTC Up/Down markets with no edge after fees.">
<meta property="og:url" content="https://jon-lange.github.io/">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:image" content="https://jon-lange.github.io/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A terminal running python3 tools/mutcheck.py --demo. Three implementations of one redaction guard: CAUGHT, NOT CAUGHT, NOT CAUGHT. The assertion passed in all three.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
<script>
/* Motion is opt-in twice over: the reader has not asked for less of it, and
   the browser can tell us when a block scrolls into view. Without both, the
   class is never set and every rule that hides content never matches. */
if ('IntersectionObserver' in window && matchMedia('(prefers-reduced-motion: no-preference)').matches) document.documentElement.classList.add('anim');
</script>
<style>
/* A session transcript, not a shell impression.
   Monospace throughout, so hierarchy comes from weight, colour, size and space
   rather than from changing family. The three accents are the three verdicts a
   claim can earn — colour is data here, the same as everywhere else. The name
   gradient runs through all three, because the page is the record of them.
   Dark is the default because the terminal is; light follows the OS. */
:root {{
  color-scheme:dark;
  --bg:#07090B; --pane:#0D1013; --bar:#15191D; --ink:#E8EBE5; --muted:#9BA49D;
  --rule:#1F262A; --rule2:#2D363B;
  --failed:#FF7D62; --narrowed:#F4BE57; --confirmed:#62D3A8;
  --focus:#F4BE57; --glow:rgba(255,125,98,.28); --scan:rgba(255,255,255,.022);
  --vig:rgba(0,0,0,.28);
  --shadow:0 50px 110px -40px rgba(0,0,0,.9), 0 20px 44px -24px rgba(0,0,0,.7);
}}
@media (prefers-color-scheme: light) {{
  :root {{
    color-scheme:light;
    --bg:#E2E4DD; --pane:#FBFBF8; --bar:#EEEFEA; --ink:#14171A; --muted:#545C57;
    --rule:#E1E4DC; --rule2:#CFD3CA;
    --failed:#A0321B; --narrowed:#7A4E0D; --confirmed:#1A644F;
    --focus:#A0321B; --glow:rgba(174,56,32,.16); --scan:rgba(0,0,0,.016);
    --vig:rgba(0,0,0,.035);
    --shadow:0 46px 90px -40px rgba(30,36,30,.5), 0 14px 30px -18px rgba(30,36,30,.3);
  }}
}}
*,*::before,*::after {{ box-sizing:border-box; }}
html {{ -webkit-text-size-adjust:100%; }}
body {{
  margin:0; min-height:100vh; color:var(--ink); background-color:var(--bg);
  background-image:
    radial-gradient(55rem 38rem at 6% -10%, color-mix(in srgb, var(--failed) 17%, transparent), transparent 62%),
    radial-gradient(48rem 36rem at 104% 4%, color-mix(in srgb, var(--confirmed) 12%, transparent), transparent 60%),
    radial-gradient(64rem 32rem at 50% 110%, color-mix(in srgb, var(--narrowed) 9%, transparent), transparent 66%);
  background-attachment:fixed;
  font:400 14px/1.75 "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-variant-ligatures:none;
}}
/* a faint dot grid behind the window — the desk the terminal sits on */
body::before {{
  content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
  background-image:radial-gradient(color-mix(in srgb, var(--ink) 10%, transparent) 1px, transparent 1.3px);
  background-size:22px 22px;
  -webkit-mask-image:radial-gradient(ellipse 80% 70% at 50% 30%, #000 15%, transparent 75%);
          mask-image:radial-gradient(ellipse 80% 70% at 50% 30%, #000 15%, transparent 75%);
}}
@media (min-width:48rem) {{ body {{ font-size:14.5px; }} }}
a {{ color:inherit; }}
::selection {{ background:color-mix(in srgb, var(--failed) 35%, transparent); }}
:focus-visible {{ outline:2px solid var(--focus); outline-offset:3px; border-radius:6px; }}

/* the window */
.win {{
  position:relative; width:min(64rem, 100% - 2rem);
  margin:clamp(1rem,5vw,4rem) auto clamp(1.5rem,6vw,4.5rem);
  background:var(--pane); border-radius:14px;
  box-shadow:var(--shadow), 0 0 0 1px var(--rule2), 0 0 160px -50px var(--glow);
}}
.bar {{
  display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:.75rem;
  padding:.72rem 1rem; border-bottom:1px solid var(--rule); border-radius:14px 14px 0 0;
  background:linear-gradient(to bottom, color-mix(in srgb, var(--bar), #fff 3%), var(--bar));
}}
.dots {{ display:flex; gap:.5rem; }}
.dots i {{ width:.75rem; height:.75rem; border-radius:50%; flex:none; box-shadow:inset 0 0 0 .5px rgba(0,0,0,.3); }}
.dots i:nth-child(1) {{ background:#FF5F57; }}
.dots i:nth-child(2) {{ background:#FEBC2E; }}
.dots i:nth-child(3) {{ background:#28C840; }}
.bar .t {{
  color:var(--muted); font-size:.75rem; letter-spacing:.04em; text-align:center;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; min-width:0;
}}
.pane {{
  position:relative; border-radius:0 0 14px 14px;
  padding:clamp(1.5rem,4.5vw,3.25rem) clamp(1rem,4.8vw,3.5rem) clamp(2rem,5vw,3.25rem);
}}
/* CRT: scanlines and a vignette, both too faint to cost any contrast */
.pane::after {{
  content:""; position:absolute; inset:0; pointer-events:none; border-radius:inherit;
  background:
    repeating-linear-gradient(to bottom, var(--scan) 0 1px, transparent 1px 3px),
    radial-gradient(130% 90% at 50% 0%, transparent 55%, var(--vig));
}}

/* the banner */
.hero {{ padding-bottom:clamp(1.8rem,4vw,2.6rem); border-bottom:1px solid var(--rule); }}
.motd {{ margin:0 0 1.6rem; font-weight:700; line-height:1; }}
.nm {{
  position:relative; display:block; width:max-content; max-width:100%;
  font-size:clamp(2.7rem, 11vw, 6rem); letter-spacing:-.05em; padding:.04em 0 .1em;
  filter:drop-shadow(0 0 28px var(--glow));
}}
.nt {{ color:var(--ink); }}
@supports ((-webkit-background-clip:text) or (background-clip:text)) {{
  .nt {{
    background:linear-gradient(100deg, var(--failed) 8%, var(--narrowed) 50%, var(--confirmed) 92%);
    -webkit-background-clip:text; background-clip:text; color:transparent;
  }}
}}
@media (forced-colors: active) {{ .nt {{ background:none; color:CanvasText; }} }}
.tg {{ line-height:1.35;
  display:block; margin-top:.85rem; font-size:clamp(1rem,2.6vw,1.4rem);
  font-weight:500; letter-spacing:-.01em; color:var(--ink);
}}
.lead {{ font-size:clamp(1rem,1.9vw,1.14rem); line-height:1.65; }}

/* the transcript grammar */
.blk {{ margin-top:clamp(2.4rem,5vw,3.4rem); }}
/* baseline, not stretch: the cursor is a flex item, so vertical-align on it
   is ignored and it would otherwise hang from the top of the line box. */
.cmd {{
  margin:0 0 1rem; display:flex; gap:.65rem; flex-wrap:wrap; align-items:baseline;
  font-size:1.0625em; font-weight:400; line-height:1.75;
}}
.cmd .p {{ color:var(--failed); user-select:none; font-weight:700; text-shadow:0 0 16px var(--glow); }}
.cmd .k {{ position:relative; font-weight:600; color:var(--ink); }}
.cmd .dim {{ font-size:.88em; }}
.out {{ color:var(--muted); margin:0 0 .9rem; max-width:72ch; }}
.out strong {{ color:var(--ink); font-weight:600; }}
.out.ink {{ color:var(--ink); }}
.hi {{ color:var(--ink); font-weight:600; }}
.ok {{ color:var(--confirmed); }} .no {{ color:var(--failed); }} .wa {{ color:var(--narrowed); }}
.dim {{ color:var(--muted); }}

.lnk {{
  color:var(--ink); text-decoration:none; padding-bottom:1px;
  background:
    linear-gradient(var(--failed), var(--failed)) 0 100% / 0 1px no-repeat,
    linear-gradient(var(--rule2), var(--rule2)) 0 100% / 100% 1px no-repeat;
  transition:background-size .35s ease, color .2s;
}}
.lnk:hover {{ background-size:100% 1px, 100% 1px; }}
.btn {{
  display:inline-block; padding:.3rem .95rem; border-radius:999px; line-height:1.5;
  background:color-mix(in srgb, var(--ink) 4%, transparent);
  box-shadow:inset 0 0 0 1px var(--rule2);
  transition:box-shadow .25s, background .25s, color .25s, transform .25s;
}}
.btn:hover {{
  color:var(--failed); background:color-mix(in srgb, var(--failed) 9%, transparent);
  box-shadow:inset 0 0 0 1px color-mix(in srgb, var(--failed) 60%, transparent), 0 0 24px -6px var(--glow);
}}
.links {{ line-height:2.7; }}

/* the one project card */
.card {{
  position:relative; margin:0 0 .9rem; padding:1.3rem clamp(1rem,3vw,1.6rem) .5rem;
  border-radius:12px; max-width:76ch;
  background:linear-gradient(160deg, color-mix(in srgb, var(--failed) 7%, transparent), transparent 55%);
  box-shadow:inset 0 0 0 1px var(--rule2);
}}
.card::before {{
  content:""; position:absolute; left:1.2rem; right:1.2rem; top:-1px; height:1px;
  background:linear-gradient(90deg, transparent, var(--failed), transparent);
}}
.proj {{ font-size:1.0625rem; }}
.proj .lnk {{ font-weight:700; font-size:1.3em; letter-spacing:-.02em; }}

/* The output blocks carry fixed-width tables whose right-hand column is the
   whole point — CAUGHT vs NOT CAUGHT, the failure counts. Left at body size
   they run off a phone and the verdict is the part that disappears. Scaled to
   the viewport so the longest line fits, with horizontal scroll as a floor
   rather than the primary way to read it. */
pre {{
  margin:0 0 1rem; padding:1rem 1.2rem; overflow-x:auto; color:var(--muted);
  font-size:clamp(8.5px, 2.2vw, 14.5px); line-height:1.8;
  background:color-mix(in srgb, var(--ink) 3%, transparent);
  border-radius:10px; box-shadow:inset 0 0 0 1px var(--rule);
}}
@media (min-width:44rem) {{ pre {{ font-size:inherit; }} }}
/* the verdicts in a table become badges; the negative margin keeps the
   column they start in where the header says it is */
pre .ok, pre .no {{ font-weight:600; padding:.08em .45em; margin-left:-.45em; border-radius:4px; }}
pre .ok {{ color:var(--confirmed); background:color-mix(in srgb, var(--confirmed) 13%, transparent); }}
pre .no {{ color:var(--failed); background:color-mix(in srgb, var(--failed) 14%, transparent); }}

/* the register */
.row {{ --v:var(--muted); border-bottom:1px solid var(--rule); }}
.row--failed {{ --v:var(--failed); }}
.row--narrowed {{ --v:var(--narrowed); }}
.row--confirmed {{ --v:var(--confirmed); }}
.row:first-of-type {{ border-top:1px solid var(--rule); }}
.row > summary {{
  position:relative; display:grid; grid-template-columns:2.5rem minmax(0,1fr) auto .9rem;
  gap:.85rem; align-items:center; padding:.62rem .6rem; margin:2px 0;
  cursor:pointer; list-style:none; border-radius:8px; transition:background .2s;
}}
.row > summary::-webkit-details-marker {{ display:none; }}
.row > summary::before {{
  content:""; position:absolute; left:0; top:.55rem; bottom:.55rem; width:2px; border-radius:2px;
  background:var(--v); opacity:0; transition:opacity .2s;
}}
.row > summary::after {{
  content:""; justify-self:center; width:.42rem; height:.42rem; margin-top:-.2rem;
  border-right:1.5px solid var(--muted); border-bottom:1.5px solid var(--muted);
  transform:rotate(45deg); transition:transform .25s, border-color .2s;
}}
.row[open] > summary::after {{ transform:rotate(-135deg); margin-top:.2rem; }}
.row > summary:hover {{ background:color-mix(in srgb, var(--v) 7%, transparent); }}
.row > summary:hover::before, .row[open] > summary::before {{ opacity:1; }}
.row > summary:hover::after {{ border-color:var(--ink); }}
.c-n {{ color:var(--muted); font-variant-numeric:tabular-nums; }}
.c-name {{ font-weight:500; }}
.row--failed .c-name {{ font-weight:600; }}
.c-v {{
  display:inline-flex; align-items:center; gap:.45rem; white-space:nowrap;
  padding:.15rem .65rem .15rem .55rem; border-radius:999px; line-height:1.5;
  font-size:.75rem; font-weight:500; letter-spacing:.02em; color:var(--v);
  background:color-mix(in srgb, var(--v) 9%, transparent);
  box-shadow:inset 0 0 0 1px color-mix(in srgb, var(--v) 28%, transparent);
}}
.row--failed .c-v {{
  font-weight:600; background:color-mix(in srgb, var(--v) 14%, transparent);
  box-shadow:inset 0 0 0 1px color-mix(in srgb, var(--v) 45%, transparent);
}}
.mark {{ width:.45rem; height:.45rem; border-radius:50%; flex:none; background:var(--v); }}
.row--failed .mark {{ box-shadow:0 0 8px var(--v); }}
.row--confirmed .mark {{ background:transparent; box-shadow:inset 0 0 0 1.5px var(--v); }}
.row__body {{ padding:.35rem .6rem 1.35rem 3.95rem; max-width:80ch; }}
.kv {{ display:grid; grid-template-columns:5.5rem minmax(0,1fr); gap:.6rem; margin-bottom:.35rem; }}
.kv span:first-child {{ color:var(--muted); }}
.kv b {{
  font-weight:600; color:var(--ink); padding:0 .25em; border-radius:3px;
  background:color-mix(in srgb, var(--v) 12%, transparent);
}}
.row__body .lnk {{ display:inline-block; margin-top:.6rem; }}
.legend {{ margin-top:1.1rem; }}

/* listings */
.ls {{ list-style:none; margin:0 0 .9rem; padding:0; }}
.ls li {{ border-bottom:1px solid var(--rule); }}
.ls li:first-child {{ border-top:1px solid var(--rule); }}
.ls a {{
  display:grid; grid-template-columns:2.75rem minmax(0,1fr) minmax(0,1.15fr);
  gap:.85rem; padding:.7rem .6rem; margin:2px 0; text-decoration:none; align-items:baseline;
  border-radius:8px; transition:background .2s;
}}
.ls a:hover {{ background:color-mix(in srgb, var(--ink) 5%, transparent); }}
.ls .n {{ color:var(--muted); font-variant-numeric:tabular-nums; transition:color .2s; }}
.ls a:hover .n {{ color:var(--failed); }}
.ls .t {{ font-weight:500; }}
.ls .f {{ color:var(--muted); font-size:.8125rem; }}

.grep {{ list-style:none; margin:0 0 .9rem; padding:0; }}
.grep a {{
  display:flex; gap:.75rem; padding:.42rem .6rem; border-radius:8px;
  text-decoration:none; color:var(--muted); transition:color .2s, background .2s;
}}
.grep a:hover {{ color:var(--ink); background:color-mix(in srgb, var(--ink) 4%, transparent); }}
.grep b {{ color:var(--failed); font-weight:700; transition:transform .2s; }}
.grep a:hover b {{ transform:translateX(3px); }}

.dims {{ list-style:none; margin:0 0 .9rem; padding:0; }}
.dims li {{
  display:grid; grid-template-columns:1.75rem minmax(0,1fr) auto; gap:.75rem; align-items:center;
  padding:.4rem .6rem; color:var(--muted); border-bottom:1px dashed var(--rule);
}}
.dims li:last-child {{ border-bottom:0; }}
.dims .m {{ color:var(--ink); }}
.dims .m span:nth-child(2) {{ font-weight:500; }}
.dims a {{
  text-decoration:none; font-size:.75rem; line-height:1.5; padding:.12rem .65rem; border-radius:999px;
  box-shadow:inset 0 0 0 1px var(--rule2); transition:box-shadow .2s, background .2s;
}}
.dims a:hover {{ box-shadow:inset 0 0 0 1px currentColor; }}
.dims .m a {{
  color:var(--confirmed); background:color-mix(in srgb, var(--confirmed) 10%, transparent);
  box-shadow:inset 0 0 0 1px color-mix(in srgb, var(--confirmed) 35%, transparent);
}}
.dims .m a:hover {{ box-shadow:inset 0 0 0 1px currentColor; }}

.foot {{
  margin-top:2.6rem; padding-top:1.2rem; border-top:1px solid var(--rule);
  color:var(--muted); font-size:.8125rem; max-width:80ch;
}}
/* A flex item's baseline is its bottom margin edge, so this sits the block
   on the text baseline and grows upward, the way a terminal cursor does. */
.cursor {{ width:.6em; height:1.1em; background:var(--failed); box-shadow:0 0 14px var(--glow); }}

@media (max-width:40rem) {{
  .win {{ width:calc(100% - 1rem); margin:.5rem auto 1.5rem; border-radius:12px; }}
  .bar {{ grid-template-columns:auto minmax(0,1fr); border-radius:12px 12px 0 0; }}
  .bar .t {{ text-align:left; }}
  .pane {{ border-radius:0 0 12px 12px; }}
  pre {{ padding:.7rem .75rem; }}
  .row > summary {{ grid-template-columns:2rem minmax(0,1fr) .8rem; gap:.3rem .6rem; }}
  .c-v {{ grid-column:2; grid-row:2; justify-self:start; }}
  .row > summary::after {{ grid-column:3; grid-row:1 / span 2; }}
  .row__body {{ padding-left:3.2rem; }}
  .ls a {{ grid-template-columns:2rem minmax(0,1fr); row-gap:.15rem; }}
  .ls .f {{ grid-column:2; }}
  .kv {{ grid-template-columns:1fr; gap:0; }}
}}

/* Motion. Everything below is gated on the reader not asking for less, and
   everything that starts hidden is further gated on .anim, which only the
   script in <head> sets — with JS off, the page is simply all there. */
@media (prefers-reduced-motion: no-preference) {{
  .cursor {{ animation:blink 1.15s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity:0; }} }}
  .row[open] .row__body {{ animation:rise .35s ease both; }}
  @keyframes rise {{ from {{ opacity:0; transform:translateY(8px); }} }}
  @keyframes type {{
    from {{ clip-path:inset(-.3em 100% -.3em -.2em); }}
    to   {{ clip-path:inset(-.3em -.2em -.3em -.2em); }}
  }}
  @keyframes caret {{ to {{ left:100%; }} }}
  @keyframes gone {{ to {{ opacity:0; visibility:hidden; }} }}
  @keyframes winin {{ from {{ opacity:0; transform:translateY(22px) scale(.985); }} }}
  @keyframes risein {{ from {{ opacity:0; transform:translateY(12px); filter:blur(3px); }} }}

  .anim .win {{ animation:winin .9s cubic-bezier(.2,.7,.2,1) both; }}
  .anim .nt {{ animation:type .72s steps(9,end) .45s both; }}
  .anim .nm::after {{
    content:""; position:absolute; left:0; bottom:.16em; width:.42em; height:.8em; margin-left:.08em;
    background:var(--confirmed); box-shadow:0 0 18px var(--confirmed);
    animation:caret .72s steps(9,end) .45s both, blink 1.15s steps(1) 1.3s infinite;
  }}
  .anim .tg {{ animation:risein .7s cubic-bezier(.2,.7,.2,1) 1.2s both; }}
  .anim .hero > p {{ animation:risein .7s cubic-bezier(.2,.7,.2,1) both; }}
  .anim .hero > p:nth-of-type(1) {{ animation-delay:1.4s; }}
  .anim .hero > p:nth-of-type(2) {{ animation-delay:1.55s; }}
  .anim .hero > p:nth-of-type(3) {{ animation-delay:1.7s; }}

  /* each block: fade up, type the command, then print its output line by line */
  .anim .blk {{ --d:calc(260ms + var(--n, 0) * 38ms); transition:opacity .55s ease, transform .75s cubic-bezier(.2,.7,.2,1); }}
  .anim .blk:not(.in) {{ opacity:0; transform:translateY(18px); }}
  .anim .blk > :not(.cmd), .anim .blk .cmd .dim {{ opacity:0; transform:translateY(6px); }}
  .anim .blk.in > :not(.cmd) {{
    opacity:1; transform:none;
    transition:opacity .45s ease, transform .55s cubic-bezier(.2,.7,.2,1);
    transition-delay:calc(var(--d) + 120ms + var(--i, 0) * 55ms);
  }}
  .anim .blk.in .cmd .dim {{ opacity:1; transform:none; transition:opacity .4s ease var(--d), transform .4s ease var(--d); }}
  .anim .blk.in .kt {{ animation:type calc(var(--n) * 38ms) steps(var(--n), end) 260ms both; }}
  .anim .blk.in .k::after {{
    content:""; position:absolute; left:0; top:50%; width:.6em; height:1.1em; margin:-.58em 0 0 .1em;
    background:var(--failed);
    animation:caret calc(var(--n) * 38ms) steps(var(--n), end) 260ms both, gone 1ms linear calc(var(--d) + 380ms) forwards;
  }}
}}
@supports (animation-timeline: scroll()) {{
  @media (prefers-reduced-motion: no-preference) {{
    body::after {{
      content:""; position:fixed; left:0; right:0; top:0; height:2px; z-index:10; pointer-events:none;
      background:linear-gradient(90deg, var(--failed), var(--narrowed), var(--confirmed));
      transform-origin:0 50%; animation:progress linear both; animation-timeline:scroll(root);
    }}
    @keyframes progress {{ from {{ transform:scaleX(0); }} to {{ transform:scaleX(1); }} }}
  }}
}}
</style>
</head>
<body>
<div class="win">

<div class="bar">
  <span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>
  <span class="t">jon-lange@github — ~/building</span>
</div>

<div class="pane">
<main>

<header class="hero">
<h1 class="motd"><span class="nm"><span class="nt">Jon Lange</span></span> <span class="tg"><span class="dim">·</span> AI, mostly in fintech</span></h1>
<p class="out ink lead">While everyone argues doom vs. hype, I'm building. All in on AI, mostly in fintech.</p>
<p class="out">I also publish claims about AI systems, then try to <span class="no">prove them wrong</span>. Knowing when a system should decline is half the job.</p>
<p class="out">Everything below is a real command. The output is what it prints.</p>
</header>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">whoami --short</span></h2>
<p class="out">Building in public. Day job in fintech AI. Side projects below are personal — not my employer's.</p>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">cat ~/projects/settleview</span></h2>
<div class="card">
<p class="out ink proj"><a class="lnk" href="https://github.com/jon-lange/settleview">Settleview</a> <span class="dim">·</span> personal side project</p>
<p class="out">A local research tool and trading front end for short-window BTC Up/Down prediction markets (Kalshi and Polymarket US). You make every call; the app does not claim an edge.</p>
<p class="out">Our own research found no rule that beats the market price after fees. Settleview is a decision aid, not an edge. Not financial advice. Not affiliated with my employer.</p>
<p class="out links"><a class="lnk btn" href="https://github.com/jon-lange/settleview">open github.com/jon-lange/settleview</a></p>
</div>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">python3 tools/mutcheck.py --demo</span></h2>
<pre>  implementation                            mutation caught?
  ---------------------------------------   ----------------
  redaction works                           <span class="ok">CAUGHT</span>
  rollout flag off — nothing is logged      <span class="no">NOT CAUGHT</span>
  schema change — field no longer carried   <span class="no">NOT CAUGHT</span>

  The assertion passed in all three. Two were never watching.</pre>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">make check</span></h2>
<pre>  12 patterns
  12 adjudications
  <span class="hi">16 derived count claims</span>
  12 falsification conditions
  208 relative links
  <span class="ok">0 failure(s)</span></pre>
<p class="out">Every published count is derived from the twelve specimens. Rephrase a sentence
and the check fails rather than quietly stopping.</p>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">cat register.tsv</span> <span class="dim"># {total} claims · all measured · {survived} survived</span></h2>
<p class="out">Each was written as a claim, put in front of real models or a real adversary,
then rewritten to whatever came back. <span class="hi">{survived} survived that; {failed} did not</span>, and the {failed}
are why the {survived} are worth anything. Open a row for what was predicted and what happened.</p>
{rows}
<p class="out legend">
<span class="no">●</span> {failed} did not hold &nbsp;&nbsp;<span class="wa">●</span> {narrowed} held, narrowed &nbsp;&nbsp;<span class="ok">○</span> {confirmed} held</p>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">grep -rl "$SYMPTOM" patterns/</span></h2>
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
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">cat ~/context-engineering/dimensions</span></h2>
<ul class="dims">{dimensions}</ul>
<p class="out">Two came from specimens that ship their harness. Four are runnable demonstrations —
the failure is real, and nothing here measured how often it happens.</p>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">ls training/</span> <span class="dim"># 45–60 min each, no API key</span></h2>
<ol class="ls">{labs}</ol>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">ls tools/ skills/ okf/</span></h2>
<ul class="ls">
<li><a href="https://github.com/jon-lange/not-evidence/blob/main/tools/mutcheck.py"><span class="n">1</span><span class="t">tools/mutcheck.py</span><span class="f">one file, no dependencies — prove an assertion would have failed</span></a></li>
<li><a href="https://github.com/jon-lange/not-evidence/tree/main/skills"><span class="n">5</span><span class="t">skills/</span><span class="f">installable: /plugin marketplace add jon-lange/not-evidence</span></a></li>
<li><a href="https://github.com/jon-lange/not-evidence/tree/main/okf"><span class="n">27</span><span class="t">okf/</span><span class="f">the catalogue as an Open Knowledge Format bundle</span></a></li>
<li><a href="https://github.com/jon-lange/not-evidence/blob/main/EVIDENCE.md"><span class="n">1</span><span class="t">EVIDENCE.md</span><span class="f">every measured figure on one page, each linked to its working</span></a></li>
</ul>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">cat METHOD.md | head -6</span></h2>
<p class="out">Working in regulated fintech usually means publishing nothing. I wrote down the
discipline that makes personal research publishable instead — six rules, enforced by hooks and CI rather
than by remembering, including the one that matters most:
<span class="hi">no number appears that was not generated here.</span></p>
<p class="out links"><a class="lnk btn" href="https://github.com/jon-lange/not-evidence/blob/main/METHOD.md">open METHOD.md</a></p>
</section>

<section class="blk">
<h2 class="cmd"><span class="p">$</span><span class="k">contact --what-i-want</span></h2>
<p class="out ink">A result that contradicts one of the twelve. Or a sharp take on where AI in fintech is actually going.</p>
<p class="out">Every specimen states what would falsify it. Run one, get something different, and the
entry gets rewritten with you credited in it — not as a courtesy, but because a catalogue
whose claims were only ever checked by their author is a catalogue of one person's confidence.</p>
<p class="out links">
<a class="lnk btn" href="https://github.com/jon-lange/not-evidence/issues/new/choose">open an issue</a>
&nbsp; <a class="lnk btn" href="https://www.linkedin.com/in/jonathan-lange-ai-architect/">linkedin</a>
&nbsp; <a class="lnk btn" href="https://x.com/langej117">x</a>
&nbsp; <a class="lnk btn" href="https://github.com/jon-lange">github</a></p>
</section>

<div class="blk"><div class="cmd"><span class="p">$</span><span class="cursor" aria-hidden="true"></span></div></div>

</main>

<footer class="foot">
  Register measured 2026-08-05; generated from the catalogue, so this page cannot claim something it does not.
  Settleview and not-evidence are personal projects. Views are my own.
</footer>

</div>
</div>
<script>
/* Only runs when <head> opted in. Counts each command's characters so CSS can
   type it in that many steps, numbers the output lines for the stagger, and
   reveals each block the first time it scrolls into view. */
(function () {{
  var root = document.documentElement;
  if (!root.classList.contains('anim')) return;
  var blocks = document.querySelectorAll('.blk');
  Array.prototype.forEach.call(blocks, function (b) {{
    var k = b.querySelector('.k'), n = 0;
    if (k) {{
      n = k.textContent.length;
      var t = document.createElement('span');
      t.className = 'kt';
      while (k.firstChild) t.appendChild(k.firstChild);
      k.appendChild(t);
    }}
    b.style.setProperty('--n', n);
    var i = 0;
    Array.prototype.forEach.call(b.children, function (c) {{
      if (!c.classList.contains('cmd')) c.style.setProperty('--i', Math.min(i++, 14));
    }});
  }});
  var io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (e) {{
      if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }}
    }});
  }}, {{ rootMargin: '0px 0px -8% 0px' }});
  Array.prototype.forEach.call(blocks, function (b) {{ io.observe(b); }});
}})();
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
