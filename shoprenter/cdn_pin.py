"""Élesítés előtt: a pagehead / footer_scripts beszúrandó részeinek legenerálása jsDelivr-hivatkozással,
egy rögzített commitra (amit a GitHubra már feltöltöttünk).

Használat:  python3 shoprenter/cdn_pin.py [commit-hash]   (alapértelmezés: az origin/main legutolsó commitja)

A rögzített hash miatt egy későbbi repó-módosítás nem kerül ki véletlenül élesbe; frissítéskor új hash-sel újra kell futtatni,
és a két sort a téma fájlszerkesztőjében kicserélni.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sha = sys.argv[1] if len(sys.argv) > 1 else subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=HERE, text=True).strip()
CDN = f'https://cdn.jsdelivr.net/gh/stratoswebdesign/kontyos@{sha}/shoprenter/assets/'

# Shoprenter-termékopciók (pl. szín): éles product_id → [opció-azonosító, alapértelmezett érték] a catalog.json „opts” mezőiből
_cat = json.load(open(os.path.join(HERE, '..', 'src', 'catalog.json'), encoding='utf-8'))
_pid = json.load(open(os.path.join(HERE, 'live_pid.json'), encoding='utf-8'))
_src = {x['id']: x['src'] for x in _cat}
_man = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
_sku = {v['url'].strip('/'): v.get('sku') for v in _man.values() if v.get('url')}
OPTS = {}
for x in _cat:
    o = x.get('opts')
    if not o:
        continue
    sku = _sku.get(x['src'])
    if sku and _pid.get(sku):
        OPTS[int(_pid[sku])] = [o['oid'], o['vals'][0][0]]
    else:
        print('FIGYELEM: nincs éles product_id:', x['id'])
OPTS_JS = json.dumps(OPTS, separators=(',', ':'))

head = f"""{{# ===== KONTYOS – a pagehead.tpl-ben a </head> ELÉ szúrandó (a {{{{ content_for_header }}}} maradjon!) ===== #}}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Montserrat:wght@400..800&display=swap" rel="stylesheet">
{{# stílus: jsDelivr CDN, rögzített commit ({sha[:7]}) – frissítés: shoprenter/cdn_pin.py #}}
<link rel="stylesheet" href="{CDN}kontyos.css">
<style>
/* A Párizs-téma saját fejlécének/láblécének elrejtése a Kontyos-fejléc mellett */
body .ky-head ~ header:not(.site-head), body .ky-foot ~ footer:not(.site-foot){{display:none!important}}
</style>
{{# KONTYOS – Széchenyi 2020 infoblokk (kötelező uniós tájékoztatás): a főoldalon fix a jobb alsó sarokban, minden más oldalon a láblécben #}}
<style>
.ky-legal-logos .szechenyi{{position:fixed!important;right:0;bottom:0;z-index:900;margin:0;padding:0;line-height:0;background:none}}
body .ky-foot .site-foot .ky-legal-logos .szechenyi img,body .ky-legal-logos .szechenyi img{{display:block;width:200px!important;height:auto!important;max-width:none!important;max-height:none!important;aspect-ratio:10/7;object-fit:contain}}
/* aloldalak (minden, ami nem a főoldal): a láblécben, saját sorban */
body:not(.home-body) .ky-legal-logos{{flex-wrap:wrap}}
body:not(.home-body) .ky-legal-logos .szechenyi{{position:static!important;order:5;flex:0 0 100%;margin:14px 0 0;line-height:0}}
@media (max-width:760px){{
body:not(.home-body) .ky-foot .site-foot .ky-legal-logos .szechenyi img,body:not(.home-body) .ky-legal-logos .szechenyi img{{width:180px!important}}
body.home-body .ky-foot .site-foot .ky-legal-logos .szechenyi img,body.home-body .ky-legal-logos .szechenyi img{{width:120px!important}}
}}
@media (min-width:761px){{body.home-body .ky-foot .site-foot .legal{{padding-right:210px}}}}
/* a Shoprenter beépített korhatár-ablaka helyett a Kontyos-kapu (kontyos.live.js) */
#auroraOverlay{{display:none!important}}
body{{visibility:visible!important}}
</style>
{{# KONTYOS – termékopciók (szín, grafika): a Kosárba-kérés (POST product_id) mellé az option[ID] mező – a termékoldalon a kiválasztott, máshol (kártyák, ajánlók) az első érték #}}
<script>(function(){{var O={OPTS_JS},f=window.fetch;if(!f)return;window.fetch=function(u,o){{try{{var b=o&&o.body;if(b&&typeof FormData!=='undefined'&&b instanceof FormData&&b.has('product_id')){{var x=O[b.get('product_id')];if(x&&!b.has('option['+x[0]+']')){{var c=document.querySelector('input[name="option['+x[0]+']"]:checked');b.append('option['+x[0]+']',c?c.value:x[1]);}}}}}}catch(e){{}}return f.apply(this,arguments);}};}})();</script>
"""

def foot(js):
    return f"""{{# ===== KONTYOS – a footer_scripts.tpl VÉGÉRE ===== #}}
<script>window.KY_SHOPRENTER = true; window.KY_ROOT = '/';</script>
{{# oldallogika + kosár: jsDelivr CDN, rögzített commit ({sha[:7]}) – frissítés: shoprenter/cdn_pin.py #}}
<script src="{CDN}{js}" defer></script>
"""

T = os.path.join(HERE, 'templates', 'common')
open(os.path.join(T, 'pagehead.tpl.KONTYOS-BESZURAS.txt'), 'w', encoding='utf-8').write(head)
open(os.path.join(T, 'footer_scripts.tpl.KONTYOS-BESZURAS.txt'), 'w', encoding='utf-8').write(foot('kontyos.live.js'))
open(os.path.join(T, 'footer_scripts.tpl.KONTYOS-BESZURAS-SANDBOX.txt'), 'w', encoding='utf-8').write(foot('kontyos.js'))
print('rögzítve:', sha)
