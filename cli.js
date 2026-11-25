(function () {
  'use strict';

  function initialize() {
    var trigger = document.getElementById('skill-trigger');
    var activeSkill = document.getElementById('active-skill');
    var dialog = document.getElementById('skills-dialog');
    var closeButton = document.getElementById('skills-close');
    var search = document.getElementById('skill-search');
    var options = document.getElementById('skill-options');
    var resultScroll = document.getElementById('result-scroll');
    var result = document.getElementById('result-output');
    var status = document.getElementById('command-status');
    var themeButton = document.getElementById('theme-toggle');
    if (!trigger || !activeSkill || !dialog || !closeButton || !search || !options || !result || !status) return;

    var skills = [
      { command: '/about', view: 'about', title: 'About Jon', description: 'Meet the person behind the work', aliases: ['about', 'who is jon', 'who are you', 'whoami', 'hello', 'home', '/home'] },
      { command: '/work', view: 'work', title: 'Selected work', description: 'Explore products, systems, and experiments', aliases: ['work', 'what are you building', 'show me what youre building', 'show me your work', 'projects', 'ls'] },
      { command: '/langspan', view: 'langspan', title: 'LangSpan', description: 'Explore the flagship: your agents, on the same page', aliases: ['langspan', 'lang span', 'show me langspan', 'open langspan', 'try langspan', 'flagship', 'agent coordination', 'tour'] },
      { command: '/botbench', view: 'botbench', title: 'Botbench', description: 'Explore the coding-agent workbench', aliases: ['botbench', 'show me botbench', 'open botbench', 'try botbench', 'botbench tour'] },
      { command: '/writing', view: 'writing', title: 'Writing', description: 'Open the notebook', aliases: ['writing', 'what are you thinking about', 'notes', 'essay', 'open notebook'] },
      { command: '/lab', view: 'lab', title: 'The lab', description: 'Try a small feedback illustration', aliases: ['lab', 'let me try something', 'experiments', 'feedback', 'show me the lab'] },
      { command: '/contact', view: 'contact', title: 'Say hello', description: 'Find a way to connect', aliases: ['contact', 'lets talk', 'say hello', 'get in touch'] },
      { command: '/duck', view: 'duck', title: 'Ask the duck', description: 'Get a useful question', aliases: ['duck', 'quack', 'ask the duck'] }
    ];
    var helpSkill = { command: '/help', view: 'help', title: 'Available skills', description: 'Choose something to explore', aliases: ['help', 'jon --help', '?'] };
    var currentSkill = null;
    var filteredSkills = skills.slice();
    var pickerOpener = trigger;
    var closeReason = '';
    var navigationToken = 0;
    var pendingTimers = [];
    var navigating = false;
    var duckIndex = 0;
    var duckQuestions = [
      'What is the smallest thing you could learn next?',
      'Is the hard part the code, or the decision?',
      'What would change your mind?',
      'Who gets to say this is done?',
      'Have you tried explaining it to a duck?'
    ];

    function normalize(value) {
      var text = String(value || '').trim().toLowerCase();
      if (text === '?') return text;
      return text.replace(/[\u2018\u2019']/g, '').replace(/[?!.,]+$/, '').replace(/\s+/g, ' ');
    }

    function findSkill(value) {
      var normalized = normalize(value);
      return skills.concat(helpSkill).find(function (skill) {
        return skill.command === normalized || skill.aliases.includes(normalized);
      });
    }

    function setBusy(busy) {
      result.setAttribute('aria-busy', String(busy));
      result.inert = busy;
      if (resultScroll) resultScroll.classList.toggle('is-transitioning', busy);
    }

    function cancelNavigation() {
      navigationToken++;
      pendingTimers.forEach(function (timer) { window.clearTimeout(timer); });
      pendingTimers = [];
      navigating = false;
      setBusy(false);
    }

    function initializeLab() {
      var range = result.querySelector('#cli-checkpoints');
      var countOutput = result.querySelector('#cli-checkpoint-count');
      var timeline = result.querySelector('#cli-timeline');
      var feedback = result.querySelector('#cli-feedback-result');
      if (!range || !countOutput || !timeline || !feedback) return;
      function update() {
        var count = Math.min(5, Math.max(1, Number(range.value) || 1));
        var plannedDays = [];
        for (var index = 1; index <= count; index++) plannedDays.push(Math.ceil(index * 5 / count));
        timeline.replaceChildren();
        for (var day = 1; day <= 5; day++) {
          var planned = plannedDays.includes(day);
          var cell = document.createElement('div');
          cell.className = 'timeline-day' + (planned ? ' checkpoint' : '');
          var label = document.createElement('span');
          label.className = 'timeline-day-label';
          label.textContent = 'Day ' + day;
          var bar = document.createElement('span');
          bar.className = 'timeline-bar';
          bar.setAttribute('aria-hidden', 'true');
          var checkLabel = document.createElement('span');
          checkLabel.className = 'timeline-check-label';
          checkLabel.textContent = planned ? 'Check' : 'Build';
          cell.append(label, bar, checkLabel);
          timeline.appendChild(cell);
        }
        countOutput.value = String(count);
        countOutput.textContent = String(count);
        range.setAttribute('aria-valuetext', count + (count === 1 ? ' planned checkpoint' : ' planned checkpoints'));
        feedback.textContent = count === 1
          ? 'Your first planned check comes on day 5.'
          : 'Your first planned check comes on day ' + plannedDays[0] + ', with ' + count + ' planned chances to ask a better question.';
      }
      range.addEventListener('input', update);
      update();
    }

    function updateCurrentControls() {
      document.querySelectorAll('nav [data-command], [data-nav][data-command]').forEach(function (button) {
        var selected = currentSkill && button.dataset.command === currentSkill.command;
        button.classList.toggle('is-active', Boolean(selected));
        if (selected) button.setAttribute('aria-current', 'page');
        else button.removeAttribute('aria-current');
      });
      trigger.setAttribute('aria-label', 'Choose a skill. Current skill ' + currentSkill.command);
    }

    function render(skill, announce) {
      var template = document.getElementById('view-' + skill.view);
      if (!template || !template.content) return false;
      result.replaceChildren(template.content.cloneNode(true));
      if (resultScroll) resultScroll.scrollTop = 0;
      currentSkill = skill;
      activeSkill.textContent = skill.command;
      result.dataset.view = skill.view;
      document.title = 'Jon Lange — ' + skill.title;
      setBusy(false);
      updateCurrentControls();
      if (skill.view === 'lab') initializeLab();
      if (skill.view === 'duck') {
        var question = result.querySelector('#duck-question');
        if (question) question.textContent = duckQuestions[duckIndex++ % duckQuestions.length];
      }
      if (announce) status.textContent = 'Showing ' + skill.title + '.';
      return true;
    }

    function updateOptions() {
      var query = normalize(search.value);
      filteredSkills = skills.filter(function (skill) {
        return !query || skill.command.includes(query) || skill.title.toLowerCase().includes(query) || skill.description.toLowerCase().includes(query) || skill.aliases.some(function (alias) { return alias.includes(query); });
      });
      options.replaceChildren();
      filteredSkills.forEach(function (skill) {
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'skill-option';
        button.dataset.skill = skill.command;
        button.dataset.command = skill.command;
        if (currentSkill && currentSkill.command === skill.command) {
          button.classList.add('is-selected');
          button.setAttribute('aria-current', 'page');
        }
        var command = document.createElement('code');
        command.className = 'skill-option-command';
        command.textContent = skill.command;
        var description = document.createElement('span');
        description.className = 'skill-option-description';
        description.textContent = skill.description;
        button.append(command, description);
        options.appendChild(button);
      });
      if (!filteredSkills.length) {
        var empty = document.createElement('p');
        empty.className = 'skill-empty';
        empty.textContent = 'No matching skills. Try a name like LangSpan, writing, or lab.';
        options.appendChild(empty);
      }
    }

    function openPicker() {
      if (!dialog.open) {
        pickerOpener = document.activeElement instanceof HTMLElement ? document.activeElement : trigger;
        search.value = '';
        updateOptions();
        closeReason = '';
        dialog.showModal();
      }
      trigger.setAttribute('aria-expanded', 'true');
      if (window.matchMedia('(max-width: 760px)').matches) {
        var selected = options.querySelector('.is-selected') || options.querySelector('button');
        (selected || closeButton).focus({ preventScroll: true });
      } else search.focus({ preventScroll: true });
    }

    function closePicker(reason) {
      if (!dialog.open) return;
      closeReason = reason || 'dismiss';
      dialog.close();
    }

    function setRoute(skill) {
      var hash = skill.view === 'about' ? '' : '#' + skill.view;
      if (window.location.hash !== hash) {
        window.history.pushState({ skill: skill.view }, '', window.location.pathname + window.location.search + hash);
      }
    }

    function selectSkill(skill, source) {
      if (!skill) return;
      if (skill.view === 'help' && !document.getElementById('view-help')) {
        openPicker();
        return;
      }
      cancelNavigation();
      closePicker('selection');
      trigger.focus({ preventScroll: true });
      setRoute(skill);
      if (currentSkill && currentSkill.view === skill.view && skill.view !== 'duck') {
        if (source === 'keyboard') result.focus({ preventScroll: true });
        return;
      }
      var token = navigationToken;
      var startText = activeSkill.textContent || (currentSkill ? currentSkill.command : '/about');
      var focusResult = source === 'keyboard';
      var finish = function () {
        if (token !== navigationToken) return;
        pendingTimers = [];
        navigating = false;
        render(skill, true);
        if (focusResult) {
          result.setAttribute('tabindex', '-1');
          result.focus({ preventScroll: true });
        }
      };
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        finish();
        return;
      }
      navigating = true;
      setBusy(true);
      trigger.setAttribute('aria-label', 'Choose a skill. Opening ' + skill.command);
      var frames = [];
      for (var length = startText.length - 1; length >= 0; length--) frames.push(startText.slice(0, length));
      for (var position = 1; position <= skill.command.length; position++) frames.push(skill.command.slice(0, position));
      // A command is high-frequency navigation, not a product film.
      var duration = 140;
      frames.forEach(function (frame, index) {
        pendingTimers.push(window.setTimeout(function () {
          if (token !== navigationToken) return;
          activeSkill.textContent = frame;
          if (index === frames.length - 1) finish();
        }, duration * (index + 1) / frames.length));
      });
    }

    function updateThemeButton() {
      if (!themeButton) return;
      var light = document.documentElement.dataset.theme === 'light';
      themeButton.setAttribute('aria-pressed', String(light));
      themeButton.setAttribute('aria-label', light ? 'Switch to dark theme' : 'Switch to light theme');
      var label = themeButton.querySelector('[data-theme-label]');
      if (label) label.textContent = light ? 'Dark mode' : 'Light mode';
      else themeButton.textContent = light ? 'Dark mode' : 'Light mode';
    }

    function toggleTheme() {
      var light = document.documentElement.dataset.theme !== 'light';
      var root = document.documentElement;
      root.setAttribute('data-theme-switching', '');
      root.dataset.theme = light ? 'light' : 'dark';
      void root.offsetHeight;
      window.requestAnimationFrame(function () { root.removeAttribute('data-theme-switching'); });
      updateThemeButton();
      status.textContent = (light ? 'Light' : 'Dark') + ' theme enabled.';
    }

    function activate(value, source) {
      var normalized = normalize(value);
      if (normalized === '/theme' || normalized === 'theme') {
        toggleTheme();
        return;
      }
      var skill = findSkill(value);
      if (skill) selectSkill(skill, source);
      else {
        openPicker();
        status.textContent = 'Choose one of the available skills.';
      }
    }

    trigger.setAttribute('aria-haspopup', 'dialog');
    trigger.setAttribute('aria-controls', 'skills-dialog');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.addEventListener('click', openPicker);
    closeButton.addEventListener('click', function () { closePicker('dismiss'); });
    dialog.addEventListener('close', function () {
      trigger.setAttribute('aria-expanded', 'false');
      if (closeReason !== 'selection') {
        var destination = pickerOpener && pickerOpener.isConnected ? pickerOpener : trigger;
        destination.focus({ preventScroll: true });
      }
      closeReason = '';
    });
    dialog.addEventListener('cancel', function () { closeReason = 'dismiss'; });
    dialog.addEventListener('click', function (event) {
      if (event.target !== dialog) return;
      var bounds = dialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) closePicker('dismiss');
    });
    search.addEventListener('input', updateOptions);
    search.addEventListener('keydown', function (event) {
      if (event.isComposing) return;
      if (event.key === 'ArrowDown') {
        var first = options.querySelector('button');
        if (first) {
          event.preventDefault();
          first.focus();
        }
      } else if (event.key === 'Enter') {
        event.preventDefault();
        var exact = findSkill(search.value);
        if (exact || filteredSkills[0]) selectSkill(exact || filteredSkills[0], 'keyboard');
        else status.textContent = 'No matching skills. Try LangSpan, writing, or lab.';
      }
    });
    document.addEventListener('click', function (event) {
      var target = event.target instanceof Element ? event.target : null;
      if (target && target.closest('.skip-link')) {
        event.preventDefault();
        result.focus();
        return;
      }
      var command = target ? target.closest('[data-command], [data-skill]') : null;
      if (!command || command === trigger || command === themeButton) return;
      if (command.tagName === 'A' && (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey)) return;
      event.preventDefault();
      activate(command.dataset.command || command.dataset.skill, event.detail === 0 ? 'keyboard' : 'pointer');
    });
    document.addEventListener('keydown', function (event) {
      if (event.isComposing) return;
      var target = event.target instanceof Element ? event.target : null;
      var editing = target && (target.matches('input, textarea, select') || target.closest('[contenteditable="true"]'));
      var commandShortcut = (event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k';
      var slashShortcut = event.key === '/' && !event.metaKey && !event.ctrlKey && !event.altKey && !editing;
      if (commandShortcut || slashShortcut) {
        event.preventDefault();
        openPicker();
      }
    });
    if (themeButton) themeButton.addEventListener('click', toggleTheme);

    function readRoute(announce) {
      var view = window.location.hash.slice(1).toLowerCase();
      if (!view || view === 'home') view = 'about';
      var skill = skills.find(function (entry) { return entry.view === view; });
      if (!skill && view === 'help' && document.getElementById('view-help')) skill = helpSkill;
      skill = skill || skills[0];
      if (!navigating && currentSkill && currentSkill.view === skill.view) return;
      cancelNavigation();
      if (dialog.open) closePicker('route');
      render(skill, announce);
    }
    window.addEventListener('popstate', function () { readRoute(true); });
    window.addEventListener('hashchange', function () { readRoute(true); });
    updateThemeButton();
    readRoute(false);
    trigger.disabled = false;
    if (themeButton) themeButton.disabled = false;
    document.documentElement.dataset.enhanced = 'true';
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
}());
