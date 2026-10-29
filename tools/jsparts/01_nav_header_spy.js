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
