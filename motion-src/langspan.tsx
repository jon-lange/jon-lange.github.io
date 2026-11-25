import React, { useEffect, useState } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { Stage } from './kit/stage';
import type { Act } from './kit/act';
import './langspan.css';

type Scene = { step: number };
const initial: Scene = { step: 0 };
const poster: Scene = { step: 4 };
const captions = [
  'Claude Code is editing src/ledger.ts.',
  'Codex starts work on the same file.',
  'LangSpan shows the overlapping intent in shared context.',
  'Codex redirects to an independent test file.',
  'The team has a clearer picture to review together.'
];

async function story(a: Act<Scene>) {
  a.mark('editing');
  await a.wait(850);
  await a.click('codex-intent');
  await a.set({ step: 1 });
  a.mark('second-intent');
  await a.wait(1050);
  await a.set({ step: 2 });
  a.mark('overlap-signalled');
  await a.wait(1650);
  await a.click('codex-scope');
  await a.set({ step: 3 });
  a.mark('independent-work');
  await a.wait(1450);
  await a.set({ step: 4 });
  a.mark('review');
  await a.wait(2400);
}

function Scenario({ step }: Scene) {
  return (
    <div className="ls-scene" data-step={step} role="img" aria-label="Illustrated LangSpan scenario: Claude Code edits a ledger file; Codex sees an overlapping intent, moves to independent tests, and the work is ready for human review.">
      <div className="ls-topline"><span className="ls-topword">LangSpan <span className="ls-topsep">/</span> shared context</span><span className="ls-topstate"><i /> Scenario preview</span></div>
      <div className="ls-columns">
        <section className="ls-agent ls-first" aria-label="Claude Code session">
          <div className="ls-agent-head"><span className="ls-agent-title">Claude Code</span><span className="ls-agent-status"><span className="ls-status-dot" />Editing</span></div>
          <div className="ls-path">src/ledger.ts</div>
          <div className="ls-editor" aria-hidden="true">
            <div><em>18</em><span>export function reconcile(rows) {'{'}</span></div>
            <div><em>19</em><span className="ls-code-comment">  // match ledger entries</span></div>
            <div className="ls-edited"><em>20</em><span>  return rows.filter(match);</span></div>
            <div><em>21</em><span>{'}'}</span></div>
          </div>
          <div className="ls-agent-foot">Working tree <span>feature/reconciliation</span></div>
        </section>
        <div className="ls-connector" aria-hidden="true"><span /></div>
        <section className="ls-agent ls-second" aria-label="Codex session">
          <div className="ls-agent-head"><span className="ls-agent-title">Codex</span><span className="ls-agent-status ls-codex-status">{step === 0 ? 'Ready' : step < 3 ? 'Intent shared' : 'Continuing'}</span></div>
          <div className="ls-path" data-target="codex-intent"><span className="ls-path-before">src/ledger.ts</span><span className="ls-path-after">tests/ledger.test.ts</span></div>
          <div className="ls-editor ls-codex-editor" aria-hidden="true">
            <div><em>01</em><span>{step < 3 ? '// inspect matching logic' : 'import { reconcile }'}</span></div>
            <div><em>02</em><span>{step < 3 ? 'const target = "ledger";' : 'test("matches rows", () => {'}</span></div>
            <div className="ls-codex-change"><em>03</em><span>{step < 3 ? '// pending file intent' : '  expect(result).toBeDefined();'}</span></div>
            <div><em>04</em><span>{step < 3 ? '' : '});'}</span></div>
          </div>
          <div className="ls-agent-foot" data-target="codex-scope">Working tree <span>feature/ledger-tests</span></div>
        </section>
      </div>
      <div className="ls-response" aria-hidden="true">
        <span className="ls-response-signal">{step < 2 ? 'Watching relevant activity' : step === 2 ? 'Overlapping intent · src/ledger.ts' : step === 3 ? 'Separate file · work can continue' : 'Review the combined result'}</span>
        <span className="ls-response-outcome">{step === 2 ? 'Shared signal' : step === 4 ? 'Ready for review' : 'Shared context'}</span>
      </div>
      <div className="ls-bottomline"><span>Hooks · CLI · MCP</span><span>Authored illustration, not a live session</span></div>
    </div>
  );
}

function Demonstration() {
  const [take, setTake] = useState(0);
  const [outcome, setOutcome] = useState(false);
  const [theme, setTheme] = useState(document.documentElement.dataset.theme === 'light' ? 'light' : 'dark');
  useEffect(() => {
    const observer = new MutationObserver(() => setTheme(document.documentElement.dataset.theme === 'light' ? 'light' : 'dark'));
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => observer.disconnect();
  }, []);
  return (
    <div className="langspan-demo" data-stage-showcase>
      <div className="ls-stage-outer">
        <Stage<Scene>
          key={take + '-' + (outcome ? 'outcome' : 'play')}
          width={940}
          height={500}
          compact={{ below: 620, width: 358, height: 565 }}
          initial={outcome ? poster : initial}
          poster={poster}
          script={outcome ? undefined : story}
          play="once"
          theme={theme}
          accent="#bdb1ff"
          cursor={{ at: {wide: { x: 780, y: 110 },compact: { x: 310, y: 270 }}, style: 'real', ripple: true }}
        >
          {(state) => <Scenario step={state.step} />}
        </Stage>
      </div>
      <div className="ls-stage-footer">
        <div className="ls-stage-narration"><strong>One file. Two agent sessions.</strong><span>Watch shared intent surface, then choose independent work.</span></div>
        <div className="ls-demo-actions">
          <button type="button" onClick={() => { setOutcome(false); setTake((x) => x + 1); }}>Replay demonstration</button>
          <button type="button" aria-pressed={outcome} onClick={() => { setOutcome(true); setTake((x) => x + 1); }}>Show outcome</button>
        </div>
      </div>
      <p className="ls-screenreader">Story: {captions.join(' ')}</p>
    </div>
  );
}

const mounted = new Map<Element, Root>();
function reconcile() {
  for (const [host, root] of mounted) {
    if (!host.isConnected) { root.unmount(); mounted.delete(host); }
  }
  document.querySelectorAll('[data-langspan-stage]').forEach((host) => {
    if (mounted.has(host)) return;
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
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true});
else init();
