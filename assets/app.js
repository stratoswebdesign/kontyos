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
  /* Kupon (demó): a hírlevél-kupon −5% a termékek árából; élesben a Shoprenter kuponkezelése */
  var COUPONS = { HIRLEVEL5: { pct: 5, label: 'Hírlevél-kupon −5%' } };
  var CKEY = 'kontyos-demo-coupon';
  function coupon() { var c = null; try { c = localStorage.getItem(CKEY); } catch (e) {} return c && COUPONS[c] ? c : null; }
  function disc(sub) { var c = coupon(); return c ? Math.round(sub * COUPONS[c].pct / 100) : 0; }
  function paintDisc(sub) {
    var c = coupon(), d = disc(sub);
    document.querySelectorAll('[data-disc]').forEach(function (el) { el.hidden = !d; });
    document.querySelectorAll('[data-disc-l]').forEach(function (el) { el.textContent = c ? 'Kupon (' + c + ')' : 'Kupon'; });
    document.querySelectorAll('[data-disc-v]').forEach(function (el) { el.textContent = '−' + fmt(d); });
    document.querySelectorAll('[data-coupon-wrap]').forEach(function (w) {
      var m = w.querySelector('[data-coupon-msg]');
      if (c) { w.open = true; m.innerHTML = '<b style="color:#2E8C5A">✓ ' + esc(COUPONS[c].label) + ' beváltva.</b> <button type="button" class="linkbtn" data-coupon-rm>Eltávolítás</button>'; }
    });
    return d;
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
      document.querySelectorAll('[data-free-text]').forEach(function (el) { el.textContent = (p.free || left === 0) ? 'Ezzel ingyenes a szállítás.' : (el.hasAttribute('data-free-short') ? 'Még ' + fmt(left) + ' az ingyenes szállításig' : 'Kosarad ezzel ' + fmt(after) + ' – még ' + fmt(left) + ' az ingyenes szállításig.'); });
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
    var touch = window.matchMedia('(hover: none), (max-width: 860px)');
    fsel.querySelectorAll('[data-fruit]').forEach(function (el) {
      el.addEventListener('mouseenter', function () { if (!touch.matches) show(el); });
      el.addEventListener('focus', function () { show(el); });
      /* mobilon az első koppintás csak vált, a „Részletek” gomb visz a termékoldalra */
      el.addEventListener('click', function (e) { if (touch.matches && el.getAttribute('aria-current') !== 'true') { e.preventDefault(); show(el); } });
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
    f.addEventListener('submit', function (e) { e.preventDefault(); f.innerHTML = '<p style="font-weight:800">Köszönjük! Az 5%-os kuponkódot e-mailben küldjük. (Demó – élesben itt indul a feliratkozás és a kuponlevél.)</p>'; });
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
    var d = paintDisc(t.sub);
    document.querySelectorAll('[data-shipfee]').forEach(function (el) { el.textContent = t.free ? 'Ingyenes' : '1 800 Ft-tól'; });
    document.querySelectorAll('[data-grand]').forEach(function (el) { el.innerHTML = fmt(t.sub - d) + (t.free ? '' : '<small>+ szállítás (1 800 Ft-tól)</small>'); });
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
  var rerender = function () { if (cr) renderCart(); if (window.__coRecalc) window.__coRecalc(); };
  document.querySelectorAll('[data-coupon]').forEach(function (f) {
    var w = f.closest('[data-coupon-wrap]'), m = w.querySelector('[data-coupon-msg]');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var code = (f.querySelector('input').value || '').trim().toUpperCase().replace(/\s+/g, '');
      if (!code) { m.innerHTML = '<span style="color:#C8284E">Írd be a kuponkódot.</span>'; return; }
      if (!COUPONS[code]) { m.innerHTML = '<span style="color:#C8284E">Ez a kuponkód nem érvényes vagy lejárt.</span>'; return; }
      try { localStorage.setItem(CKEY, code); } catch (err) {}
      f.querySelector('input').value = ''; rerender();
    });
    w.addEventListener('click', function (e) {
      if (!e.target.closest('[data-coupon-rm]')) return;
      try { localStorage.removeItem(CKEY); } catch (err) {}
      m.textContent = ''; document.querySelectorAll('[data-disc]').forEach(function (el) { el.hidden = true; }); rerender();
    });
  });
  /* Lépésjelző: üres kosárral ne lehessen előre lépni */
  document.querySelectorAll('[data-need-cart]').forEach(function (a) {
    a.addEventListener('click', function (e) { if (!load().length) e.preventDefault(); });
  });

  /* Csomagpont-választó (demó pontok; élesben a futár valós listája) */
  var PP_CITIES = [['Budapest', 47.4979, 19.0402, ['1'], 6], ['Debrecen', 47.5316, 21.6273, ['40', '41'], 3], ['Szeged', 46.2530, 20.1414, ['67'], 3],
    ['Miskolc', 48.1035, 20.7784, ['35'], 3], ['Pécs', 46.0727, 18.2323, ['76'], 3], ['Győr', 47.6875, 17.6504, ['90', '91'], 3],
    ['Nyíregyháza', 47.9558, 21.7167, ['44'], 3], ['Kecskemét', 46.9062, 19.6913, ['60'], 3], ['Székesfehérvár', 47.1860, 18.4221, ['80'], 3],
    ['Szombathely', 47.2307, 16.6218, ['97'], 3], ['Veszprém', 47.0933, 17.9115, ['82'], 3], ['Hódmezővásárhely', 46.4181, 20.3300, ['68'], 2], ['Makó', 46.2219, 20.4809, ['69'], 2]];
  var PP_LABEL = { 'mpl-automata': 'MPL csomagautomata', 'mpl-postapont': 'MPL PostaPont', 'mpl-posta': 'Posta', 'gls-pont': 'GLS csomagpont' };
  var PP_TITLE = { 'mpl-automata': 'Csomagautomata kiválasztása', 'mpl-postapont': 'PostaPont kiválasztása', 'mpl-posta': 'Posta kiválasztása', 'gls-pont': 'GLS csomagpont kiválasztása' };
  var PP_AREA = ['belváros', 'északi városrész', 'déli városrész', 'keleti városrész', 'nyugati városrész', 'bevásárlóközpont'];
  function ppPoints(key) {
    var out = [], salt = { 'mpl-automata': 1, 'mpl-postapont': 2, 'mpl-posta': 3, 'gls-pont': 4 }[key];
    PP_CITIES.forEach(function (c, ci) {
      for (var k = 0; k < c[4]; k++) {
        var a = (ci * 7 + k * 13 + salt * 5) % 360 * Math.PI / 180, r = k === 0 ? 0.004 : 0.012 + 0.006 * ((k + salt) % 3);
        out.push({ id: key + '-' + ci + '-' + k, n: PP_LABEL[key] + ' – ' + c[0] + ', ' + PP_AREA[k % PP_AREA.length], city: c[0], zips: c[3], lat: c[1] + Math.sin(a) * r, lng: c[2] + Math.cos(a) * r * 1.4 });
      }
    });
    return out;
  }
  function initPP(co) {
    var modal = document.getElementById('pp-modal'); if (!modal) return;
    co._pp = {};
    var map = null, layer = null, curKey = null, pts = [];
    var norm = function (t) { return (t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    var list = modal.querySelector('[data-pp-list]'), q = modal.querySelector('[data-pp-q]');
    var pick = function (p) {
      co._pp[curKey] = p;
      var box = co.querySelector('[data-pp-box="' + curKey + '"]');
      box.classList.remove('err'); box.classList.add('set');
      box.querySelector('[data-pp-sel]').innerHTML = '<b>' + esc(p.n) + '</b><small>Demó átvételi pont</small>';
      box.querySelector('[data-pp-open]').textContent = 'Módosítás';
      close();
    };
    var draw = function () {
      var v = norm(q.value.trim()), dig = /^\d+$/.test(v);
      var hit = !v ? pts : pts.filter(function (p) { return dig ? p.zips.some(function (z) { return v.indexOf(z) === 0 || z.indexOf(v) === 0; }) : norm(p.city).indexOf(v) >= 0 || norm(p.n).indexOf(v) >= 0; });
      list.innerHTML = hit.length ? hit.map(function (p, i) { return '<li><button type="button" data-pp-i="' + pts.indexOf(p) + '"><b>' + esc(p.n) + '</b><small>' + esc(p.city) + '</small></button></li>'; }).join('') : '<li class="none">Nincs találat ezen a néven. Próbáld a közeli nagyobb várost vagy az irányítószám első két számjegyét.</li>';
      if (map && window.L) {
        if (layer) layer.remove();
        layer = L.layerGroup(hit.map(function (p) { return L.marker([p.lat, p.lng], { icon: L.divIcon({ className: 'ppm', html: '<span></span>', iconSize: [22, 22], iconAnchor: [11, 11] }) }).bindTooltip(p.n).on('click', function () { pick(p); }); })).addTo(map);
        if (hit.length) map.fitBounds(hit.map(function (p) { return [p.lat, p.lng]; }), { padding: [30, 30], maxZoom: 13, animate: false });
      }
    };
    var close = function () { modal.hidden = true; document.body.classList.remove('modal-open'); };
    var open = function (key) {
      curKey = key; pts = ppPoints(key);
      modal.querySelector('#pp-title').textContent = PP_TITLE[key];
      var zip = (co.querySelector('[name=zip]') || {}).value || '', city = (co.querySelector('[name=city]') || {}).value || '';
      q.value = city || zip;
      modal.hidden = false; document.body.classList.add('modal-open');
      if (!map && window.L) {
        map = L.map('pp-map', { scrollWheelZoom: true }).setView([47.15, 19.2], 7);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; OpenStreetMap' }).addTo(map);
      }
      setTimeout(function () { if (map) map.invalidateSize(); draw(); q.focus(); }, 30);
    };
    co.addEventListener('click', function (e) { var b = e.target.closest('[data-pp-open]'); if (b) { e.preventDefault(); open(b.getAttribute('data-pp-open')); } });
    modal.addEventListener('click', function (e) {
      if (e.target === modal || e.target.closest('[data-pp-close]')) { close(); return; }
      var it = e.target.closest('[data-pp-i]'); if (it) pick(pts[+it.getAttribute('data-pp-i')]);
    });
    q.addEventListener('input', draw);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) close(); });
  }

  /* Pénztár lépésjelző: görgetés szerint vált 2 és 3 között, kattintható */
  var cst = document.querySelector('[data-co-steps]');
  if (cst && 'IntersectionObserver' in window) {
    var fz = document.getElementById('fizetes');
    if (fz) new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        var past = x.isIntersecting || x.boundingClientRect.top < 0;
        cst.querySelector('[data-step="2"]').parentNode.classList.toggle('on', !past);
        cst.querySelector('[data-step="2"]').parentNode.classList.toggle('done', past);
        cst.querySelector('[data-step="3"]').parentNode.classList.toggle('on', past);
      });
    }, { rootMargin: '0px 0px -40% 0px' }).observe(fz);
  }

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
        /* ha ingyenes a szállítás, minden opciónál ezt mutatjuk: áthúzott díj + „Ingyenes” */
        co.querySelectorAll('[name=ship]').forEach(function (inp) {
          var f0 = +inp.getAttribute('data-fee'), fa = +inp.getAttribute('data-free'), pr = inp.closest('.opt').querySelector('[data-ship-price]');
          var fr = f0 === 0 || packFree || (fa && t.sub >= fa);
          pr.innerHTML = !f0 ? 'Ingyenes' : (fr ? '<s>' + fmt(f0) + '</s> <span class="free-tag">Ingyenes</span>' : fmt(f0));
        });
        co.querySelectorAll('[data-pp-box]').forEach(function (b) { b.hidden = b.getAttribute('data-pp-box') !== key; });
        var d = paintDisc(t.sub);
        document.querySelectorAll('[data-shipfee]').forEach(function (el) { el.textContent = shipFee ? fmt(shipFee) : 'Ingyenes'; });
        document.querySelectorAll('[data-grand]').forEach(function (el) { el.textContent = fmt(t.sub - d + shipFee + codFee); });
        co._total = t.sub - d + shipFee + codFee; co._disc = d;
      };
      window.__coRecalc = recalc;
      co.addEventListener('change', recalc); recalc();
      initPP(co);
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
      var shk = (form.querySelector('[name=ship]:checked') || {}).getAttribute ? form.querySelector('[name=ship]:checked').getAttribute('data-key') : '';
      var ppb = form.querySelector('[data-pp-box="' + shk + '"]');
      if (ppb) { var miss = !(co._pp && co._pp[shk]); ppb.classList.toggle('err', miss); if (miss) ok = false; }
      var msg = document.getElementById('co-msg');
      if (!ok) { msg.textContent = 'Kérjük, töltsd ki a pirossal jelölt mezőket' + (ppb && ppb.classList.contains('err') ? ', válassz átvételi pontot' : '') + ', és fogadd el a 18 év feletti nyilatkozatot és az ÁSZF-et.'; var first = form.querySelector('.err'); if (first) first.scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
      msg.textContent = '';
      var payKey = form.querySelector('[name=pay]:checked').getAttribute('data-key');
      var finish = function (paid) {
        var order = { no: 'DEMO-' + String(Date.now()).slice(-6), lines: load(), sub: totals(load()).sub, disc: co._disc || 0, coupon: coupon(), total: co._total, free: totals(load()).free, name: form.querySelector('[name=name]').value, email: form.querySelector('[name=email]').value, ship: (form.querySelector('[name=ship]:checked') || {}).value, point: co._pp && co._pp[shk] ? co._pp[shk].n : '', pay: (form.querySelector('[name=pay]:checked') || {}).value, payKey: payKey, paid: !!paid };
        try { sessionStorage.setItem('kontyos-demo-order', JSON.stringify(order)); localStorage.removeItem(CKEY); } catch (err) {}
        track('purchase', order.no, 1);
        save([]); location.href = ROOT + 'koszonjuk.html';
      };
      if (payKey !== 'kartya') { finish(false); return; }
      var sp = document.getElementById('sp-modal');
      sp.querySelector('[data-sp-total]').textContent = fmt(co._total);
      sp.hidden = false; document.body.classList.add('modal-open');
      sp.onclick = function (ev) {
        var b = ev.target.closest('[data-sp]'), x = ev.target.closest('[data-sp-close]') || ev.target === sp;
        if (b && b.getAttribute('data-sp') === 'ok') { finish(true); return; }
        if (b || x) {
          sp.hidden = true; document.body.classList.remove('modal-open');
          if (b) { msg.textContent = 'A bankkártyás fizetés nem sikerült (a bank elutasította vagy megszakadt). A rendelésed nem jött létre, a kosarad megmaradt – próbáld újra, vagy válassz másik fizetési módot.'; msg.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
        }
      };
    });
  }

  /* Köszönőoldal */
  var ty = document.getElementById('thanks');
  if (ty) {
    var o = null; try { o = JSON.parse(sessionStorage.getItem('kontyos-demo-order') || 'null'); } catch (e) {}
    if (o) {
      ty.querySelector('[data-o-no]').textContent = o.no;
      ty.querySelector('[data-o-mail]').textContent = o.email;
      ty.querySelector('[data-o-lines]').innerHTML = o.lines.map(function (l) { var p = K.p[l.id]; return p ? '<div style="display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--rule)"><span>' + esc(p.n) + ' × ' + l.q + '</span><b>' + fmt(unit(p, l.q) * l.q) + '</b></div>' : ''; }).join('') +
        (o.disc ? '<div style="display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--rule)"><span>Kupon (' + esc(o.coupon || '') + ')</span><b>−' + fmt(o.disc) + '</b></div>' : '') +
        '<div style="display:flex;justify-content:space-between;padding-top:10px"><b>Összesen (szállítással)</b><b>' + fmt(o.total || o.sub) + '</b></div>';
      var pe = ty.querySelector('[data-o-pay]');
      if (pe) pe.innerHTML = 'Szállítás: ' + esc(o.point || o.ship || '') + '<br>Fizetés: ' + esc(o.pay || '') +
        (o.payKey === 'kartya' ? ' – <b style="color:#2E8C5A">sikeres</b> (SimplePay, demó)' : o.payKey === 'atutalas' ? ' – az utalási adatokat a visszaigazoló e-mailben küldjük' : o.payKey === 'utanvet' ? ' – fizetés átvételkor' : '');
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

  /* Kövess minket: adventi standok – státusz, térkép, értesítő */
  var FAIRS = window.KONTYOS_FAIRS || [];
  if (FAIRS.length && document.querySelector('[data-fair]')) {
    var sim = null; try { sim = localStorage.getItem('kontyos-demo-sim') || null; } catch (e) {}
    var HU = ['jan.', 'febr.', 'márc.', 'ápr.', 'máj.', 'jún.', 'júl.', 'aug.', 'szept.', 'okt.', 'nov.', 'dec.'];
    var dfmt = function (d) { return HU[d.getMonth()] + ' ' + d.getDate() + '.'; };
    var day = function (iso) { var a = iso.split('-'); return new Date(+a[0], a[1] - 1, +a[2]); };
    var today = function () { var d = sim ? day(sim) : new Date(); return new Date(d.getFullYear(), d.getMonth(), d.getDate()); };
    var status = function (f) { if (f.tbd) return 'up'; var t = today(), a = day(f.start), b = day(f.end); return t < a ? 'up' : (t > b ? 'dn' : 'lv'); };
    var dtxt = function (f) { return f.tbd ? 'Időpont hamarosan' : dfmt(day(f.start)) + ' – ' + dfmt(day(f.end)); };
    var label = function (f) {
      if (f.tbd) return 'Hamarosan';
      var st = status(f), t = today(), a = day(f.start);
      if (st === 'lv') { var iso = t.getFullYear() + '-' + ('0' + (t.getMonth() + 1)).slice(-2) + '-' + ('0' + t.getDate()).slice(-2); return (f.closed || []).indexOf(iso) > -1 ? 'Ma zárva' : 'Most itt vagyunk'; }
      if (st === 'dn') return 'Véget ért';
      var n = Math.round((a - t) / 864e5);
      return n <= 14 ? (n === 1 ? 'Holnaptól' : n + ' nap múlva') : 'Hamarosan';
    };
    var paint = function () {
      FAIRS.forEach(function (f) {
        document.querySelectorAll('[data-fair="' + f.id + '"]').forEach(function (el) {
          el.setAttribute('data-st', status(f));
          var s1 = el.querySelector('[data-fair-status]'); if (s1) s1.textContent = label(f);
          var s2 = el.querySelector('[data-fair-dates]'); if (s2) s2.textContent = dtxt(f);
          if (f.tbd && s1 && s2 && s1.parentNode === s2.parentNode && s1.parentNode.classList.contains('dt')) s1.parentNode.textContent = 'Időpont hamarosan';
        });
      });
      /* a sor: élők elöl, aztán a Kontyos fontossági sorrendje (Sanyi, 2026-11-02) */
      document.querySelectorAll('.fair-row, .flist').forEach(function (row) {
        var order = { lv: 0, up: 1, dn: 2 };
        Array.prototype.slice.call(row.children).sort(function (x, y) {
          var fx = FAIRS.filter(function (f) { return f.id === x.getAttribute('data-fair'); })[0], fy = FAIRS.filter(function (f) { return f.id === y.getAttribute('data-fair'); })[0];
          return (order[status(fx)] - order[status(fy)]) || (FAIRS.indexOf(fx) - FAIRS.indexOf(fy));
        }).forEach(function (c) { row.appendChild(c); });
      });
      if (window.__fairMarkers) window.__fairMarkers.forEach(function (m) { m.setIcon(icon(status(m.fair))); m.setPopupContent(popup(m.fair)); });
    };
    var icon = function (st) { return window.L ? L.divIcon({ className: 'fmk ' + st, html: '<span></span>', iconSize: [26, 26], iconAnchor: [13, 13] }) : null; };
    var popup = function (f) { return '<b>' + esc(f.city) + '</b><br>' + esc(f.place) + '<br>' + dtxt(f) + (f.note ? '<br><small>' + esc(f.note) + '</small>' : '') + '<br><em>' + label(f) + '</em><br><a href="https://www.google.com/maps/dir/?api=1&destination=' + f.lat + ',' + f.lng + '" target="_blank" rel="noopener">Útvonal →</a>'; };
    var mapEl = document.getElementById('fmap');
    if (mapEl && window.L) {
      var map = L.map(mapEl, { scrollWheelZoom: false }).setView([47.15, 19.2], 7);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; OpenStreetMap' }).addTo(map);
      window.__fairMarkers = FAIRS.map(function (f) { var m = L.marker([f.lat, f.lng], { icon: icon(status(f)) }).addTo(map).bindPopup(popup(f)); m.fair = f; return m; });
      var B = window.KONTYOS_BORHAZ; if (B) L.marker([B.lat, B.lng], { icon: L.divIcon({ className: 'fmk bh', html: '<span></span>', iconSize: [22, 22], iconAnchor: [11, 11] }) }).addTo(map).bindPopup('<b>' + esc(B.city) + '</b><br>' + esc(B.place));
      map.fitBounds(FAIRS.map(function (f) { return [f.lat, f.lng]; }).concat(B ? [[B.lat, B.lng]] : []), { padding: [30, 30] });
      document.querySelectorAll('[data-go]').forEach(function (b) {
        b.addEventListener('click', function () { var m = window.__fairMarkers.filter(function (x) { return x.fair.id === b.getAttribute('data-go'); })[0]; map.setView(m.getLatLng(), 13); m.openPopup(); mapEl.scrollIntoView({ behavior: 'smooth', block: 'center' }); });
      });
    }
    document.querySelectorAll('[data-sim]').forEach(function (b) {
      b.setAttribute('aria-pressed', String((b.getAttribute('data-sim') || null) === sim));
      b.addEventListener('click', function () { sim = b.getAttribute('data-sim') || null; try { sim ? localStorage.setItem('kontyos-demo-sim', sim) : localStorage.removeItem('kontyos-demo-sim'); } catch (e) {} document.querySelectorAll('[data-sim]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); paint(); });
    });
    paint();
    /* Telefonon a vásár-karusszel alapállása: a középső (3.) kártya középen, mindkét oldalon kilóg a szomszéd (Artúr, 11-03) */
    var centerFairs = function () {
      if (!window.matchMedia('(max-width:760px)').matches) return;
      var row = document.getElementById('fair-row'); if (!row) return;
      var c = row.children[2]; if (!c) return;
      var rr = row.getBoundingClientRect(), cr = c.getBoundingClientRect();
      row.scrollLeft += (cr.left + cr.width / 2) - (rr.left + rr.width / 2);
    };
    centerFairs(); window.addEventListener('load', centerFairs);
    document.querySelectorAll('[data-fair-more]').forEach(function (b) {
      var row = document.getElementById(b.getAttribute('aria-controls')); if (!row) return;
      b.addEventListener('click', function () { var o = row.classList.toggle('open'); b.setAttribute('aria-expanded', String(o)); b.textContent = o ? 'Kevesebb vásár' : 'További vásárok (' + (row.children.length - 5) + ')'; });
    });
    var ff = document.querySelector('[data-fair-form]');
    if (ff) {
      var all = ff.querySelector('[data-fair-all]');
      all.addEventListener('change', function () { ff.querySelectorAll('[name=fair]').forEach(function (c) { c.checked = all.checked; }); });
      ff.addEventListener('submit', function (e) {
        e.preventDefault();
        var mail = ff.querySelector('[name=email]'), ok = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail.value.trim());
        mail.closest('.field').classList.toggle('err', !ok);
        var picked = Array.prototype.slice.call(ff.querySelectorAll('[name=fair]:checked')).map(function (c) { return FAIRS.filter(function (f) { return f.id === c.value; })[0]; });
        var msg = ff.querySelector('[data-fair-ok]');
        if (!ok) return;
        if (!picked.length) { msg.textContent = 'Jelölj be legalább egy vásárt.'; return; }
        try { localStorage.setItem('kontyos-demo-fairsub', JSON.stringify({ email: mail.value, fairs: picked.map(function (f) { return f.id; }) })); } catch (e2) {}
        msg.innerHTML = '✓ Feliratkoztál: <b>' + picked.map(function (f) { return esc(f.city); }).join(', ') + '</b>. Ütemezett e-mailek: ' + picked.map(function (f) { var a = day(f.start), b = new Date(a); b.setDate(a.getDate() - 3); return esc(f.city) + ' – ' + dfmt(b) + ' és ' + dfmt(a); }).join('; ') + ' <small>(Demó – élesben a levelezőrendszer küldi.)</small>';
      });
    }
  }

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

  /* Logó: fekete vagy fehér változat a mögötte lévő háttér világossága alapján */
  function lum(c) {
    var m = c && c.match(/rgba?\(([\d.]+)[, ]+([\d.]+)[, ]+([\d.]+)(?:[, /]+([\d.]+))?/);
    if (!m) return null;
    if (m[4] !== undefined && parseFloat(m[4]) < 0.5) return null;
    var v = [m[1], m[2], m[3]].map(function (x) { x = x / 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); });
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
  }
  function bgLum(el) {
    var cs = getComputedStyle(el), l = lum(cs.backgroundColor);
    if (l !== null) return l;
    if (cs.backgroundImage && cs.backgroundImage !== 'none' && cs.backgroundImage.indexOf('url(') > -1) return 0.1; // fotó háttér: sötétnek vesszük
    return null;
  }
  function logoTone() {
    document.querySelectorAll('.logo').forEach(function (logo) {
      var r = logo.getBoundingClientRect(), l = null;
      if (!r.width) return;
      var x = r.left + r.width / 2, y = r.top + r.height / 2;
      if (y > 0 && y < innerHeight && x > 0 && x < innerWidth) {
        var stack = document.elementsFromPoint(x, y);
        for (var i = 0; i < stack.length && l === null; i++) {
          if (logo.contains(stack[i])) continue;
          l = bgLum(stack[i]);
        }
      } else {
        for (var el = logo.parentElement; el && l === null; el = el.parentElement) l = bgLum(el);
      }
      if (l === null) l = 1;
      logo.classList.toggle('on-dark', l < 0.179); // ahol a fehér nagyobb kontrasztot ad, mint a fekete
    });
  }
  var ltRaf = 0;
  function logoToneSoon() { if (!ltRaf) ltRaf = requestAnimationFrame(function () { ltRaf = 0; logoTone(); }); }
  logoTone();
  window.addEventListener('load', logoTone);
  window.addEventListener('resize', logoToneSoon);
  window.addEventListener('scroll', logoToneSoon, { passive: true });
  document.addEventListener('click', function () { setTimeout(logoTone, 60); });
})();
