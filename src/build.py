#!/usr/bin/env python3
"""Kontyos webshop demo – statikus generátor.
Futtatás a repo gyökeréből:  python3 src/build.py
Bemenet: src/catalog.json  →  kimenet: *.html, termek/*.html, assets/catalog.js
"""
import json, os, html, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = json.load(open(os.path.join(ROOT, 'src', 'catalog.json'), encoding='utf-8'))
P = {p['id']: p for p in CAT}
LIMIT = 20000
VER = 'dev'
e = lambda s: html.escape(str(s), quote=True)


def ft(n):
    return f"{int(round(n)):,}".replace(',', ' ') + ' Ft'


LINE_LABEL = {'klasszikus': 'Klasszikus gyümölcsbor', 'klara': 'Klára prémium', 'friss': 'FRISS gyümölcsbor',
              'secco': 'Berry Secco', 'piri': 'PIRI Mama forralt bor', 'don': 'Don Cherry', 'palinka': 'Pálinka',
              'csomag': 'Válogatás', 'kiegeszito': 'Kiegészítő', 'szezon': 'Szezonális csomag'}

# Szezonális (demó) csomagok – árak a designból, tartalom javaslat
SEASON_PACKS = [
    dict(id='ujbor-valogatas', name='Újbor-válogatás', price=22340, old=26480, free=True,
         items=['edes-eperbor', 'edes-oszibarackbor', 'edes-bodza-almabor', 'szaraz-meggybor', 'friss-narancs', 'berry-secco-tonic'], extra='6 × EASY Cider 0,33 l', tint='#F6E1E4'),
    dict(id='bf-premium', name='Black Friday Prémium', price=19900, old=26840, free=True,
         items=['edes-meggybor', 'edes-ribizlibor', 'klara-edes-malnabor', 'berry-secco', 'piri-mama-forralt-bora', 'don-cherry'], tint='#F3EEE5'),
    dict(id='bf-diszkont', name='Black Friday diszkont', price=9900, old=13140, free=False,
         items=['friss-eper', 'friss-malna', 'friss-meggy'], qty=2, tint='#FBE3D2'),
    dict(id='edes-unnepek', name='Édes Ünnepek Borcsomag', price=19900, old=24840, free=True,
         items=['edes-eperbor', 'edes-meggybor', 'edes-oszibarackbor', 'edes-bodza-almabor', 'berry-secco', 'don-cherry'], tint='#FBE3E6', tag='FŐ AJÁNLAT'),
    dict(id='premium-advent', name='Prémium adventi borválogatás', price=28900, old=36040, free=True,
         items=['edes-eperbor', 'edes-ribizlibor', 'edes-kajszibor', 'edes-szilvabor', 'klara-edes-malnabor', 'don-cherry', 'don-cherry-gyumolcse', 'meggymag-parna'], tint='#EFE6D2', tag='PRÉMIUM AJÁNDÉK'),
    dict(id='konnyu-karacsony', name='Könnyű Karácsonyi Borcsomag', price=10900, old=13140, free=False,
         items=['friss-eper', 'friss-malna', 'friss-meggy', 'berry-secco-tonic', 'berry-secco-yuzu-lime', 'piri-mama-forralt-bora'], tint='#FFE8CF', tag='KISEBB KERETBŐL'),
]
SP = {s['id']: s for s in SEASON_PACKS}


def url(p):
    return f"termek/{p['id']}.html"


# ---------- catalog.js ----------
def write_catalog_js():
    out = {}
    for p in CAT:
        out[p['id']] = dict(n=p['name'], price=p['price'], tier=p['tier'], img=p['img'], url=url(p),
                            sub=LINE_LABEL.get(p['line'], ''), tint=p['arch'] if p['line'] not in ('piri', 'friss', 'don') else '#F3EEE5',
                            free=False, ups=[i for i in pdp.UPSELL.get(p['line'], lambda p: [])(p) if i in P and P[i]['avail'] and i != p['id']][:3])
    for s in SEASON_PACKS:
        first = P[s['items'][0]]
        page = 'ujbor-valogatas.html' if s['id'] == 'ujbor-valogatas' else ('black-friday.html' if s['id'].startswith('bf') else 'karacsonyi-ajandek-bor.html')
        out[s['id']] = dict(n=s['name'], price=s['price'], tier=None, img=first['img'], url=page,
                            sub=f"{len(s['items'])} tétel · szezonális csomag", tint=s['tint'], free=s['free'], ups=['kontyos-borospohar', 'kontyos-szovettaska', 'don-cherry-gyumolcse'])
    js = '/* generálva: src/build.py */\nwindow.KONTYOS={p:' + json.dumps(out, ensure_ascii=False) + '};\n'
    open(os.path.join(ROOT, 'assets', 'catalog.js'), 'w', encoding='utf-8').write(js)


# ---------- közös elemek ----------
NAV = [('gyumolcsbor.html', 'Gyümölcsborok', ''), ('termek/piri-mama-forralt-bora.html', 'Forralt bor', ''),
       ('termek/don-cherry.html', 'Don Cherry', ''), ('karacsonyi-ajandek-bor.html', 'Ajándék & csomagok', ''),
       ('palinka.html', 'Pálinka', ''), ('black-friday.html', 'Akciók', 'sale')]


def head(title, desc, r, page='', body_cls='', extra_style='', demo_extra='', topbar=''):
    return f'''<!doctype html>
<html lang="hu" data-root="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="{r}img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&family=Manrope:wght@400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/style.css?v={VER}">
{extra_style}
</head>
<body data-page="{page}" class="{body_cls}">
<div class="demo-bar"><span><b>DEMO</b> · Stratos Webdesign – nem valódi rendelés, a [szögletes] részek helykitöltők</span>{demo_extra}</div>
{topbar}
'''


def header(r, cur='', theme='pill', back=None):
    links = ''.join(f'<a href="{r}{h}" class="{c}"{" aria-current=page" if h == cur else ""}>{t}</a>' for h, t, c in NAV)
    dlinks = ''.join(f'<a href="{r}{h}">{t}</a>' for h, t, c in NAV)
    backbtn = f'<a class="back-btn" href="{r}{back}" aria-label="Vissza">←</a>' if back else ''
    return f'''<header class="site-head hd-{theme}{' has-back' if back else ''}"><div class="wrap">
{backbtn}<button class="menu-btn" type="button" data-menu aria-label="Menü"><svg width="20" height="14" viewBox="0 0 20 14"><path d="M0 1h20M0 7h20M0 13h20" stroke="#1B2A5C" stroke-width="2"/></svg></button>
<a class="logo" href="{r}index.html" aria-label="Kontyos – főoldal"><img src="{r}img/logo.png" alt="Kontyos" width="122" height="30"></a>
<nav class="nav" aria-label="Fő menü">{links}</nav>
<a class="cart-btn" href="{r}kosar.html" aria-label="Kosár"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 7h14l-1.5 12h-11z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg><span class="lbl">Kosár</span> <span data-cart-count>0</span></a>
</div></header>
<div class="drawer" id="drawer"><nav aria-label="Mobil menü"><button class="close" type="button" data-menu-close aria-label="Bezárás">×</button>
<a href="{r}index.html">Főoldal</a>{dlinks}<a href="{r}friss.html">FRISS & Secco</a><a href="{r}vasarok.html">Kövess minket – standok</a><a href="{r}kosar.html">Kosár</a><a href="{r}info.html">Szállítás & ÁSZF</a></nav></div>
'''


def footer(r):
    return f'''<footer class="site-foot"><div class="wrap">
<div class="brand"><img src="{r}img/logo.png" alt="Kontyos" width="210" height="52"><p style="margin-top:14px;max-width:340px;font-size:14px">100%-os gyümölcsborok a klárafalvi Kontyos Borháztól.</p></div>
<div><h4>Termékek</h4><a href="{r}gyumolcsbor.html">Gyümölcsborok</a><a href="{r}friss.html">FRISS & Berry Secco</a><a href="{r}termek/piri-mama-forralt-bora.html">PIRI Mama forralt bor</a><a href="{r}termek/don-cherry.html">Don Cherry</a><a href="{r}palinka.html">Pálinka</a></div>
<div><h4>Kampányok</h4><a href="{r}ujbor-valogatas.html">Újbor-válogatás</a><a href="{r}black-friday.html">Black Friday</a><a href="{r}karacsonyi-ajandek-bor.html">Karácsonyi ajándék</a><a href="{r}vasarok.html">Kövess minket – standok</a></div>
<div><h4>Infó</h4><a href="{r}info.html#szallitas">Szállítás</a><a href="{r}info.html#aszf">ÁSZF</a><a href="{r}info.html#adatkezeles">Adatkezelés</a><a href="{r}info.html#kapcsolat">Kapcsolat</a></div>
<p class="legal">Alkoholtartalmú termékeinket kizárólag 18. életévét betöltött személyek vásárolhatják meg. Fogyassz felelősségteljesen! · © Kontyos Borház Kft. · 6773 Klárafalva, Kossuth u. 183. · info@kontyos.hu · +36-20/349-2185 · Demó: Stratos Webdesign</p>
</div></footer>
{fairs_js()}<script src="{r}assets/catalog.js?v={VER}"></script>
<script src="{r}assets/app.js?v={VER}"></script>
</body></html>
'''


def stars(rating):
    try:
        v = float(rating)
    except (TypeError, ValueError):
        return ''
    return '★' * int(round(v)) + '☆' * (5 - int(round(v)))


def card(p, r, tint=None):
    out = '' if p['avail'] else ' out'
    old = f'<span class="old">{ft(p["old"])}</span>' if p.get('old') else ''
    pr = ft(p['price']) if p['avail'] else 'Elfogyott'
    plus = f'<button class="plus" type="button" data-add="{p["id"]}" aria-label="{e(p["name"])} kosárba">+</button>' if p['avail'] else ''
    taste = 'szaraz' if p['name'].lower().startswith('szár') or 'száraz' in p['name'].lower() else 'edes'
    t = tint or (p['arch'] if p['line'] not in ('friss', 'piri', 'don') else '#F8F4EC')
    return f'''<div class="pcard{out}" data-taste="{taste}" data-card style="position:relative"><a href="{r}{url(p)}" style="text-decoration:none;display:flex;flex-direction:column;flex:1" class="in">
<div class="ph" style="--tint:{t}"><img src="{r}{p['img']}" alt="{e(p['name'])}" loading="lazy" width="500" height="500"></div>
<div class="tx"><span class="k">{LINE_LABEL[p['line']]}</span><span class="n">{e(p['name'])}</span>
<div class="row"><span class="pr">{old}{pr}</span></div></div></a>
<div style="position:absolute;right:16px;bottom:14px">{plus}</div></div>'''


def cards(ids, r, cls='cards'):
    return f'<div class="{cls}">' + ''.join(card(P[i], r) for i in ids) + '</div>'


def hb(p, r, h, ml=0, rot='0deg'):
    return f'''<div class="hb" style="--h:{h};margin-left:{ml}px"><div class="hbi"><span class="hbr" style="transform:rotate({rot})"><img src="{r}{p['tight']}" alt="{e(p['name'])}">
<a class="hbl" href="{r}{url(p)}" aria-label="{e(p['name'])} – termékoldal"></a></span>
<div class="hw"><div class="in"><span class="n">{e(p['name'])}</span><span class="p">{ft(p['price'])}</span><button type="button" data-add="{p['id']}">Kosárba +</button></div></div>
<button class="hbp" type="button" data-add="{p['id']}" aria-label="{e(p['name'])} kosárba">+</button></div></div>'''


STAMP = '''<div class="stamp" aria-hidden="true"><svg viewBox="0 0 200 200" width="168" height="168"><defs><path id="sc-{uid}" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
<circle cx="100" cy="100" r="98" fill="{bg}"/><text font-family="Manrope" font-weight="800" font-size="15" letter-spacing="4" fill="{fg}"><textPath href="#sc-{uid}">{txt}</textPath></text></svg><b style="color:{fg}">{center}</b></div>'''


def write(path, s):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if path.endswith('.html'):
        s = re.sub(r'(img/[\w./-]+\.(?:webp|png))(?=["\)\s])', lambda m: m.group(1) + '?v=' + VER, s)
    open(full, 'w', encoding='utf-8').write(s)


# ---------- főoldal ----------
SEASONS = [
    dict(k='forralt', lbl='Forralt szezon', bg='#F08A3C', fg='#1B2A5C', word='FORRALT', hword='#1B2A5C', acc='#1B2A5C', ctafg='#FFFFFF',
         stampbg='#1B2A5C', stampfg='#F3C66B', stamp='CSAK MEGMELEGÍTED · ÉS KÉSZ · PIRI MAMA · ',
         bottles=[('piri-mama-forralt-bora', 'clamp(280px,50vh,430px)', '-9deg'), ('narancsos-piri-mama-forralt-bora', 'clamp(330px,60vh,520px)', '4deg'), ('epres-piri-mama-forralt-bora', 'clamp(270px,49vh,420px)', '12deg')],
         ml=64, eyebrow='Új · Narancsos PIRI Mama', t='Csak megmelegíted, és kész.', s='Narancsos, fűszeres forralt gyümölcsbor egyliteres palackban – azonnal fogyasztható.',
         cta=('PIRI Mama forralt borok', 'termek/narancsos-piri-mama-forralt-bora.html'), price=None),
    dict(k='ujbor', lbl='Újbor', bg='#F6E1E4', fg='#1B2A5C', word='ÚJBOR', hword='#EFC9CF', acc='#EF4E73', ctafg='#fff',
         bottles=[('edes-eperbor', 'clamp(300px,58vh,560px)'), ('edes-meggybor', 'clamp(330px,64vh,610px)'), ('edes-kajszibor', 'clamp(300px,58vh,560px)')],
         eyebrow='Limitált · nov. 5–23.', t='Az idei gyümölcs, palackban.', s='Válogass a klasszikus gyümölcsborokból – 6 palacktól mennyiségi áron.',
         cta=('Újbor-válogatás', 'ujbor-valogatas.html'), price=('ujbor-valogatas', '6 palack')),
    dict(k='bf', lbl='Black Friday', bg='#141A33', fg='#F3EEE5', word='BLACK', hword='#222B4D', acc='#EF4E73', ctafg='#fff',
         bottles=[('klara-szaraz-barrique-meggybor', 'clamp(300px,58vh,560px)'), ('klara-edes-malnabor', 'clamp(330px,64vh,610px)'), ('don-cherry', 'clamp(300px,58vh,560px)')],
         eyebrow='Black Friday · nov. 23–29.', t='A prémium polc, egy évben egyszer ennyiért.', s='Klára, Don Cherry és válogatások – csak a kampány idején.',
         cta=('Black Friday ajánlatok', 'black-friday.html'), price=('bf-premium', 'prémium csomag')),
    dict(k='karacsony', lbl='Karácsony', bg='#7A1C2C', fg='#F3EEE5', word='ÜNNEP', hword='#8A2A3A', acc='#F3C66B', ctafg='#1B2A5C',
         bottles=[('edes-ribizlibor', 'clamp(300px,58vh,560px)'), ('klara-edes-malnabor', 'clamp(330px,64vh,610px)'), ('szamocapalinka', 'clamp(290px,56vh,540px)')],
         eyebrow='Karácsonyi ajándék bor', t='Ajándék, amit tényleg kibontanak.', s='Összeállított ajándékcsomagok dec. 1–22. között – utolsó rendelési nap: [DÁTUM].',
         cta=('Ajándékcsomagok', 'karacsonyi-ajandek-bor.html'), price=('premium-advent', 'ajándékcsomag')),
]


def price_of(pid):
    return P[pid] if pid in P else SP[pid]


def season_hero(s, r):
    b = ''.join(hb(P[bt[0]], r, bt[1], 0 if i == 0 else s.get('ml', 4), bt[2] if len(bt) > 2 else '0deg') for i, bt in enumerate(s['bottles']))
    price = ''
    if s['price']:
        pp = price_of(s['price'][0])
        old = f'<s>{ft(pp["old"])}</s>' if pp.get('old') else ''
        price = f'<div class="price"><div class="in">{old}<b>{ft(pp["price"])}</b><small>{s["price"][1]}</small></div></div>'
    return f'''<section class="hero" data-season="{s['k']}" style="--hbg:{s['bg']};--hfg:{s['fg']};--hword:{s['hword']};--haccent:{s['acc']};--hctafg:{s['ctafg']}">
<p class="word" aria-hidden="true">{s['word']}</p>
<div class="bottles">{b}</div>
{STAMP.format(bg=s.get('stampbg', s['acc']), fg=s.get('stampfg', s['ctafg']), txt=s.get('stamp', '100% GYÜMÖLCSBŐL · KLÁRAFALVA · KONTYOS ·'), uid=s['k'], center='100%')}
<div class="copy"><div class="wrap"><div class="txt"><span class="eyebrow">{s['eyebrow']}</span><p class="t">{s['t']}</p><p class="s">{s['s']}</p><a class="btn" href="{r}{s['cta'][1]}">{s['cta'][0]} →</a></div>
{price}</div></div>
</section>'''


FRUITS = ['edes-meggybor', 'edes-eperbor', 'edes-ribizlibor', 'edes-kajszibor', 'edes-oszibarackbor', 'edes-szilvabor', 'edes-bodza-almabor', 'szaraz-meggybor']


def fruit_selector(r):
    def nm(p):
        return p['name'].replace('Édes ', '').replace('bor', 'bor').capitalize()
    items = ''
    for i, pid in enumerate(FRUITS):
        p = P[pid]
        items += (f'<a href="{r}{url(p)}" data-fruit data-id="{pid}" data-img="{r}{p["tight"]}" data-tint="{p["arch"]}" data-bg="{p["arch"]}" '
                  f'data-ink="{p["accent"]}" data-name="{e(p["name"])}" data-k="{LINE_LABEL[p["line"]]}" data-line="{e(p["short"][:150].rsplit(" ", 1)[0])}…" '
                  f'data-price="{ft(p["price"])}" style="--fc:{p["accent"]}" aria-current="{"true" if i == 0 else "false"}">{e(p["name"])}<small>{ft(p["price"])}</small></a>')
    p = P[FRUITS[0]]
    return f'''<section class="sec" id="frui" style="background:{p['arch']}"><div class="wrap">
<p class="kicker" style="--accent:#1B2A5C">Válassz gyümölcsöt</p><h2 class="h2" style="margin:8px 0 34px">Melyik gyümölcs a tiéd?</h2>
<div class="fsel" data-fruits><div class="list">{items}</div>
<div class="view" data-fruit-view style="--tint:rgba(255,255,255,.55)"><a class="arch" href="{r}{url(p)}" data-f-href><img src="{r}{p['tight']}" alt="{e(p['name'])}"></a>
<div class="meta"><span class="kicker" data-f-k style="--accent:#1B2A5C">{LINE_LABEL[p['line']]}</span><b data-f-n style="color:{p['accent']}">{e(p['name'])}</b><p data-f-l style="font-size:15px;line-height:1.6">{e(p['short'][:150].rsplit(' ', 1)[0])}…</p>
<span data-f-p style="font-family:var(--serif);font-weight:800;font-size:28px">{ft(p['price'])}</span>
<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn pink" type="button" data-add="{p['id']}">Kosárba</button><a class="btn ghost" href="{r}{url(p)}" data-f-href>Részletek</a></div></div></div></div>
</div></section>'''


# ---------- kampány-landingek a design (BlackFriday.dc / Karacsony.dc) alapján ----------
XMAS_BAR = '<div class="xbar">UTOLSÓ RENDELÉS KARÁCSONYRA: [DÁTUM – A KONTYOS ADJA]</div>'


def dotc(p):
    c = p['accent']
    return p['arch'] if c.upper() in ('#FFFFFF', '#FFF6EA', '#1B2A5C') and p['line'] == 'friss' else c


def pack_bottles(sp, r, h='88%'):
    return ''.join(f'<img src="{r}{P[i]["tight"]}" alt="{e(P[i]["name"])}" loading="lazy"{" class=jar" if i in ("don-cherry-gyumolcse",) else ""}{" class=pil" if i == "meggymag-parna" else ""}>' for i in sp['items'] if i != 'meggymag-parna')


def pack_contents(sp):
    names = [P[i]['name'] for i in sp['items']]
    if sp.get('qty'):
        names = [f"{sp['qty']}× {n}" for n in names]
    if sp.get('extra'):
        names.append(sp['extra'])
    return ' · '.join(names)


def bf_landing(r, phase, htag='h1', uid='bf'):
    wait = phase == 'varolista'
    eyebrow = 'NOV. 23–29. · HAMAROSAN' if wait else 'NOV. 23–29. · MOST FUT · <span data-countdown="2026-11-29T23:59:59+01:00"></span>'
    note = 'Iratkozz fel, és elsőként szólunk.' if wait else 'Nov. 29-ig, vagy amíg a készlet tart.'
    prem, disz = SP['bf-premium'], SP['bf-diszkont']

    def cta(sp, primary):
        if wait:
            return f'<a class="btn {"navy" if primary else "ghost"} block" href="#bf-wait-{uid}">Értesítést kérek</a>'
        return f'<button class="btn {"blue" if primary else "ghost"} block" type="button" data-add="{sp["id"]}">Kosárba teszem</button>'
    b = hb(P['piri-mama-forralt-bora'], r, 'clamp(300px,58vh,540px)', 0, '-9deg') + hb(P['don-cherry'], r, 'clamp(340px,66vh,620px)', 12, '4deg')
    out = f'''<section class="hero lp-bf" style="--hbg:#141A33;--hfg:#fff;--hword:#EF4E73;--haccent:#EF4E73;--hctafg:#fff">
<p class="word" aria-hidden="true">−25,9%</p>
<div class="bottles">{b}</div>
{STAMP.format(bg='#F3C66B', fg='#141A33', txt='BLACK FRIDAY · NOV. 23–29. · INGYEN SZÁLLÍTVA · ', uid='bf-' + uid, center='BF')}
<div class="copy"><div class="wrap"><div class="txt" style="text-shadow:0 2px 18px rgba(20,26,51,.6)"><span class="eyebrow">{eyebrow}</span>
<{htag} class="t">Black Friday borcsomag akció – akár −25,9%</{htag}><p class="t2">Black Friday a borházban.</p><p class="s">Két doboz, egy hét. {note}</p>
<a class="btn" href="#bf-dobozok-{uid}">A dobozok →</a></div></div></div></section>
<section class="lp-boxes" id="bf-dobozok-{uid}"><div class="wrap">
<article class="lp-box big"><div class="in">
<div class="tagrow"><span style="color:#C8284E">LEGJOBB VÁLASZTÁS</span><span>40 DOBOZ</span></div>
<h2>Black Friday Prémium</h2>
<div class="ph" style="--tint:{prem['tint']}">{pack_bottles(prem, r)}</div>
<p class="ct">{e(pack_contents(prem))}</p>
<div class="pr"><s>{ft(prem['old'])}</s><b>{ft(prem['price'])}</b><em>INGYENES SZÁLLÍTÁS</em></div>
{cta(prem, True)}</div></article>
<article class="lp-box small"><div class="in">
<div class="tagrow"><span style="color:#6A6F7E">KISEBB KERETBŐL</span></div>
<h2>Black Friday diszkont</h2>
<div class="ph" style="--tint:{disz['tint']};height:180px">{pack_bottles(disz, r)}</div>
<p class="ct">2-2 palack FRISS eper, málna és meggy</p>
<div class="pr"><s>{ft(disz['old'])}</s><b>{ft(disz['price'])}</b></div>
<span style="font-size:12px;font-weight:700;color:#6A6F7E">−24,7% · szállítási díjas</span>
<p class="note2">A Prémiumban pluszban: Klára Málna, Don Cherry, PIRI Mama és Berry Secco – és ingyen jön.</p>
{cta(disz, False)}</div></article></div></section>'''
    if wait:
        out += f'''<section class="lp-wait" id="bf-wait-{uid}"><div class="wrap"><h2>Szólunk nov. 23-án reggel.</h2>
<form data-newsletter><label class="sr" for="bfm-{uid}">E-mail-cím</label><input id="bfm-{uid}" type="email" required placeholder="E-mail-címed"><button class="btn" style="background:#141A33" type="submit">Értesítést kérek</button></form></div></section>'''
    return out


def xmas_landing(r, phase, htag='h1', uid='x'):
    pre = phase == 'elozetes'
    eyebrow = 'DEC. 1-TŐL RENDELHETŐ' if pre else 'KARÁCSONY · DEC. 1–22.'
    b = (hb(P['epres-piri-mama-forralt-bora'], r, 'clamp(290px,54vh,500px)', 0, '-10deg')
         + hb(P['don-cherry'], r, 'clamp(330px,64vh,590px)', 12, '3deg')
         + hb(P['narancsos-piri-mama-forralt-bora'], r, 'clamp(280px,52vh,470px)', 12, '11deg'))

    def band(price):
        return 'lt5' if price < 5000 else ('5-15' if price <= 15000 else 'gt15')
    packs = ''
    for k, pid in enumerate(['edes-unnepek', 'premium-advent', 'konnyu-karacsony']):
        sp = SP[pid]
        rot = ['-0.6deg', '0.5deg', '-0.4deg'][k]
        dots = ''.join(f'<i title="{e(P[i]["name"])}" style="background:{dotc(P[i])}"></i>' for i in sp['items'])
        btn = (f'<a class="btn navy block" href="#xn-{uid}">Értesítést kérek dec. 1-jén</a>' if pre
               else f'<button class="btn block" style="background:#7A1C2C" type="button" data-add="{pid}">Ajándékba kérem</button>')
        packs += f'''<article class="lp-pack" data-taste="{band(sp['price'])}" data-xpack style="transform:rotate({rot})"><div class="in">
<div class="ph" style="--tint:{sp['tint']}">{pack_bottles(sp, r)}</div>
<div class="tx"><div class="tagrow"><span style="color:#7A1C2C">{sp['tag']}</span><span>{'INGYENES SZÁLLÍTÁS' if sp['free'] else '+ SZÁLLÍTÁSI DÍJ'}</span></div>
<h2>{e(sp['name'])}</h2><div class="dots">{dots}</div><p class="ct">{e(pack_contents(sp))}</p>
<div class="pr"><s>{ft(sp['old'])}</s><b>{ft(sp['price'])}</b></div>{btn}</div></div></article>'''
    extras = ['szamocapalinka', 'birspalinka', 'meggypalinka', 'kontyos-borospohar', 'piri-mama-bogreje', 'meggymag-parna']
    out = f'''<section class="hero lp-xmas" style="--hbg:#7A1C2C;--hfg:#fff;--hword:#F3C66B;--haccent:#F3C66B;--hctafg:#4A0F19">
<p class="word" aria-hidden="true">ÜNNEP</p>
<div class="bottles">{b}</div>
<div class="copy"><div class="wrap"><div class="txt" style="text-shadow:0 2px 18px rgba(74,15,25,.6)"><span class="eyebrow">{eyebrow}</span>
<{htag} class="t">Karácsonyi ajándék bor és borcsomagok</{htag}><p class="s">Dobozba rakva, a pöttysor megmutatja, mi van benne.</p>
<a class="btn" href="#csomagok-{uid}">Ajándékcsomagok →</a></div></div></div></section>
<section class="lp-xpacks" id="csomagok-{uid}"><div class="wrap">
<div class="filters" data-filter-group="#csomagok-{uid} [data-xpack]"><span class="kicker" style="--accent:#1B2A5C;margin-right:8px">Keret</span><button type="button" data-filter="all" aria-pressed="true">Mind</button><button type="button" data-filter="lt5" aria-pressed="false">5 000 Ft alatt</button><button type="button" data-filter="5-15" aria-pressed="false">5–15 000 Ft</button><button type="button" data-filter="gt15" aria-pressed="false">15 000 Ft felett</button></div>
{packs}'''
    if pre:
        out += f'''<div class="lp-wait" id="xn-{uid}" style="background:#7A1C2C;border-radius:6px"><div style="padding:30px;display:flex;flex-wrap:wrap;gap:16px 40px;align-items:center"><h2>Dec. 1-jén szólunk.</h2>
<form data-newsletter><label class="sr" for="xm-{uid}">E-mail-cím</label><input id="xm-{uid}" type="email" required placeholder="E-mail-címed"><button class="btn" style="background:#F3C66B;color:#4A0F19" type="submit">Értesítést kérek</button></form></div></div>'''
    out += f'''</div></section>
<section class="lp-don"><div class="wrap"><img src="{r}img/photo/don_ajandek.webp" alt="Don Cherry palack és üveg meggy" loading="lazy">
<div class="tx"><p class="kicker" style="--accent:#2E8C86;letter-spacing:.3em">AJÁNDÉKBA – PRÉMIUM</p><h2>DON <span>CHERRY</span></h2>
<p>Kis és nagy ajándékcsomag. [Összetétel és ár – a Kontyos adja]</p>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" style="background:#C8282E;letter-spacing:.14em;font-size:13px" href="{r}termek/don-cherry.html">KIS CSOMAG</a><a class="btn ghost" style="color:#C8282E;letter-spacing:.14em;font-size:13px" href="{r}termek/don-cherry.html">NAGY CSOMAG</a></div></div></div></section>
<section class="sec" id="palinka-{uid}"><div class="wrap" style="display:flex;flex-direction:column;gap:26px"><h2 class="h2">Mellé: pálinka és apróság</h2>{cards(extras, r)}</div></section>'''
    return out


def bf_page():
    r = ''
    segs = '<span class="seg">' + ''.join(f'<button type="button" data-phase-btn="{k}">{l}</button>' for k, l in [('aktiv', 'BF aktív'), ('varolista', 'BF előtt (várólista)')]) + '</span>'
    pg = head('Black Friday borcsomag akció – akár −25,9% | Kontyos', 'Black Friday borcsomag akció nov. 23–29.: Prémium csomag 19 900 Ft ingyenes szállítással, diszkont csomag 9 900 Ft.', r, 'black-friday', 'overlay-head', demo_extra=segs)
    pg += header(r, 'black-friday.html') + '<main>'
    pg += ''.join(f'<div data-phase="{ph}">{bf_landing(r, ph, "h1", ph)}</div>' for ph in ('aktiv', 'varolista'))
    pg += home_body(r, 'h2') + '</main>' + footer(r)
    write('black-friday.html', pg)


def xmas_page():
    r = ''
    segs = '<span class="seg">' + ''.join(f'<button type="button" data-phase-btn="{k}">{l}</button>' for k, l in [('aktiv', 'Aktív'), ('elozetes', 'Előzetes')]) + '</span>'
    pg = head('Karácsonyi ajándék bor és borcsomagok | Kontyos', 'Karácsonyi ajándék bor és borcsomagok dec. 1–22.: Édes Ünnepek, Prémium adventi és Könnyű karácsonyi borcsomag.', r, 'karacsony', 'overlay-head', demo_extra=segs, topbar=XMAS_BAR)
    pg += header(r, 'karacsonyi-ajandek-bor.html') + '<main>'
    pg += ''.join(f'<div data-phase="{ph}">{xmas_landing(r, ph, "h1", ph)}</div>' for ph in ('aktiv', 'elozetes'))
    pg += home_body(r, 'h2') + '</main>' + footer(r)
    write('karacsonyi-ajandek-bor.html', pg)


MSEARCH = '''<section class="m-search"><form role="search" action="kereses.html"><label class="sr" for="ms">Keresés</label><input id="ms" name="q" type="search" placeholder="Meggy, forralt bor, ajándék…"><button type="submit" aria-label="Keresés"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg></button></form>
<nav aria-label="Gyors kategóriák"><a href="termek/piri-mama-forralt-bora.html" style="background:#1B2A5C;color:#fff">Forralt bor</a><a href="gyumolcsbor.html#klasszikus" style="box-shadow:inset 0 0 0 1.5px #1B2A5C">Klasszikus</a><a href="friss.html" style="background:#F28C28">FRISS</a><a href="gyumolcsbor.html#klara" style="box-shadow:inset 0 0 0 1.5px #C0284A;color:#C0284A">Klára</a><a href="termek/don-cherry.html" style="box-shadow:inset 0 0 0 1.5px #5FB8B3;color:#C8282E">Don Cherry</a><a href="karacsonyi-ajandek-bor.html" style="box-shadow:inset 0 0 0 1.5px #1B2A5C">Csomagok</a><a href="palinka.html" style="box-shadow:inset 0 0 0 1.5px #A8823C;color:#6B5414">Pálinka</a></nav></section>'''


def search_page():
    r = ''
    pg = head('Keresés | Kontyos', 'Keresés a Kontyos termékei között', r, 'search') + header(r)
    pg += '''<main><div class="wrap" style="padding-top:10px;padding-bottom:90px;display:flex;flex-direction:column;gap:22px"><h1 class="h2">Keresés</h1>
<form role="search" action="kereses.html" class="m-search" style="display:block;background:none;border:0;padding:0"><label class="sr" for="sq">Keresés</label><div style="display:flex;align-items:center;gap:8px;background:#fff;border-radius:999px;padding:0 6px 0 18px;max-width:640px"><input id="sq" name="q" type="search" placeholder="Meggy, forralt bor, ajándék…" style="flex:1;min-width:0;height:52px;border:0;background:transparent;font:inherit;font-size:16px;outline:none"><button type="submit" class="btn blue" style="min-height:42px;padding:0 20px">Keresés</button></div></form>
<p id="search-sum" class="muted"></p><div id="search-res" class="cards"></div></div></main>''' + footer(r)
    write('kereses.html', pg)


# ---------- Kövess minket: adventi standok (DEMÓ időpontok – a valós menetrendet a Kontyos adja) ----------
FAIRS = [
    dict(id='szeged', city='Szeged', place='Dóm tér – Szegedi Adventi Vásár', lat=46.2496, lng=20.1490, start='2026-11-20', end='2027-01-04', hours='[NYITVATARTÁS]'),
    dict(id='obuda', city='Budapest – Óbuda', place='Fő tér – Óbudai Advent', lat=47.5414, lng=19.0450, start='2026-11-27', end='2026-12-23', hours='[NYITVATARTÁS]'),
    dict(id='gyor', city='Győr', place='Árkád bevásárlóközpont', lat=47.6817, lng=17.6426, start='2026-11-23', end='2026-12-24', hours='[NYITVATARTÁS]'),
    dict(id='veszprem', city='Veszprém', place='Óváros tér – Veszprémi Advent', lat=47.0932, lng=17.9076, start='2026-11-28', end='2026-12-23', hours='[NYITVATARTÁS]'),
    dict(id='szombathely', city='Szombathely', place='Fő tér – Szombathelyi Advent', lat=47.2306, lng=16.6219, start='2026-12-04', end='2026-12-23', hours='[NYITVATARTÁS]'),
]
BORHAZ = dict(city='Klárafalva', place='Kontyos Borház – egész évben, személyes átvétel', lat=46.2209, lng=20.3266)


def fairs_js():
    return '<script>window.KONTYOS_FAIRS=' + json.dumps(FAIRS, ensure_ascii=False) + ';window.KONTYOS_BORHAZ=' + json.dumps(BORHAZ, ensure_ascii=False) + ';</script>'


def fairs_strip(r=''):
    cards = ''.join(f'''<a class="fair-card" href="{r}vasarok.html#{f['id']}" data-fair="{f['id']}"><span class="st" data-fair-status>Hamarosan</span><b>{e(f['city'])}</b><span class="pl">{e(f['place'])}</span><span class="dt" data-fair-dates></span></a>''' for f in FAIRS)
    return f'''<section class="sec follow"><div class="wrap"><div class="fhead"><div><p class="kicker" style="--accent:#F3C66B">Kövess minket</p><h2 class="h2">Itt találkozhatunk adventkor</h2>
<p class="lead">Öt városban várunk a standunkkal. Nézd meg, hol vagyunk éppen, és iratkozz fel: szólunk, mielőtt a városodba érkezünk.</p></div>
<a class="btn" style="background:#F3C66B;color:#1B2A5C" href="{r}vasarok.html">Térkép és értesítő →</a></div>
<div class="fair-row">{cards}</div><p class="ph-note" style="color:#F3EEE5">Időpontok: a 2026-os menetrend egyeztetés alatt.</p></div></section>'''


def fairs_page():
    r = ''
    segs = '<span class="seg"><button type="button" data-sim="">Ma</button><button type="button" data-sim="2026-12-06">Szimuláció: dec. 6.</button></span>'
    extra = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">'
    pg = head('Kövess minket – adventi standjaink térképen | Kontyos', 'Hol van most a Kontyos standja? Adventi vásárok térképen, élő státusszal és e-mail értesítővel: szólunk, mielőtt a városodba érünk.', r, 'fairs', '', extra, demo_extra=segs)
    pg += header(r)
    rows = ''.join(f'''<li id="{f['id']}" data-fair="{f['id']}"><button type="button" class="fl-go" data-go="{f['id']}"><span class="st" data-fair-status>Hamarosan</span><b>{e(f['city'])}</b><span class="pl">{e(f['place'])}</span><span class="dt" data-fair-dates></span><span class="hr">Nyitva: {e(f['hours'])}</span></button></li>''' for f in FAIRS)
    checks = ''.join(f'''<label class="check"><input type="checkbox" name="fair" value="{f['id']}"> <span><b>{e(f['city'])}</b> · {e(f['place'])}</span></label>''' for f in FAIRS)
    pg += f'''<main class="fairs"><section class="wrap fz-head"><p class="breadcrumb"><a href="index.html">Főoldal</a> / Kövess minket</p>
<p class="kicker">Kövess minket</p><h1 class="h2">Adventi standjaink</h1>
<p class="lead">A térképen láthatod, melyik vásáron vagyunk éppen, és mikor érkezünk a te városodba. Iratkozz fel, és előre szólunk.</p>
<div class="legend"><span><i class="lv"></i>Most itt vagyunk</span><span><i class="up"></i>Hamarosan</span><span><i class="dn"></i>Véget ért</span><span><i class="bh"></i>Borház</span></div></section>
<section class="wrap fz-grid"><div id="fmap" class="fmap" role="region" aria-label="Standok térképe"></div>
<ol class="flist">{rows}</ol></section>
<section class="fz-sub" id="ertesito"><div class="wrap"><div class="tx"><p class="kicker" style="--accent:#F3C66B">Értesítő</p><h2 class="h2">Szólunk, mielőtt a városodba érkezünk</h2>
<p class="lead">Jelöld be, melyik vásárról kérsz értesítést. Automatikus e-mailt küldünk 3 nappal a nyitás előtt és a nyitás reggelén, és ha valamelyik időpont változik, arról is szólunk.</p>
<div class="mailprev"><p class="mh">Így néz ki az e-mail</p><div class="mail"><small>Tárgy: Péntektől Szegeden vagyunk – Dóm tér 🍷</small><b>Szia! Hamarosan a városodban leszünk.</b><p>A PIRI Mama standja nov. 20-tól a Dóm téren vár: forralt bor, újbor-kóstoló és ajándékcsomagok. Mutasd fel ezt a levelet a standon: [AJÁNDÉK / KEDVEZMÉNY – a Kontyos adja].</p><span class="btnlike">Útvonal a standhoz →</span></div></div></div>
<form class="subform" data-fair-form><div class="field"><label for="fz-name">Keresztnév</label><input id="fz-name" name="name" autocomplete="given-name"></div>
<div class="field"><label for="fz-mail">E-mail cím</label><input id="fz-mail" name="email" type="email" required autocomplete="email"><span class="msg">Adj meg érvényes e-mail címet</span></div>
<fieldset><legend>Melyik vásárról kérsz értesítést?</legend>{checks}<label class="check all"><input type="checkbox" data-fair-all> <span><b>Mindegyikről</b></span></label></fieldset>
<label class="check"><input type="checkbox" required> <span>Hozzájárulok, hogy a Kontyos Borház Kft. a megadott vásárokról e-mailben értesítsen. Bármikor leiratkozhatok.</span></label>
<button class="btn" type="submit" style="background:#F3C66B;color:#1B2A5C">Értesítést kérek</button><p class="fz-ok" data-fair-ok role="status"></p></form></div></section>
<section class="wrap" style="padding-top:20px;padding-bottom:80px"><p class="ph-note">Demó időpontok és nyitvatartás – a valós menetrendet a Kontyos adja. A „Szimuláció” gombbal megnézheted, hogyan néz ki az oldal advent közepén, amikor több stand élőben fut.</p></section></main>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>''' + footer(r)
    write('vasarok.html', pg)


def home_body(r='', h='h1'):
    mq = ' · '.join(['100% gyümölcsből', 'Klárafalvi Kontyos Borház', 'Ingyenes szállítás 20 000 Ft felett', '6 palacktól mennyiségi ár'] * 2)
    pg = ''
    pg += f'<div class="marquee" aria-hidden="true"><div><span>{mq} · </span><span>{mq} · </span></div></div>'
    pg += f'''<section class="sec" style="padding-bottom:40px"><div class="wrap" style="display:flex;flex-direction:column;gap:22px">
<{h} class="h2" style="max-width:980px">100%-os gyümölcsborok a klárafalvi Kontyos Borháztól</{h}>
<ul class="usp"><li>100% gyümölcsből</li><li>Ingyenes szállítás 20 000 Ft felett</li><li>6 palacktól mennyiségi ár</li><li>Kiszállítás 1–5 munkanap</li><li>Törzsvásárlói kedvezmény akár 15%</li></ul>
<div style="margin-top:20px">{cards(['edes-meggybor', 'edes-eperbor', 'klara-edes-malnabor', 'friss-malna', 'don-cherry'], r, 'cards home-picks')}</div>
</div></section>'''
    pg += fruit_selector(r)
    pg += f'''<section class="sec"><div class="wrap"><div class="collage">
<img class="a" src="{r}img/photo/piri_nar_life.webp" alt="Narancsos PIRI Mama forralt bora" loading="lazy">
<img src="{r}img/photo/don_life.webp" alt="Don Cherry meggyvermut" loading="lazy"><img src="{r}img/photo/friss_malna.webp" alt="FRISS málna" loading="lazy">
<img src="{r}img/photo/klara.webp" alt="Klára prémium gyümölcsbor" loading="lazy" style="grid-column:2/4;aspect-ratio:2/1"></div></div></section>'''
    pg += f'''<section class="sec" style="background:#F28C28;color:#1B2A5C"><div class="wrap split">
<div><img src="{r}img/photo/friss_flat.webp" alt="FRISS gyümölcsborok" loading="lazy"></div>
<div style="display:flex;flex-direction:column;gap:18px"><p class="kicker" style="--accent:#1B2A5C">FRISS · Berry Secco</p><h2 class="h2">Könnyű, színes, hűtve az igazi.</h2>
<p class="lead">A FRISS gyümölcsborok és a Berry Secco a könnyebb, lazább oldal – {ft(2190)}-tól.</p>
<div>{cards(['friss-narancs', 'friss-eper', 'friss-malna', 'friss-meggy'], r, 'scroller')}</div><a class="btn navy" href="{r}friss.html" style="align-self:flex-start">Mind a FRISS →</a></div></div></section>'''
    pg += f'''<section class="sec"><div class="wrap" style="display:flex;flex-direction:column;gap:28px"><p class="kicker">Válogatások</p><h2 class="h2">Csomagban jobban megéri</h2>
{cards(['meggy-paros', 'eper-paros', 'konnyu-trio', 'bubi-paros'], r)}</div></section>'''
    pg += f'''<section class="sec" style="background:#fff"><div class="wrap split">
<div style="display:flex;flex-direction:column;gap:18px"><p class="kicker">Klárafalva</p><h2 class="h2">Mitől 100%-os a gyümölcsbor?</h2>
<p class="lead">Gyümölcsboraink 100%-ban magyar gyümölcsökből készülnek. Édesapánk közel két évtizede alkotta meg első gyümölcsborát: a család hölgy tagjai olyan italra vágytak, mely édes és zamatos, akár egy nyári gyümölcs.</p>
<p style="line-height:1.7;opacity:.85">2006 óta alkotunk elsőrangú hazai gyümölcsökből gyümölcsbor-különlegességeket, hagyományos és reduktív eljárással. A 2019-ben épült modern üzemünk Szegedhez közel, Klárafalván működik.</p>
<a class="btn ghost" href="{r}info.html#rolunk" style="align-self:flex-start">Rólunk</a></div>
<div><img src="{r}img/photo/borhaz.webp" alt="A klárafalvi Kontyos Borház" loading="lazy"></div></div></section>'''
    pg += fairs_strip(r)
    pg += newsletter()
    return pg


def index():
    r = ''
    segs = '<span class="seg" aria-label="Szezon váltó">' + ''.join(f'<button type="button" data-season-btn="{s["k"]}">{s["lbl"]}</button>' for s in SEASONS) + '</span>'
    heroes = ''
    for s_ in SEASONS:
        if s_['k'] == 'bf':
            heroes += f'<div data-season="bf">{bf_landing(r, "aktiv", "h2", "home")}</div>'
        elif s_['k'] == 'karacsony':
            heroes += f'<div data-season="karacsony">{xmas_landing(r, "aktiv", "h2", "home")}</div>'
        else:
            heroes += season_hero(s_, r)
    pg = head('Kontyos – 100%-os gyümölcsborok a klárafalvi Kontyos Borháztól', 'Meggybor, eperbor, ribizlibor, forralt bor, Don Cherry és pálinka – 100%-os gyümölcsborok közvetlenül a klárafalvi Kontyos Borháztól.', r, 'home', 'overlay-head', demo_extra=segs, topbar=f'<div data-season="karacsony">{XMAS_BAR}</div>')
    pg += header(r) + '<main>' + heroes + MSEARCH + home_body(r, 'h1')
    pg += '</main>' + footer(r)
    write('index.html', pg)


def newsletter():
    return '''<section class="sec news"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:30px;align-items:center;justify-content:space-between">
<div><p class="kicker" style="--accent:#fff">Hírlevél</p><h2 class="h2">−5% az első rendelésedből</h2><p style="margin-top:8px">Iratkozz fel: a kuponkódot azonnal küldjük, mellé újdonságok, szezonális csomagok és akciók – elsőként.</p></div>
<form data-newsletter><label class="sr" for="nl">E-mail cím</label><input id="nl" type="email" placeholder="E-mail címed" required><button class="btn navy" type="submit">Feliratkozom</button></form></div></section>'''


# ---------- kategória ----------
def category():
    r = ''
    kl = [p['id'] for p in CAT if p['line'] == 'klasszikus']
    pg = head('Gyümölcsbor – 100%-os gyümölcsborok webshop | Kontyos', 'Meggybor, eperbor, ribizlibor, kajszibor és más 100%-os gyümölcsborok közvetlenül a termelőtől. 6 palacktól mennyiségi ár.', r, 'cat')
    pg += header(r, 'gyumolcsbor.html')
    pg += f'''<main><section style="padding:20px 0 40px"><div class="wrap" style="display:flex;flex-direction:column;gap:16px">
<p class="breadcrumb"><a href="index.html">Főoldal</a> / Gyümölcsborok</p>
<h1 class="h2" style="font-size:clamp(44px,6vw,86px)">Gyümölcsborok</h1><p class="lead" style="max-width:640px">100%-os gyümölcsborok közvetlenül a klárafalvi Kontyos Borháztól – a klasszikus édesektől a prémium Klára sorozatig.</p>
<nav class="chips" aria-label="Kategóriák"><a class="chip" href="#klasszikus">Klasszikus</a><a class="chip" href="#klara">Klára prémium</a><a class="chip" href="friss.html">FRISS & Secco</a><a class="chip" href="termek/piri-mama-forralt-bora.html">Forralt bor</a><a class="chip" href="termek/don-cherry.html">Don Cherry</a><a class="chip" href="palinka.html">Pálinka</a></nav></div></section>
<section id="klasszikus" style="padding-bottom:70px"><div class="wrap" style="display:flex;flex-direction:column;gap:22px">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px"><h2 class="h2">Klasszikus gyümölcsborok</h2>
<div class="filters" data-filter-group="#klasszikus [data-card]"><button type="button" data-filter="all" aria-pressed="true">Mind</button><button type="button" data-filter="edes" aria-pressed="false">Édes</button><button type="button" data-filter="szaraz" aria-pressed="false">Száraz</button></div></div>
{cards(kl, r)}</div></section>
<section id="klara" class="sec" style="background:#fff"><div class="wrap split">
<div><img src="img/photo/klara.webp" alt="Klára prémium gyümölcsbor" loading="lazy"></div>
<div style="display:flex;flex-direction:column;gap:18px"><p class="kicker" style="--accent:#C0284A">Prémium</p><h2 class="h2">Klára</h2><p class="lead">A Kontyos prémium sorozata – málna, rozé eper, barrique meggy.</p>
{cards([p['id'] for p in CAT if p['line'] == 'klara'], r)}</div></div></section>
<section class="sec" style="background:#5FB8B3"><div class="wrap split"><div style="display:flex;flex-direction:column;gap:16px;color:#fff"><p class="kicker" style="--accent:#fff">Meggyvermut</p><h2 class="h2">Don Cherry</h2><p class="lead">Édes meggyvermut, koktélba vagy jéggel.</p><a class="btn" style="background:#C8282E;align-self:flex-start" href="termek/don-cherry.html">Don Cherry →</a></div>
<div><img src="img/photo/don_flat.webp" alt="Don Cherry" loading="lazy"></div></div></section>
<section class="sec"><div class="wrap" style="max-width:900px;display:flex;flex-direction:column;gap:24px"><h2 class="h2">Gyakori kérdések</h2><div class="faq">
<details><summary>Mi az a gyümölcsbor?</summary><p>Szőlő helyett más gyümölcsből – meggyből, eperből, ribizliből – erjesztett bor. A Kontyos borai 100%-ban gyümölcsből készülnek.</p></details>
<details><summary>Mivel édesítitek a borokat?</summary><p>Édes borainkat az adott gyümölcs saját, 100%-os levével édesítjük, és kizárólag annyi cukor hozzáadásával készítjük, amennyi életre hívja a gyümölcs valódi karakterét.</p></details>
<details><summary>Mennyi a szállítási díj?</summary><p>MPL csomagautomata, PostaPont és postán maradó csomag: 1 800 Ft, GLS csomagpont: 2 100 Ft – 20 000 Ft felett ingyenes. GLS házhozszállítás: 2 400 Ft, 25 000 Ft felett ingyenes. Utánvét (csak GLS): +500 Ft. Részletek a <a href="info.html#szallitas">szállítási oldalon</a>.</p></details>
<details><summary>Mennyi idő alatt érkezik meg?</summary><p>GLS-sel a visszaigazolástól számított 3–5, MPL PostaPontra vagy postára 1–3 munkanap.</p></details>
<details><summary>Van mennyiségi kedvezmény?</summary><p>Igen: a legtöbb bornál 6 palacktól alacsonyabb darabár érvényes. Regisztrált vásárlóként 30 000 Ft összrendelés felett törzsvásárlói kedvezmény jár (5–15%) – részletek az <a href="info.html#torzsvasarlo">információs oldalon</a>.</p></details>
</div><div style="display:flex;flex-direction:column;gap:12px;margin-top:10px"><h2 class="serif" style="font-size:30px">Miért a Kontyos?</h2><p class="lead">Magyarország legnagyobb különleges minőségű gyümölcsborászataként tradicionális és reduktív eljárásokat ötvözünk. Gyümölcsboraink 100%-ban magyar gyümölcsökből, szívvel-lélekkel készülnek – gazdag ízüknek és színüknek köszönhetően egész évben a nyár friss, üde hangulatát hordozzák.</p>
<p>A <a href="#klasszikus">klasszikus gyümölcsborok</a> mellett a prémium <a href="#klara">Klára</a> sorozatot, a könnyű <a href="friss.html">FRISS és Berry Secco</a> borokat, a <a href="termek/piri-mama-forralt-bora.html">PIRI Mama forralt borokat</a>, a <a href="termek/don-cherry.html">Don Cherry meggyvermutot</a> és kisüsti <a href="palinka.html">pálinkáinkat</a> is megtalálod.</p></div></div></section>
</main>''' + footer(r)
    write('gyumolcsbor.html', pg)


def simple_list(path, title, desc, h1, lead, ids, bg, fg, kicker, photo=None, cur=''):
    r = ''
    pg = head(title, desc, r, path.split('.')[0]) + header(r, cur)
    ph = f'<div><img src="{photo}" alt="" loading="lazy"></div>' if photo else ''
    pg += f'''<main><section class="sec" style="background:{bg};color:{fg};padding-top:30px"><div class="wrap split"><div style="display:flex;flex-direction:column;gap:16px">
<p class="breadcrumb" style="color:inherit"><a href="index.html" style="color:inherit">Főoldal</a> / {h1}</p><p class="kicker" style="--accent:{fg}">{kicker}</p>
<h1 class="h2" style="font-size:clamp(44px,6vw,86px)">{h1}</h1><p class="lead">{lead}</p></div>{ph}</div></section>
<section class="sec"><div class="wrap">{cards(ids, r)}</div></section></main>''' + footer(r)
    write(path, pg)


# ---------- termékoldal ----------
def theme(p):
    L = p['line']
    if L == 'friss':
        return dict(page=p['arch'], ink=p['accent'], arch='rgba(255,255,255,.22)', accent=p['accent'], btn='#1B2A5C', hw=900)
    if L == 'klara':
        return dict(page='#FFFFFF', ink='#1B2A5C', arch=p['arch'], accent=p['accent'], btn='#1B2A5C', hw=500)
    if L == 'don':
        return dict(page='#FFFFFF', ink='#1B2A5C', arch='#5FB8B3', accent='#C8282E', btn='#C8282E', hw=800)
    if L == 'palinka':
        return dict(page='#F4EDE0', ink='#2A2118', arch=p['arch'], accent=p['accent'], btn='#2A2118', hw=700)
    if L == 'piri':
        return dict(page='#F3EEE5', ink='#1B2A5C', arch=p['arch'], accent=p['accent'] if p['accent'] != p['arch'] else '#EF4E73', btn='#1B2A5C', hw=900)
    return dict(page='#F3EEE5', ink='#1B2A5C', arch=p['arch'], accent=p['accent'], btn='#1B2A5C', hw=800)


def param(p, key):
    for k, v in p['params']:
        if k.lower().startswith(key.lower()):
            return v
    return None


def ingredients(p):
    m = re.search(r'Összetevők?:?\s*(.+)$', p['short'])
    return m.group(1).strip() if m else 'lásd a termék címkéjén'


STORY = {
    'klasszikus': ('GYÜMÖLCS', 'Jól behűtve, akár jéggel vagy szódával.', 'Édes borainkat az adott gyümölcs saját, 100%-os levével édesítjük, és csak annyi cukrot adunk hozzá, amennyi életre hívja a gyümölcs valódi karakterét. Kizárólag hazai idénygyümölccsel dolgozunk.'),
    'klara': ('KLÁRA', 'A gyümölcskertek istennője.', 'Olyan borokról álmodtunk, melyek egyszerre fejezik ki a gyümölcsök iránti rajongásunkat, a borkészítés iránti szenvedélyünket és a borászatunk otthona, az idilli-zöld Klárafalva iránt érzett szeretetünket. A közös metszet a felhőtlen természetesség, mely életre hívta a gyümölcskertek istennőjét, Klárát.'),
    'friss': ('FRISS', 'Pár szem jéggel, a naplementébe.', 'Könnyű, friss és kellemesen édes – baráti társaságba vagy egy nehéz nap után, egy szép pohárban.'),
    'secco': ('SECCO', 'Alaposan behűtve, jégkockával.', 'Kínáld piros gyümölcsökkel, vagy lime-mal és mentával – a buborékok kedvelőinek.'),
    'piri': ('FORRALT', 'Otthon csak melegíteni kell.', 'Vidd haza az adventi vásárok forralt bor hangulatát: bontsd ki, lassan melegítsd fel – ne forrald –, és már töltheted is. Felbontás után hűtőben tárolandó, 1 héten belül fogyasztandó.'),
    'don': ('DON', 'Klasszikus vagy meggy shot.', 'Klasszikus: tölts meg egy poharat jéggel, tegyél rá egy narancskarikát, és öntsd rá a 8 cl meggyvermutot. Meggy shot: egy 5 cl-es pohár aljára tegyél egy meggyszemet, önts rá 4 cl vermutot, és idd meg két kortyban.'),
    'palinka': ('PÁLINKA', 'Pincehidegen, a zamatok teljességéért.', 'Kisüsti módon készült, 46%-os pálinkák friss, érett gyümölcsből cefrézve – a gyümölcsös ágyas változatokban egy szem gyümölccsel a palackban.'),
}


BACK = {'klasszikus': 'gyumolcsbor.html', 'klara': 'gyumolcsbor.html#klara', 'piri': 'index.html', 'don': 'gyumolcsbor.html',
        'friss': 'friss.html', 'secco': 'friss.html', 'palinka': 'palinka.html'}


def product_designed(p):
    r = '../'
    res = pdp.TEMPLATES[p['line']](p)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p['name'], "image": p['img'], "description": p['short'],
          "brand": {"@type": "Brand", "name": "Kontyos"},
          "offers": {"@type": "Offer", "priceCurrency": "HUF", "price": p['price'], "availability": "https://schema.org/" + ("InStock" if p['avail'] else "OutOfStock")}}
    if p['rcount'] and p['rating']:
        ld["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": p['rating'], "reviewCount": p['rcount']}
    style = f'<style>:root{{--page:{res["page"]};--ink:{res["ink"]}}}</style><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    pg = head(f"{p['name']} – {LINE_LABEL[p['line']]} | Kontyos", p['short'][:155], r, 'product', 'pdp pdp-' + p['line'] + (' has-buybar' if res['bar'] else ''), style)
    pg += header(r, '', res['theme'], BACK.get(p['line'])) + '<main>' + res['html'] + '</main>' + res['bar'] + footer(r)
    write(f"termek/{p['id']}.html", pg)


def product(p):
    r = '../'
    if p['line'] in pdp.TEMPLATES:
        return product_designed(p)
    t = theme(p)
    L = p['line']
    is_pack = L in ('csomag', 'kiegeszito')
    img = p['img'] if is_pack else p['tight']
    sibs = [x for x in CAT if x['line'] == L and x['id'] != p['id']] if L not in ('kiegeszito',) else []
    chips = ''
    if L not in ('csomag', 'kiegeszito', 'palinka') and sibs:
        chips = '<nav class="chips" aria-label="Változatok">' + ''.join(
            f'<a class="chip" href="{x["id"]}.html"{" aria-current=page" if x["id"] == p["id"] else ""}><i style="background:{x["accent"] if x["accent"] not in ("#FFFFFF", "#FFF6EA") else x["arch"]}"></i>{e(x["name"].replace("Piri Mama ", "").replace("Klára ", ""))}</a>'
            for x in [y for y in CAT if y['line'] == L]) + '</nav>'
    badge = '<div class="badge">Azonnal<br>fogyaszt-<br>ható</div>' if L == 'piri' else ''
    rating = ''
    if p['rcount']:
        rating = f'<a class="stars" href="#ertekelesek"><span>{stars(p["rating"])}</span><span>{p["rating"]} · {p["rcount"]} értékelés</span></a>'
    alc = param(p, 'Alkohol')
    vol = param(p, 'Űrmérték')
    meta = ' · '.join(x for x in [vol, alc, param(p, 'Édes/Száraz')] if x)
    packs = ''
    if p['avail'] and p['tier'] and L not in ('csomag', 'kiegeszito', 'palinka'):
        em = ''
        if p['tier']:
            pct = round((1 - p['tier'][1] / p['price']) * 100)
            em = f'<em>−{pct}%</em>'
        packs = f'''<div class="packs" role="group" aria-label="Kiszerelés"><button type="button" data-pack="1" aria-pressed="true"><strong>1 palack</strong><span>{ft(p['price'])}/db</span></button>
<button type="button" data-pack="3" aria-pressed="false"><strong>3 palack</strong><span>{ft(p['price'])}/db</span></button>
<button type="button" data-pack="6" aria-pressed="false">{em}<strong>6 palack</strong><span>{ft(p['tier'][1] if p['tier'] else p['price'])}/db</span></button></div>'''
    old = f'<s style="opacity:.55;font-size:15px">{ft(p["old"])}</s>' if p.get('old') else ''
    if p['avail']:
        buy = f'''<div class="buyrow"><div class="price">{old}<b data-line>{ft(p['price'])}</b><small><span data-unit>{ft(p['price'])}</span>/db · bruttó{' · ' + param(p, 'Egységár') if param(p, 'Egységár') else ''}</small></div>
<div class="qty"><button type="button" data-dec aria-label="Kevesebb">−</button><span data-q id="q">1</span><button type="button" data-inc aria-label="Több">+</button></div>
<button class="btn add" type="button" data-add="{p['id']}" data-qty-from="#q">Kosárba</button></div>
<div class="free"><span data-free-text></span><div class="bar"><i data-free-bar style="width:0"></i></div></div>'''
        bar = f'''<div class="buybar"><div class="pb"><b data-line>{ft(p['price'])}</b><small><span data-q>1</span> db</small></div><div class="qty"><button type="button" data-dec aria-label="Kevesebb">−</button><span data-q>1</span><button type="button" data-inc aria-label="Több">+</button></div><button class="btn" type="button" data-add="{p['id']}" data-qty-from="#q">Kosárba</button></div>'''
    else:
        buy = '<div class="buyrow"><div class="price"><b>Elfogyott</b><small>Hamarosan újra elérhető</small></div><button class="btn ghost" type="button" disabled>Értesítést kérek</button></div>'
        bar = ''
    long = ''.join(f'<p>{e(x)}</p>' for x in p['long']) if p['id'] != 'meggymag-parna' else ''
    params = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in p['params'])
    legal = ''
    if L not in ('kiegeszito',):
        legal = f'''<div class="legalbox"><div class="in"><p class="kicker" style="margin-bottom:8px">Kötelező termékinformáció</p><dl class="kv">
<div><dt>Megnevezés</dt><dd>{e(p['name'])}</dd></div>
{f'<div><dt>Alkoholtartalom</dt><dd>{e(alc)}</dd></div>' if alc else ''}{f'<div><dt>Névleges térfogat</dt><dd>{e(vol)}</dd></div>' if vol else ''}
<div><dt>Összetevők, allergének</dt><dd>{e(ingredients(p))}</dd></div>
<div><dt>Előállító</dt><dd>Kontyos Borház Kft., 6773 Klárafalva, Kossuth u. 183.</dd></div>
<div><dt>Figyelmeztetés</dt><dd>18 éven aluliak részére alkoholtartalmú termék nem értékesíthető.</dd></div></dl></div></div>'''
    reviews = ''.join(f'<div class="review"><span class="s">★★★★★</span><p>„{e(x["t"])}”</p><small>{e(x["n"])} · {e(x["d"])}</small></div>' for x in p['reviews'])
    if not reviews:
        reviews = '<p class="muted">Még nincs értékelés – légy te az első! (Élesben: értékelés a vásárlás után e-mailben.)</p>'
    st = STORY.get(L)
    story = ''
    if st:
        vrow = ''
        if sibs:
            vrow = '<div class="vrow">' + ''.join(f'<a href="{x["id"]}.html"{" aria-current=page" if x["id"] == p["id"] else ""}><img src="{r}{x["tight"]}" alt="" loading="lazy"{' class="jar"' if x["id"] == "don-cherry-gyumolcse" else ""}><b>{e(x["name"].replace("Piri Mama ", "").replace("Klára ", ""))}</b></a>' for x in [y for y in CAT if y['line'] == L][:6]) + '</div>'
        sbg = {'friss': '#1B2A5C', 'don': '#5FB8B3', 'piri': p['arch'] if p['arch'] != '#F3EEE5' else '#2B3B78', 'palinka': '#2A2118', 'klara': '#F7F1F2'}.get(L, p['arch'])
        sfg = {'friss': p['arch'] if p['arch'] not in ('#D23C6E',) else '#FBD5D9', 'don': '#fff', 'piri': '#fff', 'palinka': '#E8D29A', 'klara': '#1B2A5C'}.get(L, '#1B2A5C')
        story = f'''<section class="story" style="--sbg:{sbg};--sfg:{sfg}"><p class="bigword" aria-hidden="true">{st[0]}</p><div class="wrap">
<div style="flex:1 1 380px;display:flex;flex-direction:column;gap:14px"><h2 class="h2">{e(st[1])}</h2><p class="lead">{e(st[2])}</p></div><div style="flex:1 1 380px">{vrow}</div></div></section>'''
    cross_ids = [x['id'] for x in sibs[:4]] or ['edes-meggybor', 'edes-eperbor', 'friss-malna', 'don-cherry']
    if len(cross_ids) < 4:
        cross_ids += [i for i in ['edes-meggybor', 'klara-edes-malnabor', 'friss-eper', 'don-cherry', 'meggy-paros'] if i != p['id'] and i not in cross_ids][:4 - len(cross_ids)]
    ship = f'''<dl class="ship"><div><dt>Szállítás</dt><dd>GLS futár / csomagpont, MPL automata / PostaPont · 1–5 munkanap, vagy személyes átvétel Klárafalván</dd></div><div><dt>Ingyenes szállítás</dt><dd>20 000 Ft felett (GLS házhoz 25 000 Ft felett)</dd></div><div><dt>Fizetés</dt><dd>Bankkártya (SimplePay), átutalás, utánvét (GLS)</dd></div></dl>'''
    desc = p['short'][:155]
    info_style = f'--ink:#1B2A5C;--accent:{p["accent"] if p["accent"] not in ("#FFFFFF", "#FFF6EA", "#1B2A5C") else "#EF4E73"};color:#1B2A5C'
    style = f'<style>:root{{--page:{t["page"]};--ink:{t["ink"]};--arch:{t["arch"]};--accent:{t["accent"]};--btn:{t["btn"]};--hw:{t["hw"]}}}</style>'
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p['name'], "image": p['img'], "description": p['short'],
          "brand": {"@type": "Brand", "name": "Kontyos"},
          "offers": {"@type": "Offer", "priceCurrency": "HUF", "price": p['price'], "availability": "https://schema.org/" + ("InStock" if p['avail'] else "OutOfStock")}}
    if p['rcount'] and p['rating']:
        ld["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": p['rating'], "reviewCount": p['rcount']}
    style += f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    pg = head(f"{p['name']} – {LINE_LABEL[L]} | Kontyos", desc, r, 'product', 'has-buybar' if p['avail'] else '', style)
    pg += header(r)
    crumb_cat = {'klasszikus': ('gyumolcsbor.html', 'Gyümölcsborok'), 'klara': ('gyumolcsbor.html#klara', 'Klára'), 'friss': ('friss.html', 'FRISS & Secco'),
                 'secco': ('friss.html', 'FRISS & Secco'), 'palinka': ('palinka.html', 'Pálinka'), 'csomag': ('karacsonyi-ajandek-bor.html', 'Csomagok')}.get(L, ('gyumolcsbor.html', 'Termékek'))
    pg += f'''<main><div class="wrap"><p class="breadcrumb" style="padding-top:4px;color:var(--ink)"><a href="{r}index.html" style="color:inherit">Főoldal</a> / <a href="{r}{crumb_cat[0]}" style="color:inherit">{crumb_cat[1]}</a> / {e(p['name'])}</p></div>
<section class="wrap p-hero"><div class="p-media"><div class="arch"><img class="{'pack' if is_pack else ('jar' if p['id'] == 'don-cherry-gyumolcse' else '')}" src="{r}{img}" alt="{e(p['name'])}" width="500" height="1400"></div>{badge}</div>
<div class="p-buy"><span class="kicker">{LINE_LABEL[L]}</span><h1>{e(p['name'])}</h1>{rating}
<p style="font-size:16px;line-height:1.6;opacity:.9">{e(p['short'])}</p>{f'<p style="font-size:13px;font-weight:700;opacity:.75">{e(meta)}</p>' if meta else ''}
{chips}{packs}<div data-buy="{p['id']}" style="display:flex;flex-direction:column;gap:16px">{buy}</div>{ship}{pdp.upsell(p)}</div></section>
{story}
<section class="p-info" style="{info_style}"><div class="wrap"><div class="desc"><h2 class="h2" style="font-size:36px">A termékről</h2><p>{e(p['short'])}</p>{long}</div>
<div class="side">{f'<dl class="kv">{params}</dl>' if params else ''}{legal}</div></div></section>
<section class="sec" id="ertekelesek" style="color:var(--ink)"><div class="wrap" style="display:flex;flex-direction:column;gap:22px"><h2 class="h2" style="font-size:40px">Értékelések{f' · {p["rating"]}' if p['rcount'] else ''}</h2><div class="reviews">{reviews}</div></div></section>
<section class="sec" style="background:#fff;color:#1B2A5C;--ink:#1B2A5C"><div class="wrap" style="display:flex;flex-direction:column;gap:22px"><h2 class="h2" style="font-size:40px">Ezt is szeretni fogod</h2>{cards(cross_ids, r)}</div></section>
</main>{bar if p['avail'] else ''}''' + footer(r)
    if not p['avail']:
        pg = pg.replace('data-buy=', 'data-nobuy=')
    write(f"termek/{p['id']}.html", pg)


# ---------- kampányoldalak ----------
def pack_card(s, r, active=True):
    imgs = ''.join(f'<img src="{r}{P[i]["tight"]}" alt="" loading="lazy">' for i in s['items'][:5])
    lis = ''.join(f'<li><a href="{r}{url(P[i])}">{e(P[i]["name"])}</a></li>' for i in s['items'])
    btn = f'<button class="btn pink block" type="button" data-add="{s["id"]}">Kosárba</button>' if active else '<button class="btn ghost block" type="button" data-waitlist>Szólj, ha indul</button>'
    return f'''<div class="pack-card"><div class="in"><div class="ph" style="--tint:{s['tint']}">{imgs}</div><h3>{e(s['name'])}</h3><ul>{lis}</ul>
<div class="pr"><b>{ft(s['price']) if active else '<span style="font-size:18px">Ár a kampány indulásakor</span>'}</b>{f"<s>{ft(s['old'])}</s>" if active else ''}</div>{'<small style="font-weight:700;color:#2E8C5A">Ingyenes szállítással</small>' if s['free'] and active else ''}{btn}</div></div>'''


def campaign(path, title, desc, h1, eyebrow, lead, bg, fg, acc, packs, bottles, phases=None, extra='', start='[DÁTUM]'):
    r = ''
    demo = ''
    if phases:
        demo = '<span class="seg">' + ''.join(f'<button type="button" data-phase-btn="{k}">{l}</button>' for k, l in phases) + '</span>'
    pg = head(title, desc, r, path.split('.')[0], demo_extra=demo) + header(r, 'black-friday.html' if 'black' in path else '')
    b = ''.join(hb(P[pid], r, 'clamp(240px,46vh,440px)', 0 if i == 0 else 6) for i, pid in enumerate(bottles))
    if phases:
        pre, act = phases[0][0], phases[1][0]
        body = f'''<div data-phase="{pre}"><section class="sec"><div class="wrap" style="display:flex;flex-direction:column;gap:22px;max-width:760px">
<h2 class="h2">Indul: {start}</h2><p class="lead">Iratkozz fel, és elsőként kapod meg az ajánlatokat.</p>
<form data-newsletter style="display:flex;gap:10px;flex-wrap:wrap"><label class="sr" for="wl">E-mail</label><input id="wl" type="email" required placeholder="E-mail címed" style="flex:1 1 240px;min-height:54px;border:1px solid #1B2A5C;border-radius:999px;padding:0 22px;font:inherit"><button class="btn pink" type="submit">Feliratkozom a várólistára</button></form></div></section>
<section class="sec" style="padding-top:0"><div class="wrap packs-grid">{''.join(pack_card(SP[i], r, False) for i in packs)}</div></section></div>
<div data-phase="{act}"><section class="sec"><div class="wrap" style="display:flex;flex-direction:column;gap:24px"><h2 class="h2">A csomagok</h2><div class="packs-grid">{''.join(pack_card(SP[i], r) for i in packs)}</div>
<p class="ph-note">Demó árak és összeállítás a designból – a végleges tartalmat és árat a Kontyos határozza meg.</p></div></section></div>'''
    else:
        body = f'''<section class="sec"><div class="wrap" style="display:flex;flex-direction:column;gap:24px"><h2 class="h2">A csomag</h2><div class="packs-grid">{''.join(pack_card(SP[i], r) for i in packs)}</div>
<p class="ph-note">Demó ár és összeállítás – a végleges tartalmat és árat a Kontyos határozza meg.</p></div></section>'''
    pg += f'''<main><section class="c-hero" style="--hbg:{bg};--hfg:{fg}"><div class="wrap row"><div style="flex:1 1 420px;display:flex;flex-direction:column;gap:18px;max-width:640px">
<p class="kicker" style="--accent:{acc}">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p></div><div class="bt">{b}</div></div></section>
{body}{extra}</main>''' + footer(r)
    write(path, pg)


# ---------- kosár, pénztár, köszönő, info ----------
def cart():
    r = ''
    pg = head('Kosár | Kontyos', 'Kosár', r, 'cart') + header(r)
    pg += f'''<main><div class="wrap" style="display:flex;flex-direction:column;gap:22px;padding-top:10px">
<ol class="steps"><li class="on">1 · Kosár</li><li>2 · Adatok</li><li>3 · Fizetés</li></ol><h1 class="h2">Kosár</h1>
<div class="cart-grid"><div class="cart-main"><div id="cart-root"></div>
<div style="display:flex;flex-direction:column;gap:14px"><h2 class="serif" style="font-size:26px">Tedd mellé</h2>{cards(['friss-malna', 'berry-secco', 'kontyos-borospohar', 'don-cherry-gyumolcse'], r)}</div></div>
<aside class="cart-side" id="cart-side"><div class="box" style="display:flex;flex-direction:column;gap:14px"><h2 class="serif" style="font-size:24px">Összesítő</h2>
<div class="tot"><div><span>Részösszeg</span><b data-sum>0 Ft</b></div><div><span>Szállítás</span><span data-shipfee>–</span></div><div class="grand"><span>Fizetendő</span><b data-grand>0 Ft</b></div></div>
<details class="coupon"><summary>Van kuponkódod?</summary><form data-coupon style="display:flex;gap:8px;margin-top:6px"><div class="field" style="flex:1"><input aria-label="Kuponkód" placeholder="KUPONKÓD"></div><button class="btn navy" type="submit">Beváltom</button></form><p data-coupon-msg class="muted" style="font-size:13px"></p></details>
<a class="btn pink block" href="penztar.html">Tovább a pénztárhoz →</a><div id="cart-ups" class="pd-ups"></div>
<p class="muted" style="font-size:12px;text-align:center">Biztonságos bankkártyás fizetés: SimplePay · 18+ termékek</p></div></aside></div></div></main>''' + footer(r)
    write('kosar.html', pg)


def checkout():
    r = ''
    pg = head('Pénztár | Kontyos', 'Pénztár', r, 'checkout') + header(r)
    ship_opts = [('mpl-automata', 'MPL csomagautomata', '1–5 munkanap · max. 20 kg · utánvét nem elérhető', 1800, 20000),
                 ('mpl-postapont', 'MPL PostaPont', '1–3 munkanap · közel 3000 átvételi pont · utánvét nem elérhető', 1800, 20000),
                 ('mpl-posta', 'MPL postán maradó csomag', '1–3 munkanap · utánvét nem elérhető', 1800, 20000),
                 ('gls-pont', 'GLS csomagpont', '3–5 munkanap · fizetés az átadó boltban is', 2100, 20000),
                 ('gls-haz', 'GLS házhozszállítás', '3–5 munkanap · max. 40 kg', 2400, 25000),
                 ('szemelyes', 'Személyes átvétel', 'A klárafalvi borászatnál – 6773 Klárafalva, Kossuth u. 183.', 0, 0)]
    pay_opts = [('kartya', 'Bankkártya', 'SimplePay – biztonságos online fizetés', 0),
                ('atutalas', 'Átutalás (előre utalás)', 'A visszaigazolásban küldjük az adatokat', 0),
                ('utanvet', 'Utánvét', 'Csak GLS-szel: készpénz vagy kártya a futárnak / az átadó boltban', 500)]

    def ship_html():
        return ''.join(f'<label class="opt"><input type="radio" name="ship" value="{e(t)}" data-fee="{fee}" data-free="{free}" data-key="{k}"{" checked" if i == 0 else ""}><span><b>{t}</b><small>{sub}{" · ingyenes " + ft(free) + " felett" if free else ""}</small></span><b>{ft(fee) if fee else "Ingyenes"}</b></label>' for i, (k, t, sub, fee, free) in enumerate(ship_opts))

    def pay_html():
        return ''.join(f'<label class="opt"><input type="radio" name="pay" value="{e(t)}" data-fee="{fee}" data-key="{k}"{" checked" if i == 0 else ""}><span><b>{t}</b><small>{sub}</small></span><b>{"+" + ft(fee) if fee else ""}</b></label>' for i, (k, t, sub, fee) in enumerate(pay_opts))

    def fld(name, label, cls, typ='text', req='1', ac=''):
        return f'<div class="field {cls}"><label for="f-{name}">{label}</label><input id="f-{name}" name="{name}" type="{typ}" {"data-req=" + chr(34) + req + chr(34) if req else ""} autocomplete="{ac}"><span class="msg">Kötelező mező</span></div>'
    pg += f'''<main><div class="wrap" style="display:flex;flex-direction:column;gap:22px;padding-top:10px">
<ol class="steps"><li class="done">✓ Kosár</li><li class="on">2 · Adatok</li><li>3 · Fizetés</li></ol><h1 class="h2">Pénztár</h1>
<div class="cart-grid"><div class="cart-main" id="checkout"><form id="co-form" novalidate style="display:flex;flex-direction:column;gap:20px">
<div class="box" style="display:flex;flex-direction:column;gap:14px"><h2 class="serif" style="font-size:24px">1. Elérhetőség</h2><div class="fgrid">
{fld('email', 'E-mail cím', 's3', 'email', '1', 'email')}{fld('phone', 'Telefonszám', 's3', 'tel', '1', 'tel')}</div>
<p class="muted" style="font-size:13px">Regisztráció nem szükséges – vendégként is rendelhetsz.</p></div>
<div class="box" style="display:flex;flex-direction:column;gap:14px"><h2 class="serif" style="font-size:24px">2. Szállítási cím</h2><div class="fgrid">
{fld('name', 'Teljes név', 's6', 'text', '1', 'name')}{fld('zip', 'Irányítószám', 's2', 'text', 'zip', 'postal-code')}{fld('city', 'Település', 's4', 'text', '1', 'address-level2')}{fld('street', 'Utca, házszám', 's6', 'text', '1', 'street-address')}</div>
<label class="check"><input type="checkbox" checked> A számlázási cím megegyezik a szállítási címmel</label></div>
<div class="box" style="display:flex;flex-direction:column;gap:10px"><h2 class="serif" style="font-size:24px">3. Szállítás</h2>{ship_html()}</div>
<div class="box" style="display:flex;flex-direction:column;gap:10px"><h2 class="serif" style="font-size:24px">4. Fizetés</h2>{pay_html()}<p class="note" data-cod-note hidden>Utánvét csak GLS szállítással választható.</p></div>
<div class="box" style="display:flex;flex-direction:column;gap:8px">
<div class="field"><label for="f-src">Honnan hallottál rólunk? (nem kötelező)</label><select id="f-src"><option value="">Válassz…</option><option>Google</option><option>Facebook / Instagram</option><option>Ismerős ajánlotta</option><option>Rendezvény, vásár</option><option>Egyéb</option></select></div>
<label class="check"><input type="checkbox" data-req-check> <span>Kijelentem, hogy elmúltam 18 éves. <small class="muted">(Alkoholtermék csak nagykorú részére értékesíthető; átvételkor a futár ellenőrizheti.)</small></span></label>
<label class="check"><input type="checkbox" data-req-check> <span>Elfogadom az <a href="info.html#aszf">ÁSZF</a>-et és az <a href="info.html#adatkezeles">adatkezelési tájékoztatót</a>.</span></label>
<label class="check"><input type="checkbox"> <span>Kérek hírlevelet (−5% a következő rendelésemből). Hozzájárulok, hogy a Kontyos Borház Kft. a nevemet és e-mail címemet hírlevelezési céllal kezelje, és gazdasági reklámot is tartalmazó hírleveleket küldjön.</span></label>
<p id="co-msg" role="alert" style="color:#C8284E;font-weight:700;font-size:14px"></p>
<button class="btn pink block" type="submit" style="min-height:60px;font-size:17px">Megrendelés elküldése (fizetési kötelezettséggel)</button>
<p class="note">Demó: a gomb nem indít valódi rendelést, csak a köszönőoldalt mutatja.</p></div></form></div>
<aside class="cart-side" id="co-summary"><div class="box" style="display:flex;flex-direction:column;gap:14px"><h2 class="serif" style="font-size:24px">Rendelésed</h2>
<div data-co-lines style="display:flex;flex-direction:column;gap:10px"></div>
<div class="free"><span data-free-left></span><div class="bar"><i data-free-bar></i></div></div>
<div class="tot"><div><span>Részösszeg</span><b data-sum></b></div><div><span>Szállítás</span><span data-shipfee></span></div><div data-codrow hidden><span>Utánvét díja</span><span>500 Ft</span></div><div class="grand"><span>Fizetendő</span><b data-grand></b></div></div>
<a href="kosar.html" style="font-size:13px">← Vissza a kosárhoz</a></div></aside></div></div></main>''' + footer(r)
    write('penztar.html', pg)


def thanks():
    r = ''
    pg = head('Köszönjük a rendelést! | Kontyos', 'Köszönjük', r, 'thanks') + header(r)
    pg += '''<main><div class="wrap" style="max-width:760px;padding-top:30px;padding-bottom:90px" id="thanks"><div class="label tag"><div class="in" style="display:flex;flex-direction:column;gap:16px;align-items:center;text-align:center">
<p class="kicker">Rendelés: <span data-o-no>DEMO</span></p><h1 class="h2">Köszönjük a rendelést!</h1>
<p class="lead">A visszaigazolást elküldtük ide: <b data-o-mail>–</b>. (Demó – valójában nem ment ki levél.)</p>
<div data-o-lines style="width:100%;text-align:left"></div>
<div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center"><a class="btn blue" href="index.html">Vissza a főoldalra</a><a class="btn ghost" href="gyumolcsbor.html">Gyümölcsborok</a></div></div></div></div></main>''' + footer(r)
    write('koszonjuk.html', pg)


def legal_html(lines):
    out = []
    for ln in lines:
        t = ln.strip()
        if not t:
            continue
        if len(t) < 90 and not t.endswith('.') and (t.endswith(':') or t.endswith('?') or len(t) < 60) and not re.match(r'^[a-z]{1,2}\)', t):
            out.append(f'<h4 style="margin:22px 0 6px;font-size:15px">{e(t)}</h4>')
        else:
            out.append(f'<p style="margin:0 0 10px;font-size:14px;line-height:1.7">{e(t)}</p>')
    return ''.join(out)


def info():
    r = ''
    lines = open(os.path.join(ROOT, 'src', 'content', 'aszf.txt'), encoding='utf-8').read().split('\n')
    k = next(i for i, l in enumerate(lines) if l.strip() == 'Adatkezelési tájékoztató')
    aszf, adat = lines[:k], lines[k + 1:]
    pg = head('Rólunk, szállítás, ÁSZF, adatkezelés | Kontyos', 'A Kontyos Borházról, szállítási díjak és határidők, törzsvásárlói program, ÁSZF és adatkezelési tájékoztató.', r, 'info') + header(r)
    sec = lambda i, h, body: f'<section id="{i}" style="padding:34px 0;border-bottom:1px solid var(--rule)"><h2 class="serif" style="font-size:36px;margin-bottom:14px">{h}</h2>{body}</section>'
    P_ = lambda t: f'<p class="lead" style="margin-bottom:12px">{t}</p>'
    pg += '<main><div class="wrap" style="max-width:900px;padding-bottom:80px"><p class="breadcrumb"><a href="index.html">Főoldal</a> / Információk</p><h1 class="h2" style="margin-top:10px">Vásárlási információk</h1>'
    pg += '<nav class="chips" style="margin-top:20px"><a class="chip" href="#rolunk">Rólunk</a><a class="chip" href="#szallitas">Szállítás</a><a class="chip" href="#torzsvasarlo">Törzsvásárlóknak</a><a class="chip" href="#kapcsolat">Kapcsolat</a><a class="chip" href="#aszf">ÁSZF</a><a class="chip" href="#adatkezeles">Adatkezelés</a></nav>'
    pg += sec('rolunk', 'Rólunk', P_('A Kontyos gyümölcsborászat tradicionális-kísérletező szellemiségű, hagyományos és reduktív eljárással dolgozó üzem, ahol közösségünk 2006 óta alkot elsőrangú hazai gyümölcsökből nyárillatú gyümölcsbor-különlegességeket.')
              + P_('Édesapánk közel két évtizede alkotta meg első gyümölcsborát. Az ötlet egy karácsonyi összejövetelen született: a család hölgy tagjai olyan italra vágytak, mely édes és zamatos, akár egy nyári gyümölcs. Kitartó kísérletezéssel addig tökéletesítette receptjét, míg megszületett az az eszményi különlegesség, mely igazán megfelel a gyümölcsös, friss ízeket kedvelők ízlésvilágának.')
              + P_('A 2019-ben épült modern üzemünk idilli természeti környezetben, egy Szegedhez közeli kis faluban, Klárafalván működik. Gyümölcsboraink 100%-ban magyar gyümölcsökből készülnek.')
              + '<h3 class="serif" style="font-size:24px;margin:22px 0 10px">Felelősségvállalás</h3><ul style="line-height:1.75;padding-left:20px">'
              + '<li><b>Tudatos fogyasztóknak:</b> édes borainkat az adott gyümölcs saját, 100%-os levével édesítjük, és csak annyi cukrot adunk hozzá, amennyi életre hívja a gyümölcs valódi karakterét.</li>'
              + '<li><b>Hazai gyümölcs:</b> nagy tételben vásárolunk hazai gazdáktól.</li>'
              + '<li><b>Szezonális gyümölcsök:</b> kizárólag idénygyümölcsökkel dolgozunk, a borokat helyben palackozzuk.</li>'
              + '<li><b>Tudatos fejlődés:</b> együttműködünk a Szőlészeti és Borászati Intézettel.</li></ul>')
    rows = [('GLS házhozszállítás', '3–5 munkanap', '2 400 Ft', '25 000 Ft felett', 'átutalás, utánvét (+500 Ft), bankkártya'),
            ('GLS csomagpont', '3–5 munkanap', '2 100 Ft', '20 000 Ft felett', 'átutalás, fizetés az átadó boltban (+500 Ft), bankkártya'),
            ('MPL csomagautomata', '3–5 munkanap', '1 800 Ft', '20 000 Ft felett', 'átutalás, bankkártya'),
            ('MPL PostaPont', '1–3 munkanap', '1 800 Ft', '20 000 Ft felett', 'átutalás, bankkártya'),
            ('MPL postán maradó', '1–3 munkanap', '1 800 Ft', '20 000 Ft felett', 'átutalás, bankkártya'),
            ('Személyes átvétel', '–', 'ingyenes', '–', 'a klárafalvi borászatnál')]
    tbl = '<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:14px;background:#fff;border-radius:6px"><thead><tr>' + ''.join(f'<th style="text-align:left;padding:12px;border-bottom:2px solid var(--navy)">{h}</th>' for h in ['Mód', 'Határidő*', 'Díj', 'Ingyenes', 'Fizetés']) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td style="padding:12px;border-bottom:1px solid var(--rule)">{c}</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table></div>'
    pg += sec('szallitas', 'Szállítás és fizetés', tbl + '<p class="muted" style="font-size:13px;margin-top:10px">*A megrendelés visszaigazolásától számítva. Bankkártyás fizetés: SimplePay by OTP. Csomagpont/automata: átvételi idő 3–5 nap, utána a csomag visszakerül a borászathoz. Nemzetközi (EU) szállítás egyedi ajánlat alapján: webshop@kontyos.hu.</p>'
              + P_('Ha a csomag sérülten érkezik, kérjük, ne vedd át, vegyetek fel jegyzőkönyvet a futárral, és jelezd a webshop@kontyos.hu címen – a hiányzó termékeket pótoljuk.'))
    pg += sec('torzsvasarlo', 'Törzsvásárlói program', P_('Regisztrált vásárlóink a teljesített rendelések összértéke alapján automatikusan törzsvásárlóvá válnak, és belépés után a kedvezményes árakat látják:')
              + '<ul style="line-height:1.9;padding-left:20px;font-size:16px"><li><b>Bronz</b> – 30 000 Ft-tól: 5%</li><li><b>Silver</b> – 60 000 Ft-tól: 10%</li><li><b>Gold</b> – 100 000 Ft-tól: 15%</li><li><b>Kontyos VIP</b> – 300 000 Ft-tól: különleges, személyes élmény</li></ul>'
              + P_('A csomagkedvezmények, a mennyiségi árkedvezmény és a kuponos akciók mellette is érvényesek.'))
    pg += sec('kapcsolat', 'Kapcsolat és céginformációk', '<dl class="kv">' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in [
        ('Cégnév', 'Kontyos Borház Kft.'), ('Székhely', '6773 Klárafalva, Kossuth u. 183.'), ('Telefon', '<a href="tel:+36203492185">+36-20/349-2185</a>'),
        ('E-mail', '<a href="mailto:info@kontyos.hu">info@kontyos.hu</a> · webshop: <a href="mailto:webshop@kontyos.hu">webshop@kontyos.hu</a>'),
        ('Adószám', '23503016-2-06'), ('Cégjegyzékszám', '06-09-017653'), ('NÉBIH eng. szám', '330-07-KüE-1263'), ('Tárhelyszolgáltató', 'ShopRenter.hu Kft.')]) + '</dl>')
    pg += sec('aszf', 'Általános Szerződési Feltételek', '<p class="muted" style="margin-bottom:12px">A kontyos.hu-n jelenleg érvényes ÁSZF szövege.</p><details class="faq"><summary>Teljes ÁSZF megnyitása</summary><div style="padding:6px 0 10px">' + legal_html(aszf) + '</div></details>')
    pg += sec('adatkezeles', 'Adatkezelési tájékoztató', '<details class="faq"><summary>Teljes adatkezelési tájékoztató megnyitása</summary><div style="padding:6px 0 10px">' + legal_html(adat) + '</div></details>')
    pg += '</div></main>' + footer(r)
    write('info.html', pg)


def main():
    global VER
    pdp.bind(e=e, ft=ft, param=param, ingredients=ingredients, P=P, CAT=CAT, url=url, LINE_LABEL=LINE_LABEL)
    write_catalog_js()
    import hashlib
    h = hashlib.sha1()
    for f in ('assets/style.css', 'assets/app.js', 'assets/catalog.js'):
        h.update(open(os.path.join(ROOT, f), 'rb').read())
    for dp, dn, fn in sorted(os.walk(os.path.join(ROOT, 'img'))):
        for f in sorted(fn):
            st = os.stat(os.path.join(dp, f)); h.update(f'{f}{st.st_size}{int(st.st_mtime)}'.encode())
    VER = h.hexdigest()[:10]
    index()
    category()
    simple_list('friss.html', 'FRISS gyümölcsbor és Berry Secco | Kontyos', 'Könnyű, színes FRISS gyümölcsborok és Berry Secco 2190 Ft-tól.', 'FRISS & Berry Secco',
                'Könnyű, gyümölcsös, hűtve az igazi.', [p['id'] for p in CAT if p['line'] in ('friss', 'secco')], '#F28C28', '#1B2A5C', 'Könnyű borok', 'img/photo/friss_flat.webp')
    simple_list('palinka.html', 'Gyümölcspálinka | Kontyos', 'Szamóca-, meggy-, birs-, körte- és szilvapálinka a Kontyostól.', 'Pálinka',
                'Gyümölcspálinkák a Kontyos Borháztól.', [p['id'] for p in CAT if p['line'] == 'palinka'], '#2A2118', '#E8D29A', 'Párlatok', None, 'palinka.html')
    for p in CAT:
        product(p)
    campaign('ujbor-valogatas.html', 'Újbor-válogatás 2026 | Kontyos', 'Az idei gyümölcsborok válogatásban, ingyenes szállítással.', 'Újbor-válogatás', 'Limitált · nov. 5–23.',
             '6 klasszikus gyümölcsbor egy dobozban – ingyenes szállítással.', '#F6E1E4', '#1B2A5C', '#EF4E73', ['ujbor-valogatas'],
             ['edes-eperbor', 'edes-meggybor', 'edes-ribizlibor', 'edes-kajszibor'])
    bf_page()
    xmas_page()
    cart()
    search_page()
    fairs_page()
    checkout()
    thanks()
    info()
    print('OK', len(CAT), 'termék')


if __name__ == '__main__':
    main()
