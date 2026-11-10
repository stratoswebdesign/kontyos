# Élesítési forgatókönyv – kontyos.hu (Shoprenter, Párizs téma)

Csak Artúr jóváhagyása után, és miután Gabiék minden terméknél beírták a gyártói cikkszámot (SAP).
Javasolt időpont: késő este, alacsony forgalomnál. Becsült idő: 30–45 perc + ellenőrzés.

## 0. Már elkészült élesben, rejtve (2026-11-10)
| Mi | Állapot | Miért nem látszik |
|---|---|---|
| 22 új termék (csomagok, koktélcsomagok, partnertermékek) | **Letiltott**, SEO-URL beállítva | letiltott termék nem jelenik meg |
| 68 `ky-*` snippet a `paris_global` témában | új fájlok, bájtra egyeznek a repóval | egyetlen sablon sem hivatkozik rájuk |
| Koktélok (67), Vásárok (70), Black Friday (72), Karácsonyi ajándék bor (73), Forralt bor (76) | **Letiltott**, menü/lábléc/modul nélkül | látogatóként a főoldalra irányít |
| Vásár-értesítő űrlap | létrehozva (ellenőrizni!) | nincs oldalra kitéve |

Az éles termékazonosítók: `shoprenter/live_pid.json`; az éles kosárkód: `shoprenter/assets/kontyos.live.js`
(a sandboxos `kontyos.js` a sandbox azonosítóival dolgozik – élesben **nem** az töltődik be).

## 1. Előtte (bármikor, láthatatlan)
- [ ] Biztonsági mentés az élő sablonokról a repóba (`shoprenter/live-backup/`): `common/pagehead.tpl`, `common/footer_scripts.tpl`,
      `sections/header.tpl`, `common/footer.tpl`, `common/home.tpl`, `product/product.tpl`, `information/information.tpl`.
- [ ] A 74 meglévő cikkszám éles product_id-jét összevetni a `live_pid.json`-nal (a sandbox az élesről készült, de ellenőrizni kell).
- [ ] A CSS/JS/képek helye élesben: fájlkezelő (`/custom/kontyos/…`) vagy GitHub Pages – döntés.
- [ ] 301-es átirányítási lista (régi termék- és oldal-URL-ek → új) elkészítve, felvitel csak élesítéskor.

## 2. Élesítés sorrendje
1. **Termékek**
   - 44 meglévő termék frissítése (ár, akció, leírás, kép, betétdíj-kiegészítő) Sanyi táblázata szerint;
   - 22 új termék → **Engedélyezett**;
   - 30 régi termék → **Letiltott** (nem törlés).
2. **Tartalmi oldalak** – a 5 rejtett oldal → **Engedélyezett** (menü/lábléc pipák nélkül, a menüt a ky-header adja);
   Vásár-értesítő oldal létrehozása (`/vasar-ertesito`, noindex, nofollow) az űrlap objektummal;
   Rólunk / ÁSZF / Adatkezelési tájékoztató / Kiszállítás: SEO-URL egyeztetése az `information.tpl` térképével
   (`rolunk`, `aszf`, `adatkezelesi-tajekoztato`, `kiszallitas`).
3. **Sablonok** (a `TELEPITES.md` táblázata szerint, mindegyik után Mentés + ellenőrzés):
   `pagehead` (CSS) → `footer_scripts` (**kontyos.live.js**) → `header` → `footer` → `home` → `product` → `information`.
4. **Hírlevél** – automatikus köszönő levél a HIRLEVEL5 kóddal, köszönőoldal; HIRLEVEL5 kupon (5%, első rendelés).
5. **301 átirányítások** felvitele.
6. **18+ korhatár-kapu** – a `kontyos.live.js` része, a sablonokkal együtt él.

## 3. Ellenőrzés közvetlenül utána
- főoldal, 3 termékoldal (bor, csomag, koktélcsomag), Rólunk, Koktélok, Vásárok – asztali és mobil;
- kosár: hozzáadás, darabszám, betétdíj, ingyenes szállítás határa; pénztár végig (utolsó lépés előtt megállva);
- keresés, belépés, regisztráció, kapcsolat, elállás, 404, süti-sáv;
- GA4 / Meta pixel / Google Ads események (kosárba tétel, vásárlás) a GTM előnézetben.

## 4. Visszaállítás
A `shoprenter/live-backup/` sablonjait visszamásolni a téma fájlszerkesztőjében (7 fájl). A termék- és oldalállapotokat
a fenti listák alapján vissza lehet kapcsolni; a snippetek maradhatnak, mert hivatkozás nélkül nem látszanak.
