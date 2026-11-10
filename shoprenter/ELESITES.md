# Élesítési forgatókönyv – kontyos.hu (Shoprenter, Párizs téma)

## ÉLESÍTVE – 2026-11-10 este
- 44 meglévő termék = sandbox (főkép, ár, akció; cikkszám/gyártói cikkszám érintetlen) – ellenőrizve mezőnként.
- 22 új termék **Engedélyezett**, 29 régi **Letiltott** (a natúr almalé marad Engedélyezett – Sanyi dönt róla).
  A régi kampánycsomagok (382, 384, 389, 414, 427, 454) Kifutott maradtak, mint a sandboxban; az URL-átvétel elmaradt,
  az új szezonális csomagok URL-je `…-<id>` (pl. `/edes-unnepek-borcsomag-522`).
- 8 sablon a sandbox szerint (a `product_list.tpl` utólag, 22:29) (footer_scripts: `kontyos.live.js`, jsDelivr @219c1df) – bájtra ellenőrizve.
- Tartalmi oldalak 67, 70, 72, 73, 76, 78 Engedélyezett; ÁSZF (5) → `/aszf`, Adatkezelés (49) → `/adatkezelesi-tajekoztato` a sandbox szövegével.
- HIRLEVEL5 Engedélyezett; hírlevél köszönőoldal + automatikus köszönő levél = sandbox.
- 301: a lenti lista 25 sora (a `nonapi-csomag` régi, `oszi-borcsomag`-ra mutató sora átírva) + a két régi jogi URL.
- Karbantartási mód KI. Kosár → pénztár (utolsó lépés előtt) élesben kipróbálva, a tesztkosár kiürítve.

**Utóélet, 2026-11-10 22:00–22:52 – vegyes régi/új dizájn → témaváltás:**
- Nyitás után a nem bejelentkezett látogatók kéréseinek ~25–33%-a a módosítás előtti Párizs-sablonnal renderelődött
  (friss adatokkal) – a Shoprenter egyes kiszolgálóinak elavult sablon-gyorsítótára. Admin nézetben nem jött elő.
  A Labor › Cache törlés (2×) és a sablonok újramentése nem segített; közben a bolt karbantartásban volt.
- Megoldás: **Téma másolása** (Párizs → „Kontyos”, belső név `paris_1`) és aktiválása – új néven nincs elavult gyorsítótár.
  A sablonok bájtra egyeznek a `paris_global`-lal. Előtte a sandboxban kipróbálva (ott is `paris_1` az aktív).
  Elveszett: a kategória/kereső oldalsáv régi Párizs-dobozai (customcontent 5/10/11 + oldalsáv-hírlevél) – az új oldalakon nem kellenek.
- Mérés nyitás után: ~400 anonim lekérés (69 oldal, asztali + iPhone UA) – 0 régi, 0 borító; 22:50-től élesben.
- **Ezentúl minden sablonmódosítás a `paris_1` témában!** (Téma fájl szerkesztő URL: `/admin/themeEditor/theme/paris_1`)
- Közben javítva: `product/product_list.tpl` (Gyümölcsborok, Csomagajánlatok kategóriaoldal) – kimaradt az élesítésből;
  Széchenyi 2020 infoblokk fix, jobb alsó sarokban (200×140, mobilon 120×84) – a `pagehead.tpl` Kontyos-blokkjában.

**Tanulság (termékmentés POST-tal):** a keresőbarát URL (`keywords[1][keyword]`) és a bruttó árak (`gross_price`,
`product_special[n][gross_price]`) a Vue-űrlapban élnek, a HTML-ből nem olvashatók ki. Ha kimaradnak, a Shoprenter
`név-id` URL-t generál, illetve akciós terméknél elutasítja a mentést („Az akciós ár mező nem lehet üres”).
Mindhármat ki kell tölteni (URL: `document.ShopRenter.data.keywords`; bruttó = nettó × 1,27).

Csak Artúr jóváhagyása után, és miután Gabiék minden terméknél beírták a gyártói cikkszámot (SAP).
Javasolt időpont: késő este, alacsony forgalomnál. Becsült idő: 30–45 perc + ellenőrzés.

## 0. Már elkészült élesben, rejtve (2026-11-10)
| Mi | Állapot | Miért nem látszik |
|---|---|---|
| 22 új termék (csomagok, koktélcsomagok, partnertermékek) | **Letiltott**, SEO-URL beállítva | letiltott termék nem jelenik meg |
| 68 `ky-*` snippet a `paris_global` témában | új fájlok, bájtra egyeznek a repóval | egyetlen sablon sem hivatkozik rájuk |
| Koktélok (67), Vásárok (70), Black Friday (72), Karácsonyi ajándék bor (73), Forralt bor (76) | **Letiltott**, menü/lábléc/modul nélkül | látogatóként a főoldalra irányít |
| Vásár-értesítő űrlap (form 3) + oldal (78, `/vasar-ertesito`, noindex) | űrlap kész, oldal **Letiltott** | az oldal letiltott |
| HIRLEVEL5 kupon (5%, vevőnként 1×) | **Letiltott** | letiltott kupon nem váltható be |
| Lezáró borító: `common/maintenance.tpl` (forrás: `karbantartas.html`), az eredeti `ky-backup-maintenance` néven | kész | csak karbantartási módban jelenik meg |
| 38 meglévő termék új főképe `product/Kontyos2026/kontyos-<id>.jpg` | feltöltve, termékhez még nincs kötve | nincs hivatkozás rá |
| Sablon-mentések: `ky-backup-pagehead`, `-footer-scripts`, `-footer`, `-home`, `-header`, `-product`, `-information` | snippetként a témában | nincs használatban |

Az éles termékazonosítók: `shoprenter/live_pid.json`; az éles kosárkód: `shoprenter/assets/kontyos.live.js`
(a sandboxos `kontyos.js` a sandbox azonosítóival dolgozik – élesben **nem** az töltődik be).

## 1. Előtte (bármikor, láthatatlan)
- [x] Biztonsági mentés az élő sablonokról: a témában `snippets/ky-backup-*.tpl` (7 db, 2026-11-10) + a Shoprenter „Korábbi verziók”.
- [x] A 74 meglévő cikkszám éles product_id-je egyezik a `live_pid.json`-nal (2026-11-10; a „farsang 2026” élesben két szóközzel szerepel, kifutott termék).
- [x] A CSS/JS helye élesben: **jsDelivr CDN, rögzített commitra** (jóváhagyva 2026-11-10). A sandbox már így tölt és működik. Élesítés előtt: `python3 shoprenter/cdn_pin.py` (a legutolsó commitra rögzít), majd a `pagehead` / `footer_scripts` beszúrandó része a `templates/common/*.KONTYOS-BESZURAS.txt`-ből (élesben `kontyos.live.js`!).
- [x] 301-es átirányítási lista: `shoprenter/atiranyitasok.csv` (felvitel csak élesítéskor). Nyitott: a natúr almalé kikapcsolása (most is árulják).

## 2. Élesítés sorrendje
0. **Hirdetések szüneteltetése** (Google Ads, Meta), majd **karbantartási mód BE** – a látogatók a lezáró borítót látják, adminként a bolt tovább tesztelhető.
1. **Termékek**
   - 44 meglévő termék frissítése (ár, akció, leírás, kép, betétdíj-kiegészítő) Sanyi táblázata szerint;
   - 22 új termék → **Engedélyezett**;
   - 30 régi termék → **Letiltott** (nem törlés);
   - URL-átvétel: a régi Édes Ünnepek (384), Könnyű karácsonyi (454), Prémium adventi (427) SEO-URL-je kap `-2025` végződést,
     az új 522/531/536 megkapja a tiszta URL-t (`edes-unnepek-borcsomag`, `konnyu-karacsonyi-borcsomag`, `premium-adventi-borvalogatas`).
2. **Tartalmi oldalak** – az 5 rejtett oldal és a Vásár-értesítő (78) → **Engedélyezett** (menü/lábléc pipák nélkül, a menüt a ky-header adja);
   Rólunk / ÁSZF / Adatkezelési tájékoztató / Kiszállítás: SEO-URL egyeztetése az `information.tpl` térképével
   (`rolunk`, `aszf`, `adatkezelesi-tajekoztato`, `kiszallitas`).
3. **Sablonok** (a `TELEPITES.md` táblázata szerint, mindegyik után Mentés + ellenőrzés):
   `pagehead` (CSS) → `footer_scripts` (**kontyos.live.js**) → `header` → `footer` → `home` → `product` → `information`.
4. **Hírlevél** – HIRLEVEL5 kupon → **Engedélyezett**; automatikus köszönő levél a kóddal, köszönőoldal.
5. **301 átirányítások** felvitele.
6. **18+ korhatár-kapu** – a `kontyos.live.js` része, a sablonokkal együtt él.

7. **Karbantartási mód KI**, hirdetések vissza.

## 3. Ellenőrzés közvetlenül utána
- főoldal, 3 termékoldal (bor, csomag, koktélcsomag), Rólunk, Koktélok, Vásárok – asztali és mobil;
- kosár: hozzáadás, darabszám, betétdíj, ingyenes szállítás határa; pénztár végig (utolsó lépés előtt megállva);
- keresés, belépés, regisztráció, kapcsolat, elállás, 404, süti-sáv;
- GA4 / Meta pixel / Google Ads események (kosárba tétel, vásárlás) a GTM előnézetben.

## 4. Visszaállítás
A `ky-backup-*` snippetek tartalmát (az első megjegyzéssor nélkül) visszamásolni a téma fájlszerkesztőjében (7 fájl). A termék- és oldalállapotokat
a fenti listák alapján vissza lehet kapcsolni; a snippetek maradhatnak, mert hivatkozás nélkül nem látszanak.
