"""DON CHERRY landing – kontyos.hu/don-cherry (Stratos, 2026-11-26).

A Graphasel Lovable-ben készült landingjének (don-cherry-cocktail-carousel) statikus átültetése a webshopba,
a PIRI Mama-landing (src/pirimama.py) szabályai szerint: ugyanaz a szerkezet és látványvilág, de
- a „Vásárlás” / „Koktélcsomag” gombok valódi kosárba tesznek (data-add → Shoprenter-kosár), mellettük ár és termékoldal-link;
- a vásárlista a webshop közös vásár-adataiból kapja a dátumot és az élő státuszt (FAIRS / KONTYOS_FAIRS);
- a mailto-s kapcsolati űrlap helyett hírlevél (HIRLEVEL5) + elérhetőségek, a cím 6773 Klárafalva;
- a Lovable saját fix menüje helyett a webshop fejléce + ragadós belső menü;
- nincs React / Embla: a lebegés, parallax, Don lóbáló lába és a húzható koktélsor CSS + kevés natív JS,
  prefers-reduced-motion esetén a mozgás kikapcsol.

A stílus az oldal saját <style> blokkjában van (.dc gyökér alatt), a JS is az oldalon él, így élesben
nem kell a jsDelivr-re rögzített kontyos.css / kontyos.live.js-t újrakiadni.
A képek a GitHub Pages-ről jönnek (img/doncherry/), mint a /pirimama-n.
"""
import json

LIVE = 'https://www.kontyos.hu/'
LIVE_URL = {'don-cherry': 'don-cherry-edes-meggyvermut-075-l', 'don-cherry-gyumolcse': 'don-cherry-edes-meggyvermut-025-l-and-meggy-100-g'}
IMG = 'img/doncherry/'

# A Graphasel koktélsora (cherry-data.ts) – a sorrend és a szövegek az eredetiek; pack = a webshop koktélcsomagja
COCKTAILS = [
    dict(name='DON TONIC', img='don-tonic', kind='tonic', pack='koktel-tonic',
         desc='Frissítő, gyümölcsös, könnyed – egy kis csavar a megszokott tonikban.',
         method='Tölts meg egy hosszú poharat jéggel, öntsd rá a Don Cherryt és a tonikot. Finoman keverd meg, majd narancskarikával és meggyel díszítsd.',
         ing=['4 cl Don Cherry', '12 cl tonic', 'jég', 'narancs', 'meggy']),
    dict(name='NEGRONI', img='negroni', kind='rocks', pack='koktel-negroni',
         desc='Karakteres, gyümölcsös, kissé kesernyés – mégis selymesen fűszeres.',
         method='Önts minden hozzávalót jéggel teli keverőpohárba, keverd össze, majd szűrd egy jéggel teli whiskys pohárba. Narancshéjjal díszítsd.',
         ing=['3 cl Don Cherry', '3 cl gin', '3 cl Campari', 'jég', 'narancshéj']),
    dict(name='AMERICANO', img='americano', kind='americano', pack='koktel-americano',
         desc='A klasszikus olasz aperitif, Don Cherry gyümölcsös karakterével.',
         method='A Don Cherryt és a Camparit jéggel teli pohárban keverd össze. Töltsd fel szódával, és egy narancshéjjal tedd teljessé.',
         ing=['3 cl Don Cherry', '3 cl Campari', '6 cl szóda', 'jég', 'narancshéj']),
    dict(name='DONHATTAN', img='donhattan', kind='manhattan', pack='koktel-manhattan',
         desc='Érett, fűszeres, selymes – a meggy és a whisky elegáns találkozója.',
         method='Öntsd a hozzávalókat jéggel teli keverőpohárba, keverd jól össze, majd szűrd egy hűsített koktélpohárba. A meggyet arany pálcán tedd a tetejére.',
         ing=['5 cl Don Cherry', '5 cl whisky', '2 csepp Angostura', 'jég', 'meggy arany pálcán']),
]
# A Graphasel helyszín-feliratai; dátum és státusz a közös FAIRS-adatokból (data-fair)
LOCS = {'szeged': ('SZEGEDI ADVENT', 'Szeged, Dóm tér'), 'obuda': ('ADVENT ÓBUDÁN', 'Budapest, III. kerület, Szentlélek tér'),
        'gyor': ('ADVENT GYŐRBEN', 'Győr, Baross utca'), 'szombathely': ('SZOMBATHELYI ADVENT', 'Szombathely, Fő tér'),
        'veszprem': ('ILLATOS ADVENT VESZPRÉM', 'Veszprém, Kossuth L. utca, belváros'), 'pecs': ('PÉCSI ADVENTI VÁSÁR', 'Pécs, Széchenyi tér'),
        'nyiregyhaza': ('NYÍREGYHÁZI ADVENTI FORGATAG', 'Nyíregyháza, Kossuth tér')}
SUBNAV = [('vermut', 'Vermut'), ('ki-az-a-don', 'Ki az a Don?'), ('ahogy-a-don-szereti', 'Ahogy a Don szereti'), ('koktelok', 'Koktélok'),
          ('meggy', 'Don & meggy'), ('hol-kaphato', 'Hol kapható?')]

ICO_BAG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>'
ICO_GIFT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/></svg>'
ICO_DRAG = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m18 8 4 4-4 4"/><path d="M2 12h20"/><path d="m6 8-4 4 4 4"/></svg>'

CSS = r'''
.dc{--dc-red:#A90111;--dc-deep:#7C000B;--dc-hero:#B90012;--dc-cyan:#00C3D4;--dc-ink:#008EA1;--dc-paper:#fff;--dc-line:#F7D5D2;--dc-shadow:rgba(47,0,1,.55);
  --dc-sans:'Montserrat',Arial,sans-serif;--dc-wide:'Archivo','Montserrat',Arial,sans-serif;
  position:relative;display:block;overflow-x:clip;background:var(--dc-red);color:#fff;font-family:var(--dc-sans);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
.dc *{box-sizing:border-box}
.dc img{display:block;max-width:100%;height:auto}
.dc p,.dc h1,.dc h2,.dc h3,.dc h4,.dc ul,.dc figure{margin:0;padding:0}
.dc ul{list-style:none}
.dc a{color:inherit;text-decoration:none}
.dc [hidden]{display:none!important}
.dc :is(p,li,a,span,strong,b,s,label,input,button,small,h4,div){font-family:var(--dc-sans)}
.dc .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.dc ::selection{background:var(--dc-cyan);color:var(--dc-red)}
.dc :focus-visible{outline:2px solid var(--dc-cyan);outline-offset:3px}
.dc .dc-in{max-width:1240px;margin:0 auto;position:relative}
.dc .dc-eyebrow{font-family:var(--dc-wide);font-stretch:112.5%;font-size:15px;font-weight:700;letter-spacing:7px;line-height:1.6;text-transform:uppercase}
.dc h1,.dc h2,.dc h3{font-family:var(--dc-sans);font-weight:800;text-transform:none;letter-spacing:0}
.dc [id]{scroll-margin-top:64px}
/* gombok */
.dc .dc-b{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:48px;padding:0 28px;border:0;border-radius:5px;cursor:pointer;white-space:nowrap;
  font-family:var(--dc-wide);font-stretch:112.5%;font-size:12px;font-weight:700;letter-spacing:1px;line-height:1;text-transform:uppercase;transition:background .25s,color .25s,opacity .25s}
.dc .dc-b svg{width:16px;height:16px;flex:none}
.dc .dc-b.cy{background:var(--dc-cyan);color:var(--dc-deep)}
.dc .dc-b.cy:hover{background:#1FD2E2}
.dc .dc-b.rd{background:var(--dc-red);color:#fff}
.dc .dc-b.rd:hover{background:#C2081A}
.dc .dc-b.ol{background:transparent;color:var(--dc-cyan);box-shadow:inset 0 0 0 1px currentColor}
.dc .dc-b.ol:hover{background:rgba(255,255,255,.06)}
.dc .dc-b.pp{background:#fff;color:var(--dc-ink)}
.dc .dc-b.pp:hover{background:#F2FBFC}
.dc .dc-b.ky-adding{opacity:.7;pointer-events:none}
.dc .dc-join{display:flex;justify-content:center}
.dc .dc-join .dc-b:first-child{border-radius:5px 0 0 5px}
.dc .dc-join .dc-b:last-child{border-radius:0 5px 5px 0}
.dc .dc-price{margin:0 0 16px;font-size:13px;letter-spacing:.04em}
.dc .dc-price b{font-size:18px;font-weight:800;letter-spacing:0;margin-right:6px}
.dc .dc-pl{display:inline-block;margin-top:16px;font-size:12px;font-weight:700;letter-spacing:.06em;text-decoration:underline!important;text-underline-offset:4px;opacity:.9}
.dc .dc-pl:hover{opacity:1}
/* mozgás – lebegés, parallax (--px) */
.dc .dc-mo{position:absolute;transform:translate3d(0,var(--px,0px),0);will-change:transform;pointer-events:none}
.dc .dc-fl{animation:dc-float 6s ease-in-out infinite;will-change:transform}
.dc .dc-sh{position:absolute;height:17px;width:75%;left:12%;bottom:-43px;background:var(--dc-shadow);border-radius:50%;filter:blur(3px);animation:dc-shadow 6s ease-in-out infinite}
@keyframes dc-float{0%,100%{transform:translate(0,0) rotate(-2deg)}50%{transform:translate(7px,-20px) rotate(2deg)}}
@keyframes dc-float-l{0%,100%{transform:translate(0,0) rotate(-17deg)}50%{transform:translate(-7px,-26px) rotate(-14deg)}}
@keyframes dc-float-r{0%,100%{transform:translate(0,0) rotate(18deg)}50%{transform:translate(8px,-30px) rotate(15deg)}}
@keyframes dc-shadow{0%,100%{transform:scaleX(1);opacity:.8;filter:blur(3px)}50%{transform:scaleX(1.3);opacity:.4;filter:blur(6px)}}
@keyframes dc-enter{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes dc-shin{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(6deg)}}
@keyframes dc-jump{0%,100%{transform:translateY(0)}35%{transform:translateY(-16px)}65%{transform:translateY(4px)}}
@keyframes dc-nudge{0%,100%{transform:translateX(-3px)}50%{transform:translateX(3px)}}
.dc .dc-enter{animation:dc-enter .45s ease both}
/* belső menü */
.dc .dc-subnav{position:sticky;top:0;z-index:30;background:rgba(124,0,11,.94);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);box-shadow:0 12px 22px -16px rgba(47,0,1,.9)}
.dc .dc-subnav ul{display:flex;justify-content:center;gap:clamp(18px,3vw,48px);overflow-x:auto;scrollbar-width:none;padding:0 20px;white-space:nowrap}
.dc .dc-subnav ul::-webkit-scrollbar{display:none}
.dc .dc-subnav li{flex:none}
.dc .dc-subnav a{position:relative;display:block;padding:17px 0 16px;font-family:var(--dc-wide);font-stretch:112.5%;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;transition:color .2s}
.dc .dc-subnav a:hover,.dc .dc-subnav a[aria-current]{color:var(--dc-cyan)}
.dc .dc-subnav a[aria-current]:after{content:"";position:absolute;left:0;right:0;bottom:10px;height:1px;background:var(--dc-cyan)}
@media (max-width:767px){.dc .dc-subnav ul{justify-content:flex-start}}
/* ---- hero ---- */
.dc .dc-hero{position:relative;background:radial-gradient(ellipse at 48% 39%,var(--dc-hero) 0%,var(--dc-red) 58%,var(--dc-deep) 100%);min-height:860px;overflow:hidden}
.dc .dc-stage{position:relative;height:860px;max-width:1200px;margin:0 auto;text-align:center}
.dc .dc-copy{position:relative;z-index:3;padding-top:150px}
.dc .dc-copy .dc-eyebrow{margin-bottom:24px}
.dc .dc-hero h1{font-size:84px;line-height:.98;color:#fff}
.dc .dc-cta{margin-top:127px}
.dc .dc-hb{width:145px;z-index:5}
.dc .dc-hb-l{left:8%;top:180px}
.dc .dc-hb-r{right:12%;top:245px}
.dc .dc-hb-l .dc-fl{transform:rotate(-17deg);animation-name:dc-float-l}
.dc .dc-hb-r .dc-fl{transform:rotate(18deg);animation-name:dc-float-r;animation-duration:7.2s;animation-delay:-2s}
.dc .dc-hb-l .dc-sh{left:30%}
.dc .dc-hb-r .dc-sh{left:-4%;animation-duration:7.2s;animation-delay:-2s}
.dc .dc-hf{width:150px;top:415px;left:35%;z-index:4}
.dc .dc-hf .dc-fl{animation-duration:4.6s}
.dc .dc-hf .dc-sh{bottom:12px;width:45%;left:27%;height:9px}
.dc .dc-hf2{width:155px;top:85px;left:49%;z-index:2}
.dc .dc-hf2 .dc-fl{animation-delay:-3s}
/* ---- vermut ---- */
.dc .dc-vermut{position:relative;z-index:5;background:var(--dc-deep);height:700px;text-align:center}
.dc .dc-vermut .dc-in{padding-top:130px;height:100%}
.dc .dc-vermut h2{font-size:177px;line-height:.9;text-shadow:-18px 17px 0 var(--dc-shadow);color:#fff}
.dc .dc-vb{width:174px;left:21%;top:215px;z-index:3;transform:none;pointer-events:auto}
.dc .dc-vb .dc-sh{bottom:-2px;width:120%;left:-10%;height:26px;filter:blur(10px);opacity:.8;animation:none}
.dc .dc-vb img{transition:transform 1.6s cubic-bezier(.22,1,.36,1)}
@media (hover:hover){.dc .dc-vb:hover img{transform:perspective(900px) rotateY(360deg)}}
.dc .dc-pc{width:420px;margin-left:47%;margin-top:28px;position:relative;z-index:4}
.dc .dc-pc h3{font-size:17px;letter-spacing:1px;line-height:1.3}
.dc .dc-pt{margin:20px 0 26px;line-height:1.5;font-size:14px;min-height:100px}
.dc .dc-pt strong{font-weight:800}
/* ---- ki is valójában ---- */
.dc .dc-story{padding:200px 48px 100px}
.dc .dc-panel{display:grid;grid-template-columns:1fr 1fr;position:relative;border-radius:7px;background:var(--dc-cyan);box-shadow:0 24px 30px -12px var(--dc-shadow);max-width:1240px;margin:auto}
.dc .dc-life{display:block;width:100%;height:550px;object-fit:cover;border-radius:7px 0 0 7px;background:#1b6f86}
.dc .dc-sc{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:45px;position:relative;min-width:0}
.dc .dc-sc .dc-eyebrow{letter-spacing:9px;margin-bottom:40px}
.dc .dc-sc h2{font-family:'Poppins',var(--dc-sans);font-weight:700;font-size:104px;line-height:.88;letter-spacing:-1px;color:#fff}
.dc .dc-sc .dc-b{margin-top:96px}
.dc .dc-sf{width:175px;left:47%;top:31%;z-index:3}
.dc .dc-sf .dc-sh{bottom:-14px;width:32%;left:28%;height:9px}
.dc .dc-st{color:var(--dc-red);font-size:15px;line-height:1.7;max-width:400px;margin-top:20px}
.dc .dc-sc.open h2{font-size:45px}
.dc .dc-sc.open .dc-eyebrow{margin-bottom:20px}
.dc .dc-sc.open .dc-b{margin-top:22px}
.dc .dc-sc.open .dc-sf{display:none}
.dc .dc-don{position:absolute;width:138px;height:274px;top:-145px;left:calc(50% + 35px);z-index:8;pointer-events:none}
.dc .dc-don img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;object-position:top;max-width:none}
.dc .dc-don .bd{clip-path:inset(0 0 41.3% 0)}
.dc .dc-don .sl,.dc .dc-don .sr2{animation:dc-shin 3.4s ease-in-out infinite}
.dc .dc-don .sl{clip-path:polygon(0 55.8%,48% 55.8%,48% 100%,0 100%);transform-origin:27% 56.7%}
.dc .dc-don .sr2{clip-path:polygon(48% 55.8%,100% 55.8%,100% 100%,48% 100%);transform-origin:70% 56.7%;animation-delay:-1.5s;animation-duration:3.9s}
/* ---- ahogy a Don szereti ---- */
.dc .dc-serv{padding:75px 30px 90px;text-align:center}
.dc .dc-sg{display:grid;grid-template-columns:1fr 1fr;max-width:1080px;margin:78px auto 0}
.dc .dc-si{position:relative;padding:15px 60px}
.dc .dc-si+.dc-si{border-left:1px solid rgba(255,255,255,.25)}
.dc .dc-si h3{font-size:72px;line-height:1.2;color:#fff}
.dc .dc-si h4{font-size:13px;font-weight:700;margin:26px 0 18px;letter-spacing:1px}
.dc .dc-si p{font-size:14px;line-height:1.55;max-width:385px;margin:auto}
.dc .dc-so{width:68px;top:-34px;left:24%;z-index:1}
.dc .dc-sgl{width:74px;top:-12px;left:39%;z-index:3;rotate:28deg}
.dc .dc-ssh{width:52px;top:18px;left:44%;z-index:3;rotate:26deg}
.dc .dc-sfr{width:26px;top:-80px;left:52%;z-index:3}
/* ---- koktélok ---- */
.dc .dc-ck{position:relative;background:var(--dc-cyan);padding-bottom:90px}
.dc .dc-ck:before{content:"";position:absolute;inset:0 0 auto;height:230px;background:var(--dc-red)}
.dc .dc-ck>.dc-eyebrow{position:relative;text-align:center;padding:38px 20px 25px}
.dc .dc-car{position:relative;margin-top:-20px}
.dc .dc-car:before{content:"";position:absolute;width:500px;height:190px;border-radius:50% 50% 0 0;background:var(--dc-cyan);left:calc(50% - 250px);top:123px}
.dc .dc-vp{position:relative;overflow:hidden;touch-action:pan-y pinch-zoom;cursor:grab;user-select:none;-webkit-user-select:none}
.dc .dc-vp.drag{cursor:grabbing}
.dc .dc-tr{display:flex;align-items:flex-end;will-change:transform}
.dc .dc-tr.anim{transition:transform .55s cubic-bezier(.22,1,.36,1)}
.dc .dc-sl{flex:0 0 34%;min-width:0;height:475px;display:flex;justify-content:center;align-items:center;position:relative}
.dc .dc-sel{position:relative;display:flex;justify-content:center;align-items:flex-end;height:420px;width:100%;padding:0;border:0;background:transparent;color:#fff;cursor:pointer;font:inherit}
.dc .dc-ci{height:225px;width:auto;object-fit:contain;transform:translateY(52px);transition:transform .6s,height .6s;-webkit-user-drag:none;pointer-events:none}
.dc .dc-sl.on .dc-ci{height:465px;transform:none}
.dc .dc-sl.on .dc-ci.tonic,.dc .dc-sl.on .dc-ci.americano{height:374px}
.dc .dc-sl.on .dc-ci.manhattan{height:440px}
.dc .dc-cn{position:absolute;left:0;right:0;top:58.5%;font-family:var(--dc-sans);font-weight:800;font-size:42px;line-height:1.1;white-space:nowrap;z-index:4;text-align:center;transition:font-size .5s,top .5s;pointer-events:none}
@media (hover:hover){.dc .dc-sel:hover .dc-cn{animation:dc-jump .5s ease-out}}
.dc .dc-sl.on .dc-cn{font-size:76px;top:44.5%}
.dc .dc-hint{display:flex;justify-content:center;align-items:center;margin:15px 0 34px}
.dc .dc-hint svg{animation:dc-nudge 2.6s ease-in-out infinite}
.dc .dc-rec{max-width:620px;margin:auto;display:grid;grid-template-columns:1fr 1fr;gap:50px;padding:0 22px}
.dc .dc-rm{font-size:14px;line-height:1.55;padding-top:8px}
.dc .dc-rm p:first-child{font-style:italic;font-weight:600;margin-bottom:25px}
.dc .dc-ri{background:#3BC6DE;border:1px solid rgba(255,255,255,.25);padding:28px;border-radius:5px}
.dc .dc-ri h3{font-size:13px;letter-spacing:1px;margin-bottom:24px;color:#fff}
.dc .dc-ri ul{margin:0 0 22px;font-size:13px;line-height:1.25}
.dc .dc-ri .dc-pk{font-size:12px;line-height:1.4;margin-bottom:14px}
.dc .dc-ri .dc-pk b{display:block;font-size:13px}
.dc .dc-ri .dc-b{padding:0 18px;font-size:10px}
.dc .dc-ri .dc-pl{font-size:11px}
/* ---- Don & meggy ---- */
.dc .dc-pair{background:linear-gradient(to bottom,var(--dc-cyan),#fff 83%);color:var(--dc-red);padding:95px 30px 70px;text-align:center;min-height:680px}
.dc .dc-pair h2{font-size:81px;line-height:1.12;margin-top:27px;color:var(--dc-red)}
.dc .dc-pl2{display:grid;grid-template-columns:270px 420px;justify-content:center;gap:65px;align-items:center;margin-top:65px}
.dc .dc-jw{position:relative;height:350px}
.dc .dc-jw img{position:absolute;width:204px;left:20px;top:0}
.dc .dc-pair .dc-pc{margin:0;width:auto}
.dc .dc-pair .dc-b.ol{color:var(--dc-red)}
/* ---- hol kapható + kapcsolat ---- */
.dc .dc-foot{background:#fff;color:var(--dc-red);padding:85px 25px 70px}
.dc .dc-fg{max-width:930px;margin:auto;display:grid;grid-template-columns:1fr 1fr;gap:145px;text-align:center}
.dc .dc-foot .dc-eyebrow{margin-bottom:34px;font-weight:700}
.dc .dc-fi,.dc .dc-cd{font-size:14px;line-height:1.5}
.dc .dc-lidl{width:235px;margin:34px auto;border-radius:5px}
.dc .dc-locs li{margin-bottom:25px;font-size:13px;line-height:1.5}
.dc .dc-locs a{display:block}
.dc .dc-locs strong{display:block;font-size:13px;letter-spacing:2px;font-weight:700}
.dc .dc-locs .dt{display:block;font-size:11px;letter-spacing:.06em;opacity:.75}
.dc .dc-locs a:hover strong{text-decoration:underline;text-underline-offset:3px}
.dc .dc-cd a:hover{text-decoration:underline}
.dc .dc-nl{margin-top:44px;text-align:left}
.dc .dc-nl .k{font-size:12px;letter-spacing:1px;font-weight:700;text-transform:uppercase;text-align:center}
.dc .dc-nl b{display:block;margin-top:8px;font-size:20px;font-weight:800;text-align:center}
.dc .dc-nl p.d{margin-top:8px;font-size:13px;line-height:1.5;text-align:center}
.dc .dc-nl form{margin-top:10px}
.dc .dc-nl label{display:block;font-size:12px;letter-spacing:1px;margin-top:26px}
.dc .dc-nl input{display:block;width:100%;font:inherit;font-size:14px;color:var(--dc-red);background:transparent;border:0;border-bottom:1px solid var(--dc-line);border-radius:0;outline:none;padding:10px 0}
.dc .dc-nl input:focus{border-color:var(--dc-red)}
.dc .dc-nl .dc-sub{display:flex;justify-content:center;margin-top:40px}
.dc .dc-nl .dc-b.ol{color:var(--dc-red)}
.dc .dc-nl .nl-note{margin-top:18px;font-size:11.5px;line-height:1.5;text-align:center;opacity:.85}
.dc .dc-nl .nl-note a{text-decoration:underline}
/* ---- reszponzív (a Lovable-töréspontjai) ---- */
@media (max-width:1100px){
 .dc .dc-hero h1{font-size:74px}.dc .dc-hb-l{left:4%}.dc .dc-hb-r{right:8%}
 .dc .dc-vermut h2{font-size:145px}
 .dc .dc-sc h2{font-size:59px}.dc .dc-sc{padding:30px}.dc .dc-life{height:470px}
 .dc .dc-si{padding-left:35px;padding-right:35px}.dc .dc-si h3{font-size:58px}
 .dc .dc-pair h2{font-size:65px}.dc .dc-fg{gap:85px}
}
@media (max-width:767px){
 .dc .dc-eyebrow{font-size:10px;letter-spacing:4px}
 .dc .dc-hero{min-height:700px}
 .dc .dc-stage{height:700px}.dc .dc-copy{padding:70px 16px 0}
 .dc .dc-copy .dc-eyebrow{font-size:9px;letter-spacing:3px;margin-bottom:25px}
 .dc .dc-hero h1{font-size:44px;line-height:1.02}
 .dc .dc-cta{margin-top:305px}.dc .dc-b{padding:0 22px;height:46px;font-size:11px}
 .dc .dc-hb{width:88px}.dc .dc-hb-l{top:318px;left:11%}.dc .dc-hb-r{top:305px;right:17%}
 .dc .dc-hf{width:85px;top:335px;left:30%}.dc .dc-hf2{width:95px;top:22px;left:52%}
 .dc .dc-sh{height:12px;bottom:-25px}
 .dc .dc-vermut{height:705px}.dc .dc-vermut .dc-in{padding-top:55px}
 .dc .dc-vermut h2{font-size:68px;margin-top:15px;text-shadow:-5px 7px 0 var(--dc-shadow)}
 .dc .dc-vb{width:104px;left:calc(50% - 52px);top:163px}
 .dc .dc-pc{width:auto;max-width:380px;margin:337px auto 0;padding:0 24px}
 .dc .dc-pc h3{font-size:13px}.dc .dc-pt{font-size:12px;min-height:80px;margin:16px 0 20px}
 .dc .dc-story{padding:120px 20px 55px}.dc .dc-panel{grid-template-columns:1fr}
 .dc .dc-life{height:340px;border-radius:7px 7px 0 0}
 .dc .dc-sc{min-height:385px;padding:35px 25px}.dc .dc-sc .dc-eyebrow{letter-spacing:4px;margin-bottom:26px}
 .dc .dc-sc h2{font-size:60px}.dc .dc-sc .dc-b{margin-top:64px}
 .dc .dc-sf{width:98px;top:48%}.dc .dc-don{left:auto;right:20px;top:-100px;width:102px;height:202px}
 .dc .dc-sc.open h2{font-size:35px}.dc .dc-st{font-size:12px;line-height:1.6}.dc .dc-sc.open .dc-b{margin-top:20px}
 .dc .dc-serv{padding:50px 22px 65px}.dc .dc-sg{grid-template-columns:1fr;gap:83px;margin-top:63px}
 .dc .dc-si{padding:10px 10px 0}.dc .dc-si+.dc-si{border:0}
 .dc .dc-si h3{font-size:53px}.dc .dc-si h4{font-size:11px}.dc .dc-si p{font-size:12px;max-width:300px}
 .dc .dc-sgl{width:52px;left:41%}.dc .dc-so{width:54px;left:26%}.dc .dc-ssh{width:38px;left:44%}
 .dc .dc-ck:before{height:170px}.dc .dc-ck>.dc-eyebrow{padding-top:25px}
 .dc .dc-car{margin-top:0}
 .dc .dc-sl{flex-basis:78%;height:310px}.dc .dc-sel{height:285px}
 .dc .dc-ci{height:190px;transform:translateY(34px)}.dc .dc-sl.on .dc-ci{height:270px;transform:none}
 .dc .dc-sl.on .dc-ci.tonic,.dc .dc-sl.on .dc-ci.americano,.dc .dc-sl.on .dc-ci.manhattan{height:270px}
 .dc .dc-cn{font-size:28px}.dc .dc-sl.on .dc-cn{font-size:44px}
 .dc .dc-car:before{width:340px;height:140px;left:calc(50% - 170px);top:88px}
 .dc .dc-rec{gap:25px;max-width:390px;grid-template-columns:1fr;padding:0 35px}
 .dc .dc-rm{font-size:12px}.dc .dc-ri{padding:24px}.dc .dc-ck{padding-bottom:55px}
 .dc .dc-pair{padding:60px 24px 45px}.dc .dc-pair h2{font-size:41px;margin-top:20px}
 .dc .dc-pl2{grid-template-columns:1fr;gap:25px;margin-top:35px}.dc .dc-jw{height:260px}
 .dc .dc-jw img{width:158px;left:calc(50% - 79px)}.dc .dc-pair .dc-pc{padding:0;max-width:360px;margin:auto}
 .dc .dc-foot{padding:60px 24px 45px}.dc .dc-fg{grid-template-columns:1fr;gap:65px;max-width:380px}
 .dc .dc-foot .dc-eyebrow{font-size:12px;letter-spacing:5px}.dc .dc-fi,.dc .dc-cd{font-size:12px}
}
@media (max-width:380px){.dc .dc-hero h1{font-size:38px}.dc .dc-vermut h2{font-size:58px}.dc .dc-pair h2{font-size:34px}.dc .dc-sl.on .dc-cn{font-size:38px}}
/* ---- a webshop fejléce a landing vörösében – fehér logó, keret nélkül ---- */
[data-page="doncherry"] .site-head,body:has(.dc) .site-head{background:#7C000B!important;border-bottom:0!important;box-shadow:none!important}
[data-page="doncherry"] .site-head .logo,body:has(.dc) .site-head .logo{background:transparent!important;box-shadow:none!important}
[data-page="doncherry"] .site-head .logo .lb,[data-page="doncherry"] .site-head .logo .lg,body:has(.dc) .site-head .logo .lb,body:has(.dc) .site-head .logo .lg{display:none!important}
[data-page="doncherry"] .site-head .logo .lw,body:has(.dc) .site-head .logo .lw{display:block!important}
[data-page="doncherry"] .site-head .nav a,body:has(.dc) .site-head .nav a{color:#fff!important}
[data-page="doncherry"] .site-head .nav a:hover,body:has(.dc) .site-head .nav a:hover{color:#00C3D4!important}
[data-page="doncherry"] .site-head .menu-btn,body:has(.dc) .site-head .menu-btn{background:rgba(255,255,255,.12)!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.5)!important}
[data-page="doncherry"] .site-head .menu-btn path,body:has(.dc) .site-head .menu-btn path{stroke:#fff!important}
@media (prefers-reduced-motion:reduce){.dc *,.dc *:before,.dc *:after{animation:none!important;transition-duration:.01ms!important}.dc .dc-mo{transform:none!important}
 .dc .dc-hb-l .dc-fl{transform:rotate(-17deg)}.dc .dc-hb-r .dc-fl{transform:rotate(18deg)}}
'''

JS = r'''(function(){
var root=document.querySelector('.dc');if(!root)return;
var still=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
/* parallax – a Lovable-féle data-depth logika: a hero a tetejétől, a többi szakasz a képernyő 40%-ától számol */
var deps=root.querySelectorAll('[data-depth]');
if(deps.length&&!still){var fr=0;var up=function(){fr=0;deps.forEach(function(el){var s=el.closest('section');if(!s)return;var r=s.getBoundingClientRect();
var off=s.classList.contains('dc-hero')?-r.top:window.innerHeight*.4-r.top;var v=Math.max(-90,Math.min(90,off*parseFloat(el.getAttribute('data-depth'))));el.style.setProperty('--px',v.toFixed(1)+'px');});};
window.addEventListener('scroll',function(){if(!fr)fr=requestAnimationFrame(up);},{passive:true});window.addEventListener('resize',up);up();}
/* Több info / Tudni akarom / Vissza – két szöveg között vált */
root.querySelectorAll('[data-dc-flip]').forEach(function(b){var box=root.querySelector('#'+b.getAttribute('aria-controls'));if(!box)return;var a=box.querySelector('[data-a]'),z=box.querySelector('[data-b]');var host=b.closest('[data-dc-host]');
b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',String(o));b.textContent=o?'VISSZA':b.getAttribute('data-l');
a.hidden=o;z.hidden=!o;var on=o?z:a;on.classList.remove('dc-enter');void on.offsetWidth;on.classList.add('dc-enter');if(host)host.classList.toggle('open',o);});});
/* belső menü: aktív szakasz */
var links=root.querySelectorAll('.dc-subnav a');
if('IntersectionObserver' in window&&links.length){var so=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;links.forEach(function(a){if(a.getAttribute('href')==='#'+e.target.id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});});},{rootMargin:'-45% 0px -50% 0px'});
links.forEach(function(a){var s=document.getElementById(a.getAttribute('href').slice(1));if(s)so.observe(s);});}
/* életkép-videó: csak látótérben játszik */
var v=root.querySelector('.dc-life');
if(v&&v.tagName==='VIDEO'){if(still){v.removeAttribute('autoplay');}else if('IntersectionObserver' in window){var vo=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){});}else v.pause();});},{threshold:.2});vo.observe(v);}}
/* koktélsor: végtelen, húzható, a középső a kiválasztott (az Embla loop + center viselkedése) */
var car=root.querySelector('.dc-car');if(!car)return;
var vp=car.querySelector('.dc-vp'),tr=car.querySelector('.dc-tr'),sl=[].slice.call(tr.children),N=parseInt(car.getAttribute('data-n'),10);
var rps=[].slice.call(root.querySelectorAll('.dc-rp'));
var idx=N+0,w=0,x=0;
function sw(){return sl[0].getBoundingClientRect().width;}
function pos(i){return vp.clientWidth/2-(i+.5)*w;}
function place(anim){tr.classList.toggle('anim',!!anim&&!still);x=pos(idx);tr.style.transform='translate3d('+x+'px,0,0)';sl.forEach(function(s,k){var on=k===idx;s.classList.toggle('on',on);var b=s.querySelector('button');b.setAttribute('aria-pressed',String(on));b.tabIndex=(k>=N&&k<2*N)?0:-1;});}
function fill(){var k=idx%N;rps.forEach(function(p,j){p.hidden=j!==k;});var on=rps[k];on.classList.remove('dc-enter');void on.offsetWidth;on.classList.add('dc-enter');}
function go(i,anim){var prev=idx%N;idx=i;place(anim);if(idx%N!==prev)fill();}
tr.addEventListener('transitionend',function(e){if(e.target!==tr)return;if(idx<N||idx>=2*N){idx=N+(idx%N);place(false);}});
function init(){w=sw();place(false);}
window.addEventListener('resize',function(){w=sw();place(false);});
var down=false,sx=0,sx0=0,moved=0,pid=null;
vp.addEventListener('pointerdown',function(e){if(e.button!==0)return;down=true;moved=0;sx=e.clientX;sx0=x;pid=e.pointerId;tr.classList.remove('anim');});
vp.addEventListener('pointermove',function(e){if(!down)return;var d=e.clientX-sx;if(Math.abs(d)>6&&!vp.classList.contains('drag')){vp.classList.add('drag');try{vp.setPointerCapture(pid);}catch(x){}}moved=d;if(vp.classList.contains('drag'))tr.style.transform='translate3d('+(sx0+d)+'px,0,0)';});
function end(){if(!down)return;down=false;var was=vp.classList.contains('drag');vp.classList.remove('drag');if(!was)return;var steps=Math.round(-moved/w);if(steps===0&&Math.abs(moved)>w*.18)steps=moved<0?1:-1;go(Math.max(0,Math.min(3*N-1,idx+steps)),true);}
vp.addEventListener('pointerup',end);vp.addEventListener('pointercancel',end);vp.addEventListener('lostpointercapture',end);
vp.addEventListener('click',function(e){if(Math.abs(moved)>6){e.preventDefault();e.stopPropagation();moved=0;}},true);
sl.forEach(function(s,k){s.querySelector('button').addEventListener('click',function(){if(k!==idx)go(k,true);});});
vp.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();go(idx+1,true);}else if(e.key==='ArrowLeft'){e.preventDefault();go(idx-1,true);}});
if(document.readyState==='complete')init();else window.addEventListener('load',init);init();
})();'''


def build(B):
    """B: a build.py modul (head, header, footer, FAIRS, P, SP, ft, e, write)."""
    r = ''
    e, ft, P = B.e, B.ft, B.P
    SPK = {s: B.SP[s] for s in [c['pack'] for c in COCKTAILS]}
    img = lambda n: f'{r}{IMG}{n}.webp'

    def flo(src, cls, depth, shadow=False, alt=''):
        sh = '<span class="dc-sh"></span>' if shadow else ''
        hidden = '' if alt else ' aria-hidden="true"'
        return f'<div class="dc-mo {cls}" data-depth="{depth}"{hidden}><img class="dc-fl" src="{img(src)}" alt="{e(alt)}" loading="lazy">{sh}</div>'

    don, fr = P['don-cherry'], P['don-cherry-gyumolcse']

    def recipe(c):
        sp = SPK[c['pack']]
        price = f'{ft(sp["price"])}' + (f' <s style="opacity:.7">{ft(sp["old"])}</s>' if sp.get('old') else '')
        return (f'<div class="dc-rm"><p>{e(c["desc"])}</p><p>{e(c["method"])}</p></div>'
                f'<div class="dc-ri"><h3>HOZZÁVALÓK</h3><ul>{"".join(f"<li>{e(i)}</li>" for i in c["ing"])}</ul>'
                f'<p class="dc-pk"><b>{e(sp["name"])}</b>{price}</p>'
                f'<button class="dc-b pp" type="button" data-add="{sp["id"]}" aria-label="{e(sp["name"])} kosárba">{ICO_GIFT}KOKTÉLCSOMAG</button>'
                f'<br><a class="dc-pl" href="{r}termek/{sp["id"]}.html">Mi van a csomagban? →</a></div>')

    n = len(COCKTAILS)
    slides = ''.join(f'<div class="dc-sl{" on" if k == n else ""}"><button class="dc-sel" type="button" aria-label="{e(c["name"].title())} recept" aria-pressed="{"true" if k == n else "false"}"{"" if n <= k < 2 * n else " tabindex=\"-1\" aria-hidden=\"true\""}>'
                     f'<img class="dc-ci {c["kind"]}" src="{img(c["img"])}" alt="{"" if not n <= k < 2 * n else e(c["name"].title()) + " koktél"}" loading="lazy" draggable="false"><span class="dc-cn">{e(c["name"])}</span></button></div>'
                     for k, c in enumerate(COCKTAILS * 3))

    locs = ''.join(f'<li><a href="{r}vasarok.html#{f["id"]}" data-fair="{f["id"]}"><strong>{e(LOCS[f["id"]][0])}</strong>{e(LOCS[f["id"]][1])}'
                   f'<span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span></a></li>' for f in B.FAIRS if f['id'] in LOCS)
    subnav = ''.join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in SUBNAV)

    def offer(p):
        return {'@type': 'Offer', 'price': p['price'], 'priceCurrency': 'HUF', 'availability': 'https://schema.org/InStock', 'url': LIVE + LIVE_URL[p['id']]}
    ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'DON CHERRY prémium édes meggyvermut',
          'itemListElement': [{'@type': 'ListItem', 'position': k + 1, 'item': {'@type': 'Product', 'name': p['name'] + (' 0,75 l' if p['id'] == 'don-cherry' else ' – vermut 0,25 l + meggy 100 g'),
                                                                                   'image': p['img'], 'description': p['short'][:300], 'brand': {'@type': 'Brand', 'name': 'Kontyos'},
                                                                                   'url': LIVE + LIVE_URL[p['id']], 'offers': offer(p)}} for k, p in enumerate((don, fr))]}

    pg = B.head('DON CHERRY – prémium édes meggyvermut | Kontyos',
                'Egy korty, és Don levesz a lábadról. Ismerd meg a Don Cherry prémium édes meggyvermutot, a karakterét és a kedvenc koktéljait – rendeld meg online a Kontyostól!',
                r, 'doncherry', '', f'<style>{CSS}</style>')
    pg += B.header(r) + f'''<main class="dc" id="top"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112.5,700&amp;family=Montserrat:wght@400;600;700;800&amp;family=Poppins:wght@700&amp;display=swap">
<section class="dc-hero" aria-labelledby="dc-h1"><div class="dc-stage">
<div class="dc-copy"><p class="dc-eyebrow">PRÉMIUM ÉDES MEGGYVERMUT</p><h1 id="dc-h1">EGY KORTY,<br>ÉS DON LEVESZ<br>A LÁBADRÓL.</h1><div class="dc-cta"><a class="dc-b cy" href="#vermut">VEGYÉL LE A LÁBAMRÓL</a></div></div>
{flo('palack', 'dc-hb dc-hb-l', .24, True, 'DON CHERRY prémium édes meggyvermut')}{flo('palack', 'dc-hb dc-hb-r', .15, True)}
{flo('meggy', 'dc-hf', .35, True)}{flo('meggy-par', 'dc-hf2', -.15)}
</div></section>
<nav class="dc-subnav" aria-label="Az oldal tartalma"><ul>{subnav}</ul></nav>

<section class="dc-vermut" id="vermut"><div class="dc-in"><p class="dc-eyebrow">MEGGY EGY KIS CSAVARRAL</p><h2>VERMUT</h2>
<div class="dc-mo dc-vb" data-depth="0"><a href="{r}termek/don-cherry.html" aria-label="Don Cherry édes meggyvermut – termékoldal"><img src="{img('palack')}" alt="DON CHERRY meggyvermut, 750 ml" loading="lazy"></a><span class="dc-sh"></span></div>
<div class="dc-pc" id="dc-vm"><h3>· DON CHERRY ·<br>ÉDES MEGGYVERMUT</h3>
<p class="dc-pt" data-a>A friss meggy zamata, a diópálinka karaktere és a gondosan válogatott fűszerek találkozása egy igazán különleges vermutban.<br>Meggyboralap és a friss meggyágyas érlelés.</p>
<p class="dc-pt" data-b hidden>Meggyboralap, friss meggyágyas érlelés, diópálinka és gondosan válogatott fűszerek. Egy karakteres, gyümölcsös vermut.<br><strong>20% vol · 750 ml</strong><br><a class="dc-pl" href="{r}termek/don-cherry.html">Termékoldal és vélemények →</a></p>
<p class="dc-price"><b>{ft(don['price'])}</b>0,75 l · + 50 Ft betétdíj</p>
<div class="dc-join"><button class="dc-b ol" type="button" data-dc-flip data-l="TÖBB INFO" aria-expanded="false" aria-controls="dc-vm">TÖBB INFO</button><button class="dc-b cy" type="button" data-add="don-cherry" aria-label="Don Cherry édes meggyvermut kosárba">{ICO_BAG}VÁSÁRLÁS</button></div></div>
</div></section>

<section class="dc-story" id="ki-az-a-don"><div class="dc-panel">
<video class="dc-life" muted loop playsinline autoplay preload="metadata" poster="{img('lifestyle')}" aria-label="Don Cherry palack és meggyes koktélok egy retró rádió mellett, a medence partján"><source src="{r}{IMG}lifestyle-540.mp4" type="video/mp4" media="(max-width:767px)"><source src="{r}{IMG}lifestyle-832.mp4" type="video/mp4"></video>
<div class="dc-don" aria-hidden="true"><img class="bd" src="{img('don-figura')}" alt=""><img class="sl" src="{img('don-figura')}" alt=""><img class="sr2" src="{img('don-figura')}" alt=""></div>
<div class="dc-sc" id="dc-st" data-dc-host><p class="dc-eyebrow">KI IS VALÓJÁBAN</p>
<h2 data-a>DON<br>CHERRY?</h2>
<div data-b hidden><h2>DON<br>CHERRY?</h2><p class="dc-st">Don Cherry nem siet sehová. Elegánsan hátradől, megigazítja a kalapját, és élvezi a pillanatot. Egy kicsit csibész, egy kicsit úriember – de unalmasnak sosem neveznéd. A meggy a szenvedélye, a jó társaság a gyengéje. Ha megjelenik, a hétköznapból is alkalom lesz. Egy korty, és már érted, miért.</p></div>
{flo('meggy-story', 'dc-sf', .17, True)}
<button class="dc-b rd" type="button" data-dc-flip data-l="TUDNI AKAROM" aria-expanded="false" aria-controls="dc-st">TUDNI AKAROM</button></div>
</div></section>

<section class="dc-serv" id="ahogy-a-don-szereti"><h2 class="dc-eyebrow">AHOGY A DON SZERETI</h2><div class="dc-sg">
<article class="dc-si">{flo('narancs', 'dc-so', .19)}{flo('aperitif-pohar', 'dc-sgl', -.08)}<h3>APERITIF</h3><h4>· 8 CL · JÉG · NARANCS ·</h4><p>8 cl Don Cherry, jég és egy narancskarika. Frissítő, társasági ital, hosszan kitartó meggyes aromával.</p></article>
<article class="dc-si">{flo('shot-pohar', 'dc-ssh', -.1)}{flo('meggy-kicsi', 'dc-sfr', .2)}<h3>SHOT</h3><h4>· 4 CL · 1 MEGGYSZEM ·</h4><p>Egy 5 cl-es pohár aljára tegyél egy meggyszemet, önts rá 4 cl Don Cherryt, és idd meg két kortyban. Rövid, intenzív élmény, ideális buliindító.</p></article>
</div></section>

<section class="dc-ck" id="koktelok" aria-label="Koktélreceptek"><h2 class="dc-eyebrow">KOKTÉLKÉNT</h2>
<div class="dc-car" data-n="{n}"><div class="dc-vp" tabindex="0" aria-label="Koktélok – húzd vagy használd a nyilakat"><div class="dc-tr">{slides}</div></div></div>
<div class="dc-hint" aria-hidden="true">{ICO_DRAG}</div>
<div class="dc-recs" aria-live="polite">{''.join(f'<div class="dc-rec dc-rp"{"" if k == 0 else " hidden"} data-i="{k}">{recipe(c)}</div>' for k, c in enumerate(COCKTAILS))}</div>
</section>

<section class="dc-pair" id="meggy"><div class="dc-in"><p class="dc-eyebrow">EGY TÖKÉLETES PÁROSÍTÁS</p><h2>DON CHERRY &amp; MEGGY</h2>
<div class="dc-pl2"><div class="dc-jw"><a href="{r}termek/don-cherry-gyumolcse.html" aria-label="Don Cherry gyümölcse – termékoldal"><img src="{img('gyumolcse')}" alt="Don Cherry gyümölcse: vermut és meggy befőttesüvegben" loading="lazy"></a></div>
<div class="dc-pc" id="dc-gy"><h3>· DON CHERRY GYÜMÖLCSE ·</h3>
<p class="dc-pt" data-a>Ahol Don Cherry megjelenik, ott a meggy sem maradhat távol. Édes, zamatos és ellenállhatatlan társ – pontosan olyan, amilyennek egy igazi úriember a kísérőjét választja.</p>
<p class="dc-pt" data-b hidden>A vermutban érlelt meggy az aperitifek és koktélok karakteres kísérője. Egy szem a pohár aljára, egy a koktél tetejére – a Don minden részletre figyel.<br><strong>0,25 l vermut + 100 g meggy</strong><br><a class="dc-pl" href="{r}termek/don-cherry-gyumolcse.html">Termékoldal →</a></p>
<p class="dc-price"><b>{ft(fr['price'])}</b>+ 50 Ft betétdíj</p>
<div class="dc-join"><button class="dc-b ol" type="button" data-dc-flip data-l="TÖBB INFO" aria-expanded="false" aria-controls="dc-gy">TÖBB INFO</button><button class="dc-b rd" type="button" data-add="don-cherry-gyumolcse" aria-label="Don Cherry gyümölcse kosárba">{ICO_BAG}VÁSÁRLÁS</button></div></div></div>
</div></section>

<section class="dc-foot"><div class="dc-fg">
<div id="hol-kaphato"><h2 class="dc-eyebrow">HOL KAPHATÓ?</h2><p class="dc-fi">Termékeinkkel a Lidl üzleteiben, <a href="{r}termek/don-cherry.html" style="text-decoration:underline">webshopunkon</a> és az adventi vásárok helyszínein is találkozhattok!</p>
<img class="dc-lidl" src="{img('lidl')}" alt="Hamarosan a Lidl kínálatában!" width="235" height="66" loading="lazy"><ul class="dc-locs">{locs}</ul></div>
<div id="kapcsolat"><h2 class="dc-eyebrow">KAPCSOLAT</h2><p class="dc-cd"><a href="tel:+36300945042">+36 30 094 5042</a><br><a href="mailto:webshop@kontyos.hu">webshop@kontyos.hu</a><br>6773 Klárafalva, Kossuth u. 183.</p>
<div class="dc-nl"><p class="k">Hírlevél</p><b>−5% az első rendelésedből</b><p class="d">Iratkozz fel: a kuponkódot azonnal küldjük, mellé új koktélreceptek és szezonális ajánlatok – elsőként.</p>
<form data-newsletter><label for="dc-nl">E-mail cím:*</label><input id="dc-nl" type="email" autocomplete="email" required><div class="dc-sub"><button class="dc-b ol" type="submit">FELIRATKOZOM</button></div></form></div></div>
</div></section>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script>{JS}</script>
</main>''' + B.footer(r)
    import re as _re
    # a Shoprenter-generátor a Párizs-ütköző osztályokat (card, btn, row…) k- előtaggal átnevezi – az oldal saját <style>-ját nem –, ezért itt tilos
    _bad = {c for cl in _re.findall(r'class="([^"]*)"', pg[pg.find('<main'):pg.find('</main>')]) for c in cl.split()} & {'badge', 'btn', 'card', 'close', 'col', 'h1', 'h2', 'h3', 'head', 'lead', 'left', 'nav', 'price', 'right', 'row', 'small', 'tall', 'breadcrumb'}
    assert not _bad, f'Párizs-ütköző osztálynév a Don Cherry oldalon: {_bad}'
    B.write('doncherry.html', pg)
