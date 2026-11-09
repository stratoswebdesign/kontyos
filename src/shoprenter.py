#!/usr/bin/env python3
"""Shoprenter-csomag a kész GitHubos webshopból (Stratos, 2026-11-06).

A sandboxba (kontyos.sandbox.shoprenter.hu) feltöltendő fájlokat állítja elő a `shoprenter/` mappába:
  assets/kontyos.css        – a teljes stíluslap .ky gyökérosztály alá zárva (a Párizs téma CSS-ét nem írja felül)
  assets/kontyos.js         – a demó JS Shoprenterhez igazítva (szezonváltás, karusszelek, ajánlók)
  snippets/ky-*.tpl         – az oldalak tartalma Twig-snippetként (fejléc, lábléc, főoldal, aloldalak, termékcsalád-blokkok)
  termek_megfeleltetes.csv  – demó ↔ éles cikkszámok

Elvek
- Élesben SEMMI: ez csak fájlokat gyárt.
- A linkek a kontyos.hu meglévő SEO-URL-jeire mutatnak (sitemap.xml alapján), az új termékek/oldalak javasolt URL-t kapnak.
- Képek: a sandbox-fázisban a GitHub Pages-ről töltődnek (IMG_BASE); élesítéskor a Shoprenter fájlkezelőjébe
  töltjük fel őket, és IMG_BASE-t átírjuk (egy helyen).
- A „Kosárba” gombok data-add + data-sku attribútumot kapnak; a kontyos.js a Shoprenter kosár-végpontjára küldi
  (a végpontot a sandboxban ellenőrizzük).
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'shoprenter')
IMG_BASE = 'https://stratoswebdesign.github.io/kontyos/'

# ---- demó termék-id → Shoprenter cikkszám (élesben létező) ----
SKU = {'edes-meggybor': 'KONTY102X', 'edes-eperbor': 'KONTY101X', 'edes-ribizlibor': 'KONTY103X', 'edes-kajszibor': 'KONTY105X',
       'edes-oszibarackbor': 'KONTY104X', 'edes-szilvabor': 'KONTY107X', 'edes-bodza-almabor': 'KONTY106X', 'szaraz-meggybor': 'KONTY112X',
       'klara-edes-malnabor': 'KONTY109X', 'klara-szaraz-roze-eperbor': 'KONTY111X', 'klara-szaraz-barrique-meggybor': 'KONTY110X',
       'klara-edes-afonyabor': 'KONTY108X', 'friss-narancs': 'KONTY-narancs', 'friss-eper': 'KONTY250X', 'friss-malna': 'konty251X',
       'friss-meggy': 'KONTY550x', 'berry-secco': 'berry01', 'berry-secco-tonic': 'berry02', 'berry-secco-yuzu-lime': 'berry03',
       'piri-mama-forralt-bora': 'Forralt04X', 'epres-piri-mama-forralt-bora': 'Forralt_epres', 'narancsos-piri-mama-forralt-bora': 'Forralt05',
       'piri-mama-forro-itala-0': 'Forró_Itala', 'don-cherry': 'vermut01', 'don-cherry-gyumolcse': 'vermut02', 'szamocapalinka': 'pal06X',
       'birspalinka': 'pal02X', 'meggypalinka': 'pal04X', 'kortepalinka': 'pal07', 'szilvapalinka': 'pal05X', 'meggy-paros': 'PAROSMEGGY',
       'eper-paros': 'PAROSEPER', 'konnyu-trio': 'konnyutrio', 'bubi-paros': 'PAROSBERRY', 'kontyos-borospohar': 'kekpohar',
       'piri-mama-bogreje': 'piribögre', 'meggymag-parna': 'magparna', 'kontyos-szovettaska': 'szovettaska',}
# új termékek javasolt cikkszáma
NEW_SKU = {'goldberg-tonic': 'KY-GOLDBERG-TONIC', 'goldberg-ginger-ale': 'KY-GOLDBERG-GINGER', 'gunpowder-gin': 'KY-GUNPOWDER-GIN',
           'buffalo-trace': 'KY-BUFFALO-TRACE', 'campari': 'KY-CAMPARI', 'don-kis': 'KY-DON-KIS', 'don-nagy': 'KY-DON-NAGY',
           'forralt-6': 'KY-PIRI-5', 'koktel-negroni': 'KY-KOKTEL-NEGRONI', 'koktel-americano': 'KY-KOKTEL-AMERICANO',
           'koktel-tonic': 'KY-KOKTEL-TONIC', 'koktel-manhattan': 'KY-KOKTEL-MANHATTAN', 'koktel-gt-eper': 'KY-KOKTEL-EPER',
           'koktel-gt-bodza': 'KY-KOKTEL-BODZA', 'koktel-malna-ginger': 'KY-KOKTEL-MALNA', 'koktel-gt-narancs': 'KY-KOKTEL-NARANCS',
           'ujbor-valogatas': 'KY-UJBOR-6', 'bf-premium': 'KY-BF-PREMIUM', 'bf-mini': 'KY-BF-DISZKONT', 'edes-unnepek': 'KY-EDES-UNNEPEK',
           'premium-advent': 'KY-PREMIUM-ADVENT', 'konnyu-karacsony': 'KY-KONNYU-KARACSONY'}

# ---- demó oldal → kontyos.hu URL (meglévő SEO-URL-ek a sitemap.xml-ből; * = új, javasolt) ----
PAGE = {'index.html': '/', 'gyumolcsbor.html': '/gyumolcsbor', 'rolunk.html': '/rolunk', 'csomagok.html': '/kedvezmenyek/csomagajanlatok',
        'kosar.html': '/index.php?route=checkout/cart', 'info.html': '/kiszallitas', 'kereses.html': '/index.php?route=product/list',
        'koktelok.html': '/koktelok', 'vasarok.html': '/vasarok', 'black-friday.html': '/black-friday', 'karacsonyi-ajandek-bor.html': '/karacsonyi-ajandek-bor', 'forralt-bor.html': '/forralt-bor',
        'ujbor-valogatas.html': '/ujbor-valogatas', 'penztar.html': '/index.php?route=checkout/cart', 'koszonjuk.html': '/',
        'aszf.html': '/aszf', 'adatkezeles.html': '/adatkezelesi-tajekoztato', 'elallas.html': '/withdrawal'}
PROD = {'edes-eperbor': 'edes-eperbor', 'edes-szilvabor': 'edes-szilvabor', 'edes-kajszibor': 'edes-kajszibor', 'edes-meggybor': 'edes-meggybor',
        'klara-edes-malnabor': 'klara-edes-malnabor', 'edes-bodza-almabor': 'edes-bodza-almabor', 'klara-szaraz-roze-eperbor': 'klara-szaraz-roze-eperbor',
        'szaraz-meggybor': 'szaraz-meggybor', 'edes-ribizlibor': 'edes-ribizlibor', 'edes-oszibarackbor': 'edes-oszibarackbor',
        'klara-edes-afonyabor': 'klara-edes-afonyabor-075l', 'klara-szaraz-barrique-meggybor': 'klara-szaraz-barrique-meggybor',
        'piri-mama-forralt-bora': 'piri-mama-forralt-bora-1l', 'friss-eper': 'eper-edes-gyumolcsbor-075-l', 'friss-malna': 'malna-edes-gyumolcsbor-075-l',
        'berry-secco': 'berry-secco-075-l', 'berry-secco-tonic': 'berry-secco-and-tonic-075-l', 'friss-meggy': 'meggy-edes-gyumolcsbor-075-l',
        'berry-secco-yuzu-lime': 'berry-secco-yuzu-and-lime-075-l', 'epres-piri-mama-forralt-bora': 'piri-mama-epres-forralt-bora-1l',
        'piri-mama-forro-itala-0': 'piri-mama-forro-itala-0-alc', 'friss-narancs': 'narancs-edes-gyumolcsbor-075-l',
        'narancsos-piri-mama-forralt-bora': 'piri-mama-narancsos-forralt-bora-1l', 'bubi-paros': 'bubi-paros-482', 'konnyu-trio': 'konnyu-trio-483',
        'don-cherry': 'don-cherry-edes-meggyvermut-075-l', 'don-cherry-gyumolcse': 'don-cherry-edes-meggyvermut-025-l-and-meggy-100-g',
        'birspalinka': 'birspalinka', 'meggypalinka': 'meggypalinka', 'szilvapalinka': 'szilvapalinka', 'szamocapalinka': 'szamocapalinka',
        'kortepalinka': 'kortepalinka', 'kontyos-borospohar': 'kontyos-borospohar-388', 'kontyos-szovettaska': 'kontyos-szovettaska-392',
        'meggymag-parna': 'meggymag-parna', 'piri-mama-bogreje': 'piri-mama-bogreje-032-l', 'eper-paros': 'eper-paros', 'meggy-paros': 'meggy-paros'}


def page_url(href):
    """Demó relatív link → kontyos.hu útvonal (horgonnyal együtt)."""
    if href.startswith(('http', 'mailto:', 'tel:', '#', 'javascript:')):
        return href
    path, _, frag = href.partition('#')
    path = path.split('?')[0]
    path = re.sub(r'^(\.\./)+', '', path).lstrip('./')
    if path.startswith('termek/'):
        pid = path[len('termek/'):-len('.html')]
        url = '/' + PROD.get(pid, pid)            # új termék: a demó-id lesz a javasolt SEO-URL
    elif path in PAGE:
        url = PAGE[path]
    elif path.endswith('.html'):
        url = '/' + path[:-5]
    else:                                          # kép, css, egyéb fájl
        return IMG_BASE + path + (('#' + frag) if frag else '')
    return url + (('#' + frag) if frag else '')


# A Párizs/Bootstrap osztálynevekkel ütköző demó-osztályok átnevezése (k- előtag) a CSS-ben, a snippetekben és a JS-ben
COLLIDE = ['badge', 'btn', 'card', 'close', 'col', 'h1', 'h2', 'h3', 'head', 'lead', 'left', 'nav', 'price', 'right', 'row', 'small', 'tall', 'breadcrumb']
_CL = '|'.join(COLLIDE)


def ren_classattr(htm):
    return re.sub(r'class="([^"]*)"', lambda m: 'class="' + ' '.join(('k-' + c) if c in COLLIDE else c for c in m.group(1).split(' ')) + '"', htm)


def ren_css(css):
    parts = re.split(r'(url\([^)]*\))', css)
    return ''.join(x if x.startswith('url(') else re.sub(r'\.(' + _CL + r')(?![\w-])', r'.k-\1', x) for x in parts)


def ren_js(js):
    js = re.sub(r'class="([^"]*)"', lambda m: 'class="' + ' '.join(('k-' + c) if c in COLLIDE else c for c in m.group(1).split(' ')) + '"', js)
    js = re.sub(r"(?<=['\" ,>(+~])\.(" + _CL + r")(?![\w-])", r'.k-\1', js)
    js = re.sub(r"(classList\.(?:add|remove|toggle|contains)\(\s*')(" + _CL + r")'", r"\1k-\2'", js)
    return js


def rewrite(htm):
    """Linkek, képek, srcset-ek átírása; a Twig-szintaxissal ütköző karakterek semlegesítése."""
    htm = re.sub(r'(href|src|poster|data-src|data-img)="([^"]+)"', lambda m: f'{m.group(1)}="{page_url(m.group(2))}"', htm)
    htm = re.sub(r'url\((?!["\']?(?:https?:|data:))["\']?([^)"\']+)["\']?\)', lambda m: f'url({page_url(m.group(1))})', htm)
    htm = re.sub(r'data-add="([^"]+)"', lambda m: f'data-add="{m.group(1)}" data-sku="{html.escape(SKU.get(m.group(1), NEW_SKU.get(m.group(1), "")))}"', htm)
    htm = re.sub(r'\?v=[0-9a-f]{10}', '', htm)
    htm = ren_classattr(htm)
    htm = re.sub(r'"image": "(img/[^"]+)"', lambda m: f'"image": "{IMG_BASE}{m.group(1)}"', htm)  # JSON-LD
    if '{{' in htm or '{%' in htm or '{#' in htm:
        htm = '{% verbatim %}' + htm + '{% endverbatim %}'
    return htm


def body_parts(path):
    s = open(os.path.join(ROOT, path), encoding='utf-8').read()
    body = re.search(r'<body([^>]*)>(.*)</body>', s, re.S)
    attrs, inner = body.group(1), body.group(2)
    cls = re.search(r'class="([^"]*)"', attrs)
    page = re.search(r'data-page="([^"]*)"', attrs)
    main = re.search(r'<main[^>]*>.*</main>', inner, re.S)
    header = re.search(r'<header class="site-head.*?</header>\s*<div class="drawer".*?</div>\s*', inner, re.S)
    footer = re.search(r'<footer.*?</footer>', inner, re.S)
    styles = ''.join(re.findall(r'<style>.*?</style>|<script type="application/ld\+json">.*?</script>', s, re.S))
    # oldalspecifikus külső stíluslap a <head>-ből (pl. Leaflet-térkép a vásárok oldalon)
    styles = ''.join(m for m in re.findall(r'<link rel="stylesheet" href="https?://[^"]+"[^>]*>', s[:s.find('<body')]) if 'fonts.googleapis' not in m) + styles
    after_main = inner[main.end():footer.start()] if (main and footer) else ''
    pre = inner[:inner.find('<header class="site-head')].strip() if '<header class="site-head' in inner else ''
    # fejléc fölötti sáv (pl. karácsonyi .xbar) – a kontyos.js a fejléc elé teszi
    pre_html = f'<div class="ky-pre">{pre}</div>' if pre else ''
    return dict(cls=cls.group(1) if cls else '', page=page.group(1) if page else '', main=main.group(0) if main else '',
                header=header.group(0) if header else '', footer=footer.group(0) if footer else '', styles=styles, extra=after_main, pre=pre_html)


# ---------------- CSS: minden szabály a .ky gyökér alá ----------------
BODY_CLASSES = {'has-buybar', 'pdp', 'pdp-klasszikus', 'ckpage', 'pdp-partner', 'pdp-palinka', 'pdp-piri', 'pdp-klara',
                'pdp-friss', 'overlay-head', 'pdp-secco', 'pdp-don'}

# A Párizs-téma (Bootstrap) alapstílusai (.row, .btn, .h2, .lead, h1–h4/p/ul margók, link-szín, gombok…) NE hassanak a Kontyos-elemekre:
# minden .ky alatti elem a böngésző alapértékeire áll vissza, és csak a Kontyos-stíluslap szabályai érvényesek – pont mint a demóban.
# Specifikussága (0,1,0), és a stíluslap ELEJÉN van, így minden Kontyos-szabály felülírja; az SVG-k és képek kimaradnak (attribútumaik miatt).
REVERT_CSS = '.ky,.ky :where(:not(svg,svg *,img,video,canvas,iframe,picture,source)){all:revert}\n.ky :where(img,video,canvas,svg){vertical-align:baseline}\n'

# A Shoprenter-keret (Párizs) igazítása: ezek a szabályok szándékosan NEM a .ky alatt vannak.
SHELL_CSS = '''
body.product-page-body:not(:has(main .ky)) main{visibility:hidden}
.ky-cart-on .sr-cart-page-content{position:absolute!important;left:-99999px!important;top:0!important;width:1100px!important;visibility:hidden}
.ky-cart-on .page-head,.ky-cart-on .breadcrumb{display:none!important}
.ky > .ky-pre{display:none}
.ky-pre-wrap{position:relative;z-index:61}
/* --- Shoprenter-keret (Párizs) igazítása a Kontyos-oldalakhoz --- */
#section-banner_slider_paris,#section-announcement_bar_paris{display:none!important}
body:has(.ky-head) main.has-sticky{padding-top:0!important}
main .container:has(.ky){max-width:none!important;width:100%!important;padding:0!important;margin:0!important}
main .container:has(.ky) :is(.row,.col,[class*="col-"],.one-column-content,.page-body):has(.ky){max-width:none!important;width:100%!important;flex:0 0 100%!important;padding:0!important;margin:0!important}
main .container:has(.ky) :is(.breadcrumb,.page-head,.page-title,.content-title):not(.ky *){display:none!important}
main .container:has(.ky) .row:has(.ky) > :is(aside,nav,.column-left,.column-right):not(:has(.ky)){display:none!important}
main .container:has(.ky) > :is(nav,.breadcrumb):not(:has(.ky)){display:none!important}
.ky.ky-head{position:relative;z-index:60;background:transparent}
body:has(.ky-head),body:has(.ky-head) .page-wrap{background:var(--page)!important}
body:has(.ky-head) main.has-sticky{padding-bottom:0!important;margin-bottom:0!important;background:transparent!important}
body:has(.ky-head) .footer-top-position,body:has(.ky-head) .footer-bottom-2-position,body:has(.ky-head) .mobile-scroll-top-button,body:has(.ky-head) .scroll-top-button{display:none!important}
.ky-legal-logos{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:24px;padding:18px 16px;background:#1B2A5C}
.ky-legal-logos img{width:auto!important;max-width:100%!important;height:auto!important;max-height:40px}
.ky-legal-logos .simple-footer,.ky-legal-logos .szechenyi{margin:0;padding:0;background:none}
/* a kötelező fizetési logó (SimplePay) a sötét lábléc aljába kerül, nem külön sávba */
.ky-foot .site-foot .ky-legal-logos{grid-column:1/-1;justify-content:flex-start;gap:16px;padding:0;margin:-10px 0 0;background:none;border:0}
.ky-foot .site-foot .ky-legal-logos img{height:auto!important;max-height:32px}
@media (max-width:760px){.ky-foot .site-foot .ky-legal-logos{gap:10px;margin-top:-12px}.ky-foot .site-foot .ky-legal-logos img{max-height:22px}}

/* --- Párizs-oldalak (amik nincsenek a demóban: keresés, belépés, regisztráció, fiók, kapcsolat, elállás, 404, blog/info):
       Kontyos-arculat – papír háttér, navy szöveg, Prata címek, Montserrat szöveg, rózsaszín fő gomb --- */
body:has(.ky-head) main:not(:has(.ky)){font-family:'Montserrat',system-ui,-apple-system,'Segoe UI',sans-serif;color:#1B2A5C;padding:clamp(24px,4vw,56px) 0 clamp(48px,6vw,88px)!important}
body:has(.ky-head) main:not(:has(.ky)) > .container,body:has(.ky-head) main:not(:has(.ky)) .container{max-width:1360px!important;padding-left:clamp(16px,3vw,40px)!important;padding-right:clamp(16px,3vw,40px)!important}
/* a Párizs px-ben számolja az oszlopszélességet a konténerből – a keskenyebb konténerhez %-os oszlopok */
@media (min-width:768px){body:has(.ky-head) main:not(:has(.ky)) .row > .column-left,body:has(.ky-head) main:not(:has(.ky)) .row > .column-right{flex:0 0 25%!important;max-width:25%!important;width:25%!important}
body:has(.ky-head) main:not(:has(.ky)) .row > .two-column-content{flex:0 0 75%!important;max-width:75%!important;width:75%!important}
body:has(.ky-head) main:not(:has(.ky)) .row > .three-column-content{flex:0 0 50%!important;max-width:50%!important;width:50%!important}
body:has(.ky-head) main:not(:has(.ky)) .row > .one-column-content{flex:0 0 100%!important;max-width:100%!important;width:100%!important}}
/* a régi webshop oldalsáv-tartalmai (régi bannerek, régi szállítási infó, régi hírlevél-doboz) nem kellenek – a szűrő marad */
body:has(.ky-head) main :is(.column-left,.column-right) > [id^="module_customcontent"]{display:none!important}
body:has(.ky-head) main:not(:has(.ky)) :is(p,li,td,th,label,dd,dt,span,small,div){font-family:inherit}
body:has(.ky-head) main:not(:has(.ky)) :is(h1,.h1,.page-head h1,.page-title,h1.title){font-family:'Prata HU',Georgia,serif!important;font-weight:400!important;text-transform:uppercase;color:#1B2A5C!important;font-size:clamp(28px,3.4vw,44px)!important;line-height:1.1!important;letter-spacing:.01em;margin:0 0 .6em!important}
body:has(.ky-head) main:not(:has(.ky)) :is(h2,h3,h4,.h2,.h3,.h4,.module-head-title,.box-title,legend){font-family:'Prata HU',Georgia,serif!important;font-weight:400!important;text-transform:uppercase;color:#1B2A5C!important;letter-spacing:.01em}
body:has(.ky-head) main:not(:has(.ky)) :is(h2,.h2,.module-head-title){font-size:clamp(22px,2.2vw,28px)!important}
body:has(.ky-head) main:not(:has(.ky)) :is(h3,h4,.h3,.h4,legend){font-size:clamp(18px,1.6vw,21px)!important}
body:has(.ky-head) main:not(:has(.ky)) a:not(.btn):not(.button){color:#1B2A5C;text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
body:has(.ky-head) main:not(:has(.ky)) a:not(.btn):not(.button):hover{color:#EF4E73}
body:has(.ky-head) main:not(:has(.ky)) .breadcrumb{background:none!important;padding:0!important;margin:0 0 18px!important;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#5A6072}
body:has(.ky-head) main:not(:has(.ky)) .breadcrumb a{color:#5A6072!important;text-decoration:none!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.btn-primary,.button-primary,button[type=submit].btn,input[type=submit],.btn-success,#button-login,#button-register){background:#EF4E73!important;border:0!important;color:#fff!important;border-radius:999px!important;font-family:'Montserrat',sans-serif!important;font-weight:800!important;font-size:15px!important;letter-spacing:.02em;text-transform:none!important;min-height:48px;padding:12px 28px!important;box-shadow:none!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.btn-primary,.button-primary,button[type=submit].btn,input[type=submit],.btn-success):hover{background:#D93A60!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.btn-secondary,.btn-default,.btn-outline-primary,.btn-outline-secondary,.button-secondary){background:transparent!important;border:1.5px solid #1B2A5C!important;color:#1B2A5C!important;border-radius:999px!important;font-weight:800!important;min-height:48px;padding:12px 26px!important;box-shadow:none!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.btn-secondary,.btn-default,.btn-outline-primary,.btn-outline-secondary,.button-secondary):hover{background:#1B2A5C!important;color:#fff!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.form-control,input[type=text],input[type=email],input[type=password],input[type=tel],input[type=search],input[type=number],select,textarea){border:1.5px solid #1B2A5C!important;border-radius:4px!important;background:#fff!important;color:#1B2A5C!important;font-family:'Montserrat',sans-serif!important;font-size:16px!important;min-height:46px;box-shadow:none!important}
body:has(.ky-head) main:not(:has(.ky)) textarea{min-height:120px}
body:has(.ky-head) main:not(:has(.ky)) :is(.form-control,input,select,textarea):focus{border-color:#EF4E73!important;box-shadow:0 0 0 3px rgba(239,78,115,.18)!important;outline:0}
body:has(.ky-head) main:not(:has(.ky)) :is(label,.control-label,.form-label){font-weight:700;font-size:14px;color:#1B2A5C}
body:has(.ky-head) main:not(:has(.ky)) :is(.card,.box,.panel,.well,.content-box,.account-box,.login-box,.register-box){background:#fff!important;border:1px solid #E2DACB!important;border-radius:6px!important;box-shadow:none!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.card-header,.panel-heading,.box-heading){background:none!important;border-bottom:1px solid #E2DACB!important}
body:has(.ky-head) main:not(:has(.ky)) table{border-color:#E2DACB!important}
body:has(.ky-head) main:not(:has(.ky)) :is(th,thead td){background:#F6E1E4!important;color:#1B2A5C!important;font-weight:800}
body:has(.ky-head) main:not(:has(.ky)) :is(.alert-success,.success){background:#E7F2E7!important;border-color:#B9D9B9!important;color:#1B2A5C!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.alert-danger,.alert-warning,.warning,.error){border-radius:4px!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.price,.product-price,.product-card__price,.price-new){color:#1B2A5C!important;font-weight:800!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.price-old,.product-price--old){color:#5A6072!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.product-card,.product-snapshot,.snapshot-list-item){background:#fff;border:1px solid #E2DACB;border-radius:6px}
body:has(.ky-head) main:not(:has(.ky)) :is(.product-card__name,.snapshot-list-item-name,.product-card-title) a{font-family:'Prata HU',Georgia,serif;text-transform:uppercase;text-decoration:none!important;color:#1B2A5C!important}
body:has(.ky-head) main:not(:has(.ky)) :is(.pagination .active > *,.page-item.active .page-link){background:#1B2A5C!important;border-color:#1B2A5C!important;color:#fff!important}
body:has(.ky-head) main:not(:has(.ky)) :is(input[type=checkbox],input[type=radio]){accent-color:#EF4E73}
/* keresési találatok: a régi termékleírásokban beégetett kék betűszín helyett navy */
body:has(.ky-head) main:not(:has(.ky)) .product-card-description *{color:inherit!important}
body:has(.ky-head) main:not(:has(.ky)) .product-card-description{color:#5A6072!important}
/* közösségi belépés gomb: fehér felirat a Facebook-kéken */
body:has(.ky-head) main:not(:has(.ky)) a.social-login-link,body:has(.ky-head) main:not(:has(.ky)) a.social-login-link *{color:#fff!important;text-decoration:none!important}
body:has(.ky-head) main:not(:has(.ky)) a.social-login-link{border-radius:999px!important;padding:10px 22px!important}
/* telefonszám-mező (országválasztós) teljes szélességben, mint a többi mező */
body:has(.ky-head) main:not(:has(.ky)) .iti{width:100%!important;display:block!important}
/* kapcsolat oldal: a régi kék blokkok a Kontyos-színekben */
body:has(.ky-head) main:not(:has(.ky)) .contact-name{color:#1B2A5C!important;font-family:'Prata HU',Georgia,serif!important;font-weight:400!important;text-transform:uppercase;font-size:clamp(22px,2.2vw,28px)!important}
body:has(.ky-head) main:not(:has(.ky)) .contact-wallpaper-1{background:#1B2A5C!important;color:#fff!important}
body:has(.ky-head) main:not(:has(.ky)) .contact-wallpaper-1 *{color:#fff!important}
body:has(.ky-head) main:not(:has(.ky)) .contact-wallpaper-1 a:hover{color:#F6E1E4!important}
body:has(.ky-head) main:not(:has(.ky)) .contact-wallpaper-2{background:#fff!important}
/* 404: középre zárva */
body.not_found_body:has(.ky-head) main .container{text-align:center}
body.not_found_body:has(.ky-head) main .breadcrumb{justify-content:center}
/* regisztráció/fiók űrlapok: a Párizs 30 px-es sorközei és az üres sorok helyett egyenletes 16 px */
body:has(.ky-head) main:not(:has(.ky)) .checkout-input-row{margin-top:0!important}
body:has(.ky-head) main:not(:has(.ky)) .checkout-input-row:empty{display:none!important}
/* süti-sáv (nanobar) */
.nanobar,#nanobar{font-family:'Montserrat',system-ui,sans-serif!important;color:#1B2A5C!important;background:#F3EEE5!important;border-top:1px solid #E2DACB!important}
:is(.nanobar,#nanobar) :is(.btn,button){border-radius:999px!important;font-weight:800!important;box-shadow:none!important}
:is(.nanobar,#nanobar) :is(.btn-primary,.nanobar-btn-accept,[class*="accept"]){background:#EF4E73!important;border-color:#EF4E73!important;color:#fff!important}
:is(.nanobar,#nanobar) a{color:#1B2A5C!important}

/* --- Shoprenter-pénztár (egyoldalas pénztár): Kontyos-színek, betűk, gombok --- */
body:has(.checkout-app-container){background:#F3EEE5!important}
.checkout-app-container .checkout-app-left{background:#F3EEE5!important}
.checkout-app-container .checkout-app-right{background:#fff!important;border-left:1px solid #E2DACB}
.checkout-app-container,.checkout-app-container input,.checkout-app-container button,.checkout-app-container select,.checkout-app-container label,.checkout-app-container p,.checkout-app-container span,.checkout-app-container div{font-family:'Montserrat',system-ui,-apple-system,'Segoe UI',sans-serif}
.checkout-app-container{color:#1B2A5C}
.checkout-app-container h1,.checkout-app-container h2,.checkout-app-container h3,.checkout-app-container h4{font-family:'Prata HU',Georgia,serif!important;font-weight:400!important;text-transform:uppercase;color:#1B2A5C!important;letter-spacing:.01em}
.checkout-app-container h1{font-size:24px!important;line-height:1.2!important}
.checkout-app-container .btn-primary{background:#EF4E73!important;border-color:#EF4E73!important;color:#fff!important;border-radius:999px!important;font-weight:800!important;min-height:48px;box-shadow:none!important}
.checkout-app-container .btn-primary:hover,.checkout-app-container .btn-primary:focus{background:#D93A60!important;border-color:#D93A60!important}
.checkout-app-container .btn-link,.checkout-app-container a{color:#1B2A5C!important}
.checkout-app-container .form-control{border:1.5px solid #1B2A5C!important;border-radius:4px!important;min-height:46px;box-shadow:none!important;background:#fff!important}
.checkout-app-container .form-control:focus{border-color:#EF4E73!important;box-shadow:0 0 0 3px rgba(239,78,115,.18)!important}
.checkout-app-container .progress-indicator-item-current .progress-indicator-label,.checkout-app-container .progress-indicator-item-done .progress-indicator-label{color:#1B2A5C!important;border-color:#1B2A5C!important;font-weight:800}
.checkout-app-container .progress-indicator-item-current .progress-indicator-line,.checkout-app-container .progress-indicator-item-done .progress-indicator-line{background:#1B2A5C!important}
.checkout-app-container .logo img{content:url(https://stratoswebdesign.github.io/kontyos/img/logo-navy.svg);width:210px!important;height:52px!important;max-height:none!important;object-fit:contain;object-position:left center}
'''
def scope_selector(sel):
    out = []
    for part in sel.split(','):
        p = part.strip()
        if not p:
            continue
        if p.startswith((':root', 'from', 'to')) or re.match(r'^\d+%$', p):
            out.append(p); continue
        p2 = re.sub(r'^html\s*', '', p)
        m = re.match(r'^\.([\w-]+)', p2)
        if p2.startswith('body'):
            out.append('.ky' + p2[4:])           # body.pdp → .ky.pdp, body → .ky
        elif m and m.group(1) in BODY_CLASSES:
            out.append('.ky' + p2)               # .pdp-don .x → .ky.pdp-don .x (a demóban body-osztály)
        elif p2 in ('*', '*::before', '*::after'):
            out.append('.ky ' + p2)
        else:
            out.append('.ky ' + p2)
    return ','.join(out)


def scope_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, i, n = [], 0, len(css)
    stack = []   # 'rule' / 'at-keep' / 'at-scope'

    def read_block(start):
        depth, j = 0, start
        while j < n:
            if css[j] == '{': depth += 1
            elif css[j] == '}':
                depth -= 1
                if depth == 0: return j
            j += 1
        return n - 1

    def walk(chunk):
        res, k, L = [], 0, len(chunk)
        while k < L:
            b = chunk.find('{', k)
            if b < 0:
                res.append(chunk[k:]); break
            head = chunk[k:b].strip()
            depth, j = 0, b
            while j < L:
                if chunk[j] == '{': depth += 1
                elif chunk[j] == '}':
                    depth -= 1
                    if depth == 0: break
                j += 1
            inner = chunk[b + 1:j]
            if head.startswith('@media') or head.startswith('@supports') or head.startswith('@container') or head.startswith('@layer'):
                res.append(head + '{' + walk(inner) + '}')
            elif head.startswith('@keyframes') or head.startswith('@font-face') or head.startswith('@-webkit-keyframes') or head.startswith('@page'):
                res.append(head + '{' + inner + '}')
            elif head.startswith('@'):
                res.append(head + '{' + inner + '}')
            else:
                res.append(scope_selector(head) + '{' + inner + '}')
            k = j + 1
        return ''.join(res)

    return walk(css)


# ---------------- Twig-snippetek ----------------
def write(rel, txt):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(txt)
    return p


def snippet(name, html_, note=''):
    head = f'{{# Kontyos – {note or name}. Generálva: src/shoprenter.py – kézzel ne szerkeszd, a demóból újragenerálható. #}}\n'
    return write(f'snippets/{name}.tpl', head + rewrite(html_) + '\n')


def main():
    os.makedirs(OUT, exist_ok=True)
    # CSS + fontok
    css = open(os.path.join(ROOT, 'assets', 'style.css'), encoding='utf-8').read()
    css = css.replace('url(fonts/', f'url({IMG_BASE}assets/fonts/').replace('url(../img/', f'url({IMG_BASE}img/').replace('url(img/', f'url({IMG_BASE}img/')
    scoped = ren_css(scope_css(css))
    write('assets/kontyos.css', '/* Kontyos – a .ky gyökérosztály alá zárt stíluslap (Shoprenter). Generálva: src/shoprenter.py */\n'
          + REVERT_CSS +
          '.ky{background:var(--page);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}\n' + scoped + SHELL_CSS)
    js = open(os.path.join(ROOT, 'assets', 'app.js'), encoding='utf-8').read()
    cat = open(os.path.join(ROOT, 'assets', 'catalog.js'), encoding='utf-8').read()
    # katalógus: URL-ek a kontyos.hu útvonalaira, képek a képtárra; cikkszám hozzáadva
    K = json.loads(cat[cat.index('{p:') + 3:cat.rindex('}')])
    for pid, x in K.items():
        x['url'] = page_url(x['url']); x['img'] = IMG_BASE + x['img']
        x['sku'] = SKU.get(pid) or NEW_SKU.get(pid) or ''
    cat2 = 'window.KONTYOS={p:' + json.dumps(K, ensure_ascii=False) + '};\n'
    idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    fairs = re.search(r'<script>(window\.KONTYOS_FAIRS=.*?)</script>', idx, re.S).group(1)  # vásár-adatok (státusz, térkép)
    cat2 = fairs + '\n' + cat2
    js2 = js.replace("var ROOT = document.documentElement.getAttribute('data-root') || '';", "var ROOT = '';")
    js2 = js2.replace("ROOT + 'kosar.html'", "'/index.php?route=checkout/cart'").replace("ROOT + 'gyumolcsbor.html'", "'/gyumolcsbor'")
    js2 = js2.replace("document.body.getAttribute('data-page')", "(document.querySelector('main .ky[data-page]') || document.body).getAttribute('data-page')")
    # a Shoprenter-kosároldalon a kosarat a shoprenter_adapter.js rajzolja (a rejtett Vue-kosár adataiból)
    js2 = js2.replace("var cr = document.getElementById('cart-root');", "var cr = window.KY_SR_CART ? null : document.getElementById('cart-root');")
    js2 = js2[:js2.rstrip().rindex('})();')] + '  window.kyUps = upsHtml; window.kyFmt = fmt;\n})();\n'
    js2 = ren_js(js2)
    kb = body_parts('kosar.html')
    cart_html = rewrite(kb['main']).replace('{% verbatim %}', '').replace('{% endverbatim %}', '')
    cat2 += 'window.KY_CART_HTML = ' + json.dumps(cart_html, ensure_ascii=False) + ';\n'
    adapter = open(os.path.join(ROOT, 'src', 'shoprenter_adapter.js'), encoding='utf-8').read()
    pidmap = json.load(open(os.path.join(OUT, 'sandbox_pid.json'), encoding='utf-8')) if os.path.exists(os.path.join(OUT, 'sandbox_pid.json')) else {}
    pidjs = 'window.KY_PID = Object.assign(' + json.dumps(pidmap, ensure_ascii=False) + ', window.KY_PID || {});\n'  # cikkszám → product_id (sandboxból kimentve)
    write('assets/kontyos.js', '/* Kontyos – katalógus + oldallogika (Shoprenter). Generálva: src/shoprenter.py */\n' + pidjs + cat2 + adapter + '\n' + js2)

    # fejléc + lábléc (a főoldalról)
    home = body_parts('index.html')
    snippet('ky-header', '<div class="ky ky-head">' + home['header'] + '</div>', 'fejléc (menü, logó, kosár) – a sections/header.tpl schema-blokkja megmarad')
    snippet('ky-footer', '<div class="ky ky-foot">' + home['footer'] + '</div>', 'lábléc')
    snippet('ky-home', home['styles'] + f'<div class="ky {home["cls"]}" data-page="home">' + home['pre'] + home['main'] + home['extra'] + '</div>', 'főoldal – szezonális herók dátum szerint')
    # termék-URL → snippet térkép a product.tpl-hez
    slugmap = {PROD.get(pid, pid): f'ky-p-{pid}' for pid in [os.path.basename(x)[:-5] for x in __import__('glob').glob(os.path.join(ROOT, 'termek', '*.html'))]}
    write('snippets/ky-pmap.tpl', '{# Kontyos – termék SEO-URL → termékoldal-snippet. Generálva. #}\n{% set ky_pmap = ' + json.dumps(slugmap, ensure_ascii=False) + ' %}\n')

    # aloldalak
    pages = {'rolunk.html': 'ky-page-rolunk', 'koktelok.html': 'ky-page-koktelok', 'vasarok.html': 'ky-page-vasarok', 'csomagok.html': 'ky-page-csomagok',
             'black-friday.html': 'ky-page-black-friday', 'karacsonyi-ajandek-bor.html': 'ky-page-karacsony', 'forralt-bor.html': 'ky-page-forralt', 'gyumolcsbor.html': 'ky-page-gyumolcsbor',
             'info.html': 'ky-page-info', 'aszf.html': 'ky-page-aszf', 'adatkezeles.html': 'ky-page-adatkezeles'}
    manifest = {}
    for f, name in pages.items():
        if not os.path.exists(os.path.join(ROOT, f)):
            continue
        b = body_parts(f)
        snippet(name, b['styles'] + f'<div class="ky {b["cls"]}" data-page="{b["page"]}">' + b['pre'] + b['main'] + b['extra'] + '</div>', f'aloldal: {f} → {page_url(f)}')
        manifest[name] = dict(demo=f, url=page_url(f), body_class=b['cls'])

    # termékoldalak: termékenként egy snippet (a Shoprenter product.tpl a cikkszám alapján tölti be)
    import glob
    for f in sorted(glob.glob(os.path.join(ROOT, 'termek', '*.html'))):
        pid = os.path.basename(f)[:-5]
        b = body_parts(os.path.relpath(f, ROOT))
        sku = SKU.get(pid) or NEW_SKU.get(pid) or ''
        snippet(f'ky-p-{pid}', b['styles'] + f'<div class="ky {b["cls"]}" data-page="{b["page"]}" data-sku="{html.escape(sku)}">' + b['main'] + b['extra'] + '</div>',
                f'termékoldal: {pid} ({sku}) → /{PROD.get(pid, pid)}')
        manifest[f'ky-p-{pid}'] = dict(demo=f'termek/{pid}.html', url='/' + PROD.get(pid, pid), sku=sku, body_class=b['cls'])
    write('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=1))
    print('OK', len(manifest), 'snippet +', 'kontyos.css', round(len(scoped) / 1024), 'KB')


if __name__ == '__main__':
    main()
