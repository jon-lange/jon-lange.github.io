import React, { useEffect, useRef, useState } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { Stage } from './kit/stage';
import type { Act } from './kit/act';
import './langspan.css';

// LangSpan's edit coordination, in four beats. The mechanism is the product's
// own: for supported tools in one checkout, the hook denies an edit that
// overlaps another session's hold (LangSpan.dev README, "Catch overlapping
// edits"). The refusal wording is quoted from a recorded Codex run
// (LangSpan.dev docs/evidence/codex-real-host, run 2d), shortened with "…".
// The files and the closing line match langspan.dev's own card.

type Scene = { step: number };
const initial: Scene = { step: 0 };
const poster: Scene = { step: 3 };
const LAST = 3;

const captions = [
  'Claude Code is editing src/auth/session.ts. LangSpan admits the edit and holds the file for that session.',
  'Codex tries to edit the same file. Its hook refuses the overlapping edit and says why.',
  'Codex chooses other work: tests/session.test.ts is a different file, so its edit is admitted.',
  'Claude Code keeps its edit; Codex writes tests in a different file. People review the combined result.'
];
const shortCaptions = ['Claude Code holds the file.', 'The hook refuses the overlapping edit.', 'Codex chooses a different file.', 'Both sessions keep working.'];

// A pausable wait: while paused, the script holds at the next 100 ms slice.
type Control = { paused: boolean };
async function hold(a: Act<Scene>, ctl: Control, ms: number) {
  let left = ms;
  while (left > 0 || ctl.paused) {
    await a.wait(100);
    if (!ctl.paused) left -= 100;
  }
}

function makeStory(ctl: Control, onStep: (n: number) => void) {
  return async function story(a: Act<Scene>) {
    onStep(0);
    a.mark('hold');
    await hold(a, ctl, 2200);
    await a.move('codex-edit', { duration: 450 });
    await a.click('codex-edit');
    await a.set({ step: 1 });
    onStep(1);
    a.mark('refused');
    await hold(a, ctl, 3400);
    await a.move('codex-choose', { duration: 450 });
    await a.click('codex-choose');
    await a.set({ step: 2 });
    onStep(2);
    a.mark('different-file');
    await hold(a, ctl, 2200);
    await a.set({ step: 3 });
    onStep(3);
    a.mark('both-continue');
  };
}

function Scenario({ step, layout }: Scene & { layout: string }) {
  const compact = layout === 'compact';
  const refused = step === 1;
  const moved = step >= 2;
  return (
    <div className="ls-scene" data-step={step} data-layout={layout} aria-hidden="true">
      <div className="ls-topline">
        <span className="ls-topword">LangSpan{!compact && <><span className="ls-topsep">/</span>one shared checkout</>}</span>
        <span className="ls-topstate">Illustration</span>
      </div>
      <div className="ls-columns">
        <section className="ls-agent ls-first">
          <div className="ls-agent-head"><span className="ls-agent-title"><i className="ls-dot ls-dot-a" />Claude Code</span><span className="ls-pill ls-pill-held is-on">Holds file</span></div>
          <div className="ls-path"><span>src/auth/session.ts</span></div>
          <div className="ls-body">
            <div className="ls-editor is-on">
              <div><em>41</em><span>export function refresh(s) {'{'}</span></div>
              <div className="ls-edited"><em>42</em><span>  s.expires = now() + TTL;</span></div>
              <div><em>43</em><span>  return save(s);</span></div>
              <div><em>44</em><span>{'}'}</span></div>
            </div>
          </div>
          <div className="ls-agent-foot"><span>Task</span><span>Update session refresh</span></div>
        </section>
        <section className="ls-agent ls-second">
          <div className="ls-agent-head">
            <span className="ls-agent-title"><i className="ls-dot ls-dot-b" />Codex</span>
            <span className="ls-swap">
              <span className={'ls-pill ls-pill-idle' + (step === 0 ? ' is-on' : '')}>Ready</span>
              <span className={'ls-pill ls-pill-refused' + (refused ? ' is-on' : '')}>Refused</span>
              <span className={'ls-pill ls-pill-ok' + (moved ? ' is-on' : '')}>Admitted</span>
            </span>
          </div>
          <div className="ls-path ls-path-swap">
            <span className={'ls-path-before' + (moved ? '' : ' is-on')} data-target="codex-edit">Edit src/auth/session.ts</span>
            <span className={'ls-path-after' + (moved ? ' is-on' : '')}>tests/session.test.ts</span>
          </div>
          <div className="ls-body">
            <div className={'ls-editor ls-plan' + (refused || moved ? '' : ' is-on')}>
              <div><em>›</em><span>Extend session coverage.</span></div>
              <div><em>›</em><span>Start with refresh().</span></div>
            </div>
            <div className={'ls-refusal' + (refused ? ' is-on' : '')}>
              <p className="ls-refusal-text">Command blocked by PreToolUse hook: LangSpan coordination conflict. … "src/auth/session.ts" held by session claude-code… Choose other work or retry this edit later.</p>
              <span className="ls-choice" data-target="codex-choose">Choose other work</span>
            </div>
            <div className={'ls-editor ls-test' + (moved ? ' is-on' : '')}>
              <div><em>01</em><span>{compact ? "test('refresh', () => {" : "test('refresh extends expiry', () => {"}</span></div>
              <div className="ls-added"><em>02</em><span>  const r = refresh(session);</span></div>
              <div className="ls-added"><em>03</em><span>{compact ? '  assert(r.expires > t);' : '  expect(r.expires).toBeGreaterThan(t);'}</span></div>
              <div><em>04</em><span>{'});'}</span></div>
            </div>
          </div>
          <div className="ls-agent-foot"><span>Task</span><span>Extend session coverage</span></div>
        </section>
      </div>
      <div className="ls-response">
        <span className={'ls-line' + (step === 0 ? ' is-on' : '')}>Two sessions in one checkout</span>
        <span className={'ls-line ls-line-warn' + (step === 1 ? ' is-on' : '')}>Overlap caught before the edit landed</span>
        <span className={'ls-line ls-line-ok' + (step >= 2 ? ' is-on' : '')}>Overlap caught. Separate work continues.</span>
      </div>
    </div>
  );
}

function Demonstration() {
  const ctl = useRef<Control>({ paused: false }).current;
  const [take, setTake] = useState(0);
  const [paused, setPaused] = useState(false);
  const [step, setStep] = useState(0);
  const [reduced, setReduced] = useState(() => window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  const [theme, setTheme] = useState(document.documentElement.dataset.theme === 'light' ? 'light' : 'dark');
  const story = useRef(makeStory(ctl, setStep));
  useEffect(() => {
    const observer = new MutationObserver(() => setTheme(document.documentElement.dataset.theme === 'light' ? 'light' : 'dark'));
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const onMotion = () => setReduced(mq.matches);
    mq.addEventListener('change', onMotion);
    return () => { observer.disconnect(); mq.removeEventListener('change', onMotion); };
  }, []);
  const shown = reduced ? LAST : step;
  const done = shown === LAST;
  const restart = () => { ctl.paused = false; setPaused(false); setStep(0); setTake((x) => x + 1); };
  const toggle = () => {
    if (done) { restart(); return; }
    ctl.paused = !ctl.paused;
    setPaused(ctl.paused);
  };
  return (
    <figure className="langspan-demo" data-stage-showcase data-paused={paused ? '' : undefined}>
      <div className="ls-stage-outer">
        <Stage<Scene>
          key={take}
          width={940}
          height={470}
          compact={{ below: 620, width: 324, height: 640 }}
          initial={initial}
          poster={poster}
          script={story.current}
          play="once"
          fill
          theme={theme as 'light' | 'dark'}
          accent={theme === 'light' ? '#6247b6' : '#c5b8ff'}
          cursor={{ at: { wide: { x: 860, y: 70 }, compact: { x: 296, y: 300 } }, style: 'real', ripple: true }}
        >
          {(state, _rect, layout) => <Scenario step={state.step} layout={layout} />}
        </Stage>
      </div>
      <figcaption className="ls-stage-footer">
        <div className="ls-stage-narration">
          <span className="ls-step-count">{reduced ? 'Final frame' : `Step ${shown + 1} of ${LAST + 1}`}</span>
          <strong>{shortCaptions[shown]}</strong>
          <span>{captions[shown]}</span>
        </div>
        {!reduced && (
          <div className="ls-demo-actions">
            <button type="button" onClick={toggle}>{done ? 'Replay' : paused ? 'Play' : 'Pause'}</button>
            {!done && <button type="button" onClick={restart}>Replay</button>}
          </div>
        )}
        <span className="ls-screenreader">The illustration, step by step: {captions.join(' ')}</span>
      </figcaption>
    </figure>
  );
}

const mounted = new Map<Element, Root>();
function reconcile() {
  for (const [host, root] of mounted) {
    if (!host.isConnected) { root.unmount(); mounted.delete(host); }
  }
  document.querySelectorAll('[data-langspan-stage]').forEach((host) => {
    if (mounted.has(host)) return;
    host.classList.add('is-mounted');
    const root = createRoot(host);
    mounted.set(host, root);
    root.render(<Demonstration />);
  });
}
function init() {
  const output = document.getElementById('result-output');
  if (output) new MutationObserver(reconcile).observe(output, { childList: true });
  reconcile();
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
else init();
