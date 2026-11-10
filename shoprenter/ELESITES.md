# Élesítési forgatókönyv – kontyos.hu (Shoprenter, Párizs téma)

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
- [ ] A CSS/JS helye élesben – a Shoprenter fájlkezelője **nem fogad** .css/.js fájlt (2026-11-10 kipróbálva). Lehetőségek: GitHub Pages (mint a sandboxban) vagy jsDelivr rögzített commit-hash-sel; a sablonba ágyazás (inline) 240 KB-os CSS-sel minden oldalt lassítana.
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
