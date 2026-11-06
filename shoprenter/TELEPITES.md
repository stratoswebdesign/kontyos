# Kontyos → Shoprenter (SANDBOX) – telepítési lépések

> Csak a **kontyos.sandbox.shoprenter.hu** adminban! Élesben (kontyos.hu) semmit, amíg Artúr nem szól.
> A Labor oldalon a „Sandbox frissítés” gombot NE nyomjuk meg (felülírná a sandboxot).

Újragenerálás a demóból: `python3 src/build.py && python3 src/shoprenter.py`

## 0. Mentés
- Téma fájl szerkesztő → minden módosított fájlnak van verzióelőzménye, de a módosítás előtt az eredeti tartalmat
  a `shoprenter/eredeti/` mappába is elmentjük.

## 1. Fájlok
| Hova (Téma fájl szerkesztő) | Mit | Honnan |
|---|---|---|
| `assets/kontyos.css` (új fájl) | teljes stíluslap `.ky` alá zárva | `assets/kontyos.css` |
| fájlkezelő: `kontyos/kontyos.js` | katalógus + oldallogika + kosár-adapter | `assets/kontyos.js` |
| `snippets/ky-*.tpl` (új fájlok, 59 db) | fejléc, lábléc, főoldal, aloldalak, termékoldalak | `snippets/` |
| `common/pagehead.tpl` | CSS + fontok a `</head>` elé | `templates/common/pagehead.tpl.KONTYOS-BESZURAS.txt` |
| `common/footer_scripts.tpl` | kontyos.js betöltése a végére | `templates/common/footer_scripts.tpl.KONTYOS-BESZURAS.txt` |
| `sections/header.tpl` | markup → ky-header, a schema marad | `templates/sections/header.tpl.KONTYOS.txt` |
| `common/footer.tpl` | markup → ky-footer | `templates/common/footer.tpl.KONTYOS.txt` |
| `common/home.tpl` | teljes csere | `templates/common/home.tpl` |
| `product/product.tpl` | SEO-URL → ky-p-* snippet, tartalék: eredeti | `templates/product/product.tpl.KONTYOS-ELEJE.txt` |
| `information/information.tpl` | egyedi aloldalak → ky-page-* | `templates/information/information.tpl.KONTYOS.txt` |

## 2. Termékek (`termek_megfeleltetes.csv`)
- 44 meglévő: név, ár, leírás, képek frissítése (a cikkszám marad).
- 16 új: létrehozás a javasolt cikkszámmal (KY-…) és SEO-URL-lel (a demó termék-id-je), **Letiltott** állapotban, amíg nincs kész.
- 30 régi: **Letiltott** (nem törlés).
- DRS: 50 Ft / palack a Kontyos italokon (pálinka kivételével), partnertermékeken is.
- A sandboxból kimentjük a cikkszám → product_id párokat, és beírjuk a `window.KY_PID` térképbe (kosár-adapter).

## 3. Egyedi aloldalak (Tartalom → Egyedi aloldalak)
Rólunk (`/rolunk` – meglévő), Koktélok (`/koktelok`), Vásárok (`/vasarok`), Black Friday (`/black-friday`),
Karácsonyi ajándék bor (`/karacsonyi-ajandek-bor`). A tartalmat az `information.tpl` tölti be a snippetből.

## 4. Ellenőrizendő a sandboxban
- a kosár-végpont (rejtett Shoprenter-űrlap action-je) és a darabszám frissülése a fejlécben;
- a Párizs saját fejléce/lábléce nem jelenik-e meg duplán;
- pénztár és fiókoldalak (ezek a Párizs stílusát tartják) – csak színek/betűk igazítása;
- képek: sandboxban a GitHub Pages-ről (IMG_BASE), élesítéskor a fájlkezelőből.

## 5. Tapasztalatok a sandboxból (2026-11-05/06)
- **Párizs/Bootstrap ütközések:** a demó `.row`, `.col`, `.btn`, `.card`, `.price`, `.h1` … osztályai a Párizs CSS-ével ütköztek
  (negatív margó, középre zárt lábléc, fehér sáv). Megoldás: a generátor `k-` előtagot ad ezeknek (`COLLIDE` lista a
  `src/shoprenter.py`-ben – CSS, snippetek és JS egyszerre), és a `kontyos.css` elején `all:revert` nullázza a `.ky` alatti elemeket.
- **Fejléc fölötti sáv** (pl. karácsonyi `.xbar`): a snippetben `.ky-pre`, a `kontyos.js` teszi a fejléc elé.
- **Fizetési logók (SimplePay – kötelező):** a Shoprenter `.ky-legal-logos` blokkját a `kontyos.js` a sötét lábléc aljára teszi, nincs külön világos sáv.
- **Vásár-adatok:** a `window.KONTYOS_FAIRS` a `kontyos.js` elején van; a vásárok oldal Leaflet-stíluslapja a snippetben.
- **Téma-szerkesztő:** a Mentés gombot valódi kattintással kell megnyomni; egy meglévő fájl oldalbetöltésenként egyszer szerkeszthető
  (közben újratöltés); a sandboxban a CSS/JS a GitHub Pages-ről jön 10 perces gyorsítótár-kulccsal (`?v=ÉÉÉÉHHNNÓÓP`).
- **Ellenőrzés:** `shoprenter/ky_compare.js` → `kyCmp('/útvonal', 'demo.html', 1440|390)` a sandbox-oldalon futtatva elemenként összeveti
  a számított stílusokat és a fejléc/logó/lábléc helyét a demóval.

## 6. Élesítés (csak jóváhagyás után)
Ugyanezek a lépések a kontyos.hu adminban, a témacsere éjszaka, előtte mentés az eredeti fájlokról.
A CSS/JS élesben a téma `assets/` mappájából / fájlkezelőből töltődjön (ne a GitHub Pages-ről), a képek szintén.
