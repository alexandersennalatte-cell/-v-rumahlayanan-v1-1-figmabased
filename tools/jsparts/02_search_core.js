
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
