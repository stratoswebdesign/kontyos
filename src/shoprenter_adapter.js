/* Kontyos ↔ Shoprenter kosár-adapter
   A demó data-add gombjai itt a VALÓDI Shoprenter-kosárba tesznek.
   - product_id: window.KY_PID[cikkszám] (a sandboxból töltjük ki: sku → product_id), vagy a termékoldalon a rejtett Shoprenter-űrlapból.
   - végpont: a rejtett Shoprenter-űrlap action-je (productaddtocart) – így nem kell kitalálni az URL-t.
   - ha nincs product_id: a termék oldalára visz (biztonságos tartalék).
   A sandboxban ellenőrizendő: a kosár-végpont válasza és a darabszám frissítése. */
(function () {
  if (!window.KY_SHOPRENTER) return;
  window.KY_PID = window.KY_PID || {};
  // A demóban body-szintű osztályok (overlay-head, pdp-…) és data-page a fejléc/lábléc .ky-elemére is
  function syncShell() {
    var main = document.querySelector('main .ky');
    if (!main) return;
    document.querySelectorAll('.ky-head, .ky-foot').forEach(function (el) {
      main.classList.forEach(function (c) { if (c !== 'ky') el.classList.add(c); });
      if (main.dataset.page) el.dataset.page = main.dataset.page;
    });
    // a Shoprenter kötelező fizetési logói a lábléc aljára (a demóban nincs külön sáv)
    var lg = document.querySelector('.ky-legal-logos'), fw = document.querySelector('.ky-foot footer .wrap');
    if (lg && fw && !fw.contains(lg)) fw.appendChild(lg);
    // a demóban a fejléc fölött álló sáv (pl. karácsonyi .xbar) a fejléc elé kerül
    var pre = main.querySelector(':scope > .ky-pre'), head = document.querySelector('.ky-head');
    if (pre && head && head.parentNode) {
      var w = document.createElement('div');
      w.className = main.className + ' ky-pre-wrap';
      if (main.dataset.page) w.dataset.page = main.dataset.page;
      while (pre.firstChild) w.appendChild(pre.firstChild);
      pre.remove();
      head.parentNode.insertBefore(w, head);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', syncShell); else syncShell();
  function srForm() { return document.querySelector('form[action*="cart"], form#product, .ky-sr-form form'); }
  function pidFor(sku) {
    if (window.KY_PID[sku]) return window.KY_PID[sku];
    var page = document.querySelector('.ky[data-sku]');
    var f = srForm();
    if (page && f && page.getAttribute('data-sku') === sku) { var i = f.querySelector('[name=product_id]'); if (i) return i.value; }
    return null;
  }
  // A Shoprenter kosármodulja (rejtve, .ky-sr-cart) – a darabszám a betétdíj-sorok nélkül, palackban
  function srCount() {
    var box = document.querySelector('.ky-sr-cart'); if (!box) return;
    var n = 0, rows = box.querySelectorAll('.cart-quantity');
    rows.forEach(function (q) {
      var p = q.parentElement;
      while (p && p !== box && !p.querySelector('.cart-product-name-link')) p = p.parentElement;
      var a = p && p.querySelector('.cart-product-name-link');
      if (a && /^\s*Betétdíj/i.test(a.textContent)) return;
      var m = q.textContent.match(/\d+/); n += m ? parseInt(m[0], 10) : 1;
    });
    if (!rows.length) { var c = box.querySelector('.cart-product-count'); n = c ? parseInt(c.textContent, 10) || 0 : 0; }
    document.querySelectorAll('[data-cart-count]').forEach(function (b) { b.textContent = n; });
  }
  function srRefresh() {
    var hx = document.querySelector('.ky-sr-cart hx\\:include, .ky-sr-cart [src*="_fragment"]');
    var src = hx && hx.getAttribute('src');
    if (!src) { srCount(); return; }
    fetch(src, { credentials: 'same-origin' }).then(function (r) { return r.text(); }).then(function (t) { hx.innerHTML = t; srCount(); });
  }
  window.KY_SR_REFRESH = srRefresh;
  (function watch() {
    var box = document.querySelector('.ky-sr-cart');
    if (!box) { document.addEventListener('DOMContentLoaded', watch); return; }
    srCount();
    if (window.MutationObserver) new MutationObserver(function () { clearTimeout(watch.t); watch.t = setTimeout(srCount, 80); }).observe(box, { childList: true, subtree: true });
  })();
  // Kosároldal: a Shoprenter (Vue) kosara rejtve tovább dolgozik, fölötte a demó kosara jelenik meg az ő adataival
  (function srCart() {
    var sr = document.querySelector('.sr-cart-page-content');
    if (!sr || !window.KY_CART_HTML) return;
    window.KY_SR_CART = true;
    document.documentElement.classList.add('ky-cart-on');
    var box = document.createElement('div');
    box.className = 'ky ky-cart'; box.setAttribute('data-page', 'cart');
    box.innerHTML = window.KY_CART_HTML;
    sr.parentNode.insertBefore(box, sr);
    box.querySelectorAll('[data-need-cart]').forEach(function (x) { x.removeAttribute('data-need-cart'); });
    box.querySelectorAll('[data-coupon-wrap]').forEach(function (x) { x.hidden = true; });  // kupon: a Shoprenter pénztárában
    var K = window.KONTYOS.p, LIMIT = 25000, byUrl = {};
    Object.keys(K).forEach(function (id) { if (K[id].url) byUrl[K[id].url.split('#')[0]] = id; });
    var fmt = function (n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' Ft'; };
    var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var ft = function (el) { var m = el && el.textContent.replace(/ /g, ' ').match(/(\d[\d. ]*)\s*Ft/); return m ? parseInt(m[1].replace(/\D/g, ''), 10) : 0; };
    var path = function (h) { try { return new URL(h, location.href).pathname; } catch (e) { return h; } };
    var rows = [];
    function read() {
      rows = [];
      // termékenként egy <tbody> (keskeny kijelzőn a mennyiség/ár egy külön mobil-sorban van)
      sr.querySelectorAll('.sr-cart-table tbody').forEach(function (tr) {
        var a = tr.querySelector('.ac-prod-name'), nm = a ? a.textContent.trim() : '';
        if (!nm) return;
        var href = a.getAttribute('href') || '', id = byUrl[path(href)] || null, qi = tr.querySelector('.ac-quantity'), im = tr.querySelector('.ac-prod-image');
        rows.push({ tr: tr, name: nm, href: href, id: id, q: parseInt(qi && qi.value, 10) || 1, amt: ft(tr.querySelector('.ac-prod-current-price')),
          img: im && im.getAttribute('src'), drs: /^\s*Betétdíj/i.test(nm) });
      });
    }
    function next() { var b = sr.querySelector('.ac-next-to-checkout'); return (b && b.getAttribute('href')) || '/checkout'; }
    function render() {
      read();
      var root = box.querySelector('#cart-root'), side = box.querySelector('#cart-side'), items = rows.filter(function (r) { return !r.drs; });
      if (!root) return;
      if (!items.length) {
        root.innerHTML = '<div class="box" style="text-align:center;padding:48px 22px"><p class="k-h2" style="font-size:34px">A kosarad üres.</p><p class="muted" style="margin:10px 0 22px">Nézz körül a 100%-os gyümölcsborok között.</p><a class="k-btn blue" href="/gyumolcsbor">Gyümölcsborok</a></div>';
        if (side) side.hidden = true; return;
      }
      if (side) side.hidden = false;
      var sub = 0, drs = 0;
      rows.forEach(function (r) { if (r.drs) drs += r.amt; else sub += r.amt; });
      var free = sub >= LIMIT, left = Math.max(0, LIMIT - sub), pct = Math.min(100, Math.round(sub / LIMIT * 100));
      var lines = rows.map(function (r, i) {
        if (r.drs) return '';
        var p = r.id && K[r.id], img = (p && p.img) || r.img, tint = (p && p.tint) || '#F8F4EC';
        return '<div class="line"><a class="im" style="--tint:' + tint + '" href="' + esc(r.href) + '">' + (img ? '<img src="' + esc(img) + '" alt="">' : '') + '</a>' +
          '<div class="nm"><a href="' + esc(r.href) + '">' + esc(p ? p.n : r.name) + '</a><small>' + esc(p && p.sub || '') + '</small><button class="rm" type="button" data-sr-rm="' + i + '">Törlés</button></div>' +
          '<div class="q"><button type="button" aria-label="Kevesebb" data-sr-q="' + i + '" data-d="-1">−</button><span>' + r.q + '</span><button type="button" aria-label="Több" data-sr-q="' + i + '" data-d="1">+</button></div>' +
          '<div class="sum">' + fmt(r.amt) + '</div></div>';
      }).join('');
      root.innerHTML = '<div class="box" style="display:flex;flex-direction:column;gap:12px"><p class="serif" style="font-size:24px">' + (free ? 'Ingyenes a szállítás. 🎉' : 'Még <b style="color:#C8284E">' + fmt(left) + '</b>, és ingyen visszük.') + '</p><div class="bar" style="height:10px"><i style="width:' + (free ? 100 : pct) + '%"></i></div></div>' +
        '<div class="box">' + lines + '</div>';
      var grand = ft(sr.querySelector('.ac-gross-sum')) || (sub + drs);
      box.querySelectorAll('[data-sum]').forEach(function (el) { el.textContent = fmt(sub); });
      box.querySelectorAll('[data-drsrow]').forEach(function (el) { el.hidden = !drs; });
      box.querySelectorAll('[data-drs]').forEach(function (el) { el.textContent = fmt(drs); });
      box.querySelectorAll('[data-disc]').forEach(function (el) { el.hidden = true; });
      box.querySelectorAll('[data-shipfee]').forEach(function (el) { el.textContent = free ? 'Ingyenes' : '1 800 Ft-tól'; });
      box.querySelectorAll('[data-grand]').forEach(function (el) { el.innerHTML = fmt(grand) + (free ? '' : '<small>+ szállítás (1 800 Ft-tól)</small>'); });
      var to = next();
      box.querySelectorAll('a[href*="checkout/cart"]').forEach(function (x) { if (!x.closest('.steps li.on')) x.setAttribute('href', to); });
      var cu = box.querySelector('#cart-ups');
      if (cu && window.kyUps) {
        var inCart = items.map(function (r) { return r.id; }).filter(Boolean), pool = [];
        inCart.forEach(function (id) { (K[id].ups || []).forEach(function (i) { if (pool.indexOf(i) < 0) pool.push(i); }); });
        ['kontyos-borospohar', 'don-cherry-gyumolcse', 'friss-eper', 'piri-mama-bogreje'].forEach(function (i) { if (pool.indexOf(i) < 0) pool.push(i); });
        cu.innerHTML = window.kyUps(pool, inCart);
      }
    }
    box.addEventListener('click', function (e) {
      var q = e.target.closest('[data-sr-q]'), rm = e.target.closest('[data-sr-rm]');
      var r = q ? rows[+q.getAttribute('data-sr-q')] : rm ? rows[+rm.getAttribute('data-sr-rm')] : null;
      if (!r) return;
      e.preventDefault();
      var up = q && q.getAttribute('data-d') === '1';
      var t = up ? (r.tr.querySelector('.ac-quantity-up') || r.tr.querySelector('.input-group-btn-plus button')) : (q && r.q > 1) ? (r.tr.querySelector('.ac-quantity-down button') || r.tr.querySelector('.ac-quantity-down')) : r.tr.querySelector('.ac-prod-delete');
      if (t) t.click();
    });
    var tm;
    if (window.MutationObserver) new MutationObserver(function () { clearTimeout(tm); tm = setTimeout(render, 60); }).observe(sr, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['value'] });
    render();
    window.addEventListener('load', render);
  })();
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-add]'); if (!a) return;
    var id = a.getAttribute('data-add'), sku = a.getAttribute('data-sku') || ((window.KONTYOS.p[id] || {}).sku) || '';
    var q = 1, qs = a.getAttribute('data-qty-from');
    if (qs) { var qe = document.querySelector(qs); if (qe) q = parseInt(qe.getAttribute('data-value') || qe.textContent, 10) || 1; }
    var pid = pidFor(sku);
    e.preventDefault(); e.stopImmediatePropagation();
    if (!pid) { var p = window.KONTYOS.p[id]; if (p && p.url) location.href = p.url; return; }
    var f = srForm(), action = (f && f.getAttribute('action')) || '/index.php?route=checkout/cart';
    var body = new FormData(); body.append('product_id', pid); body.append('quantity', q);
    fetch(action, { method: 'POST', body: body, credentials: 'same-origin' }).then(function () {
      a.classList.add('ky-added'); setTimeout(function () { a.classList.remove('ky-added'); }, 1500);
      if (window.KY_SR_CART) { location.reload(); return; }
      srRefresh();
    });
  }, true);
})();
