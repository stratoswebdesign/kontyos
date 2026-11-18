{# Kontyos – termékértékelés írása a Kontyos-termékoldalakon. KÉZZEL ÍRT (nem a src/shoprenter.py generálja).
   A product.tpl a ky-p-* snippet UTÁN tölti be:  {% include 'snippets/ky-review.tpl' %}
   Miért kell: a Kontyos-termékoldal a Párizs teljes tartalmát lecseréli, így a Shoprenter beépített értékelő űrlapja
   (position_4 → productreview modul) eltűnt – az értékelést kérő levélből érkező vásárló nem tudott véleményt írni.
   Működés: a beépített modul rejtve renderelődik (product_id + CSRF-token), a látható Kontyos-űrlap a JS-sel bekerül az
   #ertekelesek szekcióba, és ugyanarra a Shoprenter-végpontra küld, mint a gyári űrlap:
   POST /index.php?route=product/productreview/addreview → JSON {data:{success|error|redirect_to|success_auto_accept}, formHTML}.
   A beküldött vélemény a Shoprenter admin › Termék értékelések listájába kerül (a bolt beállítása: automatikus elfogadás).
   Szabályok (Shoprenter): név 3–25 karakter, szöveg 25–1000 karakter, csillag kötelező, közzétételi hozzájárulás kötelező.
   Horgony: #ertekeles-irasa (a régi #review_form / #review is ide visz). #}
<script>(function(){var h=location.hash;if(h==='#review_form'||h==='#review'||h==='#productreview'){try{history.replaceState(null,'',location.pathname+location.search+'#ertekeles-irasa')}catch(e){}}})();</script>
<div class="ky-rv-native" hidden aria-hidden="true">{{ position_4 }}</div>
<template id="ky-rv-tpl">
<div class="ky-rv" id="ertekeles-irasa">
  <div class="ky-rv-cta">
    <div class="ky-rv-ctatx"><b>Kóstoltad már?</b><span>Mondd el, hogy ízlett – a véleményed a következő vásárlónak is segít választani.</span></div>
    <button type="button" class="ky-rv-btn ky-rv-open">Írd meg a véleményed</button>
  </div>
  <form class="ky-rv-form" hidden novalidate>
    <p class="ky-rv-title">Milyen volt?</p>
    <div class="ky-rv-field">
      <span class="ky-rv-lab" id="ky-rv-starlab">Értékelésed</span>
      <div class="ky-rv-stars" role="radiogroup" aria-labelledby="ky-rv-starlab">
        <label title="Rossz"><input type="radio" name="ky_rating" value="1"><span aria-hidden="true">★</span><i>1 csillag – rossz</i></label>
        <label title="Gyenge"><input type="radio" name="ky_rating" value="2"><span aria-hidden="true">★</span><i>2 csillag – gyenge</i></label>
        <label title="Rendben"><input type="radio" name="ky_rating" value="3"><span aria-hidden="true">★</span><i>3 csillag – rendben</i></label>
        <label title="Jó"><input type="radio" name="ky_rating" value="4"><span aria-hidden="true">★</span><i>4 csillag – jó</i></label>
        <label title="Kitűnő"><input type="radio" name="ky_rating" value="5"><span aria-hidden="true">★</span><i>5 csillag – kitűnő</i></label>
        <em class="ky-rv-starword" aria-hidden="true"></em>
      </div>
    </div>
    <label class="ky-rv-field"><span class="ky-rv-lab">Neved <small>(így jelenik meg, pl. „Kiss T.”)</small></span>
      <input type="text" name="ky_name" maxlength="25" autocomplete="name"></label>
    <label class="ky-rv-field"><span class="ky-rv-lab">Véleményed</span>
      <textarea name="ky_text" rows="5" maxlength="1000" placeholder="Mikor bontottad ki, kivel kóstoltad, mihez illett? Megérkezett rendben?"></textarea>
      <small class="ky-rv-count" aria-live="polite"></small></label>
    <label class="ky-rv-gdpr"><input type="checkbox" name="ky_gdpr"><span>Hozzájárulok, hogy a Kontyos Borház Kft. a véleményemet a weboldalon nyilvánosan közzétegye. Kijelentem, hogy az <a href="/aszf" target="_blank" rel="noopener">ÁSZF</a>-et és az <a href="/adatkezelesi-tajekoztato" target="_blank" rel="noopener">adatkezelési tájékoztatót</a> elolvastam, és tudom, hogy a hozzájárulásomat bármikor visszavonhatom.</span></label>
    <div class="ky-rv-msg" role="alert" aria-live="assertive"></div>
    <div class="ky-rv-actions">
      <button type="submit" class="ky-rv-btn ky-rv-send">Vélemény elküldése</button>
      <button type="button" class="ky-rv-cancel">Mégse</button>
    </div>
  </form>
  <div class="ky-rv-done" hidden role="status">
    <b>Köszönjük a véleményed!</b>
    <span>Megkaptuk – köszönjük, hogy segítesz a következő vásárlónak választani.</span>
  </div>
</div>
</template>
<style>
#ertekelesek.ky-rv-own{box-sizing:border-box;max-width:1240px;margin:0 auto;padding:64px 20px 40px;display:flex;flex-direction:column;gap:20px;color:#1B2A5C}
#ertekelesek.ky-rv-own .pd-lab{margin:0;font-size:12px;font-weight:800;letter-spacing:.16em;color:#C8282E}
#ertekelesek.ky-rv-own .pd-noreview{background:#fff;border:1px dashed #1B2A5C;border-radius:4px;padding:22px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;font-size:15px}
#ertekelesek .ky-rv{margin-top:6px;color:#1B2A5C;font-family:var(--sans,Montserrat,system-ui,sans-serif)}
#ertekelesek .ky-rv [hidden]{display:none!important}
#ertekelesek .ky-rv-cta{background:#fff;border:1px dashed #1B2A5C;border-radius:4px;padding:20px 22px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px}
#ertekelesek .ky-rv-ctatx{display:flex;flex-direction:column;gap:4px;font-size:15px;line-height:1.5}
#ertekelesek .ky-rv-ctatx b{font-weight:800}
#ertekelesek .ky-rv-btn{appearance:none;border:0;border-radius:999px;background:var(--ky-rv-acc,#1B2A5C);color:#fff;font:800 13px/1 var(--sans,Montserrat,sans-serif);letter-spacing:.08em;text-transform:uppercase;padding:15px 24px;cursor:pointer;transition:filter .2s,transform .2s}
#ertekelesek .ky-rv-btn:hover{filter:brightness(1.12)}#ertekelesek .ky-rv-btn:active{transform:translateY(1px)}
#ertekelesek .ky-rv-btn:focus-visible,#ertekelesek .ky-rv-cancel:focus-visible,#ertekelesek .ky-rv-stars label:focus-within{outline:2px solid var(--ky-rv-acc,#1B2A5C);outline-offset:3px}
#ertekelesek .ky-rv-btn[disabled]{opacity:.6;cursor:progress}
#ertekelesek .ky-rv-form{background:#fff;border:1px solid #E2DACB;border-radius:4px;padding:26px 24px;display:flex;flex-direction:column;gap:18px;max-width:760px}
#ertekelesek .ky-rv-title{margin:0;font-family:var(--serif,Georgia,serif);font-weight:800;font-size:26px;line-height:1.15;text-transform:uppercase}
#ertekelesek .ky-rv-field{display:flex;flex-direction:column;gap:7px}
#ertekelesek .ky-rv-lab{font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
#ertekelesek .ky-rv-lab small{font-weight:500;letter-spacing:0;text-transform:none;font-size:12px;color:#6A6F7E}
#ertekelesek .ky-rv input[type=text],#ertekelesek .ky-rv textarea{box-sizing:border-box;width:100%;border:1px solid #C9C2B4;border-radius:4px;background:#fff;color:#1B2A5C;font:400 16px/1.5 var(--text,Lora,Georgia,serif);padding:12px 14px}
#ertekelesek .ky-rv textarea{resize:vertical;min-height:120px}
#ertekelesek .ky-rv input[type=text]:focus,#ertekelesek .ky-rv textarea:focus{outline:none;border-color:var(--ky-rv-acc,#1B2A5C);box-shadow:0 0 0 3px rgba(27,42,92,.12)}
#ertekelesek .ky-rv-count{font-size:12px;color:#6A6F7E}
#ertekelesek .ky-rv-stars{display:flex;align-items:center;gap:2px}
#ertekelesek .ky-rv-stars label{position:relative;cursor:pointer;line-height:1;padding:2px}
#ertekelesek .ky-rv-stars input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
#ertekelesek .ky-rv-stars span{font-size:34px;color:#D9D3C7;transition:color .15s,transform .15s;display:block}
#ertekelesek .ky-rv-stars label.on span{color:#E8A93B}
#ertekelesek .ky-rv-stars label:hover span{transform:scale(1.12)}
#ertekelesek .ky-rv-stars i{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
#ertekelesek .ky-rv-starword{font-style:normal;font-size:14px;margin-left:10px;color:#6A6F7E}
#ertekelesek .ky-rv-gdpr{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.5;cursor:pointer}
#ertekelesek .ky-rv-gdpr input{margin:3px 0 0;width:18px;height:18px;flex:none;accent-color:var(--ky-rv-acc,#1B2A5C)}
#ertekelesek .ky-rv-gdpr a{color:inherit;text-decoration:underline}
#ertekelesek .ky-rv-msg{font-size:14px;line-height:1.5;color:#B3261E}
#ertekelesek .ky-rv-msg:empty{display:none}
#ertekelesek .ky-rv-actions{display:flex;flex-wrap:wrap;align-items:center;gap:16px}
#ertekelesek .ky-rv-cancel{appearance:none;border:0;background:none;color:#1B2A5C;font:600 14px/1 var(--sans,Montserrat,sans-serif);text-decoration:underline;cursor:pointer;padding:8px 0}
#ertekelesek .ky-rv-done{background:#fff;border:1px solid #E2DACB;border-left:4px solid #2E7D4F;border-radius:4px;padding:20px 22px;display:flex;flex-direction:column;gap:4px;font-size:15px;line-height:1.5}
#ertekelesek .ky-rv-done b{font-weight:800}
#ertekelesek .ky-rv-bad{border-color:#B3261E!important}
@media (max-width:600px){ #ertekelesek .ky-rv-form{padding:20px 16px}#ertekelesek .ky-rv-cta .ky-rv-btn,#ertekelesek .ky-rv-send{width:100%}#ertekelesek .ky-rv-title{font-size:22px}}
</style>
<script>
(function(){
  var ENDPOINT = '/index.php?route=product/productreview/addreview';
  var WORDS = ['', 'Rossz', 'Gyenge', 'Rendben', 'Jó', 'Kitűnő'];
  function ready(fn){ if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  function nativeForm(){ return document.querySelector('.ky-rv-native #review_form'); }
  ready(function(){
    var tpl = document.getElementById('ky-rv-tpl');
    var sec = document.getElementById('ertekelesek');
    if (!tpl || !nativeForm()) return;                   // nincs gyári modul → nem rajzolunk üres űrlapot
    if (!sec) {                                          // pl. koktélcsomagok: nincs vélemény-szekció → saját, „még nincs értékelés” állapotban
      var page = document.querySelector('main .ky[data-page="product"]');
      if (!page) return;
      sec = document.createElement('section');
      sec.id = 'ertekelesek'; sec.className = 'pd-wrap pd-reviews ky-rv-own';
      sec.innerHTML = '<p class="pd-lab">VÁSÁRLÓI VÉLEMÉNYEK</p><div class="pd-noreview"><span>Erről a termékről még nincs értékelés.</span><b>Kóstoltad? Írd meg elsőként!</b></div>';
      var after = page.querySelector('section.p-info') || page.querySelector('main > section:last-of-type');
      if (after && after.parentNode) after.parentNode.insertBefore(sec, after.nextSibling); else (page.querySelector('main') || page).appendChild(sec);
    }
    var box = tpl.content.firstElementChild.cloneNode(true);
    var lab = sec.querySelector('.pd-lab');
    if (lab) box.style.setProperty('--ky-rv-acc', getComputedStyle(lab).color);
    var noRev = sec.querySelector('.pd-noreview');
    var cta = box.querySelector('.ky-rv-cta');
    if (noRev) {                                         // még nincs vélemény: a meglévő „Írd meg elsőként” doboz kapja a gombot
      noRev.appendChild(box.querySelector('.ky-rv-open'));
      cta.parentNode.removeChild(cta);
      sec.insertBefore(box, noRev.nextSibling);
    } else {
      sec.appendChild(box);
    }
    var form = box.querySelector('.ky-rv-form'), msg = box.querySelector('.ky-rv-msg'), done = box.querySelector('.ky-rv-done');
    var send = box.querySelector('.ky-rv-send'), count = box.querySelector('.ky-rv-count'), word = box.querySelector('.ky-rv-starword');
    var openBtn = sec.querySelector('.ky-rv-open');
    var stars = [].slice.call(box.querySelectorAll('.ky-rv-stars label'));
    var nameIn = form.querySelector('[name=ky_name]'), textIn = form.querySelector('[name=ky_text]'), gdprIn = form.querySelector('[name=ky_gdpr]');
    var nf = nativeForm(), nfName = nf.querySelector('[name=name]');
    if (nfName && nfName.value) nameIn.value = nfName.value.slice(0, 25);   // bejelentkezett vevő neve

    function rating(){ var c = form.querySelector('[name=ky_rating]:checked'); return c ? +c.value : 0; }
    function paint(n){ stars.forEach(function(l, i){ l.classList.toggle('on', i < n); }); word.textContent = WORDS[n] || ''; }
    stars.forEach(function(l, i){
      l.addEventListener('mouseenter', function(){ paint(i + 1); });
      l.querySelector('input').addEventListener('change', function(){ paint(rating()); });
    });
    box.querySelector('.ky-rv-stars').addEventListener('mouseleave', function(){ paint(rating()); });
    function counter(){ var n = textIn.value.trim().length; count.textContent = n < 25 ? ('Még legalább ' + (25 - n) + ' karakter') : (n + ' / 1000 karakter'); }
    textIn.addEventListener('input', counter); counter();

    function open(scroll){
      form.hidden = false; done.hidden = true;
      if (openBtn) openBtn.hidden = true;
      if (cta.parentNode) cta.hidden = true;
      if (scroll) {
        var top = box.getBoundingClientRect().top + window.pageYOffset - 110;
        window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
      }
      setTimeout(function(){ try { (rating() ? nameIn : form.querySelector('[name=ky_rating]')).focus({ preventScroll: true }); } catch (e) {} }, 350);
    }
    function close(){ form.hidden = true; if (openBtn) openBtn.hidden = false; if (cta.parentNode) cta.hidden = false; }
    if (openBtn) openBtn.addEventListener('click', function(){ open(false); });
    box.querySelector('.ky-rv-cancel').addEventListener('click', close);
    // a fenti „Még nincs értékelés – legyél te az első” link az űrlapot nyissa
    [].forEach.call(document.querySelectorAll('a.pd-stars'), function(a){
      if (/első/.test(a.textContent)) a.setAttribute('href', '#ertekeles-irasa');
    });
    function fromHash(){ if (location.hash === '#ertekeles-irasa') open(true); }
    window.addEventListener('hashchange', fromHash);
    fromHash();

    function bad(el, on){ if (el) el.classList.toggle('ky-rv-bad', !!on); }
    function validate(){
      var errs = [], n = nameIn.value.trim(), t = textIn.value.trim();
      bad(box.querySelector('.ky-rv-stars'), false); bad(nameIn, false); bad(textIn, false);
      if (!rating()) errs.push('Válaszd ki, hány csillagot adsz.');
      if (n.length < 3 || n.length > 25) { errs.push('A neved 3–25 karakter legyen (pl. „Kiss T.”).'); bad(nameIn, true); }
      if (t.length < 25 || t.length > 1000) { errs.push('A vélemény legalább 25 karakter legyen – pár mondat bőven elég.'); bad(textIn, true); }
      if (!gdprIn.checked) errs.push('A közzétételhez pipáld be a hozzájárulást.');
      return errs;
    }
    function showErr(list){ msg.innerHTML = ''; list.forEach(function(s){ var p = document.createElement('div'); p.textContent = s; msg.appendChild(p); }); }

    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      var errs = validate();
      if (errs.length) { showErr(errs); return; }
      showErr([]);
      var nf = nativeForm();
      if (!nf) { showErr(['Az értékelő űrlap nem töltődött be. Frissítsd az oldalt, és próbáld újra.']); return; }
      var body = new URLSearchParams();
      [].forEach.call(nf.querySelectorAll('input[type=hidden], input[name=phone_number]'), function(i){ if (i.name) body.append(i.name, i.value); });
      body.set('name', nameIn.value.trim());
      body.set('text', textIn.value.trim());
      body.set('rating', String(rating()));
      body.set('gdpr_consent', 'on');
      send.disabled = true; send.textContent = 'Küldés…';
      fetch(ENDPOINT, { method: 'POST', credentials: 'same-origin',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest' },
        body: body.toString() })
      .then(function(r){ return r.json(); })
      .then(function(res){
        var d = (res && res.data) || {};
        if (res && res.formHTML) {                       // a válasz <div class="form"> – a gyári űrlap szülőjét cseréli (friss CSRF-token)
          var tmp = document.createElement('div');
          tmp.innerHTML = res.formHTML;
          res._errs = [].map.call(tmp.querySelectorAll('.error-list li'), function(e){ return e.textContent.trim(); })
            .filter(function(s, i, a){ return s && a.indexOf(s) === i; });
          var fresh = tmp.querySelector('.form') || tmp.firstElementChild;
          if (fresh && fresh.querySelector('#review_form') && nf.parentNode && nf.parentNode.parentNode) nf.parentNode.parentNode.replaceChild(fresh, nf.parentNode);
        }
        if (d.redirect_to) { location.href = d.redirect_to; return; }
        if (d.success || d.success_auto_accept || (d.error === false)) {
          form.hidden = true; done.hidden = false;
          if (window.dataLayer) window.dataLayer.push({ event: 'ky_review_submitted', ky_rating: rating() });
          try { done.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) {}
          return;
        }
        showErr(res._errs && res._errs.length ? res._errs : ['Most nem sikerült elküldeni. Próbáld újra, vagy írj nekünk: webshop@kontyos.hu']);
      })
      .catch(function(){ showErr(['Most nem sikerült elküldeni (hálózati hiba). Próbáld újra, vagy írj nekünk: webshop@kontyos.hu']); })
      .then(function(){ send.disabled = false; send.textContent = 'Vélemény elküldése'; });
    });
  });
})();
</script>
