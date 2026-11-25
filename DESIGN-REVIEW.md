⚠️ DEGRADED: single-context (no sub-agent runner available in this session)

# Impeccable design critique — Jon Lange portfolio

Reviewed November 25, 2026 using Impeccable Experience mode guidance, its original critique rubric and craft floor. The review used source files, a real Playwright Chromium browser at 1440px, 390px and 358px, screenshots of each core page, six motion frames, and the Impeccable CLI detector. The dual-independent-subagent and live overlay modes were unavailable, so this is explicitly a single-context assessment, not a formal multi-agent Impeccable endorsement.

## Assessment A — design review

**Design specificity:** High. The CLI is an actual skill-based navigation system, not fake terminal ornament. The focal LangSpan demonstration explains a concrete overlap scenario, from active work to overlapping intent to a shared signal, independent work and review.

**Hierarchy and composition:** The homepage uses asymmetrical editorial typography and the charcoal/lilac system rather than gradients and animated decoration. LangSpan leads the project grid. The Stageshow demo appears before extended copy and the legacy illustrated workflow is accessible through a disclosure. Botbench retains recorded product screens, while the research archive retains historical methods and limitations.

**Responsiveness:** The phone homepage has a purpose-built vertical Living Canvas illustration rather than shrinking desktop text to illegibility. The 358px compact Stageshow layout stacks agent sessions and increases code legibility. A clearly labelled More route exposes secondary skills rather than hiding them off the right edge.

**Motion:** The authored Stageshow sequence changes meaningful state; six individually captured desktop frames show actual progression. Replay and Show outcome are user controls. Reduced-motion visitors see the final result immediately. SVG focus motion stops under prefers-reduced-motion.

**Cognitive load:** Primary mobile navigation shows four destinations and More. Long supporting material uses disclosures, chapters and named sections. The one remaining cost is the natural length of LangSpan's detailed project view; the demonstration now appears first.

## Ten Nielsen heuristic scores (subjective, 0–4)

| Heuristic | Score | Rationale |
| --- | ---: | --- |
| Status visibility | 3 | Active skill and scene status appear, with labelled outcome |
| Real-world match | 4 | Developer-specific CLI and work vocabulary |
| Control and freedom | 4 | Replay, Show outcome, back, tour stepping, disclosures |
| Consistency | 3 | Consistent type/color; recorded tour intentionally uses a lighter product world |
| Error prevention | n/a | No destructive portfolio interaction |
| Recognition | 4 | Visible commands, help index and project links |
| Efficiency | 4 | Keyboard skill picker, quick navigation and direct hashes |
| Aesthetic minimalism | 4 | One meaningful focal sequence, no decorative motion clutter |
| Error recovery | n/a | No form or mutation workflow |
| Help/documentation | 3 | Help view, captions, source links and archival details |

## Assessment B — detector and browser evidence

GitHub Actions invokes the actual Impeccable CLI on generated HTML markup (index.html, tour.html, archive.html), not CSS-only sources, and records the scan output. Browser validation covers desktop and phone home/work/Botbench views, LangSpan story, tour and archive, direct skill routes, compact mode, light theme, reduced motion, stage replay/outcome, and archive disclosure. All screenshots and the six scene frames are in the portfolio-visual-evidence workflow artifact. Existing Python generated-page checks pass.

The CLI source scan is not a guarantee of visual quality, browser compatibility or WCAG conformance. Screenshots were inspected directly; the live overlay and independent sub-agent critique were not available.

## Remaining watch items

- **P3:** Chromium tests do not replace hands-on VoiceOver, Safari, TalkBack and real-device review.
- **P3:** The Stageshow bundle is loaded with the homepage; route-based lazy loading is a future performance optimization.
- **P3:** Recorded Botbench screenshots contain inherently small text on phones. The enlarge control and hotspot explanations mitigate this; approved screenshots are not altered.
- **P3:** The authored LangSpan scenario is not live production footage. Its visible disclaimer must remain in place.

## Release disposition

**SHIP**, conditional on final CI and GitHub Pages publication. No P0 or P1 visual issues remain in the inspected browser matrix. Copyright notices from the original Stageshow are preserved separately under third_party/stageshow.

Questions skipped: user requested end-to-end completion, not an interactive critique checkpoint.
