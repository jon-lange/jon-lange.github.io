(() => {
  'use strict';
  const steps = [
    {
      id: 'task', kicker: 'The task', title: 'Give the work a place.', label: 'Botbench / billing-api',
      image: 'assets/botbench-workbench.png', width: 3200, height: 1720,
      alt: 'Botbench Home groups work needing attention, waiting work, and completed work beside a phone-sized billing task ready for review.',
      caption: 'Recorded product screens from the billing-api example: Home on a Mac and a task review on a phone-sized screen.',
      next: 'Choose the boundaries',
      details: [
        { title: 'Know what needs you', text: 'Home separates work that needs your decision from waiting and completed work. The top item is a failed task that can be resumed; results below are ready to review.', x: 19.3, y: 32.6 },
        { title: 'Review on your phone', text: 'The phone shows a task to fix addition in calc.py, its branch, and a passing project check. The owner can inspect the result and choose Accept or Reject.', x: 79.8, y: 56.8 }
      ]
    },
    {
      id: 'boundaries', kicker: 'The boundaries', title: 'See the boundaries before the action.', label: 'Botbench / permissions',
      image: 'assets/permissions-check.png', width: 2880, height: 1800,
      alt: 'Botbench Settings, Permissions and autonomy: a command check for git push origin main in billing-api shows the result in three modes, with Activity below.',
      caption: 'This recorded command check runs nothing and changes nothing. It explains how the command would be treated.',
      next: 'Inspect the evidence',
      details: [
        { title: 'Ask about a command', text: 'In Permissions and autonomy, the owner checks how “git push origin main” would be handled for the billing-api repository.', x: 66.9, y: 29.8 },
        { title: 'Make the difference visible', text: 'The recorded result asks the owner in Manual and Semi-autonomous modes. Fully autonomous refuses this command because it would need approval.', x: 72.5, y: 51.2 }
      ]
    },
    {
      id: 'review', kicker: 'The evidence', title: 'Get close to what changed.', label: 'Botbench / ready for review',
      image: 'assets/botbench-review.png', width: 2880, height: 1800,
      alt: 'A billing task ready for review: one Python check passed, Codex’s model review, the calc.py diff, and the owner’s Accept or Reject decision.',
      caption: 'The recorded run shows one project check passing and a separate model review. Each has its own evidence.',
      next: 'See team coordination', branch: true,
      details: [
        { title: 'The project’s own check', text: 'Botbench ran “python3 -B -m unittest -q” on the task’s recorded commit. The screen shows one check passed and makes its output available.', x: 31.2, y: 49.8 },
        { title: 'A second opinion', text: 'The next section is Codex’s review, labeled as a model’s opinion. It records what Codex checked separately from the passing repository check.', x: 23.5, y: 63.0 }
      ]
    },
    {
      id: 'coordination', kicker: 'The conversation', title: 'Bring another workbench into it.', label: 'Botbench / a paired question',
      image: 'assets/botbench-peers.png', width: 2880, height: 1800,
      alt: 'Botbench Home shows a question from office-mac about billing-api, labeled outside text, with choices to answer yourself, give it to Claude Code, or dismiss it.',
      caption: 'Two Botbench installations on one Mac: office-mac asks studio-mac a question about billing-api.',
      next: 'Find your workbench',
      extra: 'The receiving owner stays in control. An incoming question does not run anything by itself.',
      details: [
        { title: 'A question with context', text: 'Office-mac asks whether the billing API still sends amounts in cents so its invoice change can match. The message is labeled outside text and identifies the sending workbench.', x: 22.0, y: 52.5 },
        { title: 'The owner chooses', text: 'Answer it yourself, give it to Claude Code, or dismiss it. The decision is made on the receiving workbench.', x: 55.7, y: 64.3 }
      ]
    },
    {
      id: 'build', kicker: 'Your workbench', title: 'Make room for your next idea.', finish: true,
      image: 'assets/botbench-workbench.png', width: 3200, height: 1720,
      alt: 'Botbench Home on a Mac beside a billing task ready for review on a phone-sized screen.',
      caption: 'Recorded Botbench screens from the billing-api example.', next: 'Explore again', details: []
    }
  ];

  const $ = (id) => document.getElementById(id);
  const chapters = [...document.querySelectorAll('.chapter')];
  const image = $('tour-image');
  const imageWrap = $('screen-image-wrap');
  const hotspots = $('hotspots');
  const switcher = $('detail-switcher');
  const dialog = $('screen-dialog');
  let current = 0;
  let detail = 0;
  let trail = [];
  let dialogReturnFocus = null;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function chooseDetail(index) {
    const points = steps[current].details;
    if (!points[index]) return;
    detail = index;
    $('detail-number').textContent = String(index + 1);
    $('detail-title').textContent = points[index].title;
    $('detail-copy').textContent = points[index].text;
    [...hotspots.children].forEach((button, i) => {
      button.classList.toggle('active', i === index);
      button.setAttribute('aria-pressed', String(i === index));
    });
    [...switcher.children].forEach((button, i) => {
      button.classList.toggle('active', i === index);
      button.setAttribute('aria-pressed', String(i === index));
    });
  }

  function renderDetails(step) {
    hotspots.replaceChildren();
    switcher.replaceChildren();
    step.details.forEach((point, index) => {
      const marker = document.createElement('button');
      marker.type = 'button';
      marker.className = 'hotspot';
      marker.textContent = String(index + 1);
      marker.style.left = `${point.x}%`;
      marker.style.top = `${point.y}%`;
      marker.setAttribute('aria-label', `Explore detail ${index + 1}: ${point.title}`);
      marker.setAttribute('aria-pressed', 'false');
      marker.addEventListener('click', () => chooseDetail(index));
      hotspots.append(marker);
      const selector = document.createElement('button');
      selector.type = 'button';
      selector.className = 'detail-dot';
      selector.textContent = String(index + 1);
      selector.setAttribute('aria-label', `Read detail ${index + 1}: ${point.title}`);
      selector.setAttribute('aria-pressed', 'false');
      selector.addEventListener('click', () => chooseDetail(index));
      switcher.append(selector);
    });
    chooseDetail(0);
  }

  function showStep(index, options = {}) {
    if (index < 0 || index >= steps.length) return;
    if (options.record !== false && index !== current) trail.push(current);
    current = index;
    detail = 0;
    const step = steps[index];
    $('step-kicker').textContent = step.kicker;
    $('step-title').textContent = step.title;
    $('screen-layout').hidden = Boolean(step.finish);
    $('finish-panel').hidden = !step.finish;
    $('enlarge-screen').hidden = Boolean(step.finish);
    $('branch-choice').hidden = !step.branch;
    $('chapter-extra').hidden = !step.extra;
    $('chapter-extra').textContent = step.extra || '';
    $('next-step').textContent = step.next;
    $('previous-step').disabled = trail.length === 0 && current === 0;
    $('progress-label').textContent = `Chapter ${index + 1} of ${steps.length}`;
    $('progress-fill').style.width = `${((index + 1) / steps.length) * 100}%`;
    $('tour-progress').setAttribute('aria-valuenow', String(index + 1));
    $('tour-progress').setAttribute('aria-valuetext', `Chapter ${index + 1} of ${steps.length}: ${step.kicker}`);
    chapters.forEach((button, i) => {
      button.classList.toggle('active', i === index);
      if (i === index) button.setAttribute('aria-current', 'step');
      else button.removeAttribute('aria-current');
    });
    if (!step.finish) {
      image.src = step.image;
      image.alt = step.alt;
      image.width = step.width;
      image.height = step.height;
      $('screen-label').textContent = step.label;
      $('screen-caption').textContent = step.caption;
      renderDetails(step);
      imageWrap.classList.remove('is-changing');
      if (!reducedMotion.matches) requestAnimationFrame(() => imageWrap.classList.add('is-changing'));
    }
    if (options.hash !== false) history.replaceState(null, '', `#${step.id}`);
    $('tour-announcer').textContent = `Chapter ${index + 1} of ${steps.length}. ${step.title}`;
    if (options.focus) {
      $('step-title').focus({ preventScroll: true });
      if (window.matchMedia('(max-width: 700px)').matches) {
        $('tour-stage').scrollIntoView({ behavior: reducedMotion.matches ? 'auto' : 'smooth', block: 'start' });
      }
    }
  }

  function restart() {
    trail = [];
    showStep(0, { record: false, focus: true });
  }

  function openScreen() {
    const step = steps[current];
    dialogReturnFocus = document.activeElement;
    $('dialog-image').src = step.image;
    $('dialog-image').alt = step.alt;
    $('dialog-title').textContent = step.finish ? 'The recorded workbench' : step.title;
    $('dialog-caption').textContent = step.caption;
    dialog.showModal();
    $('close-dialog').focus();
  }

  chapters.forEach((button, index) => {
    button.addEventListener('click', () => showStep(index, { focus: true }));
    button.addEventListener('keydown', (event) => {
      const directions = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 };
      if (event.key === 'Home' || event.key === 'End' || directions[event.key]) {
        event.preventDefault();
        const target = event.key === 'Home' ? 0 : event.key === 'End' ? chapters.length - 1 : (index + directions[event.key] + chapters.length) % chapters.length;
        chapters[target].focus();
      }
    });
  });
  $('next-step').addEventListener('click', () => current === steps.length - 1 ? restart() : showStep(current + 1, { focus: true }));
  $('previous-step').addEventListener('click', () => showStep(trail.length ? trail.pop() : Math.max(0, current - 1), { record: false, focus: true }));
  $('restart-tour').addEventListener('click', restart);
  $('skip-to-build').addEventListener('click', () => showStep(4, { focus: true }));
  $('enlarge-screen').addEventListener('click', openScreen);
  $('finish-enlarge').addEventListener('click', openScreen);
  $('close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => { if (dialogReturnFocus instanceof HTMLElement) dialogReturnFocus.focus({ preventScroll: true }); });
  window.addEventListener('hashchange', () => {
    const index = steps.findIndex((step) => `#${step.id}` === location.hash);
    if (index >= 0 && index !== current) showStep(index, { hash: false, focus: true });
  });
  const initial = steps.findIndex((step) => `#${step.id}` === location.hash);
  showStep(initial < 0 ? 0 : initial, { hash: false, record: false });
})();
