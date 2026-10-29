
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
