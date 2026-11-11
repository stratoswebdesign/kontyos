"""Élesítés előtt: a pagehead / footer_scripts beszúrandó részeinek legenerálása jsDelivr-hivatkozással,
egy rögzített commitra (amit a GitHubra már feltöltöttünk).

Használat:  python3 shoprenter/cdn_pin.py [commit-hash]   (alapértelmezés: az origin/main legutolsó commitja)

A rögzített hash miatt egy későbbi repó-módosítás nem kerül ki véletlenül élesbe; frissítéskor új hash-sel újra kell futtatni,
és a két sort a téma fájlszerkesztőjében kicserélni.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sha = sys.argv[1] if len(sys.argv) > 1 else subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=HERE, text=True).strip()
CDN = f'https://cdn.jsdelivr.net/gh/stratoswebdesign/kontyos@{sha}/shoprenter/assets/'

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
{{# KONTYOS – Széchenyi 2020 infoblokk: fix, jobb alsó sarok, mint a régi oldalon (kötelező uniós tájékoztatás) #}}
<style>
.ky-legal-logos .szechenyi{{position:fixed!important;right:0;bottom:0;z-index:900;margin:0;padding:0;line-height:0;background:none}}
body .ky-foot .site-foot .ky-legal-logos .szechenyi img,body .ky-legal-logos .szechenyi img{{display:block;width:200px!important;height:auto!important;max-width:none!important;max-height:none!important;aspect-ratio:10/7;object-fit:contain}}
/* telefonon: termékoldalon a láblécben (ne takarja a ragadós Kosárba-sávot), minden más oldalon lebegve jobb lent, kisebben */
@media (max-width:760px){{
body.product-page-body .ky-legal-logos{{flex-wrap:wrap}}
body.product-page-body .ky-legal-logos .szechenyi{{position:static!important;order:5;flex:0 0 100%;margin:14px 0 0;line-height:0}}
body.product-page-body .ky-foot .site-foot .ky-legal-logos .szechenyi img,body.product-page-body .ky-legal-logos .szechenyi img{{width:180px!important}}
body:not(.product-page-body) .ky-foot .site-foot .ky-legal-logos .szechenyi img,body:not(.product-page-body) .ky-legal-logos .szechenyi img{{width:120px!important}}
}}
@media (min-width:761px){{.ky-foot .site-foot .legal{{padding-right:210px}}}}
/* a Shoprenter beépített korhatár-ablaka helyett a Kontyos-kapu (kontyos.live.js) */
#auroraOverlay{{display:none!important}}
body{{visibility:visible!important}}
</style>
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
