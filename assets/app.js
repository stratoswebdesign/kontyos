/* Kontyos webshop demo – kosár, mini-kosár, termékoldal, pénztár (localStorage alapú, szerver nélkül) */
(function () {
  'use strict';
  var K = window.KONTYOS || { p: {} };
  var ROOT = document.documentElement.getAttribute('data-root') || '';
  var LIMIT = 20000;
  var KEY = 'kontyos-demo-cart';

  function fmt(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' Ft'; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var mem = null;
  function load() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v : []; } catch (e) { return mem || []; }
  }
  function save(c) { mem = c; try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} badge(); }
  function unit(p, q) { return p.tier && q >= p.tier[0] ? p.tier[1] : p.price; }
  function totals(c) {
    var sub = 0, items = 0, free = false;
    c.forEach(function (l) { var p = K.p[l.id]; if (!p) return; sub += unit(p, l.q) * l.q; items += l.q; if (p.free) free = true; });
    return { sub: sub, items: items, free: free || sub >= LIMIT, left: Math.max(0, LIMIT - sub), pct: Math.min(100, Math.round(sub / LIMIT * 100)) };
  }
  function add(id, q) {
    q = Math.max(1, parseInt(q, 10) || 1);
    var c = load(), l = c.filter(function (x) { return x.id === id; })[0];
    if (l) l.q += q; else c.push({ id: id, q: q });
    save(c); mini(id); track('add_to_cart', id, q);
  }
  function badge() {
    var t = totals(load());
    document.querySelectorAll('[data-cart-count]').forEach(function (el) { el.textContent = t.items; });
  }
  function track(ev, id, q) { try { (window.dataLayer = window.dataLayer || []).push({ event: ev, item_id: id, quantity: q }); } catch (e) {} }

  /* „Illik mellé” ajánló (mini-kosár, kosár) */
  function upsHtml(ids, exclude) {
    ids = ids.filter(function (i) { return K.p[i] && exclude.indexOf(i) < 0; }).slice(0, 3);
    if (!ids.length) return '';
    return '<div class="pd-ups mini-ups"><p>Illik mellé</p><ul>' + ids.map(function (i) {
      var x = K.p[i];
      return '<li><a href="' + ROOT + x.url + '" class="im"><img src="' + ROOT + x.img + '" alt="" loading="lazy"></a><a href="' + ROOT + x.url + '" class="nm">' + esc(x.n) + '<small>' + fmt(x.price) + '</small></a><button type="button" data-add="' + i + '" aria-label="' + esc(x.n) + ' kosárba">+</button></li>';
    }).join('') + '</ul></div>';
  }

  /* Mini-kosár */
  var miniEl;
  function mini(id) {
    var p = K.p[id]; if (!p) return;
    if (!miniEl) {
      miniEl = document.createElement('div'); miniEl.className = 'mini'; miniEl.setAttribute('role', 'dialog'); miniEl.setAttribute('aria-label', 'Kosárba került');
      document.body.appendChild(miniEl);
    }
    var t = totals(load());
    miniEl.innerHTML = '<div class="in"><div class="top"><span class="ok">✓ KOSÁRBA KERÜLT</span><button class="x" type="button" aria-label="Bezárás" data-mini-close>×</button></div>' +
      '<div class="item">' + (p.img ? '<img src="' + ROOT + p.img + '" alt="">' : '') + '<div><b>' + esc(p.n) + '</b><span>' + fmt(p.price) + '</span></div></div>' +
      '<span style="font-size:13px">' + (t.free ? 'Ingyenes a szállítás!' : 'Még <b>' + fmt(t.left) + '</b> az ingyenes szállításig.') + '</span>' +
      '<div class="bar"><i style="width:' + (t.free ? 100 : t.pct) + '%"></i></div>' +
      '<div class="acts"><a class="btn blue" href="' + ROOT + 'kosar.html">Tovább a kosárhoz</a><button class="btn ghost" type="button" data-mini-close>Vásárolok még</button></div>' +
      upsHtml(p.ups || [], load().map(function (l) { return l.id; })) + '</div>';
    miniEl.classList.add('open');
    clearTimeout(miniEl._t); miniEl._t = setTimeout(function () { miniEl.classList.remove('open'); }, 6000);
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-add]');
    if (a) {
      e.preventDefault();
      var qsrc = a.getAttribute('data-qty-from'), q = a.getAttribute('data-qty') || 1;
      if (qsrc) { var qe = document.querySelector(qsrc); if (qe) q = qe.getAttribute('data-value') || qe.textContent; }
      add(a.getAttribute('data-add'), q);
      return;
    }
    if (e.target.closest('[data-mini-close]') && miniEl) { miniEl.classList.remove('open'); return; }
    var mb = e.target.closest('[data-menu]');
    if (mb) { document.getElementById('drawer').classList.add('open'); return; }
    if (e.target.closest('[data-menu-close]') || e.target.id === 'drawer') { document.getElementById('drawer').classList.remove('open'); return; }
  });

  /* Termékoldal: mennyiség, 1/3/6 */
  var buy = document.querySelector('[data-buy]');
  if (buy) {
    var id = buy.getAttribute('data-buy'), p = K.p[id], q = 1;
    var setQ = function (n) {
      q = Math.max(1, n);
      document.querySelectorAll('[data-q]').forEach(function (el) { el.textContent = q; el.setAttribute('data-value', q); });
      document.querySelectorAll('[data-pack]').forEach(function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-pack') === q)); });
      var u = unit(p, q);
      document.querySelectorAll('[data-unit]').forEach(function (el) { el.textContent = fmt(u); });
      document.querySelectorAll('[data-line]').forEach(function (el) { el.textContent = fmt(u * q); });
      var t = totals(load()), after = t.sub + u * q, left = Math.max(0, LIMIT - after);
      document.querySelectorAll('[data-free-text]').forEach(function (el) { el.textContent = (p.free || left === 0) ? 'Ezzel ingyenes a szállítás.' : 'Kosarad ezzel ' + fmt(after) + ' – még ' + fmt(left) + ' az ingyenes szállításig.'; });
      document.querySelectorAll('[data-free-bar]').forEach(function (el) { el.style.width = (p.free ? 100 : Math.min(100, Math.round(after / LIMIT * 100))) + '%'; });
    };
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-inc]')) setQ(q + 1);
      if (e.target.closest('[data-dec]')) setQ(q - 1);
      var pk = e.target.closest('[data-pack]'); if (pk) setQ(+pk.getAttribute('data-pack'));
    });
    setQ(1); track('view_item', id, 1);
  }

  /* Főoldal: gyümölcsválasztó */
  var fsel = document.querySelector('[data-fruits]');
  if (fsel) {
    var show = function (el) {
      var d = el.dataset, box = document.querySelector('[data-fruit-view]');
      fsel.querySelectorAll('[data-fruit]').forEach(function (x) { x.setAttribute('aria-current', String(x === el)); });
      box.style.setProperty('--tint', d.tint); box.closest('section').style.background = d.bg;
      box.querySelector('img').src = d.img; box.querySelector('img').alt = d.name;
      box.querySelector('[data-f-k]').textContent = d.k; box.querySelector('[data-f-n]').textContent = d.name; box.querySelector('[data-f-n]').style.color = d.ink;
      box.querySelector('[data-f-l]').textContent = d.line; box.querySelector('[data-f-p]').textContent = d.price;
      box.querySelectorAll('a[data-f-href]').forEach(function (a) { a.href = el.href; });
      box.querySelector('[data-add]').setAttribute('data-add', d.id);
    };
    fsel.querySelectorAll('[data-fruit]').forEach(function (el) {
      el.addEventListener('mouseenter', function () { show(el); });
      el.addEventListener('focus', function () { show(el); });
    });
  }

  /* Demó-kapcsolók: szezon (főoldal), fázis (kampányoldalak) */
  function toggle(attr, btnAttr, store) {
    var btns = document.querySelectorAll('[' + btnAttr + ']'); if (!btns.length) return;
    var set = function (v) {
      document.querySelectorAll('[' + attr + ']').forEach(function (el) { el.hidden = el.getAttribute(attr).split(' ').indexOf(v) < 0; });
      btns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute(btnAttr) === v)); });
      try { localStorage.setItem(store, v); } catch (e) {}
    };
    btns.forEach(function (b) { b.addEventListener('click', function () { set(b.getAttribute(btnAttr)); }); });
    var init = btns[0].getAttribute(btnAttr);
    try { init = new URLSearchParams(location.search).get(store.split('-').pop()) || localStorage.getItem(store) || init; } catch (e) {}
    set(init);
  }
  toggle('data-season', 'data-season-btn', 'kontyos-demo-season');
  toggle('data-phase', 'data-phase-btn', 'kontyos-demo-phase-' + (document.body.getAttribute('data-page') || ''));

  /* Kategória szűrő */
  document.querySelectorAll('[data-filter-group]').forEach(function (g) {
    g.addEventListener('click', function (e) {
      var b = e.target.closest('[data-filter]'); if (!b) return;
      var v = b.getAttribute('data-filter');
      g.querySelectorAll('[data-filter]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      document.querySelectorAll(g.getAttribute('data-filter-group')).forEach(function (card) {
        card.hidden = v !== 'all' && card.getAttribute('data-taste') !== v;
      });
    });
  });

  /* Hírlevél (demó) */
  document.querySelectorAll('form[data-newsletter]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); f.innerHTML = '<p style="font-weight:800">Köszönjük! (Demó: élesben itt indul a feliratkozás és a −10% kupon.)</p>'; });
  });

  /* Kosár oldal */
  var cr = document.getElementById('cart-root');
  function renderCart() {
    var c = load(), t = totals(c);
    if (!c.length) {
      cr.innerHTML = '<div class="box" style="text-align:center;padding:48px 22px"><p class="h2" style="font-size:34px">A kosarad üres.</p><p class="muted" style="margin:10px 0 22px">Nézz körül a 100%-os gyümölcsborok között.</p><a class="btn blue" href="' + ROOT + 'gyumolcsbor.html">Gyümölcsborok</a></div>';
      document.getElementById('cart-side').hidden = true; return;
    }
    document.getElementById('cart-side').hidden = false;
    var lines = c.map(function (l) {
      var p = K.p[l.id]; if (!p) return '';
      var u = unit(p, l.q);
      return '<div class="line"><a class="im" style="--tint:' + p.tint + '" href="' + ROOT + p.url + '">' + (p.img ? '<img src="' + ROOT + p.img + '" alt="">' : '') + '</a>' +
        '<div class="nm"><a href="' + ROOT + p.url + '">' + esc(p.n) + '</a><small>' + esc(p.sub || '') + (p.tier && l.q >= p.tier[0] ? ' · mennyiségi ár: ' + fmt(u) + '/db' : '') + '</small><button class="rm" type="button" data-rm="' + l.id + '">Törlés</button></div>' +
        '<div class="q"><button type="button" aria-label="Kevesebb" data-cq="' + l.id + '" data-d="-1">−</button><span>' + l.q + '</span><button type="button" aria-label="Több" data-cq="' + l.id + '" data-d="1">+</button></div>' +
        '<div class="sum">' + fmt(u * l.q) + '</div></div>';
    }).join('');
    cr.innerHTML = '<div class="box" style="display:flex;flex-direction:column;gap:12px"><p class="serif" style="font-size:24px">' + (t.free ? 'Ingyenes a szállítás. 🎉' : 'Még <b style="color:#C8284E">' + fmt(t.left) + '</b>, és ingyen visszük.') + '</p><div class="bar" style="height:10px"><i style="width:' + (t.free ? 100 : t.pct) + '%"></i></div></div>' +
      '<div class="box">' + lines + '</div>';
    document.querySelectorAll('[data-sum]').forEach(function (el) { el.textContent = fmt(t.sub); });
    document.querySelectorAll('[data-shipfee]').forEach(function (el) { el.textContent = t.free ? 'Ingyenes' : '1 800 Ft-tól'; });
    document.querySelectorAll('[data-grand]').forEach(function (el) { el.innerHTML = fmt(t.sub) + (t.free ? '' : '<small>+ szállítás (1 800 Ft-tól)</small>'); });
    var cu = document.getElementById('cart-ups');
    if (cu) {
      var inCart = c.map(function (l) { return l.id; }), pool = [];
      c.forEach(function (l) { (K.p[l.id] && K.p[l.id].ups || []).forEach(function (i) { if (pool.indexOf(i) < 0) pool.push(i); }); });
      ['kontyos-borospohar', 'don-cherry-gyumolcse', 'friss-eper', 'piri-mama-bogreje'].forEach(function (i) { if (pool.indexOf(i) < 0) pool.push(i); });
      cu.outerHTML = '<div id="cart-ups">' + upsHtml(pool, inCart) + '</div>';
    }
  }
  if (cr) {
    renderCart();
    cr.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cq]'), r = e.target.closest('[data-rm]'), c = load();
      if (b) { c.forEach(function (l) { if (l.id === b.getAttribute('data-cq')) l.q += +b.getAttribute('data-d'); }); c = c.filter(function (l) { return l.q > 0; }); save(c); renderCart(); }
      if (r) { save(c.filter(function (l) { return l.id !== r.getAttribute('data-rm'); })); renderCart(); }
    });
    document.addEventListener('kontyos:add', renderCart);
    var oldAdd = add; add = function (id, q) { oldAdd(id, q); renderCart(); };
  }

  /* Kupon (demó) */
  document.querySelectorAll('[data-coupon]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); var m = f.querySelector('[data-coupon-msg]'); m.textContent = 'Demó: élesben a kupont a Shoprenter ellenőrzi és vonja le.'; });
  });

  /* Pénztár */
  var co = document.getElementById('checkout');
  if (co) {
    var c = load(), t = totals(c);
    var sumEl = document.getElementById('co-summary');
    if (!c.length) { co.innerHTML = '<div class="box" style="text-align:center;padding:40px"><p class="serif" style="font-size:28px">A kosarad üres.</p><a class="btn blue" style="margin-top:18px" href="' + ROOT + 'index.html">Vissza a boltba</a></div>'; if (sumEl) sumEl.hidden = true; }
    else {
      sumEl.querySelector('[data-co-lines]').innerHTML = c.map(function (l) { var p = K.p[l.id]; if (!p) return ''; return '<div style="display:flex;align-items:center;gap:12px">' + (p.img ? '<img src="' + ROOT + p.img + '" alt="" style="width:52px;height:52px;object-fit:contain;background:var(--paper);border-radius:4px">' : '') + '<span style="flex:1;font-size:14px;line-height:1.3"><b>' + esc(p.n) + '</b><br><span class="muted">' + l.q + ' db</span></span><b style="font-size:14px">' + fmt(unit(p, l.q) * l.q) + '</b></div>'; }).join('');
      document.querySelectorAll('[data-sum]').forEach(function (el) { el.textContent = fmt(t.sub); });
      var recalc = function () {
        var sh = co.querySelector('[name=ship]:checked'), py = co.querySelector('[name=pay]:checked');
        var fee = +sh.getAttribute('data-fee'), freeAt = +sh.getAttribute('data-free'), key = sh.getAttribute('data-key');
        var packFree = c.some(function (l) { return K.p[l.id] && K.p[l.id].free; });
        var shipFee = (fee === 0 || packFree || (freeAt && t.sub >= freeAt)) ? 0 : fee;
        var cod = co.querySelector('[name=pay][data-key=utanvet]'), codOk = key.indexOf('gls') === 0;
        cod.disabled = !codOk; cod.closest('.opt').style.opacity = codOk ? 1 : .45;
        if (!codOk && cod.checked) { co.querySelector('[name=pay][data-key=kartya]').checked = true; py = co.querySelector('[name=pay]:checked'); }
        var codFee = py.getAttribute('data-key') === 'utanvet' ? 500 : 0;
        document.querySelectorAll('[data-codrow]').forEach(function (el) { el.hidden = !codFee; });
        document.querySelectorAll('[data-cod-note]').forEach(function (el) { el.hidden = codOk; });
        document.querySelectorAll('[data-shipfee]').forEach(function (el) { el.textContent = shipFee ? fmt(shipFee) : 'Ingyenes'; });
        document.querySelectorAll('[data-grand]').forEach(function (el) { el.textContent = fmt(t.sub + shipFee + codFee); });
        co._total = t.sub + shipFee + codFee;
      };
      co.addEventListener('change', recalc); recalc();
      document.querySelectorAll('[data-free-left]').forEach(function (el) { el.innerHTML = t.free ? 'Ingyenes a szállítás.' : 'Még <b style="color:#C8284E">' + fmt(t.left) + '</b>, és ingyen visszük.'; });
      document.querySelectorAll('[data-free-bar]').forEach(function (el) { el.style.width = (t.free ? 100 : t.pct) + '%'; });
    }
    var form = document.getElementById('co-form');
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[data-req]').forEach(function (inp) {
        var f = inp.closest('.field'), v = inp.value.trim(), bad = !v;
        if (inp.type === 'email' && v && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) bad = true;
        if (inp.getAttribute('data-req') === 'zip' && v && !/^\d{4}$/.test(v)) bad = true;
        if (f) f.classList.toggle('err', bad); if (bad) ok = false;
      });
      form.querySelectorAll('[data-req-check]').forEach(function (cb) { cb.closest('.check').classList.toggle('err', !cb.checked); if (!cb.checked) ok = false; });
      var msg = document.getElementById('co-msg');
      if (!ok) { msg.textContent = 'Kérjük, töltsd ki a pirossal jelölt mezőket, és fogadd el a 18 év feletti nyilatkozatot és az ÁSZF-et.'; var first = form.querySelector('.err'); if (first) first.scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
      var order = { no: 'DEMO-' + String(Date.now()).slice(-6), lines: load(), sub: totals(load()).sub, total: co._total, free: totals(load()).free, name: form.querySelector('[name=name]').value, email: form.querySelector('[name=email]').value, ship: (form.querySelector('[name=ship]:checked') || {}).value, pay: (form.querySelector('[name=pay]:checked') || {}).value };
      try { sessionStorage.setItem('kontyos-demo-order', JSON.stringify(order)); } catch (err) {}
      track('purchase', order.no, 1);
      save([]); location.href = ROOT + 'koszonjuk.html';
    });
  }

  /* Köszönőoldal */
  var ty = document.getElementById('thanks');
  if (ty) {
    var o = null; try { o = JSON.parse(sessionStorage.getItem('kontyos-demo-order') || 'null'); } catch (e) {}
    if (o) {
      ty.querySelector('[data-o-no]').textContent = o.no;
      ty.querySelector('[data-o-mail]').textContent = o.email;
      ty.querySelector('[data-o-lines]').innerHTML = o.lines.map(function (l) { var p = K.p[l.id]; return p ? '<div style="display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--rule)"><span>' + esc(p.n) + ' × ' + l.q + '</span><b>' + fmt(unit(p, l.q) * l.q) + '</b></div>' : ''; }).join('') + '<div style="display:flex;justify-content:space-between;padding-top:10px"><b>Összesen (szállítással)</b><b>' + fmt(o.total || o.sub) + '</b></div>';
    }
  }

  /* Menü: ha egy sorba nem fér ki, hamburgerre vált (soha nem tör két sorba) */
  var head = document.querySelector('.site-head'), nav = head && head.querySelector('.nav');
  function fit() {
    if (!nav) return;
    var root = document.documentElement;
    root.classList.remove('burger');
    if (getComputedStyle(nav).display !== 'none' && nav.scrollWidth > nav.clientWidth + 1) root.classList.add('burger');
    document.querySelectorAll('.overlay-head main > .hero, .overlay-head main > [data-season] > .hero:first-child, .overlay-head main > [data-phase] > .hero:first-child').forEach(function (hero) { hero.style.marginTop = (-head.offsetHeight) + 'px'; });
  }
  fit();
  window.addEventListener('resize', fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  window.addEventListener('load', fit);

  /* Keresés (kereses.html) – kliensoldali, a katalógusból */
  var sres = document.getElementById('search-res');
  if (sres) {
    var norm = function (t) { return (t || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); };
    var q = ''; try { q = new URLSearchParams(location.search).get('q') || ''; } catch (e) {}
    var inp = document.getElementById('sq'); if (inp) inp.value = q;
    var words = norm(q).split(/\s+/).filter(Boolean);
    var hits = Object.keys(K.p).filter(function (id) { var p = K.p[id], h = norm(p.n + ' ' + p.sub + ' ' + id); return words.length && words.every(function (w) { return h.indexOf(w) >= 0; }); });
    document.getElementById('search-sum').textContent = q ? (hits.length + ' találat: „' + q + '”') : 'Írd be, mit keresel.';
    sres.innerHTML = hits.map(function (id) { var p = K.p[id]; return '<div class="pcard" style="position:relative"><a class="in" href="' + ROOT + p.url + '" style="text-decoration:none;display:flex;flex-direction:column;flex:1"><div class="ph" style="--tint:' + p.tint + '">' + (p.img ? '<img src="' + ROOT + p.img + '" alt="" loading="lazy">' : '') + '</div><div class="tx"><span class="k">' + esc(p.sub) + '</span><span class="n">' + esc(p.n) + '</span><div class="row"><span class="pr">' + (p.price ? fmt(p.price) : 'Elfogyott') + '</span></div></div></a><div style="position:absolute;right:16px;bottom:14px"><button class="plus" type="button" data-add="' + id + '" aria-label="Kosárba">+</button></div></div>'; }).join('');
  }

  /* Termékgaléria (íves ablak + bélyegképek) */
  document.querySelectorAll('[data-gal]').forEach(function (b) {
    b.addEventListener('click', function () {
      var main = document.querySelector('[data-gal-main]'); if (!main) return;
      main.src = b.getAttribute('data-gal');
      main.className = b.getAttribute('data-fit') === 'cover' ? 'fit-cover' : 'fit-contain';
      var cap = main.parentNode.querySelector('.cap'); if (cap) cap.hidden = b.getAttribute('data-fit') === 'cover';
      document.querySelectorAll('[data-gal]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    });
  });

  /* Visszaszámláló (Black Friday) */
  var cds = document.querySelectorAll('[data-countdown]');
  function tick() {
    cds.forEach(function (el) {
      var ms = new Date(el.getAttribute('data-countdown')) - new Date();
      if (ms <= 0) { el.textContent = 'VÉGET ÉRT'; return; }
      var d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4);
      el.textContent = 'MÉG ' + (d ? d + ' NAP ' : '') + h + ' ÓRA ' + m + ' PERC';
    });
  }
  if (cds.length) { tick(); setInterval(tick, 30000); }

  badge();
})();
