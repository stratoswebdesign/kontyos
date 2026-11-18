{# Kontyos – aloldal: pirimama.html → /pirimama. Generálva: src/shoprenter.py – kézzel ne szerkeszd, a demóból újragenerálható. #}
<style>
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
.pm .pm-script{width:min(70vw,352px);aspect-ratio:116.85/38.03;margin-top:4px;background:var(--pm-rose);-webkit-mask:url(https://stratoswebdesign.github.io/kontyos/img/pirimama/tel-fuszereivel.svg) center/contain no-repeat;mask:url(https://stratoswebdesign.github.io/kontyos/img/pirimama/tel-fuszereivel.svg) center/contain no-repeat;animation:pm-wipe 1.7s 1.1s ease-in-out both;will-change:transform}
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
</style><script type="application/ld+json">{"@context": "https://schema.org", "@type": "ItemList", "name": "PIRI Mama forralt borok", "itemListElement": [{"@type": "ListItem", "position": 1, "item": {"@type": "Product", "name": "PIRI Mama forralt bora 1 l", "image": "https://stratoswebdesign.github.io/kontyos/img/p/piri-mama-forralt-bora-1l.webp", "description": "Valódi fűszerekkel ízesített kész forralt gyümölcsbor, a tél fűszerei mellett a meggy és a szilva dominál, ahogy Piri mama készíti.", "brand": {"@type": "Brand", "name": "Kontyos"}, "url": "https://www.kontyos.hu/piri-mama-forralt-bora-1l", "offers": {"@type": "Offer", "price": 2190, "priceCurrency": "HUF", "availability": "https://schema.org/InStock", "url": "https://www.kontyos.hu/piri-mama-forralt-bora-1l"}}}, {"@type": "ListItem", "position": 2, "item": {"@type": "Product", "name": "Epres PIRI Mama forralt bora 1 l", "image": "https://stratoswebdesign.github.io/kontyos/img/p/epres-piri-mama-forralt-bora-1l.webp", "description": "Gyümölcsös ízvilágú kész forralt bor, amelyben az eper, az narancs és egy leheletnyi vanília harmonikusan érvényesül, ahogy Piri mama készíti.", "brand": {"@type": "Brand", "name": "Kontyos"}, "url": "https://www.kontyos.hu/piri-mama-epres-forralt-bora-1l", "offers": {"@type": "Offer", "price": 2190, "priceCurrency": "HUF", "availability": "https://schema.org/InStock", "url": "https://www.kontyos.hu/piri-mama-epres-forralt-bora-1l"}}}, {"@type": "ListItem", "position": 3, "item": {"@type": "Product", "name": "Narancsos PIRI Mama forralt bora 1 l", "image": "https://stratoswebdesign.github.io/kontyos/img/p/piri-mama-narancsos-forralt-bora-1l.webp", "description": "Valódi fűszerekkel ízesített kész forralt gyümölcsbor, a tél fűszerei mellett a narancsos a szegfőszeg dominál, ahogy Piri mama készíti.", "brand": {"@type": "Brand", "name": "Kontyos"}, "url": "https://www.kontyos.hu/piri-mama-narancsos-forralt-bora-1l", "offers": {"@type": "Offer", "price": 2190, "priceCurrency": "HUF", "availability": "https://schema.org/InStock", "url": "https://www.kontyos.hu/piri-mama-narancsos-forralt-bora-1l"}}}, {"@type": "ListItem", "position": 4, "item": {"@type": "Product", "name": "PIRI Mama forró itala 0% 1 l", "image": "https://stratoswebdesign.github.io/kontyos/img/p/piri-mama-forro-itala-0-alc.webp", "description": "Valódi fűszerekkel ízesített forralt bor ízű 70 % - os gyümölcsital, a tél fűszerei mellett a meggy és a szilva dominál, ahogy Piri mama készíti. Felbontás után hűtőben tárolandó, 1 héten belül fogyasztandó !", "brand": {"@type": "Brand", "name": "Kontyos"}, "url": "https://www.kontyos.hu/piri-mama-forro-itala-0-alc", "offers": {"@type": "Offer", "price": 2190, "priceCurrency": "HUF", "availability": "https://schema.org/InStock", "url": "https://www.kontyos.hu/piri-mama-forro-itala-0-alc"}}}]}</script><div class="ky " data-page="pirimama"><main class="pm" id="top"><script>document.currentScript.parentNode.classList.add('pm-js')</script>
<div class="page-snow" aria-hidden="true"><i style="left:0.0%;width:10px;opacity:0.45;--dur:10s;--delay:-0.00s;--drift:-45px"></i><i style="left:37.7%;width:17px;opacity:0.58;--dur:17s;--delay:-3.17s;--drift:55px"></i><i style="left:75.4%;width:24px;opacity:0.71;--dur:13s;--delay:-6.34s;--drift:-45px"></i><i style="left:13.1%;width:12px;opacity:0.84;--dur:20s;--delay:-9.51s;--drift:55px"></i><i style="left:50.8%;width:19px;opacity:0.57;--dur:16s;--delay:-12.68s;--drift:-45px"></i><i style="left:88.5%;width:26px;opacity:0.70;--dur:12s;--delay:-15.85s;--drift:55px"></i><i style="left:26.2%;width:14px;opacity:0.83;--dur:19s;--delay:-19.02s;--drift:-45px"></i><i style="left:63.9%;width:21px;opacity:0.56;--dur:15s;--delay:-1.19s;--drift:55px"></i><i style="left:1.6%;width:28px;opacity:0.69;--dur:11s;--delay:-4.36s;--drift:-45px"></i><i style="left:39.3%;width:16px;opacity:0.82;--dur:18s;--delay:-7.53s;--drift:55px"></i><i style="left:77.0%;width:23px;opacity:0.55;--dur:14s;--delay:-10.70s;--drift:-45px"></i><i style="left:14.7%;width:11px;opacity:0.68;--dur:10s;--delay:-13.87s;--drift:55px"></i><i style="left:52.4%;width:18px;opacity:0.81;--dur:17s;--delay:-17.04s;--drift:-45px"></i><i style="left:90.1%;width:25px;opacity:0.54;--dur:13s;--delay:-20.21s;--drift:55px"></i><i style="left:27.8%;width:13px;opacity:0.67;--dur:20s;--delay:-2.38s;--drift:-45px"></i><i style="left:65.5%;width:20px;opacity:0.80;--dur:16s;--delay:-5.55s;--drift:55px"></i><i style="left:3.2%;width:27px;opacity:0.53;--dur:12s;--delay:-8.72s;--drift:-45px"></i><i style="left:40.9%;width:15px;opacity:0.66;--dur:19s;--delay:-11.89s;--drift:55px"></i><i class="m" style="left:78.6%;width:22px;opacity:0.79;--dur:15s;--delay:-15.06s;--drift:-45px"></i><i class="m" style="left:16.3%;width:10px;opacity:0.52;--dur:11s;--delay:-18.23s;--drift:55px"></i><i class="m" style="left:54.0%;width:17px;opacity:0.65;--dur:18s;--delay:-0.40s;--drift:-45px"></i><i class="m" style="left:91.7%;width:24px;opacity:0.78;--dur:14s;--delay:-3.57s;--drift:55px"></i><i class="m" style="left:29.4%;width:12px;opacity:0.51;--dur:10s;--delay:-6.74s;--drift:-45px"></i><i class="m" style="left:67.1%;width:19px;opacity:0.64;--dur:17s;--delay:-9.91s;--drift:55px"></i><i class="m" style="left:4.8%;width:26px;opacity:0.77;--dur:13s;--delay:-13.08s;--drift:-45px"></i><i class="m" style="left:42.5%;width:14px;opacity:0.50;--dur:20s;--delay:-16.25s;--drift:55px"></i><i class="m" style="left:80.2%;width:21px;opacity:0.63;--dur:16s;--delay:-19.42s;--drift:-45px"></i><i class="m" style="left:17.9%;width:28px;opacity:0.76;--dur:12s;--delay:-1.59s;--drift:55px"></i><i class="m" style="left:55.6%;width:16px;opacity:0.49;--dur:19s;--delay:-4.76s;--drift:-45px"></i><i class="m" style="left:93.3%;width:23px;opacity:0.62;--dur:15s;--delay:-7.93s;--drift:55px"></i><i class="m" style="left:31.0%;width:11px;opacity:0.75;--dur:11s;--delay:-11.10s;--drift:-45px"></i><i class="m" style="left:68.7%;width:18px;opacity:0.48;--dur:18s;--delay:-14.27s;--drift:55px"></i></div>
<section class="pm-hero" aria-labelledby="pm-h1">
<div class="pm-hero-ph" data-px="0.35"><img src="https://stratoswebdesign.github.io/kontyos/img/pirimama/hero-1920.webp" srcset="https://stratoswebdesign.github.io/kontyos/img/pirimama/hero-800.webp 800w, https://stratoswebdesign.github.io/kontyos/img/pirimama/hero-1200.webp 1200w, https://stratoswebdesign.github.io/kontyos/img/pirimama/hero-1920.webp 1920w" sizes="100vw" alt="PIRI Mama forralt bor palackja téli fűszerek között" width="1920" height="1281" fetchpriority="high"></div>
<div class="fall" aria-hidden="true"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:36.6%;width:35px;--dur:12.5s;--delay:-19.1s;--drift:-37px;--o:0.74"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" style="left:32.7%;width:50px;--dur:21.3s;--delay:-15.4s;--drift:28px;--o:0.93"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:41.4%;width:49px;--dur:12.9s;--delay:-1.1s;--drift:-45px;--o:0.92"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:75.9%;width:39px;--dur:15.2s;--delay:-16.4s;--drift:-66px;--o:0.63"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" style="left:77.7%;width:40px;--dur:20.8s;--delay:-17.0s;--drift:-40px;--o:0.69"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:69.5%;width:23px;--dur:11.1s;--delay:-9.0s;--drift:62px;--o:0.61"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:72.2%;width:29px;--dur:20.4s;--delay:-21.2s;--drift:-26px;--o:0.78"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" style="left:19.9%;width:57px;--dur:11.1s;--delay:-1.8s;--drift:-45px;--o:0.78"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:19.4%;width:37px;--dur:11.8s;--delay:-4.2s;--drift:-55px;--o:0.61"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:70.5%;width:48px;--dur:11.5s;--delay:-5.9s;--drift:-57px;--o:0.84"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" style="left:3.4%;width:49px;--dur:20.6s;--delay:-8.9s;--drift:-28px;--o:0.75"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:82.9%;width:43px;--dur:16.7s;--delay:-12.4s;--drift:-63px;--o:0.59"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:35.8%;width:47px;--dur:13.3s;--delay:-4.4s;--drift:-39px;--o:0.79"><img src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" style="left:10.9%;width:34px;--dur:13.4s;--delay:-5.9s;--drift:-35px;--o:0.66" class=d><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:5.4%;width:36px;--dur:15.2s;--delay:-12.3s;--drift:45px;--o:0.83" class=d><img src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" style="left:72.3%;width:29px;--dur:15.7s;--delay:-5.1s;--drift:45px;--o:0.93" class=d></div>
<div class="pm-hero-in">
<div class="pm-hl" data-px="-0.08">
<div class="d1" aria-hidden="true"><img class="pm-sway" src="https://stratoswebdesign.github.io/kontyos/img/deco/holly.svg" alt=""><span class="o"><img class="pm-swing" src="https://stratoswebdesign.github.io/kontyos/img/deco/ornament-gold.svg" alt="" style="--dur:6s"></span></div>
<div class="d2" aria-hidden="true"><img class="pm-float" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/csillag-feher.svg" alt=""></div>
<div class="d3" aria-hidden="true"><img class="pm-spin" src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-blue.svg" alt=""></div>
<h1 id="pm-h1">PIRI MAMA<br>FORRALT BORA</h1></div>
<div data-px="-0.2"><p class="pm-script"><span class="sr">A tél fűszereivel</span></p></div>
<p class="pm-hero-lead">Kész forralt gyümölcsbor valódi fűszerekkel. Otthon csak melegíteni kell – és már a tiéd az adventi vásárok hangulata.</p>
<div class="pm-cta"><a class="pm-btn gold" href="#termekek">Rendeld meg online</a><a class="pm-btn" href="#hol-kaphato">Adventi vásárok</a></div>
</div>
<img class="pm-deer pm-float" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/szarvas.svg" alt="" aria-hidden="true">
</section>
<nav class="pm-subnav" aria-label="Az oldal tartalma"><ul><li><a href="#termekek">Termékek</a></li><li><a href="#miert-mas">Miért más?</a></li><li><a href="#hol-kaphato">Hol kapható?</a></li><li><a href="#tortenetunk">Történetünk</a></li><li><a href="#webshop">Webshop</a></li></ul></nav>

<section class="pm-sec pm-products" id="termekek">
<h2 class="pm-eyebrow" data-reveal>Termékeink</h2>
<p class="pm-intro" data-reveal>Egyliteres palackban, négyféle ízben – válaszd ki a kedvencedet, és megérkezik hozzád.</p>
<div class="pm-cards"><article class="pm-card" style="--bg:#5A5F88;--bg2:#414463;--d:0.00s" data-reveal>
<img class="dk pm-twinkle" src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" aria-hidden="true" style="--delay:-0s"><img class="dk2 pm-float" src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" aria-hidden="true" style="--delay:-0s">
<h3>Piri Mama</h3><p class="sb">Forralt bora</p>
<a class="bt" href="/piri-mama-forralt-bora-1l" aria-label="PIRI Mama forralt bora – termékoldal"><img src="https://stratoswebdesign.github.io/kontyos/img/t/piri-mama-forralt-bora-1l.webp" alt="PIRI Mama forralt bora 1 literes palack" width="376" height="1400" loading="lazy"></a>
<p class="rt" aria-label="Értékelés: 4.93 az 5-ből, 15 vélemény">★★★★★ 4,93 · 15 vélemény</p><p class="pr"><b>2 190 Ft</b><small>1 l · + 50 Ft betétdíj</small></p>
<div class="ac"><button class="pm-btn dark" type="button" data-add="piri-mama-forralt-bora" data-sku="Forralt04X" aria-label="PIRI Mama forralt bora kosárba"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 7h14l-1.5 12h-11z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>Kosárba</button>
<button class="pm-btn" type="button" data-pm-spec aria-expanded="false" aria-controls="pm-sp-0">Részletek</button></div>
<div class="sp" id="pm-sp-0"><h4>Piri Mama <span>Forralt bora</span></h4><p>Valódi fűszerekkel ízesített kész forralt gyümölcsbor, a tél fűszerei mellett a meggy és a szilva dominál, ahogy Piri mama készíti.</p><dl><div><dt>Alkoholtartalom</dt><dd>8 %vol</dd></div><div><dt>Gyümölcs</dt><dd>Meggybor</dd></div><div><dt>Kiszerelés</dt><dd>1000 ml</dd></div><div><dt>Összetétel</dt><dd>meggybor, almabor,szilvabor, víz, izoglükóz szörp, cukor, fahéj, szegfűszeg, aromák, szulfit</dd></div><div><dt>Ajánlott fogyasztási hőmérséklet</dt><dd>55 °C</dd></div><div><dt>Egységár</dt><dd>2 190 Ft/l</dd></div><div><dt>Minőségét megőrzi</dt><dd>címke szerint (24 hónap, felbontás után 2 hét)</dd></div></dl><p class="nt">A bort sosem forraljuk: lassan melegítsd, legfeljebb 55–60 °C-ig.</p><a href="/piri-mama-forralt-bora-1l">Termékoldal és vélemények →</a></div>
</article><article class="pm-card" style="--bg:#E54731;--bg2:#AA3222;--d:0.12s" data-reveal>
<img class="dk pm-twinkle" src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" aria-hidden="true" style="--delay:-1s"><img class="dk2 pm-float" src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" aria-hidden="true" style="--delay:-2s">
<h3>Epres Piri Mama</h3><p class="sb">Forralt bora</p>
<a class="bt" href="/piri-mama-epres-forralt-bora-1l" aria-label="Epres PIRI Mama forralt bora – termékoldal"><img src="https://stratoswebdesign.github.io/kontyos/img/t/epres-piri-mama-forralt-bora-1l.webp" alt="Epres PIRI Mama forralt bora 1 literes palack" width="376" height="1400" loading="lazy"></a>
<p class="rt" aria-label="Értékelés: 5.00 az 5-ből, 1 vélemény">★★★★★ 5,00 · 1 vélemény</p><p class="pr"><b>2 190 Ft</b><small>1 l · + 50 Ft betétdíj</small></p>
<div class="ac"><button class="pm-btn dark" type="button" data-add="epres-piri-mama-forralt-bora" data-sku="Forralt_epres" aria-label="Epres PIRI Mama forralt bora kosárba"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 7h14l-1.5 12h-11z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>Kosárba</button>
<button class="pm-btn" type="button" data-pm-spec aria-expanded="false" aria-controls="pm-sp-1">Részletek</button></div>
<div class="sp" id="pm-sp-1"><h4>Epres Piri Mama <span>Forralt bora</span></h4><p>Gyümölcsös ízvilágú kész forralt bor, amelyben az eper, az narancs és egy leheletnyi vanília harmonikusan érvényesül, ahogy Piri mama készíti.</p><dl><div><dt>Alkoholtartalom</dt><dd>8 %vol</dd></div><div><dt>Gyümölcs</dt><dd>Eperbor</dd></div><div><dt>Kiszerelés</dt><dd>1000 ml</dd></div><div><dt>Összetétel</dt><dd>almabor,eperbor, narancsbor, víz, izoglükóz szörp, cukor, fahéj, aromák, szulfit</dd></div><div><dt>Ajánlott fogyasztási hőmérséklet</dt><dd>55 °C</dd></div><div><dt>Egységár</dt><dd>2 190 Ft/l</dd></div><div><dt>Minőségét megőrzi</dt><dd>címke szerint (24 hónap, felbontás után 2 hét)</dd></div></dl><p class="nt">A bort sosem forraljuk: lassan melegítsd, legfeljebb 55–60 °C-ig.</p><a href="/piri-mama-epres-forralt-bora-1l">Termékoldal és vélemények →</a></div>
</article><article class="pm-card" style="--bg:#F96817;--bg2:#B94B0E;--d:0.24s" data-reveal>
<img class="dk pm-twinkle" src="https://stratoswebdesign.github.io/kontyos/img/deco/ornament-gold.svg" alt="" aria-hidden="true" style="--delay:-2s"><img class="dk2 pm-float" src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" aria-hidden="true" style="--delay:-4s"><span class="tg">Új</span>
<h3>Narancsos Piri Mama</h3><p class="sb">Forralt bora</p>
<a class="bt" href="/piri-mama-narancsos-forralt-bora-1l" aria-label="Narancsos PIRI Mama forralt bora – termékoldal"><img src="https://stratoswebdesign.github.io/kontyos/img/t/piri-mama-narancsos-forralt-bora-1l.webp" alt="Narancsos PIRI Mama forralt bora 1 literes palack" width="376" height="1400" loading="lazy"></a>
<p class="pr"><b>2 190 Ft</b><small>1 l · + 50 Ft betétdíj</small></p>
<div class="ac"><button class="pm-btn dark" type="button" data-add="narancsos-piri-mama-forralt-bora" data-sku="Forralt05" aria-label="Narancsos PIRI Mama forralt bora kosárba"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 7h14l-1.5 12h-11z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>Kosárba</button>
<button class="pm-btn" type="button" data-pm-spec aria-expanded="false" aria-controls="pm-sp-2">Részletek</button></div>
<div class="sp" id="pm-sp-2"><h4>Narancsos Piri Mama <span>Forralt bora</span></h4><p>Valódi fűszerekkel ízesített kész forralt gyümölcsbor, a tél fűszerei mellett a narancsos a szegfőszeg dominál, ahogy Piri mama készíti.</p><dl><div><dt>Alkoholtartalom</dt><dd>8 %vol</dd></div><div><dt>Gyümölcs</dt><dd>Almabor</dd></div><div><dt>Kiszerelés</dt><dd>1000 ml</dd></div><div><dt>Összetétel</dt><dd>narancsbor, almabor, víz, cukor, fahéj, szegfűszeg, aromák, szulfit</dd></div><div><dt>Ajánlott fogyasztási hőmérséklet</dt><dd>55 °C</dd></div><div><dt>Egységár</dt><dd>2 190 Ft/l</dd></div><div><dt>Minőségét megőrzi</dt><dd>címke szerint (24 hónap, felbontás után 2 hét)</dd></div></dl><p class="nt">A bort sosem forraljuk: lassan melegítsd, legfeljebb 55–60 °C-ig.</p><a href="/piri-mama-narancsos-forralt-bora-1l">Termékoldal és vélemények →</a></div>
</article><article class="pm-card" style="--bg:#5D7AB7;--bg2:#4A6399;--d:0.36s" data-reveal>
<img class="dk pm-twinkle" src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" aria-hidden="true" style="--delay:-3s"><img class="dk2 pm-float" src="https://stratoswebdesign.github.io/kontyos/img/deco/snow-dots.svg" alt="" aria-hidden="true" style="--delay:-6s"><span class="tg">Alkoholmentes</span>
<h3>Piri Mama</h3><p class="sb">Forró itala 0%</p>
<a class="bt" href="/piri-mama-forro-itala-0-alc" aria-label="PIRI Mama forró itala 0% – termékoldal"><img src="https://stratoswebdesign.github.io/kontyos/img/t/piri-mama-forro-itala-0-alc.webp" alt="PIRI Mama forró itala 0% 1 literes palack" width="376" height="1400" loading="lazy"></a>
<p class="pr"><b>2 190 Ft</b><small>1 l · + 50 Ft betétdíj</small></p>
<div class="ac"><button class="pm-btn dark" type="button" data-add="piri-mama-forro-itala-0" data-sku="Forró_Itala" aria-label="PIRI Mama forró itala 0% kosárba"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 7h14l-1.5 12h-11z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>Kosárba</button>
<button class="pm-btn" type="button" data-pm-spec aria-expanded="false" aria-controls="pm-sp-3">Részletek</button></div>
<div class="sp" id="pm-sp-3"><h4>Piri Mama <span>Forró itala 0%</span></h4><p>Valódi fűszerekkel ízesített forralt bor ízű 70 % - os gyümölcsital, a tél fűszerei mellett a meggy és a szilva dominál, ahogy Piri mama készíti. Felbontás után hűtőben tárolandó, 1 héten belül fogyasztandó !</p><dl><div><dt>Gyümölcs</dt><dd>Alma</dd></div><div><dt>Gyümölcstartalom</dt><dd>minimum 70 %</dd></div><div><dt>Alkoholtartalom</dt><dd>0%</dd></div><div><dt>Kiszerelés</dt><dd>1000 ml</dd></div><div><dt>Összetevők</dt><dd>gyümölcs sűrítmény (szőlő 23%, alma 19%, meggy 13%, narancs 13%, szilva 3%), szűrt ivóvíz, cukor, fahéj, szegfűszeg,savanyúságot szabályozó anyag citromsav, aromák (vanília, meggy),</dd></div><div><dt>tartósítószer</dt><dd>kálium–szorbát,nátrium–benzoát.</dd></div><div><dt>Ajánlott fogyasztási hőmérséklet</dt><dd>55 °C</dd></div><div><dt>Egységár</dt><dd>2 190 Ft/l</dd></div><div><dt>Minőségét megőrzi</dt><dd>címke szerint (6 hónap, száraz hűvös helyen tárolandó! Felbontás után hűtőben tárolandó,1 héten belül fogyasztandó!)</dd></div><div><dt>Energia</dt><dd>200 kJ / 47 kcal</dd></div><div><dt>Cukor</dt><dd>11,3 g</dd></div></dl><p class="nt">Melegen és hidegen is finom. Felbontás után hűtőben tárold, és egy héten belül fogyaszd el.</p><a href="/piri-mama-forro-itala-0-alc">Termékoldal és vélemények →</a></div>
</article></div>
<div class="pm-ups">
<div class="pm-up" data-reveal><a class="im" href="/kedvezmenyek/csomagajanlatok" aria-label="PIRI Mama forraltbor csomag – 5 palack"><img src="https://stratoswebdesign.github.io/kontyos/img/csomag/pack-forralt-6.webp" alt="PIRI Mama forraltbor csomag – 5 palack" loading="lazy"></a>
<div class="tx"><span class="k">Csomagban olcsóbb</span><b>PIRI Mama forraltbor csomag – 5 palack</b><span class="ds">3 klasszikus, 1 epres és 1 narancsos PIRI Mama.</span><span class="p">8 760 Ft<s>10 950 Ft</s></span>
<button class="pm-btn gold" type="button" data-add="forralt-6" data-sku="KY-PIRI-5">Kosárba</button></div></div>
<div class="pm-up" data-reveal style="--d:.12s"><a class="im" href="/piri-mama-bogreje-032-l" aria-label="PIRI Mama bögréje 0,32 l"><img src="https://stratoswebdesign.github.io/kontyos/img/t/piri-mama-bogreje-032-l.webp" alt="PIRI Mama bögréje 0,32 l" loading="lazy"></a>
<div class="tx"><span class="k">Hozzá illik</span><b>PIRI Mama bögréje 0,32 l</b><span class="ds">Hőálló üvegbögre – a vásári hangulathoz otthon is.</span><span class="p">2 490 Ft</span>
<button class="pm-btn" type="button" data-add="piri-mama-bogreje" data-sku="piribögre">Kosárba</button></div></div></div>
</section>

<section class="pm-sec pm-usp-sec" id="miert-mas">
<h2 class="pm-eyebrow" data-reveal>Piri Mama – Miért más?</h2>
<div class="pm-usps"><div class="pm-usp" data-reveal style="--d:0.00s"><div class="ic"><img class="pm-swing" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/usp-01.svg" alt="" aria-hidden="true" style="--delay:-0s"></div>
<h3>Zamatát a gyümölcs adja</h3><p>Saját gyümölcsborainkból készül: meggyből, szilvából, eperből, narancsból és almából.</p></div><div class="pm-usp" data-reveal style="--d:0.12s"><div class="ic"><img class="pm-float" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/usp-03.svg" alt="" aria-hidden="true" style="--delay:-1s"></div>
<h3>Csak melegíteni kell</h3><p>Otthon pár perc alatt kész – az adventi vásárok hangulata a konyhádban.</p></div><div class="pm-usp" data-reveal style="--d:0.24s"><div class="ic"><img class="pm-sway" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/usp-02.svg" alt="" aria-hidden="true" style="--delay:-2s"></div>
<h3>A tél fűszereivel</h3><p>Valódi fahéj és szegfűszeg – Piri mama jól bevált receptje szerint.</p></div><div class="pm-usp" data-reveal style="--d:0.36s"><div class="ic"><img class="pm-twinkle" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/usp-04.svg" alt="" aria-hidden="true" style="--delay:-3s"></div>
<h3>Minden ízlésre</h3><p>Klasszikus, epres, narancsos és alkoholmentes, 0%-os változatban is.</p></div></div>
</section>

<section class="pm-sec pm-where" id="hol-kaphato">
<h2 class="pm-eyebrow" data-reveal>Hol kapható?</h2>
<p class="pm-sub-eyebrow" data-reveal style="margin-top:clamp(40px,5vw,64px)">Adventi vásárok</p>
<p class="pm-intro" data-reveal>Frissen melegítve, forrón kínáljuk – keress minket a standjainkon!</p>
<div class="fair-grid fair-row" id="pm-fair-row"><a class="fair-card2" href="/vasarok#szeged" data-fair="szeged"><span class="im"><img src="https://stratoswebdesign.github.io/kontyos/img/fair/szeged.webp" alt="Adventi vásár – Szeged" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>Szeged – Dóm tér</b><span class="pl">Január 4-ig nyitva</span></span></a><a class="fair-card2" href="/vasarok#obuda" data-fair="obuda"><span class="im"><img src="https://stratoswebdesign.github.io/kontyos/img/fair/obuda.webp" alt="Adventi vásár – Budapest – Óbuda" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>Budapest – Óbuda – Szentlélek tér</b><span class="pl">December 23-ig</span></span></a><a class="fair-card2" href="/vasarok#gyor" data-fair="gyor"><span class="im"><img src="https://stratoswebdesign.github.io/kontyos/img/fair/gyor.webp" alt="Adventi vásár – Győr" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>Győr – Baross utca</b><span class="pl">Szilveszterig nyitva</span></span></a><a class="fair-card2" href="/vasarok#szombathely" data-fair="szombathely"><span class="im"><img src="https://stratoswebdesign.github.io/kontyos/img/fair/szombathely.webp" alt="Adventi vásár – Szombathely" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>Szombathely – Fő tér</b><span class="pl">Elsőként nyitunk, december 23-ig</span></span></a><a class="fair-card2" href="/vasarok#veszprem" data-fair="veszprem"><span class="im"><img src="https://stratoswebdesign.github.io/kontyos/img/fair/veszprem.webp" alt="Adventi vásár – Veszprém" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>Veszprém – Kossuth Lajos utca, belváros</b><span class="pl">December 23-ig</span></span></a><a class="fair-card2" href="/vasarok#pecs" data-fair="pecs"><span class="im"><img src="https://stratoswebdesign.github.io/kontyos/img/fair/pecs.webp" alt="Adventi vásár – Pécs" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>Pécs – Pécsi Advent</b><span class="pl">Viszonteladó partnerünk standján</span></span></a><a class="fair-card2" href="/vasarok#nyiregyhaza" data-fair="nyiregyhaza"><span class="im"><img src="https://stratoswebdesign.github.io/kontyos/img/fair/nyiregyhaza.webp" alt="Adventi vásár – Nyíregyháza" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>Nyíregyháza – Nyíregyházi Adventi Forgatag</b><span class="pl">Viszonteladó partnerünk standján</span></span></a></div>
<div class="ft"><button type="button" class="pm-btn" data-fair-more aria-controls="pm-fair-row" aria-expanded="false">További vásárok (2)</button><a class="pm-btn" href="/vasarok">Térképen és értesítővel</a></div>
<div class="pm-retail" data-reveal><p class="pm-sub-eyebrow">Megkóstoltad a vásárban? Vidd haza!</p>
<p class="big">A vásárokból ismert PIRI Mama – otthon is.<br>Keresd az üzletekben!</p>
<div class="pm-marq"><ul><li><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-lidl.svg" alt="LIDL" loading="lazy"></li><li><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-spar.svg" alt="SPAR" loading="lazy"></li><li><img class="s" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-eco-family.svg" alt="Ecofamily" loading="lazy"></li><li><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-cba.svg" alt="CBA" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-lidl.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-spar.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="s" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-eco-family.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-cba.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-lidl.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-spar.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="s" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-eco-family.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-cba.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-lidl.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-spar.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="s" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-eco-family.svg" alt="" loading="lazy"></li><li aria-hidden="true"><img class="h" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/bolt-cba.svg" alt="" loading="lazy"></li></ul></div></div>
</section>

<section class="pm-sec pm-story" id="tortenetunk">
<img class="orn pm-swing" src="https://stratoswebdesign.github.io/kontyos/img/deco/ornament-pink.svg" alt="" aria-hidden="true"><img class="orn2 pm-spin" src="https://stratoswebdesign.github.io/kontyos/img/deco/flake-gold.svg" alt="" aria-hidden="true">
<h2 class="pm-eyebrow" data-reveal>Történetünk</h2>
<div class="pm-scene" data-reveal><span class="mk"><img class="pm-float" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/mokus.svg" alt="" aria-hidden="true"></span><span class="md"><img src="https://stratoswebdesign.github.io/kontyos/img/pirimama/madar.svg" alt="" aria-hidden="true"></span><svg viewBox="0 0 1023 1200" role="img" aria-label="Piri mama boldogan főz a konyha ablakának üvege mögött"> <defs> <linearGradient id="kw-pane" x1="0" y1="0" x2="0" y2="1"> <stop offset="0" stop-color="#7c6b33" /> <stop offset="1" stop-color="#453a17" /> </linearGradient> <radialGradient id="kw-glow" cx="0.5" cy="0.45" r="0.6"> <stop offset="0" stop-color="#e8c66a" stop-opacity="0.55" /> <stop offset="1" stop-color="#e8c66a" stop-opacity="0" /> </radialGradient> <clipPath id="kw-clip"> <rect x="292" y="418" width="452" height="548" /> </clipPath> <filter id="kw-blur" x="-60%" y="-60%" width="220%" height="220%"> <feGaussianBlur stdDeviation="7" /> </filter> </defs> <rect x="266" y="392" width="504" height="600" style="fill:var(--pm-night)" /> <rect x="292" y="418" width="452" height="548" fill="url(#kw-pane)" /> <ellipse class="pm-glow" cx="518" cy="720" rx="300" ry="320" fill="url(#kw-glow)"/> <g clip-path="url(#kw-clip)"> <g transform="translate(230 550) scale(4.5)"> <g class="pm-bob"> <path d="M64.69,73.49s-1.34,1.33-3.05.26c-1.71-1.08-1.22-2.48-1.22-2.48,0,0,1.52-.77,3.04.05,1.52.82,1.23,2.17,1.23,2.17Z" fill="#00aeef" /> <path d="M60.58,65.46s.45,1.45-.94,2.27c-1.4.82-2.22-.05-2.22-.05,0,0,.02-1.37,1.16-2.15,1.14-.78,2-.07,2-.07Z" fill="#00aeef" /> <path d="M42.67,43.36s-11.49-1.27-20.14-4.72" fill="none" stroke="#00aeef" /> <path d="M36.93,70.48s1.4-1.74,3.55-.71c2.15,1.04,1.76,2.75,1.76,2.75,0,0-1.68,1.1-3.58.34-1.9-.76-1.73-2.38-1.73-2.38Z" fill="#00aeef" /> <circle cx="46.26" cy="64.16" r="2.84" fill="#e54360" /> <circle cx="37.76" cy="59.86" r="3.74" fill="#e54360" /> <circle cx="44.46" cy="56.86" r="3.17" fill="#e54360" /> <path d="M34.3,60.96c-.71,2.78-4.7,8.92-7.52,8.2-2.82-.72-3.41-8.01-2.7-10.79" fill="#daa900" /> <path d="M23.55,58.24c.78-3.07,3.94-4.93,7.05-4.14,3.12.79,5.01,3.92,4.23,7l-11.28-2.86Z" fill="#002169" stroke="#222d65" stroke-linecap="round" stroke-linejoin="round" /> <path d="M36.29,62.53c1.31,1.52,3.23,6.27,1.69,7.6-1.54,1.33-5.96-1.26-7.27-2.78" fill="#daa900" /> <path d="M30.42,67.6c-1.45-1.68-1.24-4.23.46-5.7s4.26-1.3,5.71.38l-6.16,5.32Z" fill="#002169" stroke="#222d65" stroke-linecap="round" stroke-linejoin="round" /> <path d="M30.94,54.06s.23-2.55.81-2.82" fill="none" stroke="#222d65" /> <path d="M31.49,85.86c-.2,1.88-1.89,3.23-3.76,3.03s-3.23-1.89-3.03-3.76,1.89-3.23,3.77-3.03,3.23,1.89,3.03,3.76Z" fill="#e54360" /> <path d="M22.48,56.51s5.2,20.66-5.21,21.73c-10.4,1.07.32,29.18.32,29.18,0,0-40.24,36.01.99,18.4,57.81-24.69,45.23-59.1,45.23-59.1l-41.33-10.21Z" fill="#f04c23" /> <path d="M81.96,36.01c8.63,8.23,1.72,25.42-20.72,32.27-36.95,11.28-40.21-23.49-35.81-31.61,4.39-8.12,45.81-41.54,56.53-.65Z" fill="#fcd3c1" /> <path d="M78.19,33.4s-2.24-.29-4.79-.54c-3.56,1.42-3.74,4.18-3.74,4.18,0,0,2.37,1.85,5.41.6s3.12-4.24,3.12-4.24Z" fill="#ffffff" /> <circle cx="74.11" cy="35.1" r="2.36" fill="#053134" /> <path d="M53.75,41.9s-3.94-3.12-6.39-.18c-3.06,3.68-2.92,3.73-2.92,3.73,0,0,2.37,1.85,5.41.6,3.05-1.26,3.9-4.14,3.9-4.14Z" fill="#ffffff" /> <circle cx="48.9" cy="43.5" r="2.36" fill="#053134" /> <path d="M60.59,37.28s1.5,4.35,3.48,5.05c2.11.74,4.03-.51,3.34.83s-2.94,2.53-4.33,1.95-2.49-7.83-2.49-7.83Z" fill="#daa900" /> <circle cx="76.09" cy="43.74" r="3.91" fill="#f04c23" opacity="0.4" /> <circle cx="52.26" cy="51.38" r="3.91" fill="#f04c23" opacity="0.4" /> <path d="M68.23,46.8s.42,2.76-3.41,3.61c-2.69.6-3.12-2.17-3.12-2.17l6.53-1.44Z" fill="#053134" /> <path d="M76.82,29.43s-2.12-2.49-5.06-.89c-2.94,1.59-2.97,3.47-2.97,3.47" fill="none" stroke="#daa900" /> <path d="M51.42,37.56s-2.31-1.4-5.25.19c-2.94,1.59-2.78,2.38-2.78,2.38" fill="none" stroke="#daa900" /> <path d="M76.09,14.77c1.54,6.46-2.93,10.75-12.18,10.77-9.24.02-11.06-1.57-11.06-1.57,0,0-13.78,5.2-14.35,14.26-1.17,18.45-11.15,4.8-11.15,14.51,0,7.29-4.86,11.47-7.46,1.48-6.29-24.23,11.5-37.03,22.92-43.01,9.19-4.82,31.1-5.55,33.28,3.55Z" fill="#ffffff" /> <path d="M46.02,9.54s-4.37-15.21-20.96-6.35c-22.15,11.83-5.53,27.42-3.19,27.35" fill="#ffffff" stroke="#fcd3c1" stroke-width="0.75" /> <ellipse cx="72.74" cy="31.74" rx="8.93" ry="10.1" fill="none" stroke="#f04c23" stroke-width="0.5" /> <ellipse cx="49.84" cy="40.45" rx="8.93" ry="10.1" fill="none" stroke="#f04c23" stroke-width="0.5" /> <path d="M63.77,55.78s2.44,1.58,4.12-.5" fill="none" stroke="#053134" stroke-width="0.5" /> <path d="M33.21,50.49s-1-4.78-3.88-3.56c-4.28,1.81-3.27,9.58.61,11.95,0,0,5.36,3.95,3.62-2.09" fill="#fcd3c1" stroke="#fcd3c1" stroke-width="0.5" /> <circle cx="32.75" cy="59.26" r="1.94" fill="#ffffff" /> <path d="M48.25,8.58c-.23.05-5.69,1.25-7.3,5.38-1.03,2.63-.25,5.8,2.32,9.44l.63-.44c-2.41-3.41-3.16-6.34-2.23-8.72,1.47-3.75,6.7-4.9,6.75-4.91l-.16-.75Z" fill="#daa900" /> <path d="M37.19,10.04c-1.07.82-1.27,2.34-.46,3.41s2.34,1.27,3.41.46,1.27-2.34.46-3.41-2.34-1.27-3.41-.46Z" fill="#daa900" /> <path d="M42.85,13.64c-.9.69-1.08,1.98-.39,2.88.69.9,1.98,1.07,2.88.39.9-.69,1.07-1.98.39-2.88s-1.98-1.08-2.88-.39Z" fill="#daa900" /> <path d="M43.3,22.24c-1.07.82-1.27,2.34-.46,3.41s2.34,1.27,3.41.46c1.07-.82,1.27-2.34.46-3.41s-2.34-1.27-3.41-.46Z" fill="#daa900" /> <path d="M41.26,16.83c-.11.21-2.7,5.16-7.11,5.63-2.81.3-5.66-1.28-8.5-4.72l.59-.49c2.66,3.22,5.29,4.72,7.82,4.44,4.01-.43,6.49-5.17,6.52-5.22l.68.35Z" fill="#daa900" /> <path d="M37.54,27.07c-1.07.82-2.59.61-3.41-.46-.82-1.07-.61-2.59.46-3.41s2.59-.61,3.41.46.61,2.59-.46,3.41Z" fill="#daa900" /> <path d="M33.62,20.27c-1.07.82-2.59.61-3.41-.46s-.61-2.59.46-3.41,2.59-.61,3.41.46.61,2.59-.46,3.41Z" fill="#daa900" /> <path d="M26.39,17.81c-1.07.82-2.59.61-3.41-.46-.82-1.07-.61-2.59.46-3.41,1.07-.82,2.59-.61,3.41.46s.61,2.59-.46,3.41Z" fill="#daa900" /> <path d="M28.26,24.77c-1.07.82-2.59.61-3.41-.46s-.61-2.59.46-3.41,2.59-.61,3.41.46c.82,1.07.61,2.59-.46,3.41Z" fill="#daa900" /> <path d="M46.02,9.54s15.52-5.86,26.16,2.13c6.39,4.81,3.28,9.13,3.28,9.13" fill="none" stroke="#fcd3c1" stroke-width="0.75" /> <path d="M64.75,66.92s.18,5.09-4.2,6.55c-4.47,1.49-7.03-1.05-7.03-1.05,0,0,.14,2.27-4.5,2.41s-5.02-2.9-5.02-2.9c0,0-2.28,3.09-6.56,1.21-4.28-1.88-3.61-3.68-3.61-3.68,0,0,.14,4.24-4.39,1.79s-3.16-6.49-2.1-6.88-2.85,4.37-4.32.93c-1.47-3.44,3.53-7.95,3.53-7.95,0,0,8.79,21.16,38.2,9.56Z" fill="#49aaa9" /> <circle cx="47.59" cy="2.22" r="2.22" fill="#daa900" /> <circle cx="52.79" cy="5.99" r="2.22" fill="#daa900" /> <circle cx="46.89" cy="7.82" r="2.22" fill="#daa900" /> <g class="pm-stir"> <path d="M99.25,40.14c-2.09-9.56,1.48-23.05,11.99-19.73,9.47,2.99,1.51,19.37-2.03,21.25-6.94,3.68-13,33.25-13,33.25,0,0-1.05,6.66-2.64,9.93-2.54,5.25-5.7,2.61-5.16-4.12,1.23-15.41,12.94-31.01,10.84-40.57Z" fill="#daa900" /> <path d="M90.87,74.25s.64-8.61,2.81-12.26-8.11-.19-7.36,9.24c.29,3.66.16,3.4,4.56,3.02Z" fill="#fcd3c1" /> <path d="M88.21,67.85s15.98-12.66,15.98-5.76c0,16.16-10.15,14.07-10.15,14.07l-5.83-8.31h0Z" fill="#fcd3c1" /> <path d="M101.03,34.22s-.33,5.98,3.17,6.14c3.49.16,5.01-4.24,5.01-4.24" fill="none" stroke="#fcd3c1" stroke-width="0.5" /> <path d="M104.2,20.8s-1.1,6.68,1.72,5.58c2.81-1.1,5.63-4.95,6.62,2.26,1.06,7.65-.14,6.05.93,7.22,1.07,1.18,4.57-7.96,1.45-12.47-4.2-6.07-10.72-2.6-10.72-2.6Z" fill="#f04c23" /> </g> <path d="M24.69,85.96s30.69,31.97,69.51-10.37c-1.76-5.93-7.08-9.26-7.08-9.26,0,0-28.34,24.54-57,2.96-10.88-8.19-5.43,16.67-5.43,16.67Z" fill="#fcd3c1" /> <path d="M61.69,92.65c.17.6.05,1.96,2.18,1.62" fill="none" stroke="#222d65" stroke-width="0.5" /> <path d="M46.15,77.03s-20.5,3.14-14.61,17.34c5.7,13.74-18.97-23.09-15.23-27.14,3.74-4.05,21.82,2.34,29.84,9.8Z" fill="#f04c23" /> </g></g> <g filter="url(#kw-blur)" style="fill:var(--pm-gold-soft)"> <ellipse class="pm-steam" cx="726" cy="618" rx="9" ry="15"/> <ellipse class="pm-steam d" cx="700" cy="600" rx="7" ry="12"/> </g> </g> <rect x="509" y="418" width="22" height="548" style="fill:var(--pm-night);stroke:var(--pm-gold-soft);stroke-width:2.5" /> <rect x="292" y="656" width="452" height="22" style="fill:var(--pm-night);stroke:var(--pm-gold-soft);stroke-width:2.5" /> <rect x="292" y="418" width="452" height="548" fill="none" style="stroke:var(--pm-gold-soft);stroke-width:3" /> <rect x="266" y="392" width="504" height="600" fill="none" style="stroke:var(--pm-gold-soft);stroke-width:3" /> <path d="M196 412 L518 262 L842 412" fill="none" style="stroke:var(--pm-gold-soft);stroke-width:38" /> <path d="M196 412 L518 262 L842 412" fill="none" style="stroke:var(--pm-night);stroke-width:30" /> <path d="M196 412 L518 262 L842 412 C 808 370 792 362 772 344 C 742 316 722 324 692 302 C 660 280 636 284 606 258 C 582 238 556 234 540 218 C 530 210 506 210 496 218 C 478 234 452 238 428 254 C 398 274 368 270 336 294 C 304 318 284 312 258 334 C 238 352 216 360 196 412 Z" fill="#ffffff" /> <circle cx="518" cy="258" r="24" style="fill:var(--pm-night);stroke:var(--pm-gold-soft);stroke-width:3" /> <rect x="224" y="990" width="580" height="44" style="fill:var(--pm-night);stroke:var(--pm-gold-soft);stroke-width:3" /> <path d="M226 1010 C 240 972 280 950 320 962 C 360 972 380 940 420 946 C 460 952 480 930 520 938 C 560 946 590 924 630 936 C 670 948 700 934 740 948 C 770 958 790 976 802 1010 L 802 1034 L 226 1034 Z" fill="#ffffff" /> </svg></div>
<div class="tx" data-reveal><p>A Kontyos Borháznál hiszünk abban, hogy minden évszaknak megvan a maga illata, amely különleges emlékeket és hangulatokat idéz fel. 2006 óta készítünk hazai gyümölcsökből karakteres gyümölcsborokat, ötvözve a hagyományos eljárásokat a modern technológiával.</p>
<p>Ebből a szemléletből született meg Piri mama forralt bora is.</p></div>
<div class="ft"><a class="pm-btn" href="/rolunk">Ismerd meg a borházat</a></div>
</section>

<section class="pm-video" aria-label="Hangulatvideó"><video muted loop playsinline preload="none" poster="https://stratoswebdesign.github.io/kontyos/img/video/piri_hangulat.webp" aria-label="Forró PIRI Mama forralt bor téli hangulatban"><source src="https://stratoswebdesign.github.io/kontyos/img/pirimama/hangulat-720.mp4" type="video/mp4"></video></section>

<section class="pm-shop" id="webshop">
<div class="l"><div class="pm-sc" data-reveal><img class="st pm-twinkle" src="https://stratoswebdesign.github.io/kontyos/img/pirimama/csillag-arany.svg" alt="" aria-hidden="true">
<h2>Webshop</h2><h3>Az ünnep ízei,<br>egyenesen hozzád.</h3>
<p>PIRI Mama forralt borai és a Kontyos gyümölcsborai egy helyen. Találd meg az ünnepi kedvencedet – 25 000 Ft felett ingyen szállítunk.</p>
<div class="bb"><a class="pm-btn gold" href="#termekek">Rendeld meg otthonra!</a><a class="pm-btn" href="/forralt-bor">Összes forralt bor és csomag</a></div></div></div>
<div class="r"><div class="ct" id="kapcsolat" data-reveal><h2>Kapcsolat</h2>
<ul><li><a href="tel:+36300945042">+36 30 094 5042</a></li><li><a href="mailto:webshop@kontyos.hu">webshop@kontyos.hu</a></li><li>6773 Klárafalva, Kossuth u. 183.</li></ul>
<div class="pm-nl"><p class="k">Hírlevél</p><b>−5% az első rendelésedből</b><p class="d">Iratkozz fel: a kuponkódot azonnal küldjük, mellé szezonális ajánlatok és új ízek – elsőként.</p>
<form data-newsletter><label class="sr" for="pm-nl">E-mail cím</label><input id="pm-nl" type="email" placeholder="E-mail címed" autocomplete="email" required><button class="pm-btn gold" type="submit">Feliratkozom</button><p class="nl-note">A feliratkozással hozzájárulsz, hogy a Kontyos Borház Kft. hírlevelet és ajánlatokat küldjön e-mailben. Bármikor leiratkozhatsz. <a href="/adatkezelesi-tajekoztato">Adatkezelési tájékoztató</a></p></form></div>
</div><img class="holly pm-sway" src="https://stratoswebdesign.github.io/kontyos/img/deco/holly.svg" alt="" aria-hidden="true"></div>
</section>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "ItemList", "name": "PIRI Mama forralt borok", "itemListElement": [{"@type": "ListItem", "position": 1, "item": {"@type": "Product", "name": "PIRI Mama forralt bora 1 l", "image": "https://stratoswebdesign.github.io/kontyos/img/p/piri-mama-forralt-bora-1l.webp", "description": "Valódi fűszerekkel ízesített kész forralt gyümölcsbor, a tél fűszerei mellett a meggy és a szilva dominál, ahogy Piri mama készíti.", "brand": {"@type": "Brand", "name": "Kontyos"}, "url": "https://www.kontyos.hu/piri-mama-forralt-bora-1l", "offers": {"@type": "Offer", "price": 2190, "priceCurrency": "HUF", "availability": "https://schema.org/InStock", "url": "https://www.kontyos.hu/piri-mama-forralt-bora-1l"}}}, {"@type": "ListItem", "position": 2, "item": {"@type": "Product", "name": "Epres PIRI Mama forralt bora 1 l", "image": "https://stratoswebdesign.github.io/kontyos/img/p/epres-piri-mama-forralt-bora-1l.webp", "description": "Gyümölcsös ízvilágú kész forralt bor, amelyben az eper, az narancs és egy leheletnyi vanília harmonikusan érvényesül, ahogy Piri mama készíti.", "brand": {"@type": "Brand", "name": "Kontyos"}, "url": "https://www.kontyos.hu/piri-mama-epres-forralt-bora-1l", "offers": {"@type": "Offer", "price": 2190, "priceCurrency": "HUF", "availability": "https://schema.org/InStock", "url": "https://www.kontyos.hu/piri-mama-epres-forralt-bora-1l"}}}, {"@type": "ListItem", "position": 3, "item": {"@type": "Product", "name": "Narancsos PIRI Mama forralt bora 1 l", "image": "https://stratoswebdesign.github.io/kontyos/img/p/piri-mama-narancsos-forralt-bora-1l.webp", "description": "Valódi fűszerekkel ízesített kész forralt gyümölcsbor, a tél fűszerei mellett a narancsos a szegfőszeg dominál, ahogy Piri mama készíti.", "brand": {"@type": "Brand", "name": "Kontyos"}, "url": "https://www.kontyos.hu/piri-mama-narancsos-forralt-bora-1l", "offers": {"@type": "Offer", "price": 2190, "priceCurrency": "HUF", "availability": "https://schema.org/InStock", "url": "https://www.kontyos.hu/piri-mama-narancsos-forralt-bora-1l"}}}, {"@type": "ListItem", "position": 4, "item": {"@type": "Product", "name": "PIRI Mama forró itala 0% 1 l", "image": "https://stratoswebdesign.github.io/kontyos/img/p/piri-mama-forro-itala-0-alc.webp", "description": "Valódi fűszerekkel ízesített forralt bor ízű 70 % - os gyümölcsital, a tél fűszerei mellett a meggy és a szilva dominál, ahogy Piri mama készíti. Felbontás után hűtőben tárolandó, 1 héten belül fogyasztandó !", "brand": {"@type": "Brand", "name": "Kontyos"}, "url": "https://www.kontyos.hu/piri-mama-forro-itala-0-alc", "offers": {"@type": "Offer", "price": 2190, "priceCurrency": "HUF", "availability": "https://schema.org/InStock", "url": "https://www.kontyos.hu/piri-mama-forro-itala-0-alc"}}}]}</script>
<script>(function(){
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
})();</script>
</main></div>
