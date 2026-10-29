/* ============================================================
   RUMAH LAYANAN KABUPATEN LAMONGAN
   main.js — interaksi portal
   ============================================================ */
(function () {
  'use strict';

  var $  = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---------------------------------------------------------
     1. MOBILE NAVIGATION
     --------------------------------------------------------- */
  var navToggle = $('#navToggle');
  var nav       = $('#nav');

  function closeNav() {
    if (!nav || !navToggle) return;
    nav.classList.remove('is-open');
    navToggle.setAttribute('aria-expanded', 'false');
    navToggle.setAttribute('aria-label', 'Buka menu');
  }

  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      navToggle.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
    });

    // Tutup menu saat link di dalam diklik
    $$('.nav a', nav).forEach(function (link) {
      link.addEventListener('click', closeNav);
    });

    // Tutup menu bila klik di luar
    document.addEventListener('click', function (e) {
      if (!nav.classList.contains('is-open')) return;
      if (nav.contains(e.target) || navToggle.contains(e.target)) return;
      closeNav();
    });

    // Tutup menu saat Escape ditekan
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        closeNav();
        navToggle.focus();
      }
    });

    // Reset state saat kembali ke lebar desktop
    window.addEventListener('resize', function () {
      if (window.innerWidth > 860) closeNav();
    });
  }

  /* ---------------------------------------------------------
     2. STICKY HEADER SHADOW
     --------------------------------------------------------- */
  var header = $('.header');

  function onScroll() {
    if (!header) return;
    header.classList.toggle('is-stuck', window.scrollY > 8);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------------------------------------------------
     3. ACTIVE NAV LINK (scroll spy)
     --------------------------------------------------------- */
  var sections = ['#beranda', '#perjalanan', '#direktori', '#panduan', '#pengaduan']
    .map(function (id) { return document.getElementById(id.slice(1)); })
    .filter(Boolean);
  var navLinks = $$('.nav__link');

  function spy() {
    var pos = window.scrollY + 140;
    var current = sections[0];

    sections.forEach(function (sec) {
      if (sec.offsetTop <= pos) current = sec;
    });

    navLinks.forEach(function (link) {
      var href = link.getAttribute('href');
      link.classList.toggle('is-active', href === '#' + current.id);
    });
  }

  if ('IntersectionObserver' in window) {
    var spyObs = new IntersectionObserver(spy, { rootMargin: '-140px 0px -60% 0px', threshold: 0 });
    sections.forEach(function (s) { spyObs.observe(s); });
  } else {
    window.addEventListener('scroll', spy, { passive: true });
  }
  spy();


  /* ---------------------------------------------------------
     4. SEARCH & FILTERING
     --------------------------------------------------------- */
  var form   = $('#searchForm');
  var input  = $('#searchInput');
  var dirSec = $('#direktori');

  var stageCards  = $$('.scard');
  var dirEntries  = $$('.dlist li');
  var dirCards    = $$('.dcard');
  var healthRows  = $$('.hlist li');
  var searchables = stageCards.concat(dirEntries).concat(healthRows);

  function normalize(str) {
    return (str || '').toLowerCase().trim();
  }

  function clearHighlights() {
    $$('mark.hl').forEach(function (m) {
      var parent = m.parentNode;
      parent.replaceChild(document.createTextNode(m.textContent), m);
      parent.normalize();
    });
    searchables.forEach(function (el) { el.classList.remove('is-dimmed', 'is-match'); });
    dirCards.forEach(function (c) { c.classList.remove('is-hidden', 'is-match'); });
    $$('.hcard').forEach(function (c) { c.classList.remove('is-match'); });
  }

  function highlight(root, term) {
    if (!term) return;
    var escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = node.parentNode.nodeName;
        if (p === 'MARK' || p === 'SCRIPT' || p === 'STYLE') return NodeFilter.FILTER_REJECT;
        return node.nodeValue.toLowerCase().indexOf(term) !== -1
          ? NodeFilter.FILTER_ACCEPT
          : NodeFilter.FILTER_REJECT;
      }
    });
    var nodes = [];
    var n;
    while ((n = walker.nextNode())) nodes.push(n);

    nodes.forEach(function (node) {
      var parts = node.nodeValue.split(new RegExp('(' + escaped + ')', 'ig'));
      var frag = document.createDocumentFragment();
      parts.forEach(function (part) {
        if (part.toLowerCase() === term) {
          var m = document.createElement('mark');
          m.className = 'hl';
          m.textContent = part;
          frag.appendChild(m);
        } else {
          frag.appendChild(document.createTextNode(part));
        }
      });
      node.parentNode.replaceChild(frag, node);
    });
  }

  function runSearch(rawTerm) {
    var term = normalize(rawTerm);
    clearHighlights();

    if (term.length < 2) return 0;

    var matches = [];

    stageCards.forEach(function (card) {
      var hit = normalize(card.textContent).indexOf(term) !== -1;
      card.classList.toggle('is-match', hit);
      card.classList.toggle('is-dimmed', !hit);
      if (hit) matches.push(card);
    });

    dirEntries.forEach(function (li) {
      var hit = normalize(li.textContent).indexOf(term) !== -1;
      li.classList.toggle('is-match', hit);
      li.classList.toggle('is-dimmed', !hit);
      if (hit) {
        matches.push(li);
        var card = li.closest('.dcard');
        if (card) card.classList.add('is-match');
      }
    });

    healthRows.forEach(function (li) {
      var hit = normalize(li.textContent).indexOf(term) !== -1;
      li.classList.toggle('is-match', hit);
      li.classList.toggle('is-dimmed', !hit);
      if (hit) {
        matches.push(li);
        var card = li.closest('.hcard');
        if (card) card.classList.add('is-match');
      }
    });

    dirCards.forEach(function (card) {
      var has = $$('.is-match', card).length > 0;
      card.classList.toggle('is-hidden', !has);
    });

    matches.slice(0, 60).forEach(function (el) { highlight(el, term); });

    return matches.length;
  }

  function announce(count) {
    var live = $('#searchLive');
    if (!live) return;
    live.textContent = count > 0
      ? count + ' layanan ditemukan untuk pencarian ini.'
      : 'Tidak ada layanan yang cocok.';
  }

  function scrollToDirectory() {
    if (!dirSec) return;
    var y = dirSec.getBoundingClientRect().top + window.scrollY - 90;
    window.scrollTo({ top: y, behavior: 'smooth' });
  }


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


  /* ---------------------------------------------------------
     7. SMOOTH SCROLL OFFSET FOR ANCHORS
     --------------------------------------------------------- */
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;

    var href = link.getAttribute('href');
    if (!href || href === '#') return;

    var target = document.getElementById(href.slice(1));
    if (!target) return;

    e.preventDefault();
    var y = target.getBoundingClientRect().top + window.scrollY - 88;
    window.scrollTo({ top: y, behavior: 'smooth' });
    history.replaceState(null, '', href);
  });

  /* ---------------------------------------------------------
     8. PREVENT PLACEHOLDER LINKS FROM JUMPING
     --------------------------------------------------------- */
  $$('a[href="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
    });
  });

  /* ---------------------------------------------------------
     9. CURRENT YEAR IN FOOTER
     --------------------------------------------------------- */
  $$('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
