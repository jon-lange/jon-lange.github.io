# Design system and motion provenance

The personal portfolio remains an editorial terminal with charcoal/lilac identity, light and dark themes, and an accessible skill-based navigation surface. It is an Impeccable Experience-mode design, not a simulated operating system.

LangSpan is shown through an authored illustrative sequence of its real mechanism (the hook refuses an overlapping edit; the agent chooses other work), labelled as an illustration, not a recording or a performance claim. The React demonstration uses the original Stageshow kit by Benji Taylor, pinned at commit 299140fafd08df55a9c234e610c3f64af3f45531, fetched during the reproducible build and compiled to static GitHub Pages assets. Source and installation instructions: https://github.com/benjitaylor/skills/tree/299140fafd08df55a9c234e610c3f64af3f45531/stageshow

The /about illustration is HTML in the page that applies the Living Canvas method: three labelled steps that pass the still-frame test, each highlighted once in turn, then all visible; no loop, and no motion under reduced motion. Skill source: https://github.com/shouvik12/living-canvas/blob/14a4a4f160d951d9745090a8c7f4822edd32bb18/SKILL.md

Impeccable critique, typography, motion and adaptive review guidance is anchored to https://github.com/pbakaus/impeccable/tree/9e460a87ef338ee9d12c7beed8fedc597a5af5f7. Preserve true product claims, approved marks, authored-example labels, browser Back, keyboard focus, the Lab's archival caveats, and the recorded Botbench imagery.

Build the pages with python3 build.py and validate with python3 build.py --check. Build the React Stageshow source with npm from motion-src after fetching the pinned kit into motion-src/kit. The GitHub Actions workflow fetches it, builds the static bundle, captures browser screenshots at desktop and mobile, runs an Impeccable detector pass, and commits validated distributable assets. Do not describe tests as passed until the workflow confirms them.

## Second-pass motion direction

Reviewed Jakub Krehel's [better-motion](https://github.com/jakubkrehel/skills/blob/672ae44ace6aaed65b86cbb1e2fd6fbea0e79578/skills/better-motion/SKILL.md) and [better-ui](https://github.com/jakubkrehel/skills/blob/672ae44ace6aaed65b86cbb1e2fd6fbea0e79578/skills/better-ui/SKILL.md). A command is navigation: the intentional typing cue is capped at 140 ms, current-route selection is immediate (the duck remains interactive), the cursor stops blinking, and output no longer wipes in behind a clip mask. The brand mark and product stills remain stationary. Theme changes suppress transitional color smearing. Product Stageshow playback remains independent. Do not claim a rendered review until the workflow passes; physical mobile Safari remains outside this check.

## Third pass: theme, honesty of mechanism, finite motion

Theme follows the OS and is remembered (`jl-theme`), set before first paint on every page; every colour in `cli.css` is a token with a light and dark value, and the scene uses the same tokens. Motion is finite: the About steps play once (about 3.7 s); the scene plays once when in view, has Pause/Play and Replay, and rests on its final frame (WCAG 2.2.2). The Stageshow bundle loads only with the LangSpan view. Navigation is links, with JavaScript as enhancement and `:target` routes without it.
