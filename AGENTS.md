# Personal homepage context

Read [README.md](README.md) for positioning, source files, build commands,
interaction behavior, asset provenance and the historical archive's scope.

## Design workflow

Use Impeccable for page and UI work alongside the site's established direction.
Use the installed `impeccable-product-pages` guidance or an available
`impeccable` skill. If neither is available, read the
[pinned upstream skill](https://github.com/pbakaus/impeccable/blob/b49177d32788f2dc585c42831d845dacf1ebed2c/.agents/skills/impeccable/SKILL.md)
and the relevant playbook in its `reference/` directory.
Use existing project context when optional tooling cannot run.

Treat the portfolio as an Experience surface: let the work lead while
keeping navigation easy to understand. Product explanations still need
clear context, factual claims and useful next actions.

For a substantial change, critique the view or interaction being changed,
then refine its layout, typography, copy or interaction. Use audit and adapt
checks for accessibility, performance and screen sizes. Finish with polish
and inspect the rendered result at desktop and narrow sizes. Scale the
review to the change and report only checks actually performed.

## Identity and content

Preserve the terminal concept, charcoal/lilac identity and available light theme.
Keep `/about` as the default personal front door and LangSpan as the flagship.
Use LangSpan's approved icon assets without redrawing them.
Retain the career context and other independent work.
Keep authored illustrations and historical experiments accurately qualified.
Use the README's positioning and provenance when updating product references.

## Source and delivery

Edit `template.html`, `cli.css` and `cli.js` for the homepage.
Generate `index.html` with `python3 build.py`; verify with `python3 build.py --check`.
Keep source and generated outputs together in the change.
`register.json` is historical research data, not the homepage's skill registry.
Preserve direct links, browser Back, keyboard use and no-JavaScript fallbacks.
Use the existing preview and pull-request workflow.
A design refinement follows the established identity and requested scope.
