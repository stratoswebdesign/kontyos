# Termékoldal-sablonok a design (Termek*.dc.html) alapján – termékcsaládonként saját arculat.
# A build.py importálja és tölti fel a közös segédfüggvényekkel (bind()).
import re
import json

# Prata HU nagybetűk szélessége em-ben (assets/fonts/PrataHU-Regular.woff2 hmtx alapján)
PRATA_W = {'A': 0.719, 'B': 0.745, 'C': 0.745, 'D': 0.854, 'E': 0.721, 'F': 0.672, 'G': 0.813, 'H': 0.865, 'I': 0.374, 'J': 0.448, 'K': 0.738, 'L': 0.675, 'M': 1.012, 'N': 0.814, 'O': 0.862, 'P': 0.684, 'Q': 0.862, 'R': 0.727, 'S': 0.666, 'T': 0.7, 'U': 0.809, 'V': 0.681, 'W': 1.081, 'X': 0.76, 'Y': 0.657, 'Z': 0.685, 'Á': 0.719, 'É': 0.721, 'Í': 0.374, 'Ó': 0.862, 'Ö': 0.862, 'Ő': 0.862, 'Ú': 0.809, 'Ü': 0.809, 'Ű': 0.809, '-': 0.349, '.': 0.219, ' ': 0.239, '%': 0.829}


G = {}


def bind(**kw):
    G.update(kw)


def _(name):
    return G[name]


SHIP = [('Várható kézbesítés', 'GLS 3–5, MPL 1–3 munkanap'),
        ('Szállítás', '1 800 Ft-tól · 25 000 Ft felett ingyenes'),
        ('Fizetés', 'Bankkártya (SimplePay), átutalás, utánvét · regisztráció nélkül is')]

SHORT = {'friss-narancs': 'Narancs', 'friss-eper': 'Eper', 'friss-malna': 'Málna', 'friss-meggy': 'Meggy',
         'berry-secco': 'Erdei gyümölcs', 'berry-secco-tonic': 'Eper és Tonik', 'berry-secco-yuzu-lime': 'Yuzu és Lime',
         'szamocapalinka': 'Szamóca', 'birspalinka': 'Birs', 'meggypalinka': 'Meggy', 'kortepalinka': 'Körte', 'szilvapalinka': 'Szilva',
         'piri-mama-forralt-bora': 'Klasszikus',
         'edes-meggybor': 'Meggy', 'edes-eperbor': 'Eper', 'edes-ribizlibor': 'Ribizli', 'edes-kajszibor': 'Kajszi', 'edes-oszibarackbor': 'Őszibarack',
         'edes-szilvabor': 'Szilva', 'edes-bodza-almabor': 'Bodza-alma', 'szaraz-meggybor': 'Száraz meggy',
         'klara-edes-malnabor': 'Málna', 'klara-szaraz-roze-eperbor': 'Rozé eper', 'klara-szaraz-barrique-meggybor': 'Barrique meggy', 'klara-edes-afonyabor': 'Áfonya',
         'don-cherry': 'Vermut 0,75 l', 'don-cherry-gyumolcse': 'Vermut meggyel', 'narancsos-piri-mama-forralt-bora': 'Narancsos', 'epres-piri-mama-forralt-bora': 'Epres', 'piri-mama-forro-itala-0': '0% alkohol'}
BIG = {'friss-narancs': 'NARANCS', 'friss-eper': 'EPER', 'friss-malna': 'MÁLNA', 'friss-meggy': 'MEGGY',
       'berry-secco': 'ERDEI', 'berry-secco-tonic': 'TONIK', 'berry-secco-yuzu-lime': 'YUZU'}


def e(s):
    return _('e')(s)


def ft(n):
    return _('ft')(n)


def param(p, k):
    return _('param')(p, k)


def stars_link(p, color, empty_text=True):
    if p['rcount']:
        r = str(p['rating']).replace('.', ',')
        return f'<a class="pd-stars" href="#ertekelesek"><span style="color:{color}">★★★★★</span><span>{r} · {p["rcount"]} vélemény</span></a>'
    return '<a class="pd-stars" href="#ertekelesek"><span>Még nincs értékelés – legyél te az első</span></a>' if empty_text else ''


def short_desc(p):
    t = re.split(r'\s*Összetevők?:', p['short'])[0].strip()
    if p['line'] == 'don':
        t = re.split(r'(?<=!)\s|\s*Hogyan készítsd', t)[0].strip()
    return t


def ingr(p):
    v = _('ingredients')(p)
    if v.startswith('lásd'):
        o = param(p, 'Összetétel')
        if o:
            return o
    return v


def allergens(p):
    t = (p['short'] + ' ' + ' '.join(p['long'])).lower()
    out = []
    if 'szulf' in t:
        out.append('szulfitot tartalmaz')
    if 'kinin' in t:
        out.append('kinint tartalmaz')
    return ' · '.join(out)


SHIP_SHORT = [('Kézbesítés', '1–5 munkanap'), ('Szállítás', '1 800 Ft-tól · 25 000 Ft felett ingyen'), ('Fizetés', 'Kártya, átutalás, utánvét')]


def ship_dl(rule, dd, fs=13, short=False):
    return '<dl class="pd-ship" style="--rule:' + rule + ';font-size:' + str(fs) + 'px">' + ''.join(
        f'<div><dt>{a}</dt><dd style="color:{dd}">{b}</dd></div>' for a, b in (SHIP_SHORT if short else SHIP)) + '</dl>'


def kv(rows, rule):
    return '<dl class="pd-kv" style="--rule:' + rule + '">' + ''.join(
        f'<div><dt>{e(a)}</dt><dd{" style=font-weight:800" if a == "Allergén" else ""}>{e(b)}</dd></div>' for a, b in rows if b) + '</dl>'


def legal_rows(p):
    wine = p['line'] in ('klasszikus', 'klara', 'friss')
    vol = param(p, 'Űrmérték') or param(p, 'Kiszerelés')
    return [('Megnevezés', p['name'] + (' (gyümölcsbor)' if wine else '')),
            ('Alkoholtartalom', param(p, 'Alkohol')),
            ('Névleges térfogat', (vol + ' ℮') if vol else None),
            ('Összetevők', ingr(p)),
            ('Allergén', allergens(p)),
            ('Tételazonosító', 'a címkén')]


def legal_note(p):
    a = (param(p, 'Alkohol') or '').strip()
    if a.startswith('0'):
        return 'Alkoholmentes ital. A termékadatok a kontyos.hu alapján.'
    return 'Alkoholtartalmú italt 18 éven aluli személy részére nem értékesítünk. Fogyaszd mértékkel!'


def info(p, c):
    """Leírás + paraméterek + kötelező adatok. Desktopon két oszlop, mobilon lenyíló blokkok (a mobil design szerint)."""
    long = ''.join(f'<p>{e(x)}</p>' for x in (p['long'] or [p['short']])) if p['id'] != 'meggymag-parna' else f'<p>{e(p["short"])}</p>'
    params = kv(p['params'], c['rule'])
    lab = f'style="color:{c["accent"]}"'
    desk = f'''<section class="pd-info only-d" style="background:{c.get('infobg', '#fff')}"><div class="pd-wrap pd-cols">
<div class="pd-desc"><p class="pd-lab" {lab}>LEÍRÁS</p><h2 style="{c['h2']}">{e(p['name'])}</h2>{long}</div>
<div class="pd-side"><div><p class="pd-lab" {lab}>PARAMÉTEREK</p><div style="border-top:1px solid {c['ink']}">{params}</div></div></div></div></section>'''
    acc = lambda t, body, op='': f'<details class="pd-acc" style="border-color:{c["ink"]}"{op}><summary style="{c.get("accfont", "")}">{t}<span aria-hidden="true">+</span></summary><div>{body}</div></details>'
    ship_txt = '<p>MPL csomagautomata / PostaPont / posta: 1 800 Ft, GLS csomagpont: 2 100 Ft – 25 000 Ft felett ingyenes. GLS házhoz: 2 400 Ft, 25 000 Ft felett ingyenes. Személyes átvétel Klárafalván. Regisztráció nélkül is rendelhetsz.</p>'
    mob = f'''<section class="pd-info only-m"><div class="pd-wrap">{acc('Leírás', long, ' open')}{acc('Paraméterek', params)}{acc('Összetevők, allergének', f'<p>{e(ingr(p))}</p>' + (f'<p><b>{e(allergens(p))}</b></p>' if allergens(p) else ''))}{acc('Szállítás', ship_txt)}</div></section>'''
    return desk + mob


def reviews(p, c):
    if p['rcount']:
        arts = ''.join(f'<article style="border-color:{c["rborder"]}"><span style="color:{c["accent2"]}">★★★★★</span><p>„{e(x["t"])}”</p><small>{e(x["n"])} · {e(x["d"])}</small></article>' for x in p['reviews'])
        head = f'<div class="pd-rhead"><div><p class="pd-lab" style="color:{c["accent"]}">VÁSÁRLÓI VÉLEMÉNYEK</p><div class="pd-rnum"><b style="{c.get("numfont", "")}">{str(p["rating"]).replace(".", ",")}</b><span>{p["rcount"]} vélemény alapján · a webshop értékelései</span></div></div></div>'
        return f'<section id="ertekelesek" class="pd-wrap pd-reviews">{head}<div class="pd-rlist">{arts}</div></section>'
    return f'''<section id="ertekelesek" class="pd-wrap pd-reviews"><p class="pd-lab" style="color:{c["accent"]}">VÁSÁRLÓI VÉLEMÉNYEK</p>
<div class="pd-noreview" style="border-color:{c['ink']}"><span>Erről a termékről még nincs értékelés.</span><b>Kóstoltad? Élesben itt írhatod meg elsőként.</b></div></section>'''


def buy_core(p, c, qty=True):
    """Ár + 1/3/6 + mennyiség + kosár gomb + ingyenes szállítás csík – a data-* kötéseket az app.js kezeli."""
    r = '../'
    tier = p['tier']
    unit_l = param(p, 'Egységár') or ''
    packs = ''
    if tier:
        pct = round((1 - tier[1] / p['price']) * 100)
        packs = '<div class="pd-packs" role="group" aria-label="Kiszerelés" style="--sel:' + c.get('packsel', '#fff') + '">' + ''.join(
            f'<button type="button" data-pack="{n}" aria-pressed="{"true" if n == 1 else "false"}"><strong>{n} palack</strong><span>{ft(tier[1] if n >= tier[0] else p["price"])}/db</span>{f"<em>−{pct}%</em>" if n >= tier[0] else ""}</button>' for n in (1, 3, 6)) + '</div>'
    q = '''<div class="pd-qty" role="group" aria-label="Mennyiség"><button type="button" data-dec aria-label="Kevesebb">−</button><span data-q id="q" aria-live="polite">1</span><button type="button" data-inc aria-label="Több">+</button></div>''' if qty else '<span data-q id="q" hidden>1</span>'
    return f'''<div data-buy="{p['id']}" class="pd-buy">
<div class="pd-price"><b data-unit style="{c.get('pricefont', '')}">{ft(p['price'])}</b><span>{e(unit_l)}</span></div>
{packs}
<div class="pd-addrow">{q}<button type="button" class="pd-add" style="background:{c['btn']}" data-add="{p['id']}" data-qty-from="#q">{c.get('addlabel', 'Kosárba')} · <span data-line>{ft(p['price'])}</span></button></div>
<div class="pd-free"><span data-free-text></span><div class="bar"><i data-free-bar></i></div></div></div>'''


def buybar(p, c):
    return f'''<div class="buybar pd-buybar" style="border-top:2px solid {c.get('barline', c['accent'])}"><div class="pb"><b data-line>{ft(p['price'])}</b><small><span data-q>1</span> db</small></div><div class="qty"><button type="button" data-dec aria-label="Kevesebb">−</button><span data-q>1</span><button type="button" data-inc aria-label="Több">+</button></div><button class="btn" style="background:{c['btn']}" type="button" data-add="{p['id']}" data-qty-from="#q">Kosárba</button></div>'''


def sold_out(p):
    return '<div class="pd-addrow"><button class="pd-add" type="button" disabled style="background:#8E95A8">Elfogyott – élesben itt kérhető értesítés</button></div>'


def crumbs(items, style=''):
    r = '../'
    return '<nav class="pd-crumb" aria-label="Morzsamenü" style="' + style + '">' + ' / '.join(
        (f'<a href="{r}{h}">{t}</a>' if h else t) for t, h in items) + '</nav>'


def mini_card(x, ring, kicker=None, ink=None):
    r = '../'
    return f'''<a class="pd-mcard" href="{r}{_('url')(x)}"><span style="border-color:{ring}">{_('badge')(x['id'])}<img src="{r}{x['img']}" alt="{e(x['name'])}" loading="lazy"><span class="tx"><span class="k">{e(kicker or _('LINE_LABEL')[x['line']].upper())}</span><span class="n" style="color:{ink or '#1B2A5C'}">{e(x['name'])}</span><span class="p">{ft(x['price']) if x['avail'] else 'Elfogyott'}</span></span></span></a>'''


def cross(ids, title, ring_of, h2style=''):
    P = _('P')
    return f'<section class="pd-wrap pd-cross"><h2 style="{h2style}">{title}</h2><div class="pd-cgrid">' + ''.join(mini_card(P[i], ring_of(P[i])) for i in ids if i in P) + '</div></section>'


def prem_buy(p, kind):
    """Klára (k) és Don Cherry (d) vásárlási blokk: 1/3/6 palack, saját arculatú ingyenes szállítás csík."""
    tier = p['tier']
    unit6 = tier[1] if tier else p['price']
    lab = 'üveg' if p['id'] == 'don-cherry-gyumolcse' else 'palack'
    packs = f'<div class="pd-ppacks {kind}" role="group" aria-label="Kiszerelés">' + ''.join(
        f'<button type="button" data-pack="{n}" aria-pressed="{"true" if n == 1 else "false"}"><strong>{n} {lab}</strong><span>{ft(unit6 if (tier and n >= tier[0]) else p["price"])} / {lab}</span>{f"<em>−{round((1 - tier[1] / p['price']) * 100)}%</em>" if tier and n >= tier[0] else ""}</button>' for n in (1, 3, 6)) + '</div>'
    return f'''<div class="pd-pbox {kind}" data-buy="{p['id']}">
{packs}
<div class="pd-kbuy"><span class="pr" data-unit>{ft(p['price'])}</span><span data-q id="q" hidden>1</span><button type="button" class="pd-kbtn" data-add="{p['id']}" data-qty-from="#q">KOSÁRBA · <span data-line>{ft(p['price'])}</span></button></div>
<div class="pd-pfree {kind}"><span data-free-text{' data-free-short' if kind == 'k' else ''}></span><div class="trk"><i data-free-bar></i></div></div></div>'''


UPSELL = {
    'klasszikus': lambda p: ['kontyos-borospohar', 'szaraz-meggybor' if p['id'] != 'szaraz-meggybor' else 'edes-meggybor', 'don-cherry'],
    'klara': lambda p: ['kontyos-borospohar', next(i for i in ('klara-szaraz-roze-eperbor', 'klara-szaraz-barrique-meggybor', 'klara-edes-malnabor') if i != p['id']), 'don-cherry'],
    'piri': lambda p: ['piri-mama-bogreje', next(i for i in ('narancsos-piri-mama-forralt-bora', 'epres-piri-mama-forralt-bora', 'piri-mama-forralt-bora') if i != p['id']), 'kontyos-szovettaska'],
    'don': lambda p: ['don-cherry-gyumolcse' if p['id'] == 'don-cherry' else 'don-cherry', 'kontyos-borospohar', 'klara-szaraz-barrique-meggybor'],
    'friss': lambda p: [next(i for i in ('friss-eper', 'friss-malna', 'friss-meggy') if i != p['id']), 'berry-secco', 'kontyos-borospohar'],
    'secco': lambda p: [next(i for i in ('berry-secco-tonic', 'berry-secco-yuzu-lime', 'berry-secco') if i != p['id']), 'friss-eper', 'kontyos-borospohar'],
    'palinka': lambda p: [next(i for i in ('szamocapalinka', 'birspalinka', 'meggypalinka') if i != p['id']), 'meggymag-parna', 'don-cherry'],
    'csomag': lambda p: ['kontyos-borospohar', 'kontyos-szovettaska', 'don-cherry'],
    'kiegeszito': lambda p: ['edes-meggybor', 'klara-edes-malnabor', 'piri-mama-forralt-bora'],
}


def upsell(p, kind=''):
    """Kis „illik mellé” csík a vásárlási blokk alatt – összeillő termékek egy kattintásos kosárba tétellel."""
    r = '../'
    P = _('P')
    ids = [i for i in UPSELL.get(p['line'], lambda p: [])(p) if i in P and P[i]['avail'] and i != p['id']][:3]
    if not ids:
        return ''
    items = ''.join(f'''<li><a href="{r}{_('url')(P[i])}" class="im">{_('badge')(i).replace('pbadge', 'pbadge xs')}<img src="{r}{P[i]['img']}" alt="" loading="lazy"></a><a href="{r}{_('url')(P[i])}" class="nm">{e(P[i]['name'])}<small>{ft(P[i]['price'])}</small></a><button type="button" data-add="{i}" aria-label="{e(P[i]['name'])} kosárba">+</button></li>''' for i in ids)
    return f'<div class="pd-ups {kind}"><p>Illik mellé</p><ul>{items}</ul></div>'


# ---------------------------------------------------------------- KLASSZIKUS (Termek.dc)
def caption(p):
    m = re.search(r'100%\s+(?:[\w\-]+\s+)*?([\w\-]+(?:ből|ból))', p['short'])
    return '100% ' + (m.group(1).split('-')[-1] if m else 'gyümölcsből')


def bigword(p):
    w = p['name'].replace('Édes ', '').replace('Száraz ', '')
    return w.upper()


def t_klasszikus(p):
    r = '../'
    P, CAT = _('P'), _('CAT')
    vol = param(p, 'Űrmérték') or '750 ml'
    alc = (param(p, 'Alkohol') or '').replace(' %vol', '% vol').replace('%vol', '% vol')
    taste = param(p, 'Édes') or ''
    cap = caption(p)
    c = dict(accent=p['accent'], accent2='#EF4E73', ink='#1B2A5C', rule='#E2DACB', legalbg='#F3EEE5', btn='#034EA2',
             h2="font-family:var(--serif);font-weight:800;font-size:clamp(30px,3vw,42px);line-height:1.05", rborder='#E2DACB', packsel=p['arch'])
    gal = [(r + p['tight'], 'Palack', 'contain'), (r + 'img/photo/bottles_shadow.webp', 'Hangulatkép', 'cover'), (r + 'img/photo/borhaz.webp', 'A Borház', 'cover')]
    thumbs = ''.join(f'<button type="button" data-gal="{s}" data-fit="{f}" aria-label="{l}" aria-pressed="{"true" if i == 0 else "false"}"><img src="{s}" alt=""></button>' for i, (s, l, f) in enumerate(gal))
    bw = bigword(p)
    # nagybetűs Prata HU: a szó tényleges szélességéből (em) számolt méret, hogy egy sorban maradjon a dobozban
    em = sum(PRATA_W.get(ch, 0.75) + 0.02 for ch in bw.upper()) + 0.04
    fsz = f'min(70px, calc(100cqw / {em:.2f}))'
    sibs = [x['id'] for x in CAT if x['line'] == 'klasszikus' and x['id'] != p['id']]
    cross_ids = (['szaraz-meggybor', 'klara-szaraz-barrique-meggybor', 'friss-meggy', 'don-cherry'] if 'meggy' in p['id'] else sibs[:2] + ['klara-edes-malnabor', 'friss-' + ('eper' if 'eper' in p['id'] else 'malna')])
    cross_ids = [i for i in cross_ids if i != p['id']][:4]
    ring = {'klara': '#E8DCE0', 'friss': '#F28C28', 'don': '#5FB8B3'}
    buy = buy_core(p, c) if p['avail'] else sold_out(p)
    html = f'''{u_hero(p)}
{info(p, c)}
<section class="pd-illu noimg duo"><div class="box"><h2>Mitől 100%-os a gyümölcsbor?</h2><p>{_('TXT')['klassz2']}</p><a href="{r}rolunk.html">Így készülnek a boraink →</a></div>
<div class="box"><p class="kick">A kiszerelésről</p><h2>Mert a jóból több jár.</h2><p>Hiszünk abban, hogy <b>fél liter a kedvenc gyümölcsborodból nem elég.</b> Ezért gyümölcsborainkat és vermutjainkat a megszokott <b>0,75 literes palackban</b> kínáljuk.</p><p>Forralt borainkból <b>1 liter</b> jut a közös pillanatokra, EASY CIDER-ünk pedig praktikus <b>0,33 literes</b> kiszerelésben frissít fel.</p></div></section>
{_('torta_block')(r, True) if p['id'] == 'edes-ribizlibor' else ''}
{reviews(p, c)}
{cross(cross_ids, 'Ha a meggyet szereted' if 'meggy' in p['id'] else 'Ha ezt szereted', lambda x: ring.get(x['line'], '#1B2A5C'), 'font-family:var(--serif);font-weight:700;font-size:clamp(36px,4vw,54px)')}'''
    return dict(html=html + legal_strip(p), page=ucfg(p)['bg'], ink='#1B2A5C', theme='pill', bar=buybar(p, dict(c, btn=ucfg(p)['btn'])) if p['avail'] else '')


# ---------------------------------------------------------------- KLÁRA (TermekKlara.dc)
def t_klara(p):
    r = '../'
    CAT = _('CAT')
    vol = param(p, 'Űrmérték') or '750 ml'
    alc = (param(p, 'Alkohol') or '').replace(' %vol', '% vol')
    zar = (param(p, 'Palackzárás') or '').replace('csavarzáras', 'csavarzár').replace('Csavarzáras', 'csavarzár')
    c = dict(accent='#C0284A', accent2='#C0284A', ink='#1B2A5C', rule='#EEE8E1', legalbg='#FAF7F4', btn='#1B2A5C', rborder='#EEE8E1',
             h2="font-family:var(--serif);font-weight:400;font-size:clamp(30px,3vw,42px);line-height:1.05", accfont='font-weight:400')
    tier = p['tier']
    tiertxt = f'6 palacktól {ft(tier[1])} / palack · ' if tier else ''
    nm = p['name'].replace('Klára ', '')
    if p['avail']:
        buy = prem_buy(p, 'k')
    else:
        buy = '<div class="pd-kbuy"><span class="pr" style="font-size:24px">Elfogyott</span><button type="button" class="pd-kbtn" disabled style="opacity:.5">ÉRTESÍTÉST KÉREK</button></div>'
    others = [x for x in CAT if x['line'] == 'klara' and x['id'] != p['id']]

    def taste(x):
        t = (param(x, 'Édes') or '').upper()
        return t + (' · 8 HÓNAP TÖLGY' if 'barrique' in x['id'] else '')
    row = ''.join(f'''<a href="{x['id']}.html"><img src="{r}{x['tight']}" alt="{e(x['name'])}" loading="lazy"{' style="opacity:.45"' if not x['avail'] else ''}><span class="k">{taste(x)}</span><span class="n">{e(x['name'].replace('Klára ', '').replace('édes ', '').replace('száraz ', '').capitalize())}</span><span class="p"{' style="color:#6A6F7E"' if not x['avail'] else ''}>{ft(x['price']) if x['avail'] else 'Elfogyott – értesítést kérek'}</span></a>''' for x in others)
    html = f'''{u_hero(p)}
{info(p, c)}
<section class="pd-wrap pd-klstory"><img src="{r}img/photo/klara_pohar.webp" alt="Klára édes málnabor palack pezsgőspohárral és friss málnával" loading="lazy">
<div><p class="q">„A gyümölcskertek istennője.”</p>
<p>A KLÁRA prémium sorozatunkat a gyümölcsök iránti rajongásunk, a borkészítés szenvedélye és Klárafalva szeretete ihlette. Borainkat válogatott gyümölcsökből, különös gondossággal készítjük, hogy minden palack egyedi élményt nyújtson.</p></div></section>
{reviews(p, c)}
<section class="pd-wrap pd-klrow"><p class="pd-lab" style="text-align:center;color:#6A6F7E;letter-spacing:.3em">A KLÁRA SOR TÖBBI TAGJA</p><div>{row}</div></section>'''
    cb = dict(c, btn='#1B2A5C', barline='#1B2A5C')
    return dict(html=html + legal_strip(p), page='#FFFFFF', ink='#1B2A5C', theme='pill', bar=buybar(p, cb) if p['avail'] else '')


# ---------------------------------------------------------------- PIRI MAMA (TermekPiri.dc)
def t_piri(p):
    r = '../'
    CAT, P = _('CAT'), _('P')
    alc = param(p, 'Alkohol') or ''
    abv = '0% ALKOHOL' if alc.strip().startswith('0') else alc.replace(' %vol', '% VOL').replace('%vol', '% VOL').upper()
    accent = p['accent'] if p['accent'] != p['arch'] else '#2B3B78'
    c = dict(accent=accent, accent2='#E2574C', ink='#1B2A5C', rule='#E2DACB', legalbg='#F7F1E8', btn='#1B2A5C', rborder='#E2DACB',
             h2="font-family:var(--serif);font-weight:800;font-size:38px;line-height:1.02")
    vs = [x for x in CAT if x['line'] == 'piri']
    chips = '<div class="pd-chips" role="group" aria-label="Íz">' + ''.join(
        f'<a href="{x["id"]}.html"{" aria-current=page" if x["id"] == p["id"] else ""}><i style="background:{x["arch"] if x["arch"] != "#2B3B78" else "#1B2A5C"}"></i>{SHORT[x["id"]]}</a>' for x in vs) + '</div>'
    full = p['name']
    buy = f'''<div class="pd-pbuy" data-buy="{p['id']}"><span class="pr">{ft(p['price'])}</span><div class="pd-qty"><button type="button" data-dec aria-label="Kevesebb">−</button><span data-q id="q">1</span><button type="button" data-inc aria-label="Több">+</button></div><button type="button" class="pd-add" style="background:#1B2A5C" data-add="{p['id']}" data-qty-from="#q">Kosárba · <span data-line>{ft(p['price'])}</span></button></div>
<div class="pd-free"><span data-free-text></span><div class="bar"><i data-free-bar></i></div></div>'''
    mug = P['piri-mama-bogreje']
    html = f'''{u_hero(p)}
<div class="pd-pairband"><section class="pd-wrap pd-pair"><div class="mug"><img src="{r}{mug['img']}" alt="PIRI Mama bögréje 0,32 l" loading="lazy"><div><span class="k">MELLÉ</span><strong>PIRI Mama bögréje</strong><span>0,32 l · {ft(mug['price'])}</span><button type="button" data-add="piri-mama-bogreje">Hozzáadom</button></div></div>
<div class="fair"><span class="k">ADVENTI VÁSÁROK</span><strong>Kóstold a standunknál</strong><span>Szeged · Óbuda · Győr · Szombathely · Veszprém · Pécs · Nyíregyháza</span><a href="{r}vasarok.html">Térkép és menetrend →</a></div></section></div>
{info(p, c)}
<section class="pd-video" aria-label="PIRI Mama hangulatvideó"><video src="{r}img/video/piri_hangulat.mp4" poster="{r}img/video/piri_hangulat.webp" autoplay muted loop playsinline preload="metadata"></video></section>
{reviews(p, c)}
<section class="sec pk-fblock pd-fpack"><div class="wrap" style="display:flex;flex-direction:column;gap:22px"><p class="kicker">PIRI Mama</p><h2 class="h2" style="font-size:clamp(26px,3vw,40px)">Forralt csomag</h2>
<div class="packs-grid">{_('pack_box')(_('SP')['forralt-6'], r, primary=True)}</div></div></section>
'''
    return dict(html=html + legal_strip(p), page='#111833', ink='#1B2A5C', theme='pill', bar=buybar(p, dict(c, barline='#DBB879')))


# ---------------------------------------------------------------- DON CHERRY (TermekDon.dc)
def t_don(p):
    r = '../'
    P = _('P')
    jar = p['id'] == 'don-cherry-gyumolcse'
    vol = param(p, 'Űrmérték') or ''
    alc = (param(p, 'Alkohol') or '').replace(' %', '% vol').replace('%vol', '% vol')
    c = dict(accent='#2E8C86', accent2='#C8282E', ink='#2A1416', rule='#EAF3F2', legalbg='#F2FAF9', btn='#C8282E', rborder='#D6ECEA',
             h2="font-family:var(--sans);font-weight:800;font-size:clamp(30px,3vw,42px);line-height:1.05", numfont='font-family:var(--sans)', accfont='font-family:var(--serif)')
    sub = 'ÉDES MEGGYVERMUT · 0,75 L' if not jar else 'MEGGYVERMUT ÉS MEGGY · 200 ML + 110 G'
    pair = P['don-cherry-gyumolcse'] if not jar else P['don-cherry']
    pair_desc = '200 ml édes meggyvermut és 110 g magozott meggy egy üvegben.' if not jar else 'Prémium minőségű édes meggyvermut 0,75 l-es palackban – friss meggy ágyon érlelt meggybor, dió pálinka, fűszerek.'
    contains = ', '.join(x.replace(' tartalmaz', '') for x in allergens(p).split(' · ') if x)
    html = f'''{u_hero(p)}
{_('don_packs')('../')}
{info(p, c)}
<section class="pd-wrap pd-dphotos"><img src="{r}img/photo/don_cimke.webp" alt="Don Cherry címke közelről, meggyekkel" loading="lazy"><img src="{r}img/photo/don_ajandek.webp" alt="Don Cherry palack és üveg meggy felülnézetből" loading="lazy"></section>
<section class="pd-wrap pd-drink"><p class="pd-lab" style="color:#2E8C86;letter-spacing:.3em">ÍGY IDD</p><p class="intro">Aperitifként, shotként és koktélként is működik – válaszd az alkalomhoz illőt!</p>
<div><div><span class="k">8 CL · JÉG · NARANCS</span><b>Aperitifként</b><span>8 cl Don Cherry, jég és egy narancskarika. Frissítő, társasági ital, hosszan kitartó meggyes aromával.</span></div>
<div><span class="k">4 CL · 1 MEGGYSZEM</span><b>Shotként</b><span>Egy 5 cl-es pohár aljára tegyél egy meggyszemet, önts rá 4 cl Don Cherryt, és idd meg két kortyban. Rövid, intenzív élmény, ideális buliindító.</span></div></div></section>
<section class="pd-wrap pd-cocktails"><h2 class="ck-h">Koktélként</h2><div class="cgrid">
<article><img src="{r}img/cocktail/negroni.webp" alt="Don Cherry Negroni" loading="lazy"><h3>Don Cherry Negroni</h3><p class="d">Karakteres, gyümölcsös, kissé kesernyés – mégis selymesen fűszeres.</p><ul><li>3 cl Don Cherry</li><li>3 cl gin</li><li>3 cl Campari</li><li>jég, narancshéj</li></ul><p>Önts minden hozzávalót jéggel teli keverőpohárba, keverd össze, majd szűrd egy jéggel teli whiskys pohárba. Narancshéjjal díszítsd.</p></article>
<article><img src="{r}img/cocktail/americano.webp" alt="Don Cherry Americano" loading="lazy"><h3>Don Cherry Americano</h3><p class="d">Erőteljes, elegáns és modern. Nem harsány, de nem is marad észrevétlen.</p><ul><li>6 cl Don Cherry</li><li>3 cl Campari</li><li>jég, narancskarika vagy narancshéj-spirál</li></ul><p>Öntsd a Don Cherryt és a Camparit egy jéggel teli whiskys pohárba, és keverd össze óvatosan. Díszítsd narancshéjjal.</p></article>
<article><img src="{r}img/cocktail/don-tonic.webp" alt="Don Cherry & Tonic" loading="lazy"><h3>Don Cherry &amp; Tonic</h3><p class="d">Frissítő, meggyes, finoman kesernyés – üde narancsos csavarral.</p><ul><li>1 dl Don Cherry</li><li>1 dl tonic</li><li>jég, meggy és narancskarika</li></ul><p>Tölts meg egy longdrinkes poharat jéggel, öntsd rá a Don Cherryt, majd a tonicot. Óvatosan keverd át, és díszítsd meggyel és narancskarikával.</p></article>
</div></section>
{_('cocktail_packs')(r)}
{reviews(p, c)}
<section class="pd-dpair"><div class="pd-wrap"><img src="{r}{pair['tight']}" alt="{e(pair['name'])}" loading="lazy" class="{'jar' if not jar else ''}">
<div><p class="pd-lab" style="color:#2E8C86;letter-spacing:.3em">A PÁRJA</p><h2>{e(pair['name'])}</h2><p>{pair_desc}</p>
<div class="row"><b>{ft(pair['price'])}</b><button type="button" data-add="{pair['id']}">KOSÁRBA</button><a href="{pair['id']}.html">Részletek →</a></div></div></div></section>'''
    return dict(html=html + legal_strip(p), page=ucfg(p)['bg'], ink='#2A1416', theme='pill', bar=buybar(p, dict(c, barline='#5FB8B3')))


# ---------------------------------------------------------------- FRISS / SECCO / PÁLINKA (TermekFriss/Secco/Palinka.dc)
LINECFG = {
    'friss': dict(page='#FFF6EA', kick='FRISS · KÖNNYŰ GYÜMÖLCSBOR · 0,75 L', kc='#EF4E73', h1w=900, rule='#F1E2CF', theme='pill',
                  crumb=('FRISS', 'termek/friss-malna.html'), cross=['konnyu-trio', 'berry-secco', 'bubi-paros', 'kontyos-borospohar']),
    'secco': dict(page='#F7F7FB', kick='BERRY SECCO · ÉDES HABZÓ GYÜMÖLCSBOR · 0,75 L', kc='#E86A9A', h1w=900, rule='#E3E6F2', theme='pill',
                  crumb=('Berry Secco', 'termek/berry-secco.html'), cross=['bubi-paros', 'kontyos-borospohar', 'friss-narancs', 'friss-eper']),
    'palinka': dict(page='#F4EFE6', kick='KISÜSTI PÁLINKA · 46% · {vol}', kc='#A8823C', h1w=500, rule='#E3DACB', theme='pill',
                    crumb=('Pálinka', 'termek/szamocapalinka.html'), cross=['don-cherry', 'klara-szaraz-barrique-meggybor', 'meggymag-parna', 'klara-edes-malnabor']),
}


SERVE = {'berry-secco': 'Alaposan behűtve, piros gyümölcsökkel, pár szem jégkockával.', 'berry-secco-tonic': 'Behűtve, egy karika lime-mal és jéggel.',
         'berry-secco-yuzu-lime': 'Alaposan behűtve, lime-mal és mentával, pár szem jégkockával.'}


def serve_text(p):
    if p['id'] in SERVE:
        return SERVE[p['id']]
    t = ' '.join(p['long'])
    m = re.search(r'(?:Kínáld[^.]*?|Behűtve[^.!]*)[.!]', t)
    if m:
        s = m.group(0).replace('Kínáld vendégeidnek ', '').strip()
        return s[0].upper() + s[1:]
    return 'Alaposan behűtve, jégkockával.'


def t_fsp(p):
    r = '../'
    CAT, P = _('CAT'), _('P')
    L = p['line']
    cf = LINECFG[L]
    vol = param(p, 'Űrmérték') or param(p, 'Kiszerelés') or ''
    accent = cf['kc']
    fg = p['accent']
    c = dict(accent=accent, accent2=accent, ink='#1B2A5C', rule=cf['rule'], legalbg=cf['page'], btn='#1B2A5C', rborder=cf['rule'],
             h2=f"font-family:var(--serif);font-weight:{cf['h1w']};font-size:38px;line-height:1.02", packsel=p['arch'], accfont=f"font-weight:{cf['h1w']}")
    vs = [x for x in CAT if x['line'] == L]
    chips = '<div class="pd-chips" role="group" aria-label="Íz">' + ''.join(
        f'<a href="{x["id"]}.html"{" aria-current=page" if x["id"] == p["id"] else ""}><i style="background:{_dot(x)}"></i>{SHORT.get(x["id"], x["name"])}</a>' for x in vs) + '</div>'
    kick = cf['kick'].replace('{vol}', vol.replace('500 ml', '0,5 L').replace('ml', 'ML').upper())
    buy = buy_core(p, c) if p['avail'] else sold_out(p)
    tiles = ''.join(f'''<a href="{x['id']}.html" class="tile{' on' if x['id'] == p['id'] else ''}" style="background:{x['arch'] if L == 'friss' else ('rgba(255,255,255,.7)' if L == 'secco' else '#fff')}"><img src="{r}{x['tight']}" alt="" loading="lazy"><strong style="color:{x['accent'] if L == 'friss' else ('#1E1A1D' if L == 'palinka' else x['accent'])}">{SHORT.get(x['id'], '')}</strong></a>''' for x in vs)
    if L == 'friss':
        story = f'''<section class="pd-story f" style="background:{p['arch']};color:{fg}"><div class="pd-wrap"><p aria-hidden="true" class="bigw">{BIG.get(p['id'], '')}</p>
<div class="tx"><h2>{FRISS_H.get(p['id'], _('TXT')['friss1'])}</h2><p class="s">Reduktív eljárással, friss gyümölcsből – könnyű, kellemesen édes, pár szem jéggel is. Négy íz, mind {ft(p['price'])}.</p><div class="tiles">{tiles}</div></div>
{_('friss_cut')(r, 'ph')}</div></section>'''
    elif L == 'secco':
        dots = ''.join(f'<span aria-hidden="true" class="bub" style="left:{x}%;top:{y}%;width:{s}px;height:{s}px"></span>' for x, y, s in [(6, 20, 26), (12, 62, 14), (30, 14, 10), (48, 72, 22), (66, 18, 16), (84, 64, 12), (92, 24, 20)])
        alc = (param(p, 'Alkohol') or '').replace(' %vol', '%').replace('%vol', '%')
        story = f'''<section class="pd-story s" style="background:{p['arch']};color:{fg}">{dots}<div class="pd-wrap"><div class="tx"><p class="pd-lab">ÍGY KÍNÁLD</p><h2>{e(serve_text(p))}</h2><p class="s">Habzó, édes, {alc} – a buborékok kedvelőinek.</p></div>
<div class="tiles big">{tiles}</div></div></section>'''
    else:
        facts = [(PAL_ICO['still'], 'HAGYOMÁNYOS KISÜSTI', 'Gyümölcsből cefrézve, hagyományos kisüsti eljárással főzve.'),
                 (PAL_ICO['drop'], '46% ALKOHOL', 'Karakteres párlat, 46%-os alkoholtartalommal.'),
                 (PAL_ICO['snow'], 'PINCEHIDEGEN', 'Enyhén behűtve ajánljuk, hogy a gyümölcsös aromák szépen érvényesüljenek.')]
        story = f'''<section class="pd-story p"><div class="pd-wrap"><div class="tx"><h2>Kisüsti. Tisztán gyümölcsből.</h2><div class="facts ico">{''.join(f'<div>{i}<strong>{a}</strong><span>{b}</span></div>' for i, a, b in facts)}</div></div>
<div class="tiles big">{tiles}</div></div></section>'''
    rating = stars_link(p, accent)
    html = f'''{u_hero(p)}
{story}
{info(p, c)}
{reviews(p, c)}
{cross(cf['cross'], 'Mellé ajánljuk', lambda x: cf['rule'], 'font-family:var(--serif);font-weight:700;font-size:clamp(34px,3.6vw,48px)')}'''
    return dict(html=html + legal_strip(p), page=ucfg(p)['bg'], ink='#1B2A5C', theme='pill', bar=buybar(p, dict(c, barline=p['arch'])) if p['avail'] else '')


_ICO = 'class="pico" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
PAL_ICO = {  # pálinka termékoldal: vonalas arany ikonok (Sanyi mintája, 11-04)
    'still': f'<svg {_ICO}><path d="M8 44a17 12 0 1 0 34 0a17 12 0 1 0-34 0z"/><path d="M8 44h34"/><path d="M15 59h20"/><path d="M19 56v3M31 56v3"/><path d="M17 33c0-7 4-11 8-11s8 4 8 11"/><path d="M25 22v-4"/><path d="M25 18c9-8 21-8 28 2l1 8"/><path d="M48 28h12v20H48z"/><path d="M51 34h6M51 40h6"/><path d="M54 48v8"/></svg>',
    'drop': f'<svg {_ICO}><path d="M32 6C24 18 14 28 14 40a18 18 0 0 0 36 0C50 28 40 18 32 6z"/><text x="32" y="45" text-anchor="middle" font-family="Montserrat,Arial,sans-serif" font-weight="800" font-size="13" fill="currentColor" stroke="none">46%</text></svg>',
    'snow': f'<svg {_ICO}><path d="M32 6v52M9.5 19l45 26M9.5 45l45-26"/><path d="M26 10l6 6 6-6M26 54l6-6 6 6"/><path d="M9 26l8-2-2-8M55 38l-8 2 2 8M9 38l8 2-2 8M55 26l-8-2 2-8"/></svg>',
}

FRISS_H = {'friss-narancs': 'Narancsbor és almabor. Frissítő harmóniában.', 'friss-eper': 'Eperbor és almabor. Frissítő harmóniában.',
           'friss-malna': 'Málnabor és almabor. Frissítő harmóniában.', 'friss-meggy': 'Meggybor és almabor. Frissítő harmóniában.'}


def _dot(x):
    a = x['accent']
    return x['arch'] if a.upper() in ('#FFFFFF', '#FFF6EA', '#1B2A5C') else a


# ================================================================ EGYSÉGES TERMÉKOLDAL-HERO (Klára-elrendezés minden termékcsaládra)
# Sanyi (2026-11-01): egy elrendezés mindenhol – bal: leírás, közép: nagy palack árnyék nélkül, jobb: ízválasztó, 1/3/6, +/-, nagyobb betű.
# A háttér termékcsaládonként más (minél népibb a termék, annál színesebb; a prémium fehér), ízenként nem változik.
UCFG = {
    'klasszikus': dict(bg='#E6EEDF', ink='#1B2A5C', muted='#4F5868', line='rgba(27,42,92,.16)', panel='rgba(255,255,255,.6)', btn='#1B2A5C', btnfg='#fff', crumb=('Klasszikus', 'gyumolcsbor.html#klasszikus')),
    'klara': dict(bg='#FFFFFF', ink='#1B2A5C', muted='#6A6F7E', line='#EEE8E1', panel='#FAF7F4', btn='#1B2A5C', btnfg='#fff', acc='#C0284A', crumb=('Klára prémium', 'gyumolcsbor.html#klara')),
    'friss': dict(bg='#F28C28', ink='#1B2A5C', muted='rgba(27,42,92,.8)', line='rgba(27,42,92,.22)', panel='rgba(255,255,255,.28)', btn='#1B2A5C', btnfg='#fff', acc='#1B2A5C', crumb=('FRISS', 'termek/friss-malna.html')),
    'secco': dict(bg='#EEEAF6', ink='#1B2A5C', muted='#5A6072', line='rgba(27,42,92,.14)', panel='rgba(255,255,255,.7)', btn='#1B2A5C', btnfg='#fff', acc='#C84E85', crumb=('Berry Secco', 'termek/berry-secco.html')),
    'palinka': dict(bg='#F4EFE6', ink='#2A2118', muted='#6B5E4C', line='rgba(42,33,24,.16)', panel='rgba(255,255,255,.6)', btn='#2A2118', btnfg='#fff', acc='#A8823C', crumb=('Pálinkák', 'termek/szamocapalinka.html')),
    'piri': dict(bg='#111833', ink='#E3CFA5', muted='rgba(227,207,165,.72)', line='rgba(219,184,121,.28)', panel='rgba(255,255,255,.05)', btn='#DBB879', btnfg='#111833', acc='#DBB879', crumb=('Forralt borok', 'termek/piri-mama-forralt-bora.html')),
    'don': dict(bg='#D9EEF0', ink='#2A1416', muted='#5B4A4C', line='rgba(42,20,22,.14)', panel='rgba(255,255,255,.6)', btn='#C8282E', btnfg='#fff', acc='#C8282E', crumb=('Don Cherry', 'termek/don-cherry.html')),
}
LINE_KICK = {'klasszikus': 'KLASSZIKUS · {taste} GYÜMÖLCSBOR', 'klara': 'KLÁRA PRÉMIUM · {taste}', 'friss': 'FRISS · KÖNNYŰ GYÜMÖLCSBOR',
             'secco': 'BERRY SECCO · HABZÓ GYÜMÖLCSBOR', 'palinka': 'KISÜSTI PÁLINKA · 46%', 'piri': 'PIRI MAMA · FORRALT BOR · 1 L', 'don': 'DON CHERRY · ÉDES MEGGYVERMUT'}
# 100%-os gyümölcs jelvény a klasszikus gyümölcsborokon (csak ahol egyetlen gyümölcsből készül)
PURE = {'edes-meggybor': 'MEGGY', 'szaraz-meggybor': 'MEGGY', 'edes-eperbor': 'EPER', 'edes-ribizlibor': 'RIBIZLI', 'edes-kajszibor': 'KAJSZIBARACK',
        'edes-oszibarackbor': 'ŐSZIBARACK', 'edes-szilvabor': 'SZILVA'}


def ucfg(p):
    u = dict(UCFG[p['line']])
    u.setdefault('acc', p['accent'] if p['accent'].upper() not in ('#FFFFFF', '#FFF6EA') else '#1B2A5C')
    return u


def u_big(p):
    L = p['line']
    if L == 'klara':
        return 'KLÁRA'
    if L == 'piri':
        return 'PIRI MAMA'
    if L == 'don':
        return 'DON CHERRY'
    if L in ('friss', 'secco'):
        return BIG.get(p['id'], SHORT.get(p['id'], '').upper())
    if L == 'palinka':
        return SHORT.get(p['id'], p['name']).upper()
    return bigword(p)


def fit(word, cap=88):
    """Betűméret a szó tényleges Prata HU szélességéből – a szülő (container) szélességébe egy sorban fér."""
    em = sum(PRATA_W.get(ch, 0.75) + 0.02 for ch in word.upper()) + 0.04
    return f'min({cap}px, calc(100cqw / {em:.2f}))'


def u_badge(p):
    L = p['line']
    if L == 'klasszikus':
        return f'<span class="pu-badge sq">100%<b>{PURE[p["id"]]}</b></span>' if p['id'] in PURE else ''
    if L == 'friss':
        return '<span class="pu-badge new">ÚJ</span>'
    if L == 'piri':
        return '<span class="pu-badge sq">AZONNAL<b>FOGYASZTHATÓ</b></span>'
    return ''


def u_buy(p, u):
    tier = p['tier']
    packs = ''
    if tier:
        pct = round((1 - tier[1] / p['price']) * 100)
        packs = '<div class="pu-packs" role="group" aria-label="Kiszerelés">' + ''.join(
            f'<button type="button" data-pack="{n}" aria-pressed="{"true" if n == 1 else "false"}"><strong>{n} palack</strong><span>{ft(tier[1] if n >= tier[0] else p["price"])}/db</span>{f"<em>−{pct}%</em>" if n >= tier[0] else ""}</button>' for n in (1, 3, 6)) + '</div>'
    if not p['avail']:
        return '<div class="pu-buy"><div class="pu-price"><b>Elfogyott</b></div><button class="pu-add" type="button" disabled>Értesítést kérek – élesben</button></div>'
    unit_l = param(p, 'Egységár') or ''
    return f'''<div class="pu-buy" data-buy="{p['id']}">{packs}
<div class="pu-price"><b data-unit>{ft(p['price'])}</b><span>{e(unit_l)}</span></div>
<div class="pu-addrow"><div class="pu-qty" role="group" aria-label="Mennyiség"><button type="button" data-dec aria-label="Kevesebb">−</button><span data-q id="q" aria-live="polite">1</span><button type="button" data-inc aria-label="Több">+</button></div>
<button type="button" class="pu-add" data-add="{p['id']}" data-qty-from="#q">Kosárba · <span data-line>{ft(p['price'])}</span></button></div>
<div class="pu-free"><span data-free-text></span><div class="bar"><i data-free-bar></i></div></div></div>'''


def u_hero(p):
    """A Klára-elrendezésű, minden termékcsaládra közös termékoldal-hero."""
    r = '../'
    CAT = _('CAT')
    L = p['line']
    u = ucfg(p)
    sibs = [x for x in CAT if x['line'] == L]
    i = next(k for k, x in enumerate(sibs) if x['id'] == p['id'])
    prev, nxt = sibs[i - 1], sibs[(i + 1) % len(sibs)]
    vol = param(p, 'Űrmérték') or param(p, 'Kiszerelés') or ''
    vol_h = vol.replace('750 ml', '0,75 l').replace('1000 ml', '1 l').replace('500 ml', '0,5 l')
    alc = (param(p, 'Alkohol') or '').replace(' %vol', '% vol').replace('%vol', '% vol')
    taste = (param(p, 'Édes') or '').upper()
    kick = LINE_KICK[L].replace('{taste}', taste).replace(' ·  GYÜMÖLCSBOR', ' · GYÜMÖLCSBOR').strip(' ·')
    big = u_big(p)
    mini = [('KISZERELÉS', vol_h), ('ALKOHOL', alc)]
    if taste and L in ('klasszikus', 'klara'):
        mini.append(('ÍZ', taste.capitalize()))
    zar = param(p, 'Palackzárás')
    if zar and L == 'klara':
        mini.append(('ZÁRÁS', zar.replace('csavarzáras', 'csavarzár')))
    minis = ''.join(f'<dt>{a}</dt><dd>{e(b)}</dd>' for a, b in mini if b)
    ing = ingr(p).replace(' szulfitot tartalmaz', '')
    alg = allergens(p)
    chips = ''
    if len(sibs) > 1:
        chips = f'<p class="pu-lab">{"VÁLASZD KI" if L == "don" else "VÁLASSZ ÍZT"}</p><div class="pu-chips" role="group" aria-label="Változatok">' + ''.join(
            f'<a href="{x["id"]}.html"{" aria-current=page" if x["id"] == p["id"] else ""}><i style="background:{_dot(x)}"></i>{SHORT.get(x["id"], x["name"])}</a>' for x in sibs) + '</div>'
    arrows = (f'<a class="pu-arr l" href="{prev["id"]}.html" aria-label="Előző: {e(prev["name"])}">‹</a>'
              f'<a class="pu-arr r" href="{nxt["id"]}.html" aria-label="Következő: {e(nxt["name"])}">›</a>') if len(sibs) > 1 else ''
    jar = ' jar' if p['id'] == 'don-cherry-gyumolcse' else ''
    style = f"--pu-bg:{u['bg']};--pu-ink:{u['ink']};--pu-muted:{u['muted']};--pu-line:{u['line']};--pu-panel:{u['panel']};--pu-btn:{u['btn']};--pu-btnfg:{u['btnfg']};--pu-acc:{u['acc']}"
    return f'''<section class="pu-hero" style="{style}"><div class="pd-wrap pu-grid">
<div class="pu-l">
{crumbs([('Főoldal', 'index.html'), u['crumb'], (e(SHORT.get(p['id'], p['name'])), '')], '')}
<p class="pu-kick">{e(kick)}</p>
<p aria-hidden="true" class="pu-big" style="font-size:{fit(big)}">{e(big)}</p>
<h1 class="pu-h1">{e(p['name'])} <span>{e(vol_h)}</span></h1>
{stars_link(p, u['acc'])}
<span class="pu-rule" aria-hidden="true"></span>
<p class="pu-lead">{e(short_desc(p))}</p>
<dl class="pu-mini">{minis}</dl>
<p class="pu-ingr"><strong>Összetevők:</strong> {e(ing)}{f' · <strong>{e(alg)}</strong>' if alg else ''}</p>
</div>
<div class="pu-c">{arrows}{_('badge')(p['id']).replace('pbadge', 'pbadge big') if p['line'] != 'friss' else ''}<img src="{r}{p['tight']}" alt="{e(p['name'])} {e(vol_h)}" class="pu-img{jar}">{u_badge(p)}</div>
<div class="pu-r">
{chips}
{u_buy(p, u)}
{ship_dl(u['line'], 'inherit', 14)}
{upsell(p)}
</div></div></section>'''


def legal_strip(p):
    """Kötelező termékadatok vékony sávban, a termékoldal legalján (az előállító adatai a láblécben)."""
    rows = [(a, b) for a, b in legal_rows(p) if b and a not in ('Tételazonosító',)]
    return '<section class="pu-legal"><div class="pd-wrap"><b>Kötelező adatok</b>' + ''.join(f'<span><i>{e(a)}:</i> {e(b)}</span>' for a, b in rows) + f'<span>{legal_note(p)}</span></div></section>'


TEMPLATES = {'klasszikus': t_klasszikus, 'klara': t_klara, 'piri': t_piri, 'don': t_don, 'friss': t_fsp, 'secco': t_fsp, 'palinka': t_fsp}
