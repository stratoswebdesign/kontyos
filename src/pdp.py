# Termékoldal-sablonok a design (Termek*.dc.html) alapján – termékcsaládonként saját arculat.
# A build.py importálja és tölti fel a közös segédfüggvényekkel (bind()).
import re
import json

G = {}


def bind(**kw):
    G.update(kw)


def _(name):
    return G[name]


SHIP = [('Várható kézbesítés', 'GLS 3–5, MPL 1–3 munkanap'),
        ('Szállítás', '1 800 Ft-tól · 20 000 Ft felett ingyenes'),
        ('Fizetés', 'Bankkártya (SimplePay), átutalás, utánvét · regisztráció nélkül is')]

SHORT = {'friss-narancs': 'Narancs', 'friss-eper': 'Eper', 'friss-malna': 'Málna', 'friss-meggy': 'Meggy',
         'berry-secco': 'Berry', 'berry-secco-tonic': 'Tonic', 'berry-secco-yuzu-lime': 'Yuzu & Lime',
         'szamocapalinka': 'Szamóca', 'birspalinka': 'Birs', 'meggypalinka': 'Meggy', 'kortepalinka': 'Körte', 'szilvapalinka': 'Szilva',
         'piri-mama-forralt-bora': 'Klasszikus', 'narancsos-piri-mama-forralt-bora': 'Narancsos', 'epres-piri-mama-forralt-bora': 'Epres', 'piri-mama-forro-itala-0': '0% alkohol'}
BIG = {'friss-narancs': 'NARANCS', 'friss-eper': 'EPER', 'friss-malna': 'MÁLNA', 'friss-meggy': 'MEGGY',
       'berry-secco': 'BERRY', 'berry-secco-tonic': 'TONIC', 'berry-secco-yuzu-lime': 'YUZU'}


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


SHIP_SHORT = [('Kézbesítés', '1–5 munkanap'), ('Szállítás', '1 800 Ft-tól · 20 000 Ft felett ingyen'), ('Fizetés', 'Kártya, átutalás, utánvét')]


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
            ('Előállító', 'Kontyos Borház Kft., 6773 Klárafalva, Kossuth u. 183.'),
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
    legal = kv(legal_rows(p), c['rule'])
    lab = f'style="color:{c["accent"]}"'
    desk = f'''<section class="pd-info only-d" style="background:{c.get('infobg', '#fff')}"><div class="pd-wrap pd-cols">
<div class="pd-desc"><p class="pd-lab" {lab}>LEÍRÁS</p><h2 style="{c['h2']}">{e(p['name'])}</h2>{long}</div>
<div class="pd-side"><div><p class="pd-lab" {lab}>PARAMÉTEREK</p><div style="border-top:1px solid {c['ink']}">{params}</div></div>
<div class="pd-legal" style="background:{c['legalbg']}"><div style="border-color:{c['ink']}"><p class="pd-lab">KÖTELEZŐ ADATOK</p>{legal}<p class="pd-note">{legal_note(p)}</p></div></div></div></div></section>'''
    acc = lambda t, body, op='': f'<details class="pd-acc" style="border-color:{c["ink"]}"{op}><summary style="{c.get("accfont", "")}">{t}<span aria-hidden="true">+</span></summary><div>{body}</div></details>'
    ship_txt = '<p>MPL csomagautomata / PostaPont / posta: 1 800 Ft, GLS csomagpont: 2 100 Ft – 20 000 Ft felett ingyenes. GLS házhoz: 2 400 Ft, 25 000 Ft felett ingyenes. Személyes átvétel Klárafalván. Regisztráció nélkül is rendelhetsz.</p>'
    mob = f'''<section class="pd-info only-m"><div class="pd-wrap">{acc('Leírás', long, ' open')}{acc('Paraméterek', params)}{acc('Összetevők, allergének', f'<p>{e(ingr(p))}</p>' + (f'<p><b>{e(allergens(p))}</b></p>' if allergens(p) else ''))}{acc('Kötelező adatok', legal + f'<p class="pd-note">{legal_note(p)}</p>')}{acc('Szállítás', ship_txt)}</div></section>'''
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
    return f'''<a class="pd-mcard" href="{r}{_('url')(x)}"><span style="border-color:{ring}"><img src="{r}{x['img']}" alt="{e(x['name'])}" loading="lazy"><span class="tx"><span class="k">{e(kicker or _('LINE_LABEL')[x['line']].upper())}</span><span class="n" style="color:{ink or '#1B2A5C'}">{e(x['name'])}</span><span class="p">{ft(x['price']) if x['avail'] else 'Elfogyott'}</span></span></span></a>'''


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
    items = ''.join(f'''<li><a href="{r}{_('url')(P[i])}" class="im"><img src="{r}{P[i]['img']}" alt="" loading="lazy"></a><a href="{r}{_('url')(P[i])}" class="nm">{e(P[i]['name'])}<small>{ft(P[i]['price'])}</small></a><button type="button" data-add="{i}" aria-label="{e(P[i]['name'])} kosárba">+</button></li>''' for i in ids)
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
    fsz = 'clamp(40px,5vw,70px)' if len(bw) <= 10 else 'clamp(34px,3.8vw,54px)'
    sibs = [x['id'] for x in CAT if x['line'] == 'klasszikus' and x['id'] != p['id']]
    cross_ids = (['szaraz-meggybor', 'klara-szaraz-barrique-meggybor', 'friss-meggy', 'don-cherry'] if 'meggy' in p['id'] else sibs[:2] + ['klara-edes-malnabor', 'friss-' + ('eper' if 'eper' in p['id'] else 'malna')])
    cross_ids = [i for i in cross_ids if i != p['id']][:4]
    ring = {'klara': '#E8DCE0', 'friss': '#F28C28', 'don': '#5FB8B3'}
    buy = buy_core(p, c) if p['avail'] else sold_out(p)
    html = f'''<section class="pd-wrap pd-hero-k">
{crumbs([('Főoldal', 'index.html'), ('Gyümölcsborok', 'gyumolcsbor.html'), ('Klasszikus', 'gyumolcsbor.html#klasszikus'), (e(p['name']), '')], 'font-size:13px')}
<div class="pd-row">
<div class="pd-gal"><div class="pd-arch" style="background:{p['arch']}"><img data-gal-main src="{r}{p['tight']}" alt="{e(p['name'])} {vol}" class="fit-contain"></div>
</div>
<div class="pd-label"><div class="in">
<p class="pd-kick">KLASSZIKUS · {e(taste.upper())} GYÜMÖLCSBOR</p>
<p aria-hidden="true" class="pd-big" style="color:{p['accent']};font-size:{fsz}">{e(bw)}</p>
<h1 class="pd-h1k">{e(p['name'])} {vol.replace(' ml', ' ml').replace('750 ml', '0,75 l')} – {cap}</h1>
{stars_link(p, '#EF4E73')}
<p class="pd-lead">{e(short_desc(p))}</p>
<p class="pd-ingr"><strong>Összetevők:</strong> {e(ingr(p).replace(' szulfitot tartalmaz', ''))}{' · <strong>szulfitot tartalmaz</strong>' if 'szulf' in p['short'].lower() else ''}</p>
<div class="pd-spec"><span>℮ {vol}</span><span>{alc}</span><span>{e(taste)}</span></div>
{buy}
{ship_dl('#E2DACB', '#39404F')}
{upsell(p)}
</div></div></div></section>
{info(p, c)}
<section class="pd-illu noimg"><div class="box"><h2>Mitől 100%-os a gyümölcsbor?</h2><p>Édes borainkat az adott gyümölcs saját, 100%-os levével édesítjük, és csak annyi cukrot adunk hozzá, amennyi életre hívja a gyümölcs valódi karakterét.</p><a href="{r}info.html#rolunk">Így készülnek a boraink →</a></div></section>
{reviews(p, c)}
{cross(cross_ids, 'Ha a meggyet szereted' if 'meggy' in p['id'] else 'Ha ezt szereted', lambda x: ring.get(x['line'], '#1B2A5C'), 'font-family:var(--serif);font-weight:700;font-size:clamp(36px,4vw,54px)')}'''
    return dict(html=html, page='#F3EEE5', ink='#1B2A5C', theme='pill-b', bar=buybar(p, c) if p['avail'] else '')


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
    html = f'''<section class="pd-wrap pd-hero-kl3">
<div class="pd-kltx left">
{crumbs([('Gyümölcsborok', 'gyumolcsbor.html'), ('Klára prémium', 'gyumolcsbor.html#klara')], 'font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6A6F7E')}
<div><p aria-hidden="true" class="pd-klbig">KLÁRA</p>
<h1 class="pd-klh1">{e(p['name'])} <span>{vol.replace('750 ml', '0,75 l')}</span></h1>
<p style="margin-top:12px">{stars_link(p, '#C0284A')}</p></div>
<span aria-hidden="true" class="pd-rule"></span>
<p class="pd-lead">{e(short_desc(p))}</p>
<dl class="pd-mini"><dt>KISZERELÉS</dt><dd>{vol.replace('750 ml', '0,75 l')}</dd><dt>ALKOHOL</dt><dd>{alc}</dd>{f'<dt>ZÁRÁS</dt><dd>{e(zar)}</dd>' if zar else ''}</dl>
</div>
<div class="pd-klimg"><img src="{r}{p['tight']}" alt="{e(p['name'])} {vol} palack"></div>
<div class="pd-kltx right">
{buy}
{ship_dl('#EEE8E1', '#6A6F7E', 12, True)}
{upsell(p, 'k')}
<p class="pd-small">{tiertxt}{e(param(p, 'Egységár') or '')}<br>Összetevők: {e(ingr(p).replace(' szulfitot tartalmaz', ''))} · <strong>szulfitot tartalmaz</strong></p>
</div></section>
{info(p, c)}
<section class="pd-wrap pd-klstory"><img src="{r}img/photo/klara_pohar.webp" alt="Klára édes málnabor palack pezsgőspohárral és friss málnával" loading="lazy">
<div><p class="pd-lab" style="color:#6A6F7E;letter-spacing:.3em">A SOR</p><p class="q">„A gyümölcskertek istennője.”</p>
<p>Olyan borokról álmodtunk, melyek egyszerre fejezik ki a gyümölcsök iránti rajongásunkat, a borkészítés iránti szenvedélyünket és a borászatunk otthona, az idilli-zöld Klárafalva iránt érzett szeretetünket. Egyedülálló minőségű, értékes gyümölcsökből készült friss borainkat egy olyan tiszta szépség testesíti meg, melyet csak a természet adhat.</p></div></section>
{reviews(p, c)}
<section class="pd-wrap pd-klrow"><p class="pd-lab" style="text-align:center;color:#6A6F7E;letter-spacing:.3em">A KLÁRA SOR TÖBBI TAGJA</p><div>{row}</div></section>'''
    cb = dict(c, btn='#1B2A5C', barline='#1B2A5C')
    return dict(html=html, page='#FFFFFF', ink='#1B2A5C', theme='min-k', bar=buybar(p, cb) if p['avail'] else '')


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
    html = f'''<section class="pd-wrap pd-hero-p">
<div class="pd-gal"><div class="pd-pwrap"><div class="pd-arch" style="background:{p['arch']}"><img src="{r}{p['tight']}" alt="{e(full)}" class="fit-bottle"></div><span class="pd-badge">Azonnal<br>fogyaszt&shy;ható</span></div></div>
<div class="pd-ptx">
{crumbs([('Főoldal', 'index.html'), ('Forralt bor', 'termek/piri-mama-forralt-bora.html'), ('PIRI Mama', '')], 'font-size:13px')}
<p class="pd-kick" style="color:{accent}">PIRI MAMA · 1 LITER · {abv}</p>
<h1 class="pd-ph1">{e(full)} <span>1 l</span></h1>
{stars_link(p, '#E2574C')}
<p class="pd-tag" style="color:{accent}">Csak megmelegíted, és kész.</p>
<p class="pd-lead">{e(short_desc(p))}</p>
{chips}
{buy}
{ship_dl('#E2DACB', '#39404F')}
{upsell(p)}
</div></section>
{info(p, c)}
<section class="pd-steps"><div class="pd-wrap"><div class="tx"><p class="pd-lab" style="color:#F3C66B">HÁROM LÉPÉS</p><ol><li><b>1</b><span>Nyisd ki a palackot.</span></li><li><b>2</b><span>Melegítsd fel, ne forrald.</span></li><li><b>3</b><span>Bögrébe vele – kész.</span></li></ol>
<p style="opacity:.8;font-size:14px;line-height:1.6">Felbontás után hűtőben tárolandó, 1 héten belül fogyasztandó.</p></div>
<div class="ph"><img src="{r}img/photo/piri_fa.webp" alt="Narancsos PIRI Mama karácsonyfa előtt" loading="lazy"><img src="{r}img/photo/piri_fahej.webp" alt="Narancsos PIRI Mama fahéjjal és narancsokkal" loading="lazy"></div></div></section>
{reviews(p, c)}
<section class="pd-wrap pd-pair"><div class="mug"><img src="{r}{mug['img']}" alt="PIRI Mama bögréje 0,32 l" loading="lazy"><div><span class="k">MELLÉ</span><strong>PIRI Mama bögréje</strong><span>0,32 l · {ft(mug['price'])}</span><button type="button" data-add="piri-mama-bogreje">Hozzáadom</button></div></div>
<div class="fair"><span class="k">ADVENTI VÁSÁROK</span><strong>Kóstold a standunknál</strong><span>Szeged (Dóm tér) · Óbuda · Szombathely · Veszprém · Győr (Árkád)</span><a href="{r}vasarok.html">Térkép és menetrend →</a></div></section>'''
    return dict(html=html, page='#F3EEE5', ink='#1B2A5C', theme='pill', bar=buybar(p, dict(c, barline=p['arch'])))


# ---------------------------------------------------------------- DON CHERRY (TermekDon.dc)
def t_don(p):
    r = '../'
    P = _('P')
    jar = p['id'] == 'don-cherry-gyumolcse'
    vol = param(p, 'Űrmérték') or ''
    alc = (param(p, 'Alkohol') or '').replace(' %', '% vol').replace('%vol', '% vol')
    c = dict(accent='#2E8C86', accent2='#C8282E', ink='#2A1416', rule='#EAF3F2', legalbg='#F2FAF9', btn='#C8282E', rborder='#D6ECEA',
             h2="font-family:var(--sans);font-weight:800;font-size:clamp(30px,3vw,42px);line-height:1.05", numfont='font-family:var(--sans)', accfont='font-family:var(--serif)')
    sub = 'ÉDES MEGGYVERMUT · 0,75 L' if not jar else 'MEGGYVERMUT ÉS MEGGY · 0,25 L + 100 G'
    pair = P['don-cherry-gyumolcse'] if not jar else P['don-cherry']
    pair_desc = '0,25 l édes meggyvermut és 100 g magozott meggy egy üvegben.' if not jar else 'Prémium minőségű édes meggyvermut 0,75 l-es palackban – friss meggy ágyon érlelt meggybor, dió pálinka, fűszerek.'
    contains = ', '.join(x.replace(' tartalmaz', '') for x in allergens(p).split(' · ') if x)
    html = f'''<section class="pd-wrap pd-hero-d">
<div class="pd-gal"><div class="pd-arch d" style="background:#5FB8B3"><img src="{r}{p['tight']}" alt="{e(p['name'])}" class="{'jar' if jar else 'fit-bottle'}"></div></div>
<div class="pd-dtx">
{crumbs([('Vermut', 'termek/don-cherry.html'), ('Don Cherry', '')], 'font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6A6F7E')}
<div><p aria-hidden="true" class="pd-don">DON</p><p aria-hidden="true" class="pd-cherry">CHERRY</p>
<h1 class="pd-dh1"><span class="sr">{e(p['name'])} </span>{sub}</h1>
<p style="margin-top:14px">{stars_link(p, '#C8282E')}</p></div>
<p class="pd-lead" style="color:#4A3436">{e(short_desc(p))}</p>
<dl class="pd-mini"><dt>ALKOHOL</dt><dd>{e(alc)}</dd><dt>KISZERELÉS</dt><dd>{e(vol)}</dd><dt>EGYSÉGÁR</dt><dd>{e(param(p, 'Egységár') or '')}</dd>{f'<dt>TARTALMAZ</dt><dd style="font-weight:800">{e(contains)}</dd>' if contains else ''}</dl>
{prem_buy(p, 'd')}
{ship_dl('#EAF3F2', '#4A3436')}
{upsell(p, 'd')}
</div></section>
{info(p, c)}
<section class="pd-wrap pd-dphotos"><img src="{r}img/photo/don_cimke.webp" alt="Don Cherry címke közelről, meggyekkel" loading="lazy"><img src="{r}img/photo/don_ajandek.webp" alt="Don Cherry palack és üveg meggy felülnézetből" loading="lazy"></section>
<section class="pd-wrap pd-drink"><p class="pd-lab" style="color:#2E8C86;letter-spacing:.3em">ÍGY IDD</p><p class="intro">Két külön út a meggyvermut élvezetéhez. Válaszd az alkalmadhoz illőt!</p>
<div><div><span class="k">8 CL · JÉG · NARANCS</span><b>Klasszikus – hűsítő aperitif</b><span>Ha az esti beszélgetésekhez keresel egy finom, lágyan fűszeres italt. Tölts meg egy poharat roskadásig jéggel, helyezz rá egy narancskarikát. Öntsd rá a 8 cl prémium meggyvermutot. A frissesség és az aromák tökéletes harmóniáját kapod.</span></div>
<div><span class="k">4 CL · 1 MEGGYSZEM</span><b>Intenzív meggy shot – „Shout” élmény</b><span>A gyors, brutális ízrobbanás kedvelőinek. Egy 5 cl-es pohár aljára helyezz egy meggyszemet (amit a webshopunkban megtalálsz). Önts rá 4 cl meggyvermutot. Idd két kortyban, hogy a végén a meggyszem felerősítse az ízélményt!</span></div></div></section>
{reviews(p, c)}
<section class="pd-dpair"><div class="pd-wrap"><img src="{r}{pair['tight']}" alt="{e(pair['name'])}" loading="lazy" class="{'jar' if not jar else ''}">
<div><p class="pd-lab" style="color:#2E8C86;letter-spacing:.3em">A PÁRJA</p><h2>{e(pair['name'])}</h2><p>{pair_desc}</p>
<div class="row"><b>{ft(pair['price'])}</b><button type="button" data-add="{pair['id']}">KOSÁRBA</button><a href="{pair['id']}.html">Részletek →</a></div></div></div></section>'''
    return dict(html=html, page='#FFFFFF', ink='#2A1416', theme='min-d', bar=buybar(p, dict(c, barline='#5FB8B3')))


# ---------------------------------------------------------------- FRISS / SECCO / PÁLINKA (TermekFriss/Secco/Palinka.dc)
LINECFG = {
    'friss': dict(page='#FFF6EA', kick='FRISS · KÖNNYŰ GYÜMÖLCSBOR · 0,75 L', kc='#EF4E73', h1w=900, rule='#F1E2CF', theme='pill',
                  crumb=('FRISS', 'friss.html'), cross=['konnyu-trio', 'berry-secco', 'bubi-paros', 'kontyos-borospohar']),
    'secco': dict(page='#F7F7FB', kick='BERRY SECCO · ÉDES HABZÓ GYÜMÖLCSBOR · 0,75 L', kc='#E86A9A', h1w=900, rule='#E3E6F2', theme='pill',
                  crumb=('Berry Secco', 'friss.html'), cross=['bubi-paros', 'kontyos-borospohar', 'friss-narancs', 'friss-eper']),
    'palinka': dict(page='#F4EFE6', kick='KISÜSTI PÁLINKA · 46% · {vol}', kc='#A8823C', h1w=500, rule='#E3DACB', theme='pill',
                    crumb=('Pálinka', 'palinka.html'), cross=['don-cherry', 'klara-szaraz-barrique-meggybor', 'meggymag-parna', 'klara-edes-malnabor']),
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
<div class="tx"><h2>Fele gyümölcsbor, fele almabor.</h2><p class="s">Reduktív eljárással, friss gyümölcsből – könnyű, kellemesen édes, pár szem jéggel is. Négy íz, mind {ft(p['price'])}.</p><div class="tiles">{tiles}</div></div>
<img class="ph" src="{r}img/photo/friss_csalad.webp" alt="FRISS gyümölcsborok" loading="lazy"></div></section>'''
    elif L == 'secco':
        dots = ''.join(f'<span aria-hidden="true" class="bub" style="left:{x}%;top:{y}%;width:{s}px;height:{s}px"></span>' for x, y, s in [(6, 20, 26), (12, 62, 14), (30, 14, 10), (48, 72, 22), (66, 18, 16), (84, 64, 12), (92, 24, 20)])
        alc = (param(p, 'Alkohol') or '').replace(' %vol', '%').replace('%vol', '%')
        story = f'''<section class="pd-story s" style="background:{p['arch']};color:{fg}">{dots}<div class="pd-wrap"><div class="tx"><p class="pd-lab">ÍGY KÍNÁLD</p><h2>{e(serve_text(p))}</h2><p class="s">Habzó, édes, {alc} – a buborékok kedvelőinek.</p></div>
<div class="tiles big">{tiles}</div></div></section>'''
    else:
        facts = [('KISÜSTI', 'Hagyományos, kisüsti módon főzve, gyümölcsből cefrézve.'), ('46%', '46%-os alkoholra beállítva.'), ('PINCEHIDEGEN', 'A zamatok teljessége érdekében pincehidegen ajánlott.')]
        story = f'''<section class="pd-story p"><div class="pd-wrap"><div class="tx"><h2>Kisüsti, gyümölcsből.</h2><div class="facts">{''.join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in facts)}</div></div>
<div class="tiles big">{tiles}</div></div></section>'''
    rating = stars_link(p, accent)
    html = f'''<section class="pd-wrap pd-hero-f">
<div class="pd-gal"><div class="pd-arch" style="background:{p['arch']}"><img src="{r}{p['tight']}" alt="{e(p['name'])}" class="fit-bottle"></div></div>
<div class="pd-ftx">
{crumbs([('Főoldal', 'index.html'), cf['crumb'], (SHORT.get(p['id'], e(p['name'])), '')], 'font-size:13px')}
<p class="pd-kick" style="color:{accent}">{kick}</p>
<h1 class="pd-fh1" style="font-weight:{cf['h1w']}">{e(p['name'])}</h1>
{rating}
<p class="pd-lead">{e(short_desc(p))}</p>
{chips}
{buy}
{ship_dl(cf['rule'], 'inherit')}
{upsell(p)}
</div></section>
{story}
{info(p, c)}
{reviews(p, c)}
{cross(cf['cross'], 'Mellé ajánljuk', lambda x: cf['rule'], 'font-family:var(--serif);font-weight:700;font-size:clamp(34px,3.6vw,48px)')}'''
    return dict(html=html, page=cf['page'], ink='#1B2A5C', theme=cf['theme'], bar=buybar(p, dict(c, barline=p['arch'])) if p['avail'] else '')


def _dot(x):
    a = x['accent']
    return x['arch'] if a.upper() in ('#FFFFFF', '#FFF6EA', '#1B2A5C') else a


TEMPLATES = {'klasszikus': t_klasszikus, 'klara': t_klara, 'piri': t_piri, 'don': t_don, 'friss': t_fsp, 'secco': t_fsp, 'palinka': t_fsp}
