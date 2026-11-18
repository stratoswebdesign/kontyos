"""PIRI Mama landing – kontyos.hu/pirimama (Stratos, 2026-11-17).

A Graphasel Lovable-ben készült landingjének (sticky-visions-app) statikus átültetése a webshopba:
ugyanaz a szerkezet és látványvilág, de
- a „Vásárlás” gomb valódi kosárba tesz (data-add → Shoprenter-kosár), mellette Részletek-panel a valós termékadatokkal;
- a vásárlista a webshop közös vásár-adataiból jön (FAIRS / KONTYOS_FAIRS – egy forrás a Vásárok oldallal);
- a kapcsolati űrlap helyett hírlevél (HIRLEVEL5) + elérhetőségek – a Lovable-űrlap a Graphasel adatbázisába írt;
- nincs React / framer-motion: a mozgás CSS + kevés natív JS, prefers-reduced-motion esetén kikapcsol.

A stílus az oldal saját <style> blokkjában van (.pm gyökér alatt) és a JS is az oldalon él, így élesben
nem kell a jsDelivr-re rögzített kontyos.css / kontyos.live.js-t újrakiadni.
A fejléc sötét változata: [data-page="pirimama"] (demó: body, Shoprenter: a .ky-head – a syncShell másolja)
és body:has(.pm) (JS nélkül is).
"""
import json

LIVE = 'https://www.kontyos.hu/'
# demó-id → éles SEO-URL (a JSON-LD-hez; a linkeket a shoprenter.py írja át)
LIVE_URL = {'piri-mama-forralt-bora': 'piri-mama-forralt-bora-1l', 'epres-piri-mama-forralt-bora': 'piri-mama-epres-forralt-bora-1l',
            'narancsos-piri-mama-forralt-bora': 'piri-mama-narancsos-forralt-bora-1l', 'piri-mama-forro-itala-0': 'piri-mama-forro-itala-0-alc'}

# Kártyák: a Graphasel színei (oklch → sRGB), sorrend és alcímek a landing szerint
CARDS = [
    dict(id='piri-mama-forralt-bora', t='Piri Mama', s='Forralt bora', bg='#5A5F88', bg2='#414463', deco='flake-gold',
         note='A bort sosem forraljuk: lassan melegítsd, legfeljebb 55–60 °C-ig.'),
    dict(id='epres-piri-mama-forralt-bora', t='Epres Piri Mama', s='Forralt bora', bg='#E54731', bg2='#AA3222', deco='snow-dots',
         note='A bort sosem forraljuk: lassan melegítsd, legfeljebb 55–60 °C-ig.'),
    dict(id='narancsos-piri-mama-forralt-bora', t='Narancsos Piri Mama', s='Forralt bora', bg='#F96817', bg2='#B94B0E', deco='ornament-gold', tag='Új',
         note='A bort sosem forraljuk: lassan melegítsd, legfeljebb 55–60 °C-ig.'),
    dict(id='piri-mama-forro-itala-0', t='Piri Mama', s='Forró itala 0%', bg='#5D7AB7', bg2='#4A6399', deco='flake-gold', tag='Alkoholmentes',
         note='Melegen és hidegen is finom. Felbontás után hűtőben tárold, és egy héten belül fogyaszd el.'),
]
SKIP_PARAMS = {'Évjárat', 'Édes/Száraz'}

USP = [
    ('usp-01', 'pm-swing', 'Zamatát a gyümölcs adja', 'Saját gyümölcsborainkból készül: meggyből, szilvából, eperből, narancsból és almából.'),
    ('usp-03', 'pm-float', 'Csak melegíteni kell', 'Otthon pár perc alatt kész – az adventi vásárok hangulata a konyhádban.'),
    ('usp-02', 'pm-sway', 'A tél fűszereivel', 'Valódi fahéj és szegfűszeg – Piri mama jól bevált receptje szerint.'),
    ('usp-04', 'pm-twinkle', 'Minden ízlésre', 'Klasszikus, epres, narancsos és alkoholmentes, 0%-os változatban is.'),
]
STORES = [('bolt-lidl', 'LIDL', 'h'), ('bolt-spar', 'SPAR', 'h'), ('bolt-eco-family', 'Ecofamily', 's'), ('bolt-cba', 'CBA', 'h')]
SUBNAV = [('termekek', 'Termékek'), ('miert-mas', 'Miért más?'), ('hol-kaphato', 'Hol kapható?'), ('tortenetunk', 'Történetünk'), ('webshop', 'Webshop')]

CSS = r'''
.pm{--pm-night:#080D1B;--pm-gold:#DBB879;--pm-gold-soft:#E3CFA5;--pm-rose:#DF466C;--pm-story:#1A1F1B;--pm-shop:#1C201B;--pm-stripe:#30384F;--pm-ink:#CDBB8B;
  position:relative;display:block;overflow-x:clip;background:var(--pm-night);color:var(--pm-gold-soft);font-family:var(--text);font-size:16px;line-height:1.6}
.pm *{box-sizing:border-box}
.pm img{max-width:100%;height:auto;display:block}
.pm p,.pm h1,.pm h2,.pm h3,.pm h4,.pm ul,.pm dl,.pm dd,.pm figure{margin:0;padding:0}
.pm ul{list-style:none}
.pm a{color:inherit}
.pm .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.pm .pm-eyebrow{font-family:var(--serif);font-weight:400;text-transform:uppercase;color:var(--pm-gold);text-align:center;font-size:clamp(17px,2.9vw,42px);letter-spacing:clamp(.34em,.85vw,.6em);padding-left:clamp(.34em,.85vw,.6em);line-height:1.25}
.pm .pm-sub-eyebrow{font-family:var(--serif);font-weight:400;text-transform:uppercase;color:var(--pm-gold);text-align:center;font-size:clamp(12px,2.08vw,23px);letter-spacing:clamp(.28em,.7vw,.5em);padding-left:clamp(.28em,.7vw,.5em);line-height:1.3}
.pm .pm-intro{max-width:620px;margin:22px auto 0;text-align:center;color:rgba(227,207,165,.82);font-size:clamp(15px,1.2vw,17px)}
.pm .pm-sec{position:relative;padding:clamp(72px,9vw,128px) 0}
.pm .pm-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:0 24px;border:1px solid rgba(219,184,121,.45);border-radius:3px;background:transparent;color:var(--pm-gold-soft);
  font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;line-height:1;text-decoration:none;cursor:pointer;transition:border-color .2s,background .2s,color .2s}
.pm .pm-btn:hover{border-color:var(--pm-gold);background:rgba(219,184,121,.08)}
.pm .pm-btn.gold{background:var(--pm-gold);border-color:var(--pm-gold);color:var(--pm-night)}
.pm .pm-btn.gold:hover{background:#E8C989;border-color:#E8C989}
.pm .pm-btn.dark{background:var(--pm-night);border-color:rgba(219,184,121,.3);box-shadow:0 10px 24px rgba(0,0,0,.35)}
.pm .pm-btn.dark:hover{border-color:rgba(219,184,121,.8)}
.pm .pm-btn svg{width:15px;height:15px;flex:none}
.pm :focus-visible{outline:2px solid var(--pm-gold);outline-offset:3px}
/* mozgás – a reveal csak JS mellett rejt */
@keyframes pm-float{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-10px) rotate(3deg)}}
@keyframes pm-swing{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}
@keyframes pm-sway{0%,100%{transform:rotate(-2deg)}50%{transform:rotate(3deg)}}
@keyframes pm-twinkle{0%,100%{opacity:.35;transform:scale(.9)}50%{opacity:1;transform:scale(1.08)}}
@keyframes pm-spin{to{transform:rotate(360deg)}}
@keyframes pm-marquee{from{transform:translateX(-50%)}to{transform:translateX(0)}}
@keyframes pm-wipe{from{opacity:0;clip-path:inset(0 100% 0 0);transform:translateX(-30px) rotate(-11deg)}to{opacity:1;clip-path:inset(0 0 0 0);transform:rotate(-6deg)}}
@keyframes pm-rise{from{opacity:0;transform:translateY(46px) scale(.97)}to{opacity:1;transform:none}}
@keyframes pm-fade{from{opacity:0}to{opacity:1}}
@keyframes pm-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(8px)}}
@keyframes pm-stir{0%,100%{transform:rotate(0)}25%{transform:rotate(7deg)}75%{transform:rotate(-5deg)}}
@keyframes pm-steam{0%{transform:translateY(0) scale(1);opacity:0}40%{opacity:.4}100%{transform:translateY(-95px) scale(1.9);opacity:0}}
@keyframes pm-glow{0%,100%{opacity:.7}50%{opacity:1}}
.pm .pm-float{animation:pm-float var(--dur,7s) ease-in-out var(--delay,0s) infinite}
.pm .pm-swing{transform-origin:50% 0;animation:pm-swing var(--dur,5s) ease-in-out var(--delay,0s) infinite}
.pm .pm-sway{transform-origin:80% 80%;animation:pm-sway var(--dur,8s) ease-in-out var(--delay,0s) infinite}
.pm .pm-twinkle{animation:pm-twinkle var(--dur,3.5s) ease-in-out var(--delay,0s) infinite}
.pm .pm-spin{animation:pm-spin var(--dur,40s) linear infinite}
.pm.pm-js [data-reveal]{opacity:0;transform:translateY(28px);transition:opacity .8s cubic-bezier(.22,1,.36,1),transform .8s cubic-bezier(.22,1,.36,1);transition-delay:var(--d,0s)}
.pm.pm-js [data-reveal].pm-in{opacity:1;transform:none}
/* ---- hero ---- */
.pm .pm-hero{position:relative;z-index:2;min-height:min(100svh,980px);display:flex;align-items:flex-end;justify-content:center;overflow:hidden;background:var(--pm-night)}
.pm .pm-hero-ph{position:absolute;left:0;right:0;top:-6%;bottom:6%;will-change:transform}
@media (min-width:768px){.pm .pm-hero-ph{top:-22%;bottom:22%}}
.pm .pm-hero-ph img{width:100%;height:100%;object-fit:cover;object-position:44% 100%;animation:pm-fade 1.6s ease both}
@media (min-width:768px){.pm .pm-hero-ph img{object-position:72% 100%}}
.pm .pm-hero:after{content:"";position:absolute;inset:auto 0 0;height:62%;background:linear-gradient(to top,var(--pm-night) 8%,rgba(8,13,27,.82) 45%,rgba(8,13,27,0));pointer-events:none}
.pm .pm-hero:before{content:"";position:absolute;inset:0 0 auto;height:30%;z-index:1;background:linear-gradient(to bottom,rgba(8,13,27,.6),rgba(8,13,27,0));pointer-events:none}
.pm .pm-hero .fall{z-index:2}
.pm .pm-hero-in{position:relative;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center;padding:clamp(150px,22vh,260px) var(--gutter) clamp(52px,9vh,120px)}
.pm .pm-hl{position:relative;will-change:transform}
.pm .pm-hero h1{font-family:var(--serif);font-weight:400;text-transform:uppercase;color:var(--pm-gold);font-size:clamp(42px,8vw,106px);line-height:1.05;letter-spacing:.01em;text-shadow:0 4px 30px rgba(0,0,0,.7);animation:pm-rise 1.3s .35s cubic-bezier(.22,1,.36,1) both}
.pm .pm-hl .d1{position:absolute;right:-8px;top:-78px;width:44px}
.pm .pm-hl .d1 .o{position:absolute;left:-20px;bottom:0;width:20px}
.pm .pm-hl .d2{position:absolute;left:-128px;top:50%;width:112px;margin-top:-50px;display:none}
.pm .pm-hl .d3{position:absolute;left:4px;top:-44px;width:24px}
@media (min-width:768px){.pm .pm-hl .d1{right:-162px;top:-105px;width:128px}.pm .pm-hl .d1 .o{left:-40px;bottom:4px;width:36px}.pm .pm-hl .d2{display:block}.pm .pm-hl .d3{left:32px;top:-80px;width:40px}}
.pm .pm-script{width:min(70vw,352px);aspect-ratio:116.85/38.03;margin-top:4px;background:var(--pm-rose);-webkit-mask:url(img/pirimama/tel-fuszereivel.svg) center/contain no-repeat;mask:url(img/pirimama/tel-fuszereivel.svg) center/contain no-repeat;animation:pm-wipe 1.7s 1.1s ease-in-out both;will-change:transform}
.pm .pm-hero-lead{max-width:520px;margin-top:clamp(18px,3vh,30px);font-size:clamp(15px,1.25vw,18px);color:rgba(227,207,165,.9);text-shadow:0 2px 14px rgba(0,0,0,.8);animation:pm-fade 1s 1.4s both}
.pm .pm-cta .pm-btn:not(.gold){background:rgba(8,13,27,.55)}
.pm .pm-cta{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin-top:26px;animation:pm-fade 1s 1.6s both}
.pm .pm-deer{position:absolute;z-index:2;left:max(2%,calc(50% - 680px));bottom:-28px;width:clamp(220px,19vw,300px);pointer-events:none;display:none}
@media (min-width:1180px){.pm .pm-deer{display:block}}
/* ---- belső menü ---- */
.pm .pm-subnav{position:sticky;top:0;z-index:30;background:rgba(8,13,27,.9);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border-bottom:1px solid rgba(219,184,121,.14)}
.pm .pm-subnav ul{display:flex;justify-content:center;gap:clamp(18px,3.2vw,56px);overflow-x:auto;scrollbar-width:none;padding:0 var(--gutter);white-space:nowrap}
.pm .pm-subnav ul::-webkit-scrollbar{display:none}
.pm .pm-subnav li{flex:none}
.pm .pm-subnav a{position:relative;display:block;padding:16px 0 15px;font-family:var(--serif);font-size:clamp(14px,1.1vw,16px);letter-spacing:.04em;color:var(--pm-gold-soft);text-decoration:none;transition:color .2s}
.pm .pm-subnav a:hover,.pm .pm-subnav a[aria-current]{color:var(--pm-gold)}
.pm .pm-subnav a[aria-current]:after{content:"";position:absolute;left:0;right:0;bottom:9px;height:1px;background:var(--pm-gold)}
@media (max-width:760px){.pm .pm-subnav ul{justify-content:flex-start}}
.pm [id]{scroll-margin-top:64px}
/* ---- termékek ---- */
.pm .pm-products{padding-bottom:0}
.pm .pm-cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:clamp(40px,5vw,60px)}
@media (max-width:1100px){.pm .pm-cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.pm .pm-cards{grid-template-columns:1fr}}
.pm .pm-card{position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;min-height:620px;padding:40px 24px 30px;background:var(--bg);color:#FFF6E4;text-align:center;transition:background .45s}
.pm .pm-card.open,.pm .pm-card:focus-within{background:var(--bg2)}
@media (hover:hover) and (min-width:768px){.pm .pm-card:hover{background:var(--bg2)}}
.pm .pm-card .dk{position:absolute;right:20px;top:20px;width:16px;opacity:.7}
.pm .pm-card .dk2{position:absolute;left:20px;bottom:150px;width:24px;opacity:.5}
.pm .pm-card .tg{position:absolute;left:18px;top:18px;padding:5px 10px;border:1px solid rgba(255,246,228,.55);border-radius:3px;font-family:var(--sans);font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase}
.pm .pm-card h3{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:clamp(19px,1.5vw,22px);letter-spacing:.04em;line-height:1.2;color:#FFF6E4}
.pm .pm-card .sb{margin-top:4px;font-style:italic;font-size:14px;color:rgba(255,246,228,.8)}
.pm .pm-card .bt{flex:1;display:flex;align-items:center;justify-content:center;padding:22px 0;transition:transform .45s cubic-bezier(.22,1,.36,1),opacity .45s}
.pm .pm-card .bt img{height:clamp(260px,24vw,320px);width:auto;filter:drop-shadow(0 20px 25px rgba(0,0,0,.4))}
.pm .pm-card .pr{display:flex;flex-direction:column;align-items:center;gap:2px;margin-bottom:16px}
.pm .pm-card .pr b{font-family:var(--serif);font-weight:400;font-size:26px;line-height:1.1}
.pm .pm-card .pr small{font-family:var(--sans);font-size:11px;letter-spacing:.06em;opacity:.85}
.pm .pm-card .rt{font-family:var(--sans);font-size:11px;letter-spacing:.08em;opacity:.9;margin-bottom:6px}
.pm .pm-card .ac{position:relative;z-index:3;display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.pm .pm-card .ac .pm-btn{min-width:128px}
.pm .pm-card .sp{position:absolute;inset:0 0 92px;z-index:2;display:flex;flex-direction:column;overflow-y:auto;padding:32px 24px 12px;text-align:left;color:#FFF6E4;opacity:0;visibility:hidden;transform:translateY(16px);transition:opacity .4s,transform .4s,visibility .4s}
.pm .pm-card.open .sp{opacity:1;visibility:visible;transform:none}
.pm .pm-card :is(h3,.sb,.rt,.pr,.tg,.dk,.dk2){transition:opacity .35s,visibility .35s}
.pm .pm-card.open :is(h3,.sb,.rt,.pr,.tg,.dk,.dk2){opacity:0;visibility:hidden}
.pm .pm-card.open .bt{opacity:0;transform:translateY(-60px) scale(.55)}
.pm .pm-card .sp h4{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:18px;line-height:1.25}
.pm .pm-card .sp h4 span{font-family:var(--text);text-transform:none;font-style:italic;font-size:14px;opacity:.85}
.pm .pm-card .sp p{margin-top:12px;font-size:14px;line-height:1.55}
.pm .pm-card .sp dl{margin-top:14px;border-top:1px solid rgba(255,246,228,.22);font-family:var(--sans);font-size:12px}
.pm .pm-card .sp dl div{display:grid;grid-template-columns:42% 1fr;gap:8px;padding:6px 0;border-bottom:1px solid rgba(255,246,228,.22)}
.pm .pm-card .sp dt{opacity:.8}
.pm .pm-card .sp dd{font-weight:600}
.pm .pm-card .sp .nt{font-size:12.5px;font-style:italic}
.pm .pm-card .sp a{margin-top:12px;font-family:var(--sans);font-size:12px;font-weight:700;letter-spacing:.06em;text-underline-offset:4px}
/* csomag + bögre */
.pm .pm-ups{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0;border-top:1px solid rgba(219,184,121,.16)}
@media (max-width:860px){.pm .pm-ups{grid-template-columns:1fr}}
.pm .pm-up{display:flex;align-items:center;gap:clamp(16px,2.4vw,32px);padding:clamp(24px,3vw,40px) clamp(20px,4vw,56px);border-bottom:1px solid rgba(219,184,121,.16)}
.pm .pm-up+.pm-up{border-left:1px solid rgba(219,184,121,.16)}
@media (max-width:860px){.pm .pm-up+.pm-up{border-left:0}}
.pm .pm-up a.im{flex:none;width:clamp(96px,11vw,140px);aspect-ratio:1;display:flex;align-items:center;justify-content:center;border-radius:999px;background:rgba(219,184,121,.1)}
.pm .pm-up a.im img{max-height:84%;width:auto}
.pm .pm-up .tx{flex:1;display:flex;flex-direction:column;gap:6px}
.pm .pm-up .k{font-family:var(--sans);font-size:10.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--pm-gold)}
.pm .pm-up b{font-family:var(--serif);font-weight:400;font-size:clamp(17px,1.4vw,21px);line-height:1.25;text-transform:uppercase;color:var(--pm-gold-soft)}
.pm .pm-up .ds{font-size:14px;color:rgba(227,207,165,.72)}
.pm .pm-up .p{font-family:var(--serif);font-size:20px;color:var(--pm-gold-soft)}
.pm .pm-up .p s{font-family:var(--sans);font-size:13px;opacity:.55;margin-left:8px}
.pm .pm-up .pm-btn{align-self:flex-start;margin-top:6px}
/* ---- miért más ---- */
.pm .pm-usps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:48px;max-width:1180px;margin:clamp(48px,6vw,72px) auto 0;padding:0 var(--gutter)}
@media (max-width:980px){.pm .pm-usps{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.pm .pm-usps{grid-template-columns:1fr}}
.pm .pm-usp{text-align:center}
.pm .pm-usp .ic{width:128px;height:128px;margin:0 auto}
.pm .pm-usp h3{margin-top:24px;font-family:var(--serif);font-weight:400;font-size:19px;color:var(--pm-gold-soft)}
.pm .pm-usp p{margin-top:12px;font-size:14.5px;line-height:1.65;color:rgba(227,207,165,.8)}
/* ---- hol kapható ---- */
.pm .pm-where{padding-bottom:clamp(60px,7vw,100px)}
.pm .pm-where .fair-grid{margin-top:clamp(36px,5vw,56px)}
.pm .pm-where .ft{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin-top:36px}
.pm .pm-retail{margin-top:clamp(64px,8vw,110px);text-align:center}
.pm .pm-retail .big{margin-top:22px;padding:0 var(--gutter);font-family:var(--serif);font-size:clamp(18px,1.6vw,22px);line-height:1.5;color:var(--pm-gold)}
.pm .pm-marq{position:relative;margin-top:clamp(48px,6vw,80px);overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.pm .pm-marq ul{display:flex;align-items:center;width:max-content;animation:pm-marquee 40s linear infinite}
.pm .pm-marq li{padding:0 clamp(32px,4vw,64px)}
.pm .pm-marq img{height:44px;width:auto;opacity:.9}
.pm .pm-marq img.s{height:30px}
@media (max-width:760px){.pm .pm-marq img{height:34px}.pm .pm-marq img.s{height:22px}}
/* ---- történetünk ---- */
.pm .pm-story{background:var(--pm-story);padding-top:clamp(90px,11vw,170px)}
.pm .pm-story .orn{position:absolute;right:16%;top:90px;width:34px}
.pm .pm-story .orn2{position:absolute;left:24%;top:72%;width:22px}
.pm .pm-scene{position:relative;width:min(288px,64vw);margin:56px auto 0}
.pm .pm-scene svg{display:block;width:100%;height:auto}
.pm .pm-scene .mk{position:absolute;z-index:2;left:-62%;top:29%;width:112%}
.pm .pm-scene .md{position:absolute;z-index:2;right:-46%;top:33%;width:90%;transform:scaleX(-1)}
.pm .pm-scene .md img{animation:pm-float 7s ease-in-out -2s infinite}
@media (max-width:760px){.pm .pm-scene .mk{left:-39%;top:31%;width:82%}.pm .pm-scene .md{right:-35%;top:35%;width:78%}}
.pm .pm-scene .pm-bob{animation:pm-bob 5.5s ease-in-out infinite}
.pm .pm-scene .pm-stir{transform-box:fill-box;transform-origin:8% 88%;animation:pm-stir 2.8s ease-in-out infinite}
.pm .pm-scene .pm-glow{animation:pm-glow 7s ease-in-out infinite}
.pm .pm-scene .pm-steam{transform-box:fill-box;transform-origin:50% 100%;animation:pm-steam 3.4s ease-out infinite}
.pm .pm-scene .pm-steam.d{animation-delay:1.6s}
.pm .pm-story .tx{max-width:540px;margin:40px auto 0;text-align:center;font-size:15.5px;line-height:1.75;color:rgba(227,207,165,.9)}
.pm .pm-story .tx p+p{margin-top:14px}
.pm .pm-story .ft{display:flex;justify-content:center;margin-top:30px}
/* ---- videó ---- */
.pm .pm-video{position:relative;height:min(100svh,860px);overflow:hidden;background:#000}
.pm .pm-video video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
/* ---- webshop + kapcsolat ---- */
.pm .pm-shop{display:grid;grid-template-columns:1fr 1fr;background:var(--pm-shop)}
@media (max-width:980px){.pm .pm-shop{grid-template-columns:1fr}}
.pm .pm-shop .l{position:relative;display:flex;align-items:center;padding:clamp(64px,10vw,150px) var(--gutter);background-image:repeating-linear-gradient(135deg,var(--pm-night) 0 33px,var(--pm-stripe) 33px 66px)}
.pm .pm-shop .pm-sc{position:relative;width:100%;max-width:480px;margin:0 auto;padding:clamp(56px,6vw,90px) clamp(28px,4vw,56px);background:var(--pm-shop);text-align:center;color:var(--pm-ink)}
.pm .pm-shop .pm-sc .st{position:absolute;top:-24px;right:48px;width:80px}
.pm .pm-shop h2,.pm .pm-shop .ct h2{font-family:var(--serif);font-weight:400;font-size:clamp(18px,1.8vw,24px);line-height:1.5;letter-spacing:.65em;text-indent:.65em;text-transform:uppercase;color:var(--pm-ink)}
@media (max-width:640px){.pm .pm-shop h2,.pm .pm-shop .ct h2{letter-spacing:.35em;text-indent:.35em}}
.pm .pm-shop h3{margin-top:36px;font-family:var(--serif);font-weight:400;font-size:clamp(19px,1.6vw,22px);line-height:1.4;color:var(--pm-gold-soft)}
.pm .pm-shop .pm-sc p{margin-top:28px;font-size:16px;line-height:1.5}
.pm .pm-shop .pm-sc .bb{display:flex;flex-direction:column;align-items:center;gap:12px;margin-top:40px}
.pm .pm-shop .r{position:relative;padding:clamp(64px,8vw,110px) var(--gutter);color:var(--pm-ink)}
.pm .pm-shop .ct{max-width:522px;margin:0 auto;text-align:center}
.pm .pm-shop .ct ul{margin-top:40px;font-size:18px;line-height:1.6}
.pm .pm-shop .ct ul a{text-decoration:none}
.pm .pm-shop .ct ul a:hover{color:#E8C989}
.pm .pm-shop .holly{position:absolute;right:8%;bottom:48px;width:72px}
.pm .pm-nl{margin-top:56px;padding-top:44px;border-top:1px solid rgba(205,187,139,.18)}
.pm .pm-nl .k{font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--pm-gold)}
.pm .pm-nl b{display:block;margin-top:10px;font-family:var(--serif);font-weight:400;font-size:clamp(20px,1.8vw,24px);color:var(--pm-gold-soft)}
.pm .pm-nl p.d{margin-top:8px;font-size:15px;color:rgba(205,187,139,.85)}
.pm .pm-nl form{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:22px}
.pm .pm-nl input{flex:1 1 240px;min-height:48px;padding:0 14px;border:1px solid rgba(205,187,139,.45);border-radius:3px;background:transparent;color:var(--pm-gold-soft);font-family:var(--sans);font-size:16px}
.pm .pm-nl input::placeholder{color:rgba(205,187,139,.6)}
.pm .pm-nl input:focus{outline:0;border-color:var(--pm-gold)}
.pm .pm-nl .nl-note{flex-basis:100%;margin-top:6px;font-size:12px;line-height:1.5;color:rgba(205,187,139,.7)}
.pm .pm-nl .nl-note a{color:inherit}
/* ---- sötét fejléc (a Graphasel-landing éjkék világa) – arany logó, keret nélkül (Artúr, 11-17) ---- */
[data-page="pirimama"] .site-head,body:has(.pm) .site-head{background:#080D1B!important;border-bottom:1px solid rgba(219,184,121,.14)}
[data-page="pirimama"] .site-head .logo,body:has(.pm) .site-head .logo{background:transparent!important;box-shadow:none!important}
[data-page="pirimama"] .site-head .logo .lb,[data-page="pirimama"] .site-head .logo .lw,body:has(.pm) .site-head .logo .lb,body:has(.pm) .site-head .logo .lw{display:none!important}
[data-page="pirimama"] .site-head .logo .lg,body:has(.pm) .site-head .logo .lg{display:block!important}
[data-page="pirimama"] .site-head .nav a,body:has(.pm) .site-head .nav a{color:#E3CFA5!important}
[data-page="pirimama"] .site-head .nav a:hover,body:has(.pm) .site-head .nav a:hover{color:#DBB879!important}
[data-page="pirimama"] .site-head .menu-btn,body:has(.pm) .site-head .menu-btn{background:rgba(219,184,121,.14)!important;box-shadow:inset 0 0 0 1px rgba(219,184,121,.5)!important}
[data-page="pirimama"] .site-head .menu-btn path,body:has(.pm) .site-head .menu-btn path{stroke:#DBB879!important}
@media (prefers-reduced-motion:reduce){.pm *,.pm *:before,.pm *:after{animation:none!important;transition-duration:.01ms!important}.pm.pm-js [data-reveal]{opacity:1;transform:none}}
'''

JS = r'''(function(){
var root=document.querySelector('.pm');if(!root)return;
var still=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
/* megjelenés görgetéskor */
var rv=root.querySelectorAll('[data-reveal]');
if('IntersectionObserver' in window&&!still){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('pm-in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -60px 0px'});rv.forEach(function(el){io.observe(el);});}
else{rv.forEach(function(el){el.classList.add('pm-in');});}
/* hero parallax: a fotó lefelé, a cím lassan, a kézírás gyorsabban felfelé */
var px=root.querySelectorAll('[data-px]');
if(px.length&&!still){var tick=false;var run=function(){var y=window.scrollY||0;if(y<1400)px.forEach(function(el){el.style.transform='translate3d(0,'+(y*parseFloat(el.getAttribute('data-px'))).toFixed(1)+'px,0)';});tick=false;};
window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(run);}},{passive:true});run();}
/* termékkártyák: Részletek panel (érintésre / kattintásra) */
root.querySelectorAll('[data-pm-spec]').forEach(function(b){var c=b.closest('.pm-card');b.addEventListener('click',function(){var o=c.classList.toggle('open');b.setAttribute('aria-expanded',String(o));b.textContent=o?'Bezárás':'Részletek';});});
/* belső menü: aktív szakasz */
var links=root.querySelectorAll('.pm-subnav a');
if('IntersectionObserver' in window&&links.length){var so=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;links.forEach(function(a){if(a.getAttribute('href')==='#'+e.target.id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});});},{rootMargin:'-45% 0px -50% 0px'});
links.forEach(function(a){var s=document.getElementById(a.getAttribute('href').slice(1));if(s)so.observe(s);});}
/* hangulatvideó: csak látótérben tölt és játszik */
var v=root.querySelector('.pm-video video');
if(v&&'IntersectionObserver' in window){var vo=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){if(v.preload!=='auto'){v.preload='auto';}var p=v.play();if(p&&p.catch)p.catch(function(){});}else{v.pause();}});},{threshold:.25});vo.observe(v);}
})();'''


def build(B):
    """B: a build.py modul (head, header, footer, falling, FAIRS, P, SP, ft, e, write)."""
    r = ''
    e, ft, P = B.e, B.ft, B.P

    def card(c, i):
        p = P[c['id']]
        params = [(k, v) for k, v in p['params'] if k not in SKIP_PARAMS]
        dl = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in params)
        tag = f'<span class="tg">{e(c["tag"])}</span>' if c.get('tag') else ''
        stars = ''
        if p.get('rating') and p.get('rcount'):
            stars = f'<p class="rt" aria-label="Értékelés: {p["rating"]} az 5-ből, {p["rcount"]} vélemény">★★★★★ {p["rating"].replace(".", ",")} · {p["rcount"]} vélemény</p>'
        url = f'termek/{p["id"]}.html'
        return f'''<article class="pm-card" style="--bg:{c['bg']};--bg2:{c['bg2']};--d:{i * .12:.2f}s" data-reveal>
<img class="dk pm-twinkle" src="{r}img/deco/{c['deco']}.svg" alt="" aria-hidden="true" style="--delay:-{i}s"><img class="dk2 pm-float" src="{r}img/deco/snow-dots.svg" alt="" aria-hidden="true" style="--delay:-{i * 2}s">{tag}
<h3>{e(c['t'])}</h3><p class="sb">{e(c['s'])}</p>
<a class="bt" href="{r}{url}" aria-label="{e(p['name'])} – termékoldal"><img src="{r}{p['tight']}" alt="{e(p['name'])} 1 literes palack" width="376" height="1400" loading="lazy"></a>
{stars}<p class="pr"><b>{ft(p['price'])}</b><small>1 l · + 50 Ft betétdíj</small></p>
<div class="ac"><button class="pm-btn dark" type="button" data-add="{p['id']}" aria-label="{e(p['name'])} kosárba"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 7h14l-1.5 12h-11z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>Kosárba</button>
<button class="pm-btn" type="button" data-pm-spec aria-expanded="false" aria-controls="pm-sp-{i}">Részletek</button></div>
<div class="sp" id="pm-sp-{i}"><h4>{e(c['t'])} <span>{e(c['s'])}</span></h4><p>{e(p['short'])}</p><dl>{dl}</dl><p class="nt">{e(c['note'])}</p><a href="{r}{url}">Termékoldal és vélemények →</a></div>
</article>'''

    pack = B.SP['forralt-6']
    mug = P['piri-mama-bogreje']
    ups = f'''<div class="pm-ups">
<div class="pm-up" data-reveal><a class="im" href="{r}csomagok.html" aria-label="{e(pack['name'])}"><img src="{r}img/csomag/pack-forralt-6.webp" alt="{e(pack['name'])}" loading="lazy"></a>
<div class="tx"><span class="k">Csomagban olcsóbb</span><b>{e(pack['name'])}</b><span class="ds">3 klasszikus, 1 epres és 1 narancsos PIRI Mama.</span><span class="p">{ft(pack['price'])}<s>{ft(pack['old'])}</s></span>
<button class="pm-btn gold" type="button" data-add="forralt-6">Kosárba</button></div></div>
<div class="pm-up" data-reveal style="--d:.12s"><a class="im" href="{r}termek/{mug['id']}.html" aria-label="{e(mug['name'])}"><img src="{r}{mug['tight']}" alt="{e(mug['name'])}" loading="lazy"></a>
<div class="tx"><span class="k">Hozzá illik</span><b>{e(mug['name'])}</b><span class="ds">Hőálló üvegbögre – a vásári hangulathoz otthon is.</span><span class="p">{ft(mug['price'])}</span>
<button class="pm-btn" type="button" data-add="{mug['id']}">Kosárba</button></div></div></div>'''

    usps = ''.join(f'''<div class="pm-usp" data-reveal style="--d:{i * .12:.2f}s"><div class="ic"><img class="{a}" src="{r}img/pirimama/{ic}.svg" alt="" aria-hidden="true" style="--delay:-{i}s"></div>
<h3>{e(t)}</h3><p>{e(x)}</p></div>''' for i, (ic, a, t, x) in enumerate(USP))

    fairs = ''.join(f'''<a class="fair-card2" href="{r}vasarok.html#{f['id']}" data-fair="{f['id']}"><span class="im"><img src="{r}img/fair/{f['id']}.webp" alt="Adventi vásár – {e(f['city'])}" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>{e(f['city'])} – {e(f['place'].split(' – ')[0])}</b><span class="pl">{e(f['note'])}</span></span></a>''' for f in B.FAIRS)
    stores = ''.join(f'<li{" aria-hidden=\"true\"" if k else ""}><img class="{c}" src="{r}img/pirimama/{f}.svg" alt="{"" if k else e(n)}" loading="lazy"></li>'
                     for k in range(4) for f, n, c in STORES)

    scene = open(B.os.path.join(B.ROOT, 'src', 'pirimama_scene.svg'), encoding='utf-8').read().strip()
    subnav = ''.join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in SUBNAV)

    ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'PIRI Mama forralt borok',
          'itemListElement': [{'@type': 'ListItem', 'position': n + 1, 'item': {
              '@type': 'Product', 'name': P[c['id']]['name'] + ' 1 l', 'image': P[c['id']]['img'], 'description': P[c['id']]['short'],
              'brand': {'@type': 'Brand', 'name': 'Kontyos'}, 'url': LIVE + LIVE_URL[c['id']],
              'offers': {'@type': 'Offer', 'price': P[c['id']]['price'], 'priceCurrency': 'HUF', 'availability': 'https://schema.org/InStock',
                         'url': LIVE + LIVE_URL[c['id']]}}} for n, c in enumerate(CARDS)]}

    pg = B.head('PIRI Mama forralt bor – a tél fűszereivel | Kontyos',
                'PIRI Mama kész forralt gyümölcsborai valódi fűszerekkel: klasszikus, epres, narancsos és alkoholmentes változat 1 literes palackban. Rendeld meg online, vagy kóstold meg az adventi vásárokon!',
                r, 'pirimama', '', f'<style>{CSS}</style>')
    pg += B.header(r) + f'''<main class="pm" id="top"><script>document.currentScript.parentNode.classList.add('pm-js')</script>
{B.snowfall()}
<section class="pm-hero" aria-labelledby="pm-h1">
<div class="pm-hero-ph" data-px="0.35"><img src="{r}img/pirimama/hero-1920.webp" srcset="{r}img/pirimama/hero-800.webp 800w, {r}img/pirimama/hero-1200.webp 1200w, {r}img/pirimama/hero-1920.webp 1920w" sizes="100vw" alt="PIRI Mama forralt bor palackja téli fűszerek között" width="1920" height="1281" fetchpriority="high"></div>
{B.falling(r, ('flake-gold', 'snow-dots', 'flake-gold'), 16, 9)}
<div class="pm-hero-in">
<div class="pm-hl" data-px="-0.08">
<div class="d1" aria-hidden="true"><img class="pm-sway" src="{r}img/deco/holly.svg" alt=""><span class="o"><img class="pm-swing" src="{r}img/deco/ornament-gold.svg" alt="" style="--dur:6s"></span></div>
<div class="d2" aria-hidden="true"><img class="pm-float" src="{r}img/pirimama/csillag-feher.svg" alt=""></div>
<div class="d3" aria-hidden="true"><img class="pm-spin" src="{r}img/deco/flake-blue.svg" alt=""></div>
<h1 id="pm-h1">PIRI MAMA<br>FORRALT BORA</h1></div>
<div data-px="-0.2"><p class="pm-script"><span class="sr">A tél fűszereivel</span></p></div>
<p class="pm-hero-lead">Kész forralt gyümölcsbor valódi fűszerekkel. Otthon csak melegíteni kell – és már a tiéd az adventi vásárok hangulata.</p>
<div class="pm-cta"><a class="pm-btn gold" href="#termekek">Rendeld meg online</a><a class="pm-btn" href="#hol-kaphato">Adventi vásárok</a></div>
</div>
<img class="pm-deer pm-float" src="{r}img/pirimama/szarvas.svg" alt="" aria-hidden="true">
</section>
<nav class="pm-subnav" aria-label="Az oldal tartalma"><ul>{subnav}</ul></nav>

<section class="pm-sec pm-products" id="termekek">
<h2 class="pm-eyebrow" data-reveal>Termékeink</h2>
<p class="pm-intro" data-reveal>Egyliteres palackban, négyféle ízben – válaszd ki a kedvencedet, és megérkezik hozzád.</p>
<div class="pm-cards">{''.join(card(c, i) for i, c in enumerate(CARDS))}</div>
{ups}
</section>

<section class="pm-sec pm-usp-sec" id="miert-mas">
<h2 class="pm-eyebrow" data-reveal>Piri Mama – Miért más?</h2>
<div class="pm-usps">{usps}</div>
</section>

<section class="pm-sec pm-where" id="hol-kaphato">
<h2 class="pm-eyebrow" data-reveal>Hol kapható?</h2>
<p class="pm-sub-eyebrow" data-reveal style="margin-top:clamp(40px,5vw,64px)">Adventi vásárok</p>
<p class="pm-intro" data-reveal>Frissen melegítve, forrón kínáljuk – keress minket a standjainkon!</p>
<div class="fair-grid fair-row" id="pm-fair-row">{fairs}</div>
<div class="ft"><button type="button" class="pm-btn" data-fair-more aria-controls="pm-fair-row" aria-expanded="false">További vásárok ({len(B.FAIRS) - 5})</button><a class="pm-btn" href="{r}vasarok.html">Térképen és értesítővel</a></div>
<div class="pm-retail" data-reveal><p class="pm-sub-eyebrow">Megkóstoltad a vásárban? Vidd haza!</p>
<p class="big">A vásárokból ismert PIRI Mama – otthon is.<br>Keresd az üzletekben!</p>
<div class="pm-marq"><ul>{stores}</ul></div></div>
</section>

<section class="pm-sec pm-story" id="tortenetunk">
<img class="orn pm-swing" src="{r}img/deco/ornament-pink.svg" alt="" aria-hidden="true"><img class="orn2 pm-spin" src="{r}img/deco/flake-gold.svg" alt="" aria-hidden="true">
<h2 class="pm-eyebrow" data-reveal>Történetünk</h2>
<div class="pm-scene" data-reveal><span class="mk"><img class="pm-float" src="{r}img/pirimama/mokus.svg" alt="" aria-hidden="true"></span><span class="md"><img src="{r}img/pirimama/madar.svg" alt="" aria-hidden="true"></span>{scene}</div>
<div class="tx" data-reveal><p>A Kontyos Borháznál hiszünk abban, hogy minden évszaknak megvan a maga illata, amely különleges emlékeket és hangulatokat idéz fel. 2006 óta készítünk hazai gyümölcsökből karakteres gyümölcsborokat, ötvözve a hagyományos eljárásokat a modern technológiával.</p>
<p>Ebből a szemléletből született meg Piri mama forralt bora is.</p></div>
<div class="ft"><a class="pm-btn" href="{r}rolunk.html">Ismerd meg a borházat</a></div>
</section>

<section class="pm-video" aria-label="Hangulatvideó"><video muted loop playsinline preload="none" poster="{r}img/video/piri_hangulat.webp" aria-label="Forró PIRI Mama forralt bor téli hangulatban"><source src="{r}img/pirimama/hangulat-720.mp4" type="video/mp4"></video></section>

<section class="pm-shop" id="webshop">
<div class="l"><div class="pm-sc" data-reveal><img class="st pm-twinkle" src="{r}img/pirimama/csillag-arany.svg" alt="" aria-hidden="true">
<h2>Webshop</h2><h3>Az ünnep ízei,<br>egyenesen hozzád.</h3>
<p>PIRI Mama forralt borai és a Kontyos gyümölcsborai egy helyen. Találd meg az ünnepi kedvencedet – 25 000 Ft felett ingyen szállítunk.</p>
<div class="bb"><a class="pm-btn gold" href="#termekek">Rendeld meg otthonra!</a><a class="pm-btn" href="{r}forralt-bor.html">Összes forralt bor és csomag</a></div></div></div>
<div class="r"><div class="ct" id="kapcsolat" data-reveal><h2>Kapcsolat</h2>
<ul><li><a href="tel:+36300945042">+36 30 094 5042</a></li><li><a href="mailto:webshop@kontyos.hu">webshop@kontyos.hu</a></li><li>6773 Klárafalva, Kossuth u. 183.</li></ul>
<div class="pm-nl"><p class="k">Hírlevél</p><b>−5% az első rendelésedből</b><p class="d">Iratkozz fel: a kuponkódot azonnal küldjük, mellé szezonális ajánlatok és új ízek – elsőként.</p>
<form data-newsletter><label class="sr" for="pm-nl">E-mail cím</label><input id="pm-nl" type="email" placeholder="E-mail címed" autocomplete="email" required><button class="pm-btn gold" type="submit">Feliratkozom</button></form></div>
</div><img class="holly pm-sway" src="{r}img/deco/holly.svg" alt="" aria-hidden="true"></div>
</section>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script>{JS}</script>
</main>''' + B.footer(r)
    import re as _re
    # a Shoprenter-generátor a Párizs-ütköző osztályokat (card, btn, row…) k- előtaggal átnevezi – az oldal saját <style>-ját nem –, ezért itt tilos
    _bad = {c for cl in _re.findall(r'class="([^"]*)"', pg[pg.find('<main'):pg.find('</main>')]) for c in cl.split()} & {'badge', 'btn', 'card', 'close', 'col', 'h1', 'h2', 'h3', 'head', 'lead', 'left', 'nav', 'price', 'right', 'row', 'small', 'tall', 'breadcrumb'}
    assert not _bad, f'Párizs-ütköző osztálynév a PIRI Mama oldalon: {_bad}'
    B.write('pirimama.html', pg)
