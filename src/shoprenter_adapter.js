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
  function srCount() {
    var el = document.querySelector('.ky-sr-cart [class*="count"], .ky-sr-cart .cart-count, .ky-sr-cart [data-cart-count]');
    var n = el ? parseInt(el.textContent, 10) : NaN;
    if (!isNaN(n)) document.querySelectorAll('[data-cart-count]').forEach(function (b) { b.textContent = n; });
  }
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
      try { if (window.ShopRenter && ShopRenter.cart && ShopRenter.cart.refresh) ShopRenter.cart.refresh(); } catch (er) {}
      setTimeout(srCount, 600);
    });
  }, true);
  document.addEventListener('DOMContentLoaded', srCount);
})();
