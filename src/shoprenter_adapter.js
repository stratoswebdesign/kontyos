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
      srRefresh();
    });
  }, true);
})();
