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

# ---- Sanyi szövegei (2026-11-02) ----
TXT = dict(
    friss1='Gyümölcsbor és almabor. Frissítő harmóniában.',
    friss2='Gyümölcsbor és almabor könnyed találkozása. Kétféle gyümölcsbor, egy friss élmény.',
    friss_pd='A FRISS borainkban a gyümölcsbor és az almabor fele-fele arányban találkozik. A gyümölcsök gazdag íze az almabor üdeségével párosul, így egy könnyed, kellemesen gyümölcsös ital születik. Ideális választás baráti összejövetelekhez, nyári estékre vagy egy kis kikapcsolódáshoz.',
    klassz1='A KONTYOS klasszikus gyümölcsborai 100%-ban az adott gyümölcsből erjesztett borok. Gazdag, karakteres ízüket a felhasznált gyümölcsök adják.',
    klassz2='Eper, meggy vagy sárgabarack? Klasszikus gyümölcsboraink kizárólag az adott gyümölcsből erjesztett borok. Így minden kortyban az adott gyümölcs gazdag, karakteres íze érvényesül.',
    klassz_pd='A KONTYOS klasszikus gyümölcsborai kizárólag az adott gyümölcsből készített borok. Az eper, a meggy, a málna, a feketeribizli vagy a barack sajátos íze és zamata minden kortyban érezhető. Gazdag, gyümölcsös ízvilágukkal kiválóan illenek az ünnepi alkalmakhoz vagy egy nyugodt estéhez.',
    klara1='A KLÁRA sorozat válogatott gyümölcsökből készült borai elegáns megjelenésükkel ajándéknak és különleges alkalmakra is tökéletesek.',
    klara_pd='A KLÁRA a KONTYOS prémium gyümölcsborainak sorozata, amelyben a gondosan válogatott gyümölcsök és a különleges borkészítési eljárások találkoznak. A málna gazdag ízvilága, a rozé eper könnyed eleganciája, az áfonya mélysége és a barrique meggy karakteres zamata különböző élményeket kínál. Az elegáns csomagolásnak köszönhetően a KLÁRA borok ajándéknak és ünnepi alkalmakra is kiváló választások.',
)
for _p in CAT:
    _L = _p['line']
    _pd = {'friss': TXT['friss_pd'], 'klasszikus': TXT['klassz_pd'], 'klara': TXT['klara_pd']}.get(_L)
    if _pd:
        _p['long'] = [_pd] + [x for x in _p['long'] if x != _pd]
    # Sanyi: MINDEN bor 2026-os évjárat (a vermut és a pálinka nem évjáratos)
    if _L in ('klasszikus', 'klara', 'friss', 'secco', 'piri'):
        _p['params'] = [(k, v) for k, v in _p['params'] if not k.startswith('Évj')] + [('Évjárat', '2026')]
LIMIT = 20000
VER = 'dev'
e = lambda s: html.escape(str(s), quote=True)


def ft(n):
    return f"{int(round(n)):,}".replace(',', ' ') + ' Ft'


LINE_LABEL = {'klasszikus': 'Klasszikus gyümölcsbor', 'klara': 'Klára prémium', 'friss': 'FRISS gyümölcsbor',
              'secco': 'Berry Secco', 'piri': 'PIRI Mama forralt bor', 'don': 'Don Cherry', 'palinka': 'Pálinka',
              'csomag': 'Válogatás', 'kiegeszito': 'Kiegészítő', 'szezon': 'Szezonális csomag'}

# Szezonális (demó) csomagok – árak a designból, tartalom javaslat
UJBOR6 = ['edes-meggybor', 'edes-eperbor', 'edes-ribizlibor', 'edes-kajszibor', 'edes-oszibarackbor', 'edes-szilvabor']
SEASON_PACKS = [
    # Újbor: 6 klasszikus (100%-os) gyümölcsbor, a 6 palackos mennyiségi áron – demó összeállítás, a végleges tartalmat a Kontyos adja
    dict(id='ujbor-valogatas', name='Újbor-válogatás – 6 palack', price=sum(P[i]['tier'][1] for i in UJBOR6), old=sum(P[i]['price'] for i in UJBOR6), free=True,
         items=UJBOR6, tint='#F6E1E4'),
    dict(id='bf-premium', name='Black Friday Prémium', price=19900, old=26840, free=True,
         items=['edes-meggybor', 'edes-ribizlibor', 'klara-edes-malnabor', 'berry-secco', 'piri-mama-forralt-bora', 'don-cherry'], tint='#F3EEE5'),
    dict(id='bf-mini', name='Black Friday Mini', price=9900, old=13140, free=False,
         items=['friss-eper', 'friss-malna', 'friss-meggy'], qty=2, tint='#FBE3D2'),
    dict(id='edes-unnepek', name='Édes Ünnepek Borcsomag', price=19900, old=24840, free=True,
         items=['edes-eperbor', 'edes-meggybor', 'edes-oszibarackbor', 'edes-bodza-almabor', 'berry-secco', 'don-cherry'], tint='#FBE3E6', tag='FŐ AJÁNLAT'),
    dict(id='premium-advent', name='Prémium adventi borválogatás', price=28900, old=36040, free=True,
         items=['edes-eperbor', 'edes-ribizlibor', 'edes-kajszibor', 'edes-szilvabor', 'klara-edes-malnabor', 'don-cherry', 'don-cherry-gyumolcse', 'meggymag-parna'], tint='#EFE6D2', tag='PRÉMIUM AJÁNDÉK'),
    dict(id='konnyu-karacsony', name='Könnyű Karácsonyi Borcsomag', price=10900, old=13140, free=False,
         items=['friss-eper', 'friss-malna', 'friss-meggy', 'berry-secco-tonic', 'berry-secco-yuzu-lime', 'piri-mama-forralt-bora'], tint='#FFE8CF', tag='KISEBB KERETBŐL'),
    # Don Cherry csomagok (Sanyi: kicsi = 1 vermut + 1 meggy, nagy = 2 vermut + 1 meggy + 2 tonik) – ár: demó, a palackárak összege
    dict(id='don-kis', name='Don Cherry kis csomag', price=P['don-cherry']['price'] + P['don-cherry-gyumolcse']['price'], old=None, free=False,
         items=['don-cherry', 'don-cherry-gyumolcse'], tint='#D9EEF0', tag='KIS CSOMAG'),
    dict(id='don-nagy', name='Don Cherry nagy csomag', price=2 * P['don-cherry']['price'] + P['don-cherry-gyumolcse']['price'], old=None, free=False,
         items=['don-cherry', 'don-cherry', 'don-cherry-gyumolcse'], extra='2 × tonik [a Kontyos választja]', tint='#D9EEF0', tag='NAGY CSOMAG'),
]
# Forralt csomag (Sanyi, 11-03): 6 db forralt bor – javasolt összetétel: 4 narancsos + 1 klasszikus + 1 epres; ár: demó (palackárak összege), a Kontyos véglegesíti
FORRALT6 = ['narancsos-piri-mama-forralt-bora'] * 4 + ['piri-mama-forralt-bora', 'epres-piri-mama-forralt-bora']
SEASON_PACKS.append(dict(id='forralt-6', name='PIRI Mama forralt csomag – 6 palack', price=sum(P[i]['price'] for i in FORRALT6), old=None, free=True,
                         items=FORRALT6, tint='#FBE0CC', tag='FORRALT CSOMAG'))
SP = {s['id']: s for s in SEASON_PACKS}

# ---- Termék-jelvények (Sanyi, 2026-11-02): ÚJ, LIMITÁLT, −x% / LEGJOBB ÉRTÉK ----
NEW_IDS = {'friss-narancs', 'narancsos-piri-mama-forralt-bora', 'don-kis', 'don-nagy'}
LIMITED_IDS = {'piri-mama-bogreje'}
_pk = [x for x in CAT if x['line'] == 'csomag' and x.get('old')]
BEST_VALUE = max(_pk, key=lambda x: x['old'] - x['price'])['id'] if _pk else None   # a legnagyobb forint-megtakarítás


def badge(pid):
    """Kis jelvény a termék képe fölé – kártyán, ajánlóban, termékoldalon ugyanaz."""
    if pid in NEW_IDS:
        return '<span class="pbadge new">ÚJ</span>'
    if pid in LIMITED_IDS:
        return '<span class="pbadge lim">LIMITÁLT</span>'
    x = P.get(pid)
    if x and x['line'] == 'csomag' and x.get('old'):
        pct = round((1 - x['price'] / x['old']) * 100)
        if pid == BEST_VALUE:
            return f'<span class="pbadge gold">LEGJOBB ÉRTÉK · −{pct}%</span>'
        return f'<span class="pbadge pct">−{pct}%</span>'
    return ''


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
        page = ('ujbor-valogatas.html' if s['id'] == 'ujbor-valogatas' else 'black-friday.html' if s['id'].startswith('bf')
                else 'termek/don-cherry.html' if s['id'].startswith('don-') else 'csomagok.html' if s['id'] == 'forralt-6' else 'karacsonyi-ajandek-bor.html')
        out[s['id']] = dict(n=s['name'], price=s['price'], tier=None, img=first['img'], url=page,
                            sub=f"{len(s['items'])} tétel · szezonális csomag", tint=s['tint'], free=s['free'], ups=['kontyos-borospohar', 'kontyos-szovettaska', 'don-cherry-gyumolcse'])
    js = '/* generálva: src/build.py */\nwindow.KONTYOS={p:' + json.dumps(out, ensure_ascii=False) + '};\n'
    open(os.path.join(ROOT, 'assets', 'catalog.js'), 'w', encoding='utf-8').write(js)


# ---------- közös elemek ----------
NAV = [('gyumolcsbor.html', 'Gyümölcsborok', ''), ('termek/piri-mama-forralt-bora.html', 'Forralt borok', ''),
       ('termek/don-cherry.html', 'Don Cherry', ''), ('termek/berry-secco.html', 'Berry Secco', ''),
       ('palinka.html', 'Pálinkák', ''), ('csomagok.html', 'Ajándék és csomagok', 'sale')]


def head(title, desc, r, page='', body_cls='', extra_style='', demo_extra='', topbar=''):
    return f'''<!doctype html>
<html lang="hu" data-root="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" type="image/png" href="{r}img/kontyos-ikon-48.png?v=k3"><link rel="apple-touch-icon" href="{r}img/kontyos-ikon-180.png?v=k3">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="{r}assets/fonts/PrataHU-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Montserrat:wght@400..800&display=swap" rel="stylesheet">
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
<a class="logo" href="{r}index.html" aria-label="Kontyos – főoldal"><img class="lb" src="{r}img/logo-navy.svg" alt="Kontyos" width="154" height="38"><img class="lw" src="{r}img/logo-white.svg" alt="" aria-hidden="true" width="154" height="38"><img class="lg" src="{r}img/logo-gold.svg" alt="" aria-hidden="true" width="154" height="38"></a>
<nav class="nav" aria-label="Fő menü">{links}</nav>
<a class="cart-btn" href="{r}kosar.html" aria-label="Kosár"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 7h14l-1.5 12h-11z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg><span class="lbl">Kosár</span> <span data-cart-count>0</span></a>
</div></header>
<div class="drawer" id="drawer"><nav aria-label="Mobil menü"><button class="close" type="button" data-menu-close aria-label="Bezárás">×</button>
<a href="{r}index.html">Főoldal</a>{dlinks}<a href="{r}friss.html">FRISS</a><a href="{r}info.html">Szállítás & ÁSZF</a></nav></div>
'''


def footer(r):
    return f'''<footer class="site-foot"><div class="wrap">
<div class="brand"><span class="logo"><img class="lb" src="{r}img/logo-navy.svg" alt="Kontyos" width="210" height="52"><img class="lw" src="{r}img/logo-white.svg" alt="" aria-hidden="true" width="210" height="52"></span><p style="margin-top:14px;max-width:340px;font-size:14px">100%-os gyümölcsborok a klárafalvi Kontyos Borháztól.</p></div>
<div><h4>Termékek</h4><a href="{r}gyumolcsbor.html">Gyümölcsborok</a><a href="{r}friss.html">FRISS</a><a href="{r}termek/berry-secco.html">Berry Secco</a><a href="{r}termek/piri-mama-forralt-bora.html">PIRI Mama forralt bor</a><a href="{r}termek/don-cherry.html">Don Cherry</a><a href="{r}palinka.html">Pálinka</a></div>
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
<div class="ph" style="--tint:{t}">{badge(p['id'])}<img src="{r}{p['img']}" alt="{e(p['name'])}" loading="lazy" width="500" height="500"></div>
<div class="tx"><span class="k">{LINE_LABEL[p['line']]}</span><span class="n">{e(p['name'])}</span>
<div class="row"><span class="pr">{old}{pr}</span></div></div></a>
<div style="position:absolute;right:16px;bottom:14px">{plus}</div></div>'''


def cards(ids, r, cls='cards'):
    return f'<div class="{cls}">' + ''.join(card(P[i], r) for i in ids) + '</div>'


def hb(p, r, h, ml=0, rot='0deg'):
    h = h.replace('vh', 'svh')  # iOS-en a vh a teljes (sáv nélküli) magasság – az svh a ténylegesen látható
    return f'''<div class="hb" style="--h:{h};margin-left:{ml}px"><div class="hbi"><span class="hbr" style="transform:rotate({rot})"><img src="{r}{p['tight']}" alt="{e(p['name'])}">
<a class="hbl" href="{r}{url(p)}" aria-label="{e(p['name'])} – termékoldal"></a></span>
<div class="hw"><div class="in">{badge(p['id']).replace('pbadge', 'pbadge inl')}<span class="n">{e(p['name'])}</span><span class="p">{ft(p['price'])}</span><button type="button" data-add="{p['id']}">Kosárba</button></div></div>
<button class="hbp" type="button" data-add="{p['id']}" aria-label="{e(p['name'])} kosárba">+</button></div></div>'''


STAMP = '''<div class="stamp" aria-hidden="true"><svg viewBox="0 0 200 200" width="168" height="168"><defs><path id="sc-{uid}" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
<circle cx="100" cy="100" r="98" fill="{bg}"/><text font-family="Montserrat" font-weight="800" font-size="14" fill="{fg}"><textPath href="#sc-{uid}" textLength="489" lengthAdjust="spacing">{txt}</textPath></text></svg><b style="color:{fg}">{center}</b></div>'''


def write(path, s):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if path.endswith('.html'):
        s = re.sub(r'(img/[\w./-]+\.(?:webp|png))(?=["\)\s])', lambda m: m.group(1) + '?v=' + VER, s)
    open(full, 'w', encoding='utf-8').write(s)


# ---------- főoldal ----------
SEASONS = [
    dict(k='forralt', lbl='Forralt szezon', bg='#F08A3C', fg='#1B2A5C', word='FORRALT BOR', wf='calc((100vw - 64px) / 7.9)', deco=('flake-blue', 'flake-gold', 'holly', 'snow-dots'), hword='#1B2A5C', acc='#1B2A5C', ctafg='#FFFFFF',
         stampbg='#1B2A5C', stampfg='#F3C66B', stamp='CSAK MEGMELEGÍTED ÉS KÉSZ · PIRI MAMA · ',
         bottles=[('piri-mama-forralt-bora', 'clamp(280px,50vh,430px)', '-9deg'), ('narancsos-piri-mama-forralt-bora', 'clamp(330px,60vh,520px)', '4deg'), ('epres-piri-mama-forralt-bora', 'clamp(270px,49vh,420px)', '12deg')],
         ml=64, eyebrow='Új · Narancsos PIRI Mama', t='Csak megmelegíted, és kész.', s='Narancsos, fűszeres forralt gyümölcsbor egyliteres palackban – azonnal fogyasztható.',
         cta=('PIRI Mama forralt borok', 'termek/narancsos-piri-mama-forralt-bora.html'), price=None),
    dict(k='ujbor', lbl='Újbor', bg='#F6E1E4', fg='#1B2A5C', word='ÚJBOR', hword='#D7263D', acc='#EF4E73', ctafg='#fff',
         bottles=[(i, 'clamp(240px,46vh,440px)', f'{d}deg') for i, d in zip(UJBOR6, (-8, -3, 2, -2, 3, 8))], ml=-26, fruit=True,
         eyebrow='Limitált · nov. 5–23.', t='Kóstold meg az új borainkat!', s='Az idei gyümölcs, palackban – válogass a 100%-os klasszikus gyümölcsborainkból, vagy vidd mind a hatot.',
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


def falling(r, kinds, n=22, seed=3):
    """A PIRI landing mozgó grafikai elemei (hópihe, magyal-levél, arany dísz) – lassan hulló réteg."""
    import random
    rnd = random.Random(seed)
    out = ''
    for i in range(n):
        k = kinds[i % len(kinds)]
        w = rnd.uniform(22, 50) if k != 'snow-dots' else rnd.uniform(34, 60)
        out += (f'<img src="{r}img/deco/{k}.svg" alt="" style="left:{rnd.uniform(0, 98):.1f}%;width:{w:.0f}px;'
                f'--dur:{rnd.uniform(11, 22):.1f}s;--delay:-{rnd.uniform(0, 22):.1f}s;--drift:{rnd.choice((-1, 1)) * rnd.uniform(20, 70):.0f}px;--o:{rnd.uniform(.55, .95):.2f}"'
                f'{" class=d" if i > 12 else ""}>')
    return f'<div class="fall" aria-hidden="true">{out}</div>'


# A régi forralt bor alap címkék állatai (Sanyi, 2026-11-02) – ideiglenes kivágás, Bandi végleges kivágására cseréljük
ANIMALS = '<div class="animals" aria-hidden="true"><img class="an cinege" src="{r}img/deco/allat-cinege.png" alt=""></div>'


def season_hero(s, r):
    b = ''.join(hb(P[bt[0]], r, bt[1], 0 if i == 0 else s.get('ml', 4), bt[2] if len(bt) > 2 else '0deg') for i, bt in enumerate(s['bottles']))
    price = ''
    if s['price']:
        pp = price_of(s['price'][0])
        old = f'<s>{ft(pp["old"])}</s>' if pp.get('old') else ''
        price = f'<div class="price"><div class="in">{old}<b>{ft(pp["price"])}</b><small>{s["price"][1]}</small></div></div>'
    return f'''<section class="hero{' has-fruit' if s.get('fruit') else ''}" data-season="{s['k']}" style="--hbg:{s['bg']};--hfg:{s['fg']};--hword:{s['hword']};--haccent:{s['acc']};--hctafg:{s['ctafg']}">
{fruit_burst(r, 18, 5) if s.get('fruit') else ''}{falling(r, s['deco']) if s.get('deco') else ''}{ANIMALS.format(r=r) if s['k'] == 'forralt' else ''}<p class="word" aria-hidden="true"{f' style="--wfx:{s["wf"]}"' if s.get('wf') else ''}>{s['word']}</p>
<div class="bottles">{b}</div>
{STAMP.format(bg=s.get('stampbg', s['acc']), fg=s.get('stampfg', s['ctafg']), txt=s.get('stamp', '100% GYÜMÖLCSBŐL · KLÁRAFALVA · KONTYOS · '), uid=s['k'], center='100%')}
<div class="copy"><div class="wrap"><div class="txt"><span class="eyebrow">{s['eyebrow']}</span><p class="t">{s['t']}</p><p class="s">{s['s']}</p><a class="btn" href="{r}{s['cta'][1]}">{s['cta'][0]} →</a></div>
{price}</div></div>
</section>'''


FRUITS = ['edes-meggybor', 'edes-eperbor', 'edes-ribizlibor', 'edes-kajszibor', 'edes-oszibarackbor', 'edes-szilvabor', 'edes-bodza-almabor', 'szaraz-meggybor']


def fruit_selector(r, ids=None):
    ids = ids or FRUITS
    def nm(p):
        return p['name'].replace('Édes ', '').replace('bor', 'bor').capitalize()
    items = ''
    for i, pid in enumerate(ids):
        p = P[pid]
        items += (f'<a href="{r}{url(p)}" data-fruit data-id="{pid}" data-img="{r}{p["tight"]}" data-tint="{p["arch"]}" data-bg="{p["arch"]}" '
                  f'data-ink="{p["accent"]}" data-name="{e(p["name"])}" data-k="{LINE_LABEL[p["line"]]}" data-line="{e(p["short"][:150].rsplit(" ", 1)[0])}…" '
                  f'data-price="{ft(p["price"])}" style="--fc:{p["accent"]}" aria-current="{"true" if i == 0 else "false"}">{e(p["name"])}<small>{ft(p["price"])}</small></a>')
    p = P[ids[0]]
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


def don_packs(r, title='Don Cherry csomagban', sub='Ajándékba vagy a hétvégére – a vermut és a párja egy dobozban.', dark=False):
    """Kis és nagy Don Cherry csomag (Sanyi: kicsi = 1 vermut + 1 meggy, nagy = 2 vermut + 1 meggy + 2 tonik)."""
    cardsh = ''
    for pid in ('don-kis', 'don-nagy'):
        sp = SP[pid]
        imgs = ''.join(f'<img src="{r}{P[i]["tight"]}" alt="{e(P[i]["name"])}" loading="lazy"{" class=jar" if i == "don-cherry-gyumolcse" else ""}>' for i in sp['items'])
        cardsh += f'''<article class="dpk"><div class="ph">{badge(pid)}{imgs}</div><div class="tx"><p class="k">{sp['tag']}</p><h3>{e(sp['name'])}</h3>
<p class="ct">{e(pack_contents(sp))}</p><div class="row"><b>{ft(sp['price'])}</b><button type="button" class="btn" style="background:#C8282E" data-add="{pid}">Kosárba</button></div></div></article>'''
    return f'''<section class="dpacks{' dark' if dark else ''}"><div class="wrap"><div class="hd"><p class="kicker" style="--accent:#C8282E">Don Cherry</p><h2 class="h2">{title}</h2><p class="lead">{sub}</p></div>
<div class="grid">{cardsh}</div><p class="ph-note">Demó: az ár a palackárak összege, a tonik típusát és a végleges árat a Kontyos adja.</p></div></section>'''


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


def choose_tiles(r, title='Nem tudtál választani?', sub='Böngéssz tovább a borházban.'):
    """Egyforma, kattintható kategória-csempék (Sanyi) – a csoportképeket Bandi készíti, addig a meglévő fotók."""
    tiles = [('100%-os gyümölcsborok', 'gyumolcsbor.html#klasszikus', 'meggy_hangulat.webp'), ('Klára prémium', 'gyumolcsbor.html#klara', 'klara.webp'),
             ('FRISS – könnyű', 'friss.html', 'friss_csalad.webp'), ('Forralt borok', 'termek/piri-mama-forralt-bora.html', 'piri_fa.webp'),
             ('Don Cherry', 'termek/don-cherry.html', 'don_life.webp')]
    t = ''.join(f'<a href="{r}{h}"><img src="{r}img/photo/{im}" alt="" loading="lazy"><span>{n} →</span></a>' for n, h, im in tiles)
    return f'''<section class="choose"><div class="wrap"><div class="hd"><h2 class="h2">{title}</h2><p class="lead">{sub}</p></div><div class="ctiles">{t}</div>
<p class="ph-note">A csempék képei helyére Bandi csoportképei kerülnek.</p></div></section>'''


FIRS = ''.join(f'<svg class="fir" style="left:{x}%;bottom:{b}px;height:{h}px" viewBox="0 0 60 100" aria-hidden="true"><path d="M30 0 L48 34 H40 L56 62 H44 L60 90 H0 L16 62 H4 L20 34 H12 Z" fill="{c}"/><rect x="26" y="90" width="8" height="10" fill="#4A2A1A"/></svg>'
               for x, b, h, c in [(2, 0, 230, '#0F3B2A'), (9, 0, 160, '#145238'), (86, 0, 250, '#0F3B2A'), (93, 0, 170, '#145238'), (79, 0, 120, '#1B6646')])
SNOW = ''.join(f'<i style="left:{(i * 37) % 100}%;top:{(i * 53) % 90}%;--s:{2 + i % 4}px;animation-delay:-{i % 7}s"></i>' for i in range(46))


def bf_landing(r, phase, htag='h1', uid='bf'):
    """Black Friday (Sanyi): feketébb, pink kiemeléssel; hero a Don Cherry, alatta csak a két csomag. Mini + Prémium, max. 40 csomag."""
    wait = phase == 'varolista'
    eyebrow = 'NOV. 23–29. · HAMAROSAN' if wait else 'NOV. 23–29. · MOST FUT · <span data-countdown="2026-11-29T23:59:59+01:00"></span>'
    note = 'Iratkozz fel, és elsőként szólunk.' if wait else 'Nov. 29-ig, vagy amíg a készlet tart.'
    prem, mini = SP['bf-premium'], SP['bf-mini']

    def cta(sp, primary):
        if wait:
            return f'<a class="btn {"pink" if primary else "ghost"} block" href="#bf-wait-{uid}">Értesítést kérek</a>'
        return f'<button class="btn {"pink" if primary else "ghost"} block" type="button" data-add="{sp["id"]}">Kosárba teszem</button>'

    def box(sp, big, tag, extra=''):
        pct = round((1 - sp['price'] / sp['old']) * 100)
        return f'''<article class="bfx{' big' if big else ''}"><div class="top" style="--tint:{'#EF4E73' if big else '#2A2A33'}">
<div class="tagrow"><span>{tag}</span><span>−{pct}%</span></div><h2>{e(sp['name'])}</h2>
<div class="ph">{pack_bottles(sp, r)}</div><p class="ct">{e(pack_contents(sp))}</p>{extra}</div>
<div class="pr"><s>{ft(sp['old'])}</s><b>{ft(sp['price'])}</b><em>{'INGYENES SZÁLLÍTÁS' if sp['free'] else '+ szállítási díj'}</em></div>
<p class="stock">Elérhető: max. 40 csomag</p>{cta(sp, big)}</article>'''
    b = hb(P['don-cherry'], r, 'clamp(360px,70vh,640px)', 0, '-6deg') + hb(P['don-cherry-gyumolcse'], r, 'clamp(200px,38vh,340px)', 6, '8deg')
    out = f'''<section class="hero lp-bf" style="--hbg:#0B0B10;--hfg:#fff;--hword:#EF4E73;--haccent:#EF4E73;--hctafg:#fff">
<p class="word" aria-hidden="true">BLACK FRIDAY</p>
<div class="bottles">{b}</div>
{STAMP.format(bg='#EF4E73', fg='#0B0B10', txt='BLACK FRIDAY · NOV. 23–29. · DON CHERRY · ', uid='bf-' + uid, center='BF')}
<div class="copy"><div class="wrap"><div class="txt" style="text-shadow:0 2px 18px rgba(0,0,0,.6)"><span class="eyebrow">{eyebrow}</span>
<{htag} class="t">Black Friday a borházban – egy hétig, amíg a csomagok tartanak</{htag}><p class="s">Két csomag, mindkettőből legfeljebb 40. {note}</p>
<a class="btn" href="#bf-csomagok-{uid}">A csomagok →</a></div></div></div></section>
<section class="lp-bfx" id="bf-csomagok-{uid}"><div class="wrap">
{box(prem, True, 'A LEGTÖBBEN EZT VESZIK · LEGNAGYOBB KEDVEZMÉNY')}
{box(mini, False, 'KISEBB KERETBŐL', '<p class="ct">2-2 palack FRISS eper, málna és meggy.</p>')}
</div><div class="wrap"><p class="ph-note" style="color:#BFC3D1">A darabszámot a tavalyi Black Friday-eladások alapján állítjuk be; a csomagok tartalmát és árát a Kontyos véglegesíti.</p></div></section>'''
    if wait:
        out += f'''<section class="lp-wait bf" id="bf-wait-{uid}"><div class="wrap"><h2>Szólunk nov. 23-án reggel.</h2>
<form data-newsletter><label class="sr" for="bfm-{uid}">E-mail-cím</label><input id="bfm-{uid}" type="email" required placeholder="E-mail-címed"><button class="btn pink" type="submit">Értesítést kérek</button></form></div></section>'''
    return out


def xmas_landing(r, phase, htag='h1', uid='x', full=True):
    """Karácsony (Sanyi): karácsonyi hangulat (fenyő), „karácsony/advent” – nem „ünnep”; csomagok, Don Cherry, és ha nem tudott választani: kategóriák."""
    pre = phase == 'elozetes'
    eyebrow = 'ADVENT · DEC. 1-TŐL RENDELHETŐ' if pre else 'ADVENT ÉS KARÁCSONY · DEC. 1–22.'
    b = (hb(P['epres-piri-mama-forralt-bora'], r, 'clamp(290px,54vh,500px)', 0, '-10deg')
         + hb(P['don-cherry'], r, 'clamp(330px,64vh,590px)', 12, '3deg')
         + hb(P['narancsos-piri-mama-forralt-bora'], r, 'clamp(280px,52vh,470px)', 12, '11deg'))
    packs = ''
    for pid in ('edes-unnepek', 'premium-advent', 'konnyu-karacsony'):
        sp = SP[pid]
        lis = ''.join(f'<li>{e(P[i]["name"])}</li>' for i in sp['items']) + (f'<li>{e(sp["extra"])}</li>' if sp.get('extra') else '')
        btn = (f'<a class="btn navy block" href="#xn-{uid}">Értesítést kérek dec. 1-jén</a>' if pre
               else f'<button class="btn block" style="background:#7A1C2C" type="button" data-add="{pid}">Ajándékba kérem</button>')
        packs += f'''<article class="xpk"><div class="ph">{FIRS}<div class="bt">{pack_bottles(sp, r)}</div><span class="ad">[Bandi 1200×1200-as hirdetési képe]</span></div>
<div class="tx"><p class="k">{sp['tag']}</p><h3>{e(sp['name'])}</h3><ul>{lis}</ul>
<div class="pr"><s>{ft(sp['old'])}</s><b>{ft(sp['price'])}</b><em>{'Ingyenes szállítás' if sp['free'] else '+ szállítási díj'}</em></div>{btn}</div></article>'''
    out = f'''<section class="hero lp-xmas" style="--hbg:#123B2B;--hfg:#fff;--hword:#F3C66B;--haccent:#F3C66B;--hctafg:#123B2B">
{falling(r, ("flake-gold", "flake-blue", "ornament-gold", "holly", "snow-dots", "flake-gold"), 26, 9)}<div class="firs">{FIRS}</div><div class="animals" aria-hidden="true"><img class="an renszarvas" src="{r}img/deco/allat-renszarvas.png" alt=""></div>
<p class="word" aria-hidden="true">KARÁCSONY</p>
<div class="bottles">{b}</div>
<div class="copy"><div class="wrap"><div class="txt" style="text-shadow:0 2px 18px rgba(10,30,20,.7)"><span class="eyebrow">{eyebrow}</span>
<{htag} class="t">Karácsonyi ajándék bor és borcsomagok</{htag}><p class="s">Adventi és karácsonyi borcsomagok a klárafalvi borházból – becsomagolva, ajándéknak.</p>
<a class="btn" href="#csomagok-{uid}">Karácsonyi csomagok →</a></div></div></div></section>
<section class="lp-xp" id="csomagok-{uid}"><div class="xdeco" aria-hidden="true"><img src="{r}img/deco/ornament-gold.svg" alt=""><img src="{r}img/deco/holly.svg" alt=""><img src="{r}img/deco/flake-gold.svg" alt=""><img src="{r}img/deco/ornament-pink.svg" alt=""></div><div class="wrap"><div class="hd"><p class="kicker" style="--accent:#B08A2E">Karácsony</p><h2 class="h2">Karácsonyi borcsomagok</h2></div>
<div class="xgrid">{packs}</div>'''
    if pre:
        out += f'''<div class="lp-wait" id="xn-{uid}" style="background:#7A1C2C;border-radius:6px"><div style="padding:30px;display:flex;flex-wrap:wrap;gap:16px 40px;align-items:center"><h2>Dec. 1-jén szólunk.</h2>
<form data-newsletter><label class="sr" for="xm-{uid}">E-mail-cím</label><input id="xm-{uid}" type="email" required placeholder="E-mail-címed"><button class="btn" style="background:#F3C66B;color:#4A0F19" type="submit">Értesítést kérek</button></form></div></div>'''
    out += '<p class="ph-note">Demó árak és összeállítás – a csomagok tartalmát a Kontyos véglegesíti (Gabival egyeztetve, forralt bor csomaggal is).</p></div></section>'
    if full:
        out += don_packs(r, 'Don Cherry ajándékcsomag', 'Kis és nagy csomag – a vermut és a párja karácsonyra.')
        out += choose_tiles(r)
    return out


def bf_page():
    r = ''
    segs = '<span class="seg">' + ''.join(f'<button type="button" data-phase-btn="{k}">{l}</button>' for k, l in [('aktiv', 'BF aktív'), ('varolista', 'BF előtt (várólista)')]) + '</span>'
    pg = head('Black Friday borcsomag akció | Kontyos', 'Black Friday a Kontyos Borházban nov. 23–29.: Black Friday Prémium és Mini borcsomag, mindkettőből legfeljebb 40 darab.', r, 'black-friday', 'overlay-head', demo_extra=segs)
    pg += header(r, 'black-friday.html') + '<main>'
    pg += ''.join(f'<div data-phase="{ph}">{bf_landing(r, ph, "h1", ph)}</div>' for ph in ('aktiv', 'varolista'))
    pg += newsletter() + '</main>' + footer(r)
    write('black-friday.html', pg)


def xmas_page():
    r = ''
    segs = '<span class="seg">' + ''.join(f'<button type="button" data-phase-btn="{k}">{l}</button>' for k, l in [('aktiv', 'Aktív'), ('elozetes', 'Előzetes')]) + '</span>'
    pg = head('Karácsonyi ajándék bor és borcsomagok | Kontyos', 'Karácsonyi ajándék bor és borcsomagok dec. 1–22.: Édes Ünnepek, Prémium adventi és Könnyű karácsonyi borcsomag, Don Cherry ajándékcsomag.', r, 'karacsony', 'overlay-head', demo_extra=segs, topbar=XMAS_BAR)
    pg += header(r, 'karacsonyi-ajandek-bor.html') + '<main>'
    pg += ''.join(f'<div data-phase="{ph}">{xmas_landing(r, ph, "h1", ph)}</div>' for ph in ('aktiv', 'elozetes'))
    pg += newsletter() + '</main>' + footer(r)
    write('karacsonyi-ajandek-bor.html', pg)


def ujbor_page():
    """Újbor (Sanyi): rengeteg gyümölcs a háttérben, „Kóstold meg az új borainkat”; a 6 palackos válogatás külön szekcióban a tartalmával."""
    r = ''
    sp = SP['ujbor-valogatas']
    pg = head('Újbor 2026 – kóstold meg az új gyümölcsborainkat | Kontyos', 'Az idei gyümölcs palackban: 100%-os klasszikus gyümölcsborok és 6 palackos Újbor-válogatás ingyenes szállítással, nov. 5–23.', r, 'ujbor', 'overlay-head')
    pg += header(r) + '<main>'
    bottles = ''.join(f'<a href="{r}{url(P[i])}" title="{e(P[i]["name"])}"><img src="{r}{P[i]["tight"]}" alt="{e(P[i]["name"])}"></a>' for i in sp['items'])
    lis = ''.join(f'<li><a href="{r}{url(P[i])}"><i style="background:{P[i]["accent"]}"></i>{e(P[i]["name"])}</a><span>{ft(P[i]["price"])}</span></li>' for i in sp['items'])
    pg += f'''<section class="ujh">{fruit_burst(r, 34, 11)}<div class="wrap"><div class="tx">
<p class="kicker" style="--accent:#EF4E73">Limitált · nov. 5–23.</p><h1 class="h2">Kóstold meg az új borainkat</h1>
<p class="lead">Az idei gyümölcs, palackban. Válogass a 100%-os klasszikus gyümölcsborainkból – vagy vidd mind a hatot egy dobozban.</p>
<div class="btns"><a class="btn pink" href="#valogatas">6 palackos válogatás →</a><a class="btn ghost" href="{r}gyumolcsbor.html#klasszikus">100%-os gyümölcsborok</a></div></div>
<div class="ubt">{bottles}</div></div></section>
<section class="ujv" id="valogatas"><div class="wrap"><div class="ph"><span class="tag">6 PALACK</span>{''.join(f'<img src="{r}{P[i]["tight"]}" alt="">' for i in sp['items'])}</div>
<div class="tx"><p class="kicker">Újbor-válogatás</p><h2 class="h2">Mind a hat, egy dobozban</h2><ul>{lis}</ul>
<div class="pr"><s>{ft(sp['old'])}</s><b>{ft(sp['price'])}</b><em>Ingyenes szállítás · 6 palackos ár</em></div>
<button class="btn pink" type="button" data-add="ujbor-valogatas">Kosárba teszem a válogatást</button>
<p class="ph-note">Demó összeállítás a klasszikus gyümölcsborokból, a 6 palackos mennyiségi áron – a végleges tartalmat a Kontyos adja.</p></div></div></section>
<section class="sec"><div class="wrap" style="display:flex;flex-direction:column;gap:24px"><h2 class="h2">Vagy válaszd palackonként</h2>{cards(sp['items'], r)}</div></section>'''
    pg += choose_tiles(r, 'Nézz körül tovább', 'A klasszikusok mellett a Klára, a FRISS, a forralt borok és a Don Cherry.') + newsletter() + '</main>' + footer(r)
    write('ujbor-valogatas.html', pg)


MSEARCH = '''<section class="m-search"><form role="search" action="kereses.html"><label class="sr" for="ms">Keresés</label><input id="ms" name="q" type="search" placeholder="Meggy, forralt bor, ajándék…"><button type="submit" aria-label="Keresés"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg></button></form>
<nav aria-label="Gyors kategóriák"><a href="termek/piri-mama-forralt-bora.html" style="background:#1B2A5C;color:#fff">Forralt bor</a><a href="gyumolcsbor.html#klasszikus" style="box-shadow:inset 0 0 0 1.5px #1B2A5C">Klasszikus</a><a href="friss.html" style="background:#F28C28">FRISS</a><a href="gyumolcsbor.html#klara" style="box-shadow:inset 0 0 0 1.5px #C0284A;color:#C0284A">Klára</a><a href="termek/don-cherry.html" style="box-shadow:inset 0 0 0 1.5px #5FB8B3;color:#C8282E">Don Cherry</a><a href="csomagok.html" style="box-shadow:inset 0 0 0 1.5px #1B2A5C">Csomagok</a><a href="palinka.html" style="box-shadow:inset 0 0 0 1.5px #A8823C;color:#6B5414">Pálinka</a></nav></section>'''


PK_HERO = {  # Ajándék és csomagok hero: mindig az aktuális szezon-landing heroját tükrözi, csak csomagokkal (Sanyi, 11-03)
    'forralt': dict(bg='#F08A3C', fg='#1B2A5C', hword='#1B2A5C', acc='#1B2A5C', ctafg='#fff', word='FORRALT BOR', packs=['forralt-6', 'konnyu-karacsony'],
                    eyebrow='Ajándék és csomagok · forralt szezon', s='PIRI Mama forralt borok csomagban – hideg estékre és ajándékba.'),
    'ujbor': dict(bg='#F6E1E4', fg='#1B2A5C', hword='#D7263D', acc='#EF4E73', ctafg='#fff', word='ÚJBOR', packs=['ujbor-valogatas'],
                  eyebrow='Ajándék és csomagok · újbor · nov. 5–23.', s='Hat klasszikus gyümölcsbor a 6 palackos áron.'),
    'bf': dict(bg='#0B0B10', fg='#fff', hword='#EF4E73', acc='#EF4E73', ctafg='#fff', word='BLACK FRIDAY', packs=['bf-premium', 'bf-mini'],
               eyebrow='Ajándék és csomagok · Black Friday · nov. 23–29.', s='Két csomag, mindkettőből legfeljebb 40.'),
    'karacsony': dict(bg='#123B2B', fg='#fff', hword='#DBB879', acc='#DBB879', ctafg='#123B2B', word='KARÁCSONY', packs=['edes-unnepek', 'premium-advent'],
                      eyebrow='Ajándék és csomagok · advent és karácsony', s='Összeállított ajándékcsomagok – becsomagolva, ajándéknak.'),
}


def pack_hero(k, r):
    c = PK_HERO[k]
    deco = {'forralt': falling(r, ('flake-blue', 'flake-gold', 'holly', 'snow-dots'), 22, 3) + ANIMALS.format(r=r),
            'ujbor': fruit_burst(r, 18, 5),
            'bf': '',
            'karacsony': falling(r, ('flake-gold', 'flake-blue', 'ornament-gold', 'holly', 'snow-dots', 'flake-gold'), 26, 9)
                         + f'<div class="firs">{FIRS}</div><div class="animals" aria-hidden="true"><img class="an renszarvas" src="{r}img/deco/allat-renszarvas.png" alt=""></div>'}[k]
    stamp = {'forralt': STAMP.format(bg='#1B2A5C', fg='#F3C66B', txt='CSAK MEGMELEGÍTED ÉS KÉSZ · PIRI MAMA · ', uid='pk-f', center='100%'),
             'bf': STAMP.format(bg='#EF4E73', fg='#0B0B10', txt='BLACK FRIDAY · NOV. 23–29. · DON CHERRY · ', uid='pk-bf', center='BF')}.get(k, '')
    stage = ''.join(f'''<a class="pk-st" href="#pk-{k}"><span class="ph" style="--tint:{SP[i]['tint']}">{pack_bottles(SP[i], r)}</span><b>{e(SP[i]['name'])}</b><i>{ft(SP[i]['price'])}{f" <s>{ft(SP[i]['old'])}</s>" if SP[i].get('old') else ''}</i></a>''' for i in c['packs'])
    cls = {'bf': ' lp-bf', 'karacsony': ' lp-xmas', 'ujbor': ' has-fruit'}.get(k, '')
    return f'''<section class="hero pk-hero{cls}" data-season="{k}" style="--hbg:{c['bg']};--hfg:{c['fg']};--hword:{c['hword']};--haccent:{c['acc']};--hctafg:{c['ctafg']}">
{deco}<p class="word" aria-hidden="true"{' style="--wfx:calc((100vw - 64px) / 7.9)"' if k == 'forralt' else ''}>{c['word']}</p>
<div class="bottles pk-stage">{stage}</div>
{stamp}
<div class="copy"><div class="wrap"><div class="txt"><span class="eyebrow">{c['eyebrow']}</span><h1 class="t">Csomagban jobban megéri</h1><p class="s">{c['s']}</p><a class="btn" href="#pk-{k}">A csomagok →</a></div></div></div></section>'''


def packs_page():
    """Ajándék és csomagok (Sanyi, 11-03): a hero mindig az aktuális szezon-landing heroját tükrözi (szín, felirat, díszek), csak csomagokkal;
    utána a szezon csomagjai → Don Cherry → Forralt → állandó ajánlatok (páros, trió, pohár, párna)."""
    r = ''
    segs = '<span class="seg" aria-label="Szezon váltó">' + ''.join(f'<button type="button" data-season-btn="{s["k"]}">{s["lbl"]}</button>' for s in SEASONS) + '</span>'
    pg = head('Ajándék és borcsomagok | Kontyos', 'Szezonális ajándékcsomagok, Don Cherry és PIRI Mama forralt csomagok, páros és trió borválogatások a Kontyos Borháztól.', r, 'csomagok', 'overlay-head', demo_extra=segs) + header(r, 'csomagok.html')
    H2 = 'style="font-size:clamp(26px,3vw,40px)"'

    def season(k, cls, kicker, title, ids, link):
        return (f'<section data-season="{k}" class="pk-season {cls}" id="pk-{k}"><div class="wrap"><div class="hd"><p class="kicker">{kicker}</p><h2 class="h2" {H2}>{title}</h2></div>'
                f'<div class="packs-grid">{"".join(pack_card(SP[i], r) for i in ids)}</div>{link}</div></section>')
    heroes = ''.join(pack_hero(k, r) for k in ('forralt', 'ujbor', 'bf', 'karacsony'))
    seasonal = (season('forralt', 'pk-forralt', 'Most aktuális · forralt szezon', 'Forralt borok csomagban', ['forralt-6', 'konnyu-karacsony'], '')
                + season('ujbor', 'pk-ujbor', 'Most aktuális · nov. 5–23.', 'Újbor-válogatás', ['ujbor-valogatas'], f'<a class="pk-more" href="{r}ujbor-valogatas.html">Az újbor-oldal →</a>')
                + season('bf', 'pk-bf', 'Most aktuális · Black Friday · nov. 23–29.', 'Black Friday csomagok', ['bf-premium', 'bf-mini'], f'<a class="pk-more" href="{r}black-friday.html">A Black Friday oldal →</a>')
                + season('karacsony', 'pk-xmas', 'Most aktuális · advent és karácsony', 'Karácsonyi ajándékcsomagok', ['edes-unnepek', 'premium-advent', 'konnyu-karacsony'], f'<a class="pk-more" href="{r}karacsonyi-ajandek-bor.html">A karácsonyi oldal →</a>'))
    forralt = (f'<section data-season="ujbor bf karacsony" class="sec pk-fblock"><div class="wrap" style="display:flex;flex-direction:column;gap:22px"><p class="kicker">PIRI Mama</p><h2 class="h2" {H2}>Forralt csomag</h2>'
               f'<div class="packs-grid">{pack_card(SP["forralt-6"], r)}</div></div></section>')
    pg += f'''<main>{heroes}
{seasonal}
{don_packs(r)}
{forralt}
<section class="sec pk-allando"><div class="wrap" style="display:flex;flex-direction:column;gap:22px"><p class="kicker">Állandó ajánlatok</p><h2 class="h2" {H2}>Egész évben</h2>
{cards(['meggy-paros', 'eper-paros', 'konnyu-trio', 'bubi-paros', 'kontyos-borospohar', 'meggymag-parna'], r)}
<p class="ph-note">A forralt csomag összetétele (javaslat: 4 narancsos + 1 klasszikus + 1 epres) és ára demó – a Kontyos véglegesíti.</p></div></section></main>''' + footer(r)
    write('csomagok.html', pg)


def search_page():
    r = ''
    pg = head('Keresés | Kontyos', 'Keresés a Kontyos termékei között', r, 'search') + header(r)
    pg += '''<main><div class="wrap" style="padding-top:10px;padding-bottom:90px;display:flex;flex-direction:column;gap:22px"><h1 class="h2">Keresés</h1>
<form role="search" action="kereses.html" class="m-search" style="display:block;background:none;border:0;padding:0"><label class="sr" for="sq">Keresés</label><div style="display:flex;align-items:center;gap:8px;background:#fff;border-radius:999px;padding:0 6px 0 18px;max-width:640px"><input id="sq" name="q" type="search" placeholder="Meggy, forralt bor, ajándék…" style="flex:1;min-width:0;height:52px;border:0;background:transparent;font:inherit;font-size:16px;outline:none"><button type="submit" class="btn blue" style="min-height:42px;padding:0 20px">Keresés</button></div></form>
<p id="search-sum" class="muted"></p><div id="search-res" class="cards"></div></div></main>''' + footer(r)
    write('kereses.html', pg)


# ---------- Kövess minket: adventi standok (DEMÓ időpontok – a valós menetrendet a Kontyos adja) ----------
FAIRS = [  # Sanyi (2026-11-02): 7 város, fontossági sorrendben. Időpontok: a 2025-ös menetrend azonos hétköznapokra tolva; Pécs, Nyíregyháza: egyeztetés alatt
    dict(id='szeged', city='Szeged', place='Dóm tér – Szegedi Adventi Vásár', lat=46.2496, lng=20.1490, start='2026-11-27', end='2027-01-04', closed=[], note='Szenteste és karácsonykor is nyitva, január 4-ig', hours='egyeztetés alatt'),
    dict(id='obuda', city='Budapest – Óbuda', place='Óbudai adventi vásár', lat=47.5414, lng=19.0450, start='2026-11-27', end='2026-12-23', closed=[], note='December 23-ig', hours='egyeztetés alatt'),
    dict(id='gyor', city='Győr', place='Győri adventi vásár, belváros', lat=47.6875, lng=17.6355, start='2026-11-27', end='2026-12-31', closed=['2026-12-24'], note='Szenteste zárva, utána szilveszterig nyitva', hours='egyeztetés alatt'),
    dict(id='szombathely', city='Szombathely', place='Szombathelyi adventi vásár', lat=47.2306, lng=16.6219, start='2026-11-20', end='2026-12-23', closed=[], note='Elsőként nyitunk, december 23-ig', hours='egyeztetés alatt'),
    dict(id='veszprem', city='Veszprém', place='Veszprémi adventi vásár', lat=47.0932, lng=17.9076, start='2026-11-27', end='2026-12-23', closed=[], note='December 23-ig', hours='egyeztetés alatt'),
    dict(id='pecs', city='Pécs', place='Pécsi adventi vásár', lat=46.0763, lng=18.2283, start='2026-11-27', end='2026-12-23', closed=[], note='A pontos időpontot hamarosan közöljük', hours='egyeztetés alatt', tbd=True),
    dict(id='nyiregyhaza', city='Nyíregyháza', place='Nyíregyházi adventi vásár', lat=47.9558, lng=21.7167, start='2026-11-27', end='2026-12-23', closed=[], note='A pontos időpontot hamarosan közöljük', hours='egyeztetés alatt', tbd=True),
]
BORHAZ = dict(city='Klárafalva', place='Kontyos Borház – egész évben, személyes átvétel', lat=46.2209, lng=20.3266)


def fairs_js():
    return '<script>window.KONTYOS_FAIRS=' + json.dumps(FAIRS, ensure_ascii=False) + ';window.KONTYOS_BORHAZ=' + json.dumps(BORHAZ, ensure_ascii=False) + ';</script>'


def fairs_strip(r=''):
    """Vásárok – a PIRI Mama landing „Hol kapható?” kártyáival azonos design (Sanyi, 2026-11-02).
    A képek a landing jelenlegi képei; a véglegesítettekre cseréljük, amikor a PIRI landingen is kicserélik."""
    cards = ''.join(f'''<a class="fair-card2" href="{r}vasarok.html#{f['id']}" data-fair="{f['id']}"><span class="im"><img src="{r}img/fair/vasar-{i % 4 + 1}.webp" alt="Adventi vásár – {e(f['city'])}" loading="lazy"></span>
<span class="tx"><span class="dt"><span data-fair-dates></span> · <span data-fair-status>Hamarosan</span></span><b>{e(f['city'])} – {e(f['place'].split(' – ')[0])}</b><span class="pl">{e(f['note'])}</span></span></a>''' for i, f in enumerate(FAIRS))
    return f'''<section class="follow2">{falling(r, ("flake-gold", "snow-dots", "flake-gold"), 12, 4)}<div class="wrap hd"><h2 class="lp-title">Találkozzunk az adventi vásárokon!</h2><p class="lp-sub">Szeged · Óbuda · Győr · Szombathely · Veszprém · Pécs · Nyíregyháza</p>
<div class="fz-intro"><p class="fz-txt">Adventi vásárainkban <b>frissen elkészített, forrón kínált PIRI Mama forralt borokkal és klasszikus eper forralt borunkkal</b> várunk.</p>
</div></div>
<div class="fair-grid fair-row" id="fair-row">{cards}</div>
<div class="wrap ft"><div class="ft-btns"><button type="button" class="lp-btn" data-fair-more aria-controls="fair-row" aria-expanded="false">További vásárok ({len(FAIRS) - 5})</button><a class="lp-btn" href="{r}vasarok.html">Térkép</a></div>
<p class="fz-txt fz-piri">A <b>PIRI Mama forralt borainkat</b> az üzletekben is megtalálod, így otthon is elkészítheted kedvenceidet.</p><p class="ph-note">Időpontok a tavalyi menetrend alapján – a 2026-os véglegesítés alatt. A képek a PIRI Mama landing véglegesített képeire cserélődnek.</p></div></section>'''


def fairs_page():
    r = ''
    segs = '<span class="seg"><button type="button" data-sim="">Ma</button><button type="button" data-sim="2026-12-06">Szimuláció: dec. 6.</button></span>'
    extra = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">'
    pg = head('Kövess minket – adventi standjaink térképen | Kontyos', 'Hol van most a Kontyos standja? Adventi vásárok térképen, élő státusszal és e-mail értesítővel: szólunk, mielőtt a városodba érünk.', r, 'fairs', '', extra, demo_extra=segs)
    pg += header(r)
    rows = ''.join(f'''<li id="{f['id']}" data-fair="{f['id']}"><button type="button" class="fl-go" data-go="{f['id']}"><span class="st" data-fair-status>Hamarosan</span><b>{e(f['city'])}</b><span class="pl">{e(f['place'])}</span><span class="dt" data-fair-dates></span><span class="hr">{e(f['note'])} · Nyitvatartás: {e(f['hours'])}</span></button></li>''' for f in FAIRS)
    checks = ''.join(f'''<label class="check"><input type="checkbox" name="fair" value="{f['id']}"> <span><b>{e(f['city'])}</b> · {e(f['place'])}</span></label>''' for f in FAIRS)
    pg += f'''<main class="fairs"><section class="wrap fz-head"><p class="breadcrumb"><a href="index.html">Főoldal</a> / Kövess minket</p>
<p class="kicker">Adventi vásárok · Szeged · Óbuda · Győr · Szombathely · Veszprém · Pécs · Nyíregyháza</p><h1 class="h2">Találkozzunk az adventi vásárokon!</h1>
<p class="fz-txt">Adventi vásárainkban <b>frissen elkészített, forrón kínált PIRI Mama forralt borokkal és klasszikus eper forralt borunkkal</b> várunk.</p>
</section>
<section class="wrap fz-grid fz-stack"><ol class="flist">{rows}</ol><div id="fmap" class="fmap" role="region" aria-label="Standok térképe"></div>
<p class="fz-txt fz-piri">A <b>PIRI Mama forralt borainkat</b> az üzletekben is megtalálod, így otthon is elkészítheted kedvenceidet.</p></section>
<section class="fz-sub" id="ertesito"><div class="wrap"><div class="tx"><p class="kicker" style="--accent:#F3C66B">Értesítő</p><h2 class="h2">Szólunk, mielőtt a városodba érkezünk</h2>
<p class="lead">Jelöld be, melyik vásárról kérsz értesítést. Automatikus e-mailt küldünk 3 nappal a nyitás előtt és a nyitás reggelén, és ha valamelyik időpont változik, arról is szólunk.</p>
<div class="mailprev"><p class="mh">Így néz ki az e-mail</p><div class="mail"><small>Tárgy: Péntektől Szegeden vagyunk – Dóm tér 🍷</small><b>Szia! Hamarosan a városodban leszünk.</b><p>A PIRI Mama standja nov. 27-től a szegedi Dóm téren vár. Gyere el egy pohár forralt borra!</p><span class="btnlike">Útvonal a standhoz →</span></div></div></div>
<form class="subform" data-fair-form><div class="field"><label for="fz-name">Keresztnév</label><input id="fz-name" name="name" autocomplete="given-name"></div>
<div class="field"><label for="fz-mail">E-mail cím</label><input id="fz-mail" name="email" type="email" required autocomplete="email"><span class="msg">Adj meg érvényes e-mail címet</span></div>
<fieldset><legend>Melyik vásárról kérsz értesítést?</legend>{checks}<label class="check all"><input type="checkbox" data-fair-all> <span><b>Mindegyikről</b></span></label></fieldset>
<label class="check"><input type="checkbox" required> <span>Hozzájárulok, hogy a Kontyos Borház Kft. a megadott vásárokról e-mailben értesítsen. Bármikor leiratkozhatok.</span></label>
<button class="btn" type="submit" style="background:#F3C66B;color:#1B2A5C">Értesítést kérek</button><p class="fz-ok" data-fair-ok role="status"></p></form></div></section>
<section class="wrap" style="padding-top:20px;padding-bottom:80px"><p class="ph-note">Az időpontok a 2025-ös menetrendet követik, azonos hétköznapokra tolva; a nyitvatartást és a végleges dátumokat a Kontyos adja. A „Szimuláció” gombbal megnézheted, hogyan néz ki az oldal advent közepén, amikor több stand élőben fut.</p></section></main>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>''' + footer(r)
    write('vasarok.html', pg)


# Gyümölcs-vizuál (helykitöltő, amíg Bandi elkészíti a valódi „szétrobbanó gyümölcs” képet): saját SVG-gyümölcsök szórva, lassan lebegve
FRUIT_SVGS = ['meggy', 'eper', 'alma', 'malna', 'kajszi', 'szilva', 'ribizli', 'narancs']


def fruit_burst(r, n=18, seed=1, fruits=None, cls=''):
    import random
    rnd = random.Random(seed)
    fr = fruits or FRUIT_SVGS
    out = ''
    for i in range(n):
        f = fr[i % len(fr)]
        if 'edge' in cls:  # csak a két szélén, hogy a szöveget ne takarja
            x = rnd.uniform(-5, 6) if i % 2 == 0 else rnd.uniform(84, 95)
        else:
            x = rnd.uniform(-4, 92)
        y = rnd.uniform(-6, 94)
        s, rot, d = (rnd.uniform(7, 12) if 'edge' in cls else rnd.uniform(9, 19)), rnd.uniform(-35, 35), rnd.uniform(0, 6)
        out += f'<img src="{r}img/fruit/{f}.svg" alt="" style="left:{x:.1f}%;top:{y:.1f}%;width:{s:.1f}%;--rot:{rot:.0f}deg;animation-delay:-{d:.1f}s">'
    return f'<div class="fburst {cls}" aria-hidden="true">{out}</div>'


RETAIL = [('Lidl', 'uzletlogo-lidl.svg', '2 állandó termék', '2023 januárja óta'),
          ('Spar', 'uzletlogo-spar.svg', '5 állandó termék', '2023 júniusa óta'),
          ('CBA', 'uzletlogo-cba.svg', '4 állandó termék', '2022 januárja óta'),
          ('Ecofamily', 'uzletlogo-eco-family.svg', 'Állandó partner', 'országszerte'),
          ('Janker', None, 'Állandó partner', 'országszerte')]
BOTTLE_ICON = '<svg viewBox="0 0 20 60" aria-hidden="true"><path d="M7 0h6v14c0 3 5 6 5 13v31a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V27c0-7 5-10 5-13z"/></svg>'


def trust_block(r, h='h2'):
    """Hitelesítő blokk – Sanyi mintája (2026-11-02): fő állítás, eladott palackok, gyümölcsök valódi fotókkal, saját üzem, üzletláncok."""
    bottles = ''.join(f'<i style="opacity:{1 - k * .055:.2f}">{BOTTLE_ICON}</i>' for k in range(17))
    small = [('eper', 'Eper', '', 'w'), ('meggy', 'Meggy', '', 'w'), ('oszi', 'Őszibarack', '', ''), ('sarga', 'Sárgabarack', '', ''),
             ('szilva', 'Szilva', '', ''), ('ribizli', 'Ribizli', '', ''), ('malna', 'Málna', '', ''), ('narancs', 'Narancs', '', '')]
    fr = ''.join(f'<figure class="{c}"><img src="{r}img/gyumolcs/{k}.webp" alt="{n}" loading="lazy"><figcaption>{n}{f" · {t}" if t else ""}</figcaption></figure>' for k, n, t, c in small)
    uz = ''.join(f'<img src="{r}img/uzem/{k}.webp" alt="{a}" loading="lazy">' for k, a in (('tartaly', 'Rozsdamentes erjesztőtartályok a klárafalvi üzemben'), ('palack', 'Palackozás a klárafalvi üzemben'), ('palack2', 'Automata palackozósor a klárafalvi üzemben')))
    tiles = ''.join((f'<li><img class="rlogo" src="{r}img/logos/{f}" alt="{n}" loading="lazy">' if f else f'<li><span class="rlogo txt">{n.upper()}</span>') + '</li>' for n, f, a, b in RETAIL)
    return f'''<section class="trust2"><div class="wrap">
<div class="t-hero"><figure class="tpola tp-hero" style="--r:5deg"><span class="ph">[Csapatfotó 3 – a Kontyos küldi]</span></figure><p class="kicker">Magyarország vezető gyümölcsbor-gyártója · Klárafalva</p>
<{h} class="h2">100% gyümölcsbor.<br>Ezerféle élmény.</{h}>
<p class="lead">Saját gyümölcsborokat készítünk, és ezekre építve fejlesztünk új, izgalmas italokat. A klasszikus gyümölcsboroktól a modern különlegességekig.</p></div>
<div class="t-bottles"><div class="brow">{bottles}</div><div class="tnum"><b>450 000+</b><span>palack</span></div></div>
<div class="t-fruit"><p class="kicker">Gyümölcsökből születnek az italaink</p>
<div class="t-fhead"><h3>Évente több száz tonna gyümölcsből</h3><div class="tnum"><b>500 tonna +</b><span>gyümölcs évente</span></div></div>
<figure class="alma"><img src="{r}img/gyumolcs/alma.webp" alt="Alma" loading="lazy"></figure><div class="alma-cap"><span>Alma</span></div>
<div class="frow2">{fr}</div></div>
<div class="t-plant tp2"><div class="tp-tx"><p class="kicker">Saját gyártás · folyamatos fejlesztés</p><h3>Klárafalváról az üzletekig</h3>
<p class="lead">2006 óta készítünk gyümölcsborokat. Saját üzemünkben a borászati tapasztalatot korszerű technológiával és folyamatos termékfejlesztéssel ötvözzük.</p></div>
<div class="tp-polas" aria-label="A Kontyos csapata"><figure class="tpola" style="--r:-6deg"><span class="ph">[Csapatfotó 1 – a Kontyos küldi]</span></figure><figure class="tpola" style="--r:5deg"><span class="ph">[Csapatfotó 2 – a Kontyos küldi]</span></figure></div>
<div class="tnum"><b>1 100 m²</b><span>gyártóüzem</span></div></div>
<div class="t-retail"><div class="rl-vp"><ul>{tiles}{tiles.replace('<li>', '<li class="dup" aria-hidden="true">')}</ul></div><p>Keresd a KONTYOS italait az üzletekben és webshopunkban!</p></div>

</div></section>'''


def polaroids(r):
    return f'''<div class="polas" aria-hidden="true"><figure class="pola" style="--r:-7deg"><img src="{r}img/photo/don_polaroid.webp" alt="" loading="lazy"></figure><figure class="pola" style="--r:6deg"><img src="{r}img/photo/piri_nar_life.webp" alt="" loading="lazy"></figure></div>'''

# A „100%-os gyümölcsbor” blokk: valódi, körbevágott gyümölcsfotók (Unsplash/Pexels) – szétszórva, sokszorozva, különböző szögekből potyognak
def fruit_rain(r, n=58, seed=21):
    """Statikus, sűrűn szétszórt gyümölcsök (több szögből, sokszorozva) – nem esnek."""
    import random, math
    rnd = random.Random(seed)
    kinds = ['alma', 'eper', 'meggy', 'oszibarack', 'sargabarack', 'malna', 'narancs', 'szilva', 'ribizli']
    rel = {'alma': 1.0, 'narancs': 1.0, 'oszibarack': 1.05, 'sargabarack': .8, 'eper': .78, 'szilva': .72, 'malna': .62, 'ribizli': .7, 'meggy': .62}
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:          # Poisson-disc: egyenletes, de nem rácsos szórás
        tries += 1
        x, y = rnd.uniform(-4, 104), rnd.uniform(-4, 104)
        if all(math.hypot(x - a, y - b) > 10.5 for a, b in pts):
            pts.append((x, y))
    out = ''
    for i, (x, y) in enumerate(pts):
        k = kinds[i % len(kinds)]
        w = rel[k] * rnd.uniform(14, 21)
        out += (f'<i style="left:{x:.1f}%;top:{y:.1f}%;width:{w:.1f}%;z-index:{rnd.randint(1, 4)};'
                f'transform:translate(-50%,-50%) rotate({rnd.uniform(-170, 170):.0f}deg) scaleX({rnd.choice((1, -1))})">'
                f'<img src="{r}img/gyumolcs1/{k}.webp" alt="" loading="lazy"></i>')
    return f'<div class="frain" aria-hidden="true">{out}</div>'


def friss_cut(r, cls=''):
    """A fektetett FRISS fotó körbevágva: árnyékréteg (multiply – bármilyen háttérszínen valódi árnyék) + palackréteg."""
    return (f'<div class="fcut {cls}"><img class="sh" src="{r}img/photo/friss_fekvo_arnyek.webp" alt="" loading="lazy" aria-hidden="true">'
            f'<img class="bt" src="{r}img/photo/friss_fekvo_palack.webp" alt="FRISS gyümölcsborok – málna, eper, narancs, meggy" loading="lazy"></div>')


def new_world(r):
    """„A gyümölcsbor új világa” (Sanyi mintája, 11-03): történet, mit jelent a 100%, csapat, és a gyümölcsbor új oldalai (FRISS, PIRI Mama, Don Cherry, Berry Secco, Easy Cider)."""
    lines = [('FRISS', 'friss.html', 'Gyümölcsbor és almabor fele-fele arányban. Könnyed, frissítő harmóniában.'),
             ('PIRI Mama', 'termek/piri-mama-forralt-bora.html', 'Saját klasszikus gyümölcsborainkból, valódi fűszerekkel készülő forralt borok, melyeket már csak meg kell melegíteni.'),
             ('Don Cherry', 'termek/don-cherry.html', 'Prémium meggyvermut saját, 100%-os meggyborunkból, friss meggyen érlelve, válogatott fűszerekkel gazdagítva.'),
             ('Berry Secco', 'termek/berry-secco.html', 'Többféle gyümölcsborból készült, pezsgően gyümölcsös ital. A prosecco buborékossága, egy gyümölcsös koktél izgalmával.'),
             ('Easy Cider', '', 'Az almaborkészítésben szerzett tudásunk legjava egy modern ciderben: könnyed, frissítő és karakteresen almás.')]
    cols = ''.join((f'<a class="nw-l" href="{r}{h}">' if h else '<div class="nw-l">') + f'<h4>{n}</h4><i></i><p>{d}</p>' + ('</a>' if h else '</div>') for n, h, d in lines)
    return f'''<section class="nworld"><img class="nw-fruit" src="{r}img/photo/gyumolcs_vilag.webp" alt="Eper, málna, szilva, meggy, alma, sárgabarack, narancs és ribizli" loading="lazy">
<div class="wrap">
<div class="nw-top"><p class="nw-kick"><span>Modern borászat</span></p><h2 class="h2"><span style="white-space:nowrap">A gyümölcsbor</span><br>új világa</h2><i class="nw-bar"></i>
<p class="nw-intro"><b>Történetünk édesapánkkal kezdődött,</b> aki közel két évtizede elkészítette első gyümölcsborát. Azóta sok minden változott, de a gyümölcsök iránti szeretetünk megmaradt.</p></div>
<div class="nw-what"><h3>Mit jelent a <span style="white-space:nowrap">100%-os</span> gyümölcsbor?</h3><p>Klasszikus gyümölcsboraink 100%-ban az adott gyümölcsből készülnek. Az eperbor eperből, a meggybor meggyből, a kajszibor kajsziból – így minden borban az adott gyümölcs sajátos ízvilága érvényesül.</p></div>
<div class="nw-team"><h3>A hagyományt ma egy elkötelezett csapat viszi tovább.</h3><p><b>Borászaink és munkatársaink</b> Klárafalván, modern környezetben készítik gyümölcsborainkat. Tapasztalatuk, szakértelmük és új ötleteik révén folyamatosan <b>fejlesztik italainkat</b>, és új módokat keresnek arra, hogyan mutathatják meg a gyümölcsbor sokszínűségét.</p></div>
<div class="nw-sides"><h3><span>A gyümölcsbor új oldalai</span></h3><p class="nw-sub">Modern italaink alapját saját, 100%-os gyümölcsboraink és a gyümölcsök gazdag ízvilága adják, amelyeket új ötletekkel és izgalmas párosításokkal gondolunk tovább.</p>
<div class="nw-lines">{cols}</div></div>
</div></section>'''


def claim_block(r):
    """A főoldal vége: „100%-os gyümölcsbor” állítás sok gyümölccsel, alatta az innováció."""
    return f'''<section class="claim"><div class="wrap split">
<div style="display:flex;flex-direction:column;gap:18px"><p class="kicker">Klárafalva</p><h2 class="h2 big">100%-os gyümölcsbor</h2>
<p class="lead">Gyümölcsboraink 100%-ban magyar gyümölcsökből készülnek. Édesapánk közel két évtizede alkotta meg első gyümölcsborát: a család hölgy tagjai olyan italra vágytak, mely édes és zamatos, akár egy nyári gyümölcs.</p>
<p style="line-height:1.7;opacity:.85">2006 óta alkotunk elsőrangú hazai gyümölcsökből gyümölcsbor-különlegességeket, hagyományos és reduktív eljárással. A 2019-ben épült modern üzemünk Szegedhez közel, Klárafalván működik.</p>
<p class="ph-note">[A „mitől 100%-os” szöveget Sanyival közösen véglegesítjük – addig a kontyos.hu jelenlegi szövege áll itt.]</p></div>
<div class="claim-fruit">{fruit_rain(r)}</div></div></section>
<section class="innov"><div class="wrap"><p class="kicker" style="--accent:#F3C66B">Innováció</p><h2 class="h2">Gyümölcsborból, újragondolva</h2>
<div class="ilist"><a href="{r}friss.html"><b>FRISS</b><span>{TXT['friss1']}</span></a>
<a href="{r}termek/piri-mama-forralt-bora.html"><b>PIRI Mama</b><span>Kész forralt bor gyümölcsborból – csak melegíteni kell.</span></a>
<a href="{r}termek/don-cherry.html"><b>Don Cherry</b><span>Meggyvermut friss meggy ágyon érlelt meggyborból.</span></a>
<a href="{r}termek/berry-secco.html"><b>Berry Secco</b><span>Habzó, édes gyümölcsbor a buborékok kedvelőinek.</span></a></div>
<p class="ph-note" style="color:#F3EEE5">[Az innovációs szöveget egyeztetjük – a termékleírások a kontyos.hu adataiból.]</p></div></section>'''


def home_body(r='', h='h1'):
    """Főoldal (Sanyi sorrendje, 2026-11-01): hero → hitelesítő → termékek → vásárok → gyümölcsválasztó → képek, csomagok, könnyű → 100%-os gyümölcsbor + innováció."""
    mq = ' · '.join(['Egy pohár nyár, bármelyik évszakban', 'Mintha most szedték volna a fáról', 'Koccintás, ami mosolyt hagy maga után',
                     'Édes, mint a nyár első epre', 'Hideg estékre meleg PIRI Mama',
                     'Lassú délutánok, hosszú beszélgetések', 'Baráti asztalokra termett', 'Egy családi álomból lett mindenki kedvence'])
    pg = ''
    pg += f'<div class="marquee" aria-hidden="true"><div><span>{mq} · </span><span>{mq} · </span></div></div>'
    pg += fairs_strip(r)
    # Képmátrix (Sanyi, 2026-11-02): a Klára-kép kettébontva, mellé klasszikus boros hangulatkép; minden kép a saját kategóriájára visz
    tiles = [('a', 'termek/piri-mama-forralt-bora.html', 'piri_nar_life.webp', 'Forralt borok', 'Narancsos PIRI Mama forralt bora'),
             ('', 'termek/don-cherry.html', 'don_life.webp', 'Don Cherry', 'Don Cherry meggyvermut'),
             ('', 'termek/friss-malna.html', 'friss_malna.webp', 'FRISS', 'FRISS málna'),
             ('', 'gyumolcsbor.html#klara', 'klara.webp', 'Klára prémium', 'Klára prémium gyümölcsbor'),
             ('', 'gyumolcsbor.html#klasszikus', 'klasszikus_hangulat.webp', '100%-os klasszikusok', 'Klasszikus gyümölcsborok – eper, meggy, ribizli')]
    pg += '<section class="sec"><div class="wrap"><div class="collage">' + ''.join(
        f'<a class="{c}" href="{r}{h}"><img src="{r}img/photo/{im}" alt="{e(alt)}" loading="lazy"><span>{lab} →</span></a>' for c, h, im, lab, alt in tiles) + '</div></div></section>'
    pg += trust_block(r, h)
    pg += f'''<section class="sec picks" style="padding-bottom:40px"><div class="wrap" style="display:flex;flex-direction:column;gap:22px;position:relative">
<h2 class="h2" style="max-width:820px">A mi kedvenceink</h2>{polaroids(r)}
<ul class="usp"><li>100% gyümölcsből</li><li>Ingyenes szállítás 20 000 Ft felett</li><li>6 palacktól mennyiségi ár</li><li>Kiszállítás 1–5 munkanap</li><li>Törzsvásárlói kedvezmény akár 15%</li></ul>
<div style="margin-top:20px">{cards(['edes-meggybor', 'edes-eperbor', 'klara-edes-malnabor', 'friss-malna', 'piri-mama-forralt-bora', 'don-cherry'], r, 'cards home-picks')}</div>
</div></section>'''
    pg += new_world(r)
    pg += f'''<section class="sec"><div class="wrap" style="display:flex;flex-direction:column;gap:28px"><p class="kicker">Válogatások</p><h2 class="h2">Csomagban jobban megéri</h2>
{cards(['meggy-paros', 'eper-paros', 'konnyu-trio', 'bubi-paros'], r)}</div></section>'''
    pg += choose_tiles(r, 'Nem tudtál még választani?', 'Böngéssz tovább a borházban.')
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
            heroes += f'<div data-season="karacsony">{xmas_landing(r, "aktiv", "h2", "home", full=False)}</div>'
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
<h1 class="h2" style="font-size:clamp(30px,7.6vw,86px)">Gyümölcsborok</h1><p class="lead" style="max-width:640px">100%-os gyümölcsborok közvetlenül a klárafalvi Kontyos Borháztól – a klasszikusoktól a prémium Klárán át a könnyű FRISS-ig.</p>
<nav class="chips" aria-label="Kategóriák"><a class="chip" href="#klasszikus">100%-os klasszikus</a><a class="chip" href="#klara">Klára prémium</a><a class="chip" href="#friss">FRISS</a></nav></div></section>
<section id="klasszikus" style="padding-bottom:70px"><div class="wrap" style="display:flex;flex-direction:column;gap:22px">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px"><div style="display:flex;flex-direction:column;gap:10px;max-width:760px"><h2 class="h2">100%-os klasszikus gyümölcsborok</h2><p class="lead">{TXT['klassz1']}</p></div>
<div class="filters" data-filter-group="#klasszikus [data-card]"><button type="button" data-filter="all" aria-pressed="true">Mind</button><button type="button" data-filter="edes" aria-pressed="false">Édes</button><button type="button" data-filter="szaraz" aria-pressed="false">Száraz</button></div></div>
{cards(kl, r)}</div></section>
<section id="klara" class="sec" style="background:#fff"><div class="wrap split">
<div><img src="img/photo/klara.webp" alt="Klára prémium gyümölcsbor" loading="lazy"></div>
<div style="display:flex;flex-direction:column;gap:18px"><p class="kicker" style="--accent:#C0284A">Prémium</p><h2 class="h2">Klára</h2><p class="lead">{TXT['klara1']}</p>
{cards([p['id'] for p in CAT if p['line'] == 'klara'], r)}</div></div></section>
<section id="friss" class="sec" style="background:#F28C28;color:#1B2A5C"><div class="wrap split">
<div style="display:flex;flex-direction:column;gap:18px"><p class="kicker" style="--accent:#1B2A5C">Új · könnyű</p><h2 class="h2">FRISS gyümölcsborok</h2><p class="lead">{TXT['friss1']}</p>
{cards([p['id'] for p in CAT if p['line'] == 'friss'], r, 'cards grid2')}</div>
<div>{friss_cut('')}</div></div></section>
<section class="sec"><div class="wrap" style="max-width:900px;display:flex;flex-direction:column;gap:24px"><div style="display:flex;flex-direction:column;gap:12px"><h2 class="serif" style="font-size:30px">Miért a Kontyos?</h2><p class="lead">Magyarország legnagyobb különleges minőségű gyümölcsborászataként tradicionális és reduktív eljárásokat ötvözünk. Gyümölcsboraink 100%-ban magyar gyümölcsökből, szívvel-lélekkel készülnek – gazdag ízüknek és színüknek köszönhetően egész évben a nyár friss, üde hangulatát hordozzák.</p>
<p>A <a href="#klasszikus">klasszikus gyümölcsborok</a> mellett a prémium <a href="#klara">Klára</a> sorozatot, a könnyű <a href="friss.html">FRISS</a> és a habzó <a href="termek/berry-secco.html">Berry Secco</a> borokat, a <a href="termek/piri-mama-forralt-bora.html">PIRI Mama forralt borokat</a>, a <a href="termek/don-cherry.html">Don Cherry meggyvermutot</a> és kisüsti <a href="palinka.html">pálinkáinkat</a> is megtalálod.</p></div></div></section>
</main>''' + footer(r)
    write('gyumolcsbor.html', pg)


def simple_list(path, title, desc, h1, lead, ids, bg, fg, kicker, photo=None, cur='', extra=''):
    r = ''
    pg = head(title, desc, r, path.split('.')[0]) + header(r, cur)
    ph = (f'<div>{photo}</div>' if photo.startswith('<') else f'<div><img src="{photo}" alt="" loading="lazy"></div>') if photo else ''
    pg += f'''<main><section class="sec" style="background:{bg};color:{fg};padding-top:30px"><div class="wrap split"><div style="display:flex;flex-direction:column;gap:16px">
<p class="breadcrumb" style="color:inherit"><a href="index.html" style="color:inherit">Főoldal</a> / {h1}</p><p class="kicker" style="--accent:{fg}">{kicker}</p>
<h1 class="h2" style="font-size:clamp(30px,7.6vw,86px)">{h1}</h1><p class="lead">{lead}</p></div>{ph}</div></section>
<section class="sec"><div class="wrap">{cards(ids, r)}</div></section>{extra}</main>''' + footer(r)
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
        'friss': 'friss.html', 'secco': 'termek/berry-secco.html', 'palinka': 'palinka.html'}


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
    navcur = {'klasszikus': 'gyumolcsbor.html', 'klara': 'gyumolcsbor.html', 'friss': 'gyumolcsbor.html', 'piri': 'termek/piri-mama-forralt-bora.html',
              'don': 'termek/don-cherry.html', 'secco': 'termek/berry-secco.html', 'palinka': 'palinka.html'}.get(p['line'], '')
    pg += header(r, navcur, res['theme'], BACK.get(p['line'])) + '<main>' + res['html'] + '</main>' + res['bar'] + footer(r)
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
    sbadge = '<div class="badge">Azonnal<br>fogyaszt-<br>ható</div>' if L == 'piri' else ''
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
    crumb_cat = {'klasszikus': ('gyumolcsbor.html', 'Gyümölcsborok'), 'klara': ('gyumolcsbor.html#klara', 'Klára'), 'friss': ('friss.html', 'FRISS'),
                 'secco': ('termek/berry-secco.html', 'Berry Secco'), 'palinka': ('palinka.html', 'Pálinka'), 'csomag': ('csomagok.html', 'Csomagok')}.get(L, ('gyumolcsbor.html', 'Termékek'))
    pg += f'''<main><div class="wrap"><p class="breadcrumb" style="padding-top:4px;color:var(--ink)"><a href="{r}index.html" style="color:inherit">Főoldal</a> / <a href="{r}{crumb_cat[0]}" style="color:inherit">{crumb_cat[1]}</a> / {e(p['name'])}</p></div>
<section class="wrap p-hero"><div class="p-media">{badge(p['id']).replace('pbadge', 'pbadge big')}<div class="arch"><img class="{'pack' if is_pack else ('jar' if p['id'] == 'don-cherry-gyumolcse' else '')}" src="{r}{img}" alt="{e(p['name'])}" width="500" height="1400"></div>{sbadge}</div>
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
<div class="pr"><b>{ft(s['price']) if active else '<span style="font-size:18px">Ár a kampány indulásakor</span>'}</b>{f"<s>{ft(s['old'])}</s>" if active and s.get('old') else ''}</div>{'<small style="font-weight:700;color:#2E8C5A">Ingyenes szállítással</small>' if s['free'] and active else ''}{btn}</div></div>'''


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
<div style="display:flex;flex-direction:column;gap:14px"><h2 class="serif" style="font-size:26px">Tedd mellé</h2>{cards(['friss-malna', 'berry-secco', 'kontyos-borospohar', 'don-cherry-gyumolcse'], r, 'cards cards-4')}</div></div>
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
    pdp.bind(e=e, ft=ft, param=param, ingredients=ingredients, P=P, CAT=CAT, url=url, LINE_LABEL=LINE_LABEL, don_packs=don_packs, TXT=TXT, badge=badge, friss_cut=friss_cut)
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
    simple_list('friss.html', 'FRISS gyümölcsborok | Kontyos', 'FRISS: gyümölcsbor és almabor könnyed találkozása – narancs, eper, málna, meggy, mind 2190 Ft.', 'FRISS',
                TXT['friss2'], [p['id'] for p in CAT if p['line'] == 'friss'], '#F28C28', '#1B2A5C', 'Könnyű gyümölcsborok', friss_cut(''), 'friss.html',
                fruit_selector('', ['friss-narancs', 'friss-eper', 'friss-malna', 'friss-meggy']))
    simple_list('palinka.html', 'Gyümölcspálinka | Kontyos', 'Szamóca-, meggy-, birs-, körte- és szilvapálinka a Kontyostól.', 'Pálinka',
                'Gyümölcspálinkák a Kontyos Borháztól.', [p['id'] for p in CAT if p['line'] == 'palinka'], '#2A2118', '#E8D29A', 'Párlatok', None, 'palinka.html')
    for p in CAT:
        product(p)
    ujbor_page()
    bf_page()
    xmas_page()
    cart()
    search_page()
    packs_page()
    fairs_page()
    checkout()
    thanks()
    info()
    print('OK', len(CAT), 'termék')


if __name__ == '__main__':
    main()
