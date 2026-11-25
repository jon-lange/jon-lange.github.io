# Design system and motion provenance

The personal portfolio remains an editorial terminal with charcoal/lilac identity, light and dark themes, and an accessible skill-based navigation surface. It is an Impeccable Experience-mode design, not a simulated operating system.

LangSpan is shown through an authored illustrative sequence, not a real recording or product-performance claim. The React demonstration uses the original Stageshow kit by Benji Taylor, pinned at commit 299140fafd08df55a9c234e610c3f64af3f45531, fetched during the reproducible build and compiled to static GitHub Pages assets. Source and installation instructions: https://github.com/benjitaylor/skills/tree/299140fafd08df55a9c234e610c3f64af3f45531/stageshow

The separate SVG diagram applies the Living Canvas problem → transformation → result workflow, with meaningful focus motion and a static reduced-motion alternative. Skill source: https://github.com/shouvik12/living-canvas/blob/14a4a4f160d951d9745090a8c7f4822edd32bb18/SKILL.md

Impeccable critique, typography, motion and adaptive review guidance is anchored to https://github.com/pbakaus/impeccable/tree/9e460a87ef338ee9d12c7beed8fedc597a5af5f7. Preserve true product claims, approved marks, authored-example labels, browser Back, keyboard focus, the Lab's archival caveats, and the recorded Botbench imagery.

Build the pages with python3 build.py and validate with python3 build.py --check. Build the React Stageshow source with npm from motion-src after fetching the pinned kit into motion-src/kit. The GitHub Actions workflow fetches it, builds the static bundle, captures browser screenshots at desktop and mobile, runs an Impeccable detector pass, and commits validated distributable assets. Do not describe tests as passed until the workflow confirms them.
