
  if (form && input) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var count = runSearch(input.value);
      scrollToDirectory();
      announce(count);
    });

    var debounce;
    input.addEventListener('input', function () {
      clearTimeout(debounce);
      debounce = setTimeout(function () {
        var q = input.value.trim();
        if (q.length >= 2) {
          var count = runSearch(q);
          announce(count);
        } else {
          clearHighlights();
          announce(0);
        }
      }, 220);
    });

    $$('.chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        input.value = chip.getAttribute('data-q') || '';
        input.focus();
        var count = runSearch(input.value);
        scrollToDirectory();
        announce(count);
      });
    });

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        input.value = '';
        clearHighlights();
        announce(0);
      }
    });
  }

  /* ---------------------------------------------------------
     5. TIMELINE — click & keyboard navigation
     --------------------------------------------------------- */
  var timelineItems = $$('.timeline__item');

  function selectStage(item) {
    timelineItems.forEach(function (i) { i.classList.remove('is-active'); });
    item.classList.add('is-active');

    var targetId = item.getAttribute('data-target');
    var target = targetId ? document.getElementById(targetId) : null;
    if (!target) return;

    var y = target.getBoundingClientRect().top + window.scrollY - 110;
    window.scrollTo({ top: y, behavior: 'smooth' });
  }

  timelineItems.forEach(function (item) {
    item.setAttribute('tabindex', '0');
    item.setAttribute('role', 'button');

    item.addEventListener('click', function () { selectStage(item); });

    item.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        selectStage(item);
      }
    });
  });

  /* ---------------------------------------------------------
     6. REVEAL ON SCROLL
     --------------------------------------------------------- */
  var revealTargets = $$(
    '.stage, .hcard, .dcard, .acard, .step, .wlist li, .timeline__item, .infobar'
  );

  if ('IntersectionObserver' in window) {
    var revealObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    revealTargets.forEach(function (el, i) {
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 6) * 55 + 'ms';
      revealObs.observe(el);
    });
  } else {
    revealTargets.forEach(function (el) { el.classList.add('is-visible'); });
  }
