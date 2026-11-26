# Élesítési forgatókönyv – kontyos.hu (Shoprenter, Párizs téma)

## ÉLESÍTVE – 2026-11-26 14:28: DON CHERRY landing – `/don-cherry` (aktív téma: „Kontyos 13”, `paris_15`)
- Kérés (Artúr): a Graphasel Don Cherry landingjét a PIRI Mama szabályai szerint kitenni; a doncherry.hu a kontyos.hu/don-cherry címre irányítson.
- Forrás: Graphasel csomag (WeTransfer, nov. 26., Artúr Letöltések/`fejlesztesre`): Lovable TanStack-projekt (`don-cherry-cocktail-carousel.zip`, a képek csak
  Lovable-eszközmutatók → a hiányzókat a közzétett `don-cherry-cocktail-carousel.lovable.app` `/__l5e/assets-v1/…` címeiről töltöttük le), fontleírás (Poppins Bold, Archivo SemiExpanded; a kód Montserrat 800-at használ a címekhez).
- Átültetés (commit bbb6f23 + 14d18aa): `src/doncherry.py` → `doncherry.html` (a demófájl neve azért nem `don-cherry.html`, mert az a termékoldalak testvér-linkjével ütközne) → `snippets/ky-page-doncherry.tpl`.
  Saját `<style>` (.dc) és JS az oldalon, a jsDelivr-es CSS/JS változatlan. Képek: `img/doncherry/` (webp + életkép-videó 832/540 px, 0,8 / 0,36 MB) a GitHub Pagesről.
  - Valódi kosár: Vásárlás → `don-cherry`, `don-cherry-gyumolcse`; Koktélcsomag → `koktel-tonic` / `-negroni` / `-americano` / `-manhattan`; ár + termékoldal-link mindenhol.
  - Vásárlista: a Graphasel feliratai, dátum + élő státusz a közös FAIRS-ból (`data-fair`). Kapcsolat: mailto-űrlap helyett HIRLEVEL5 hírlevél; cím 6773 (a forrásban 6775).
  - Fejléc: sötétvörös (#7C000B), fehér logó, keret nélkül (`body:has(.dc)`); a Lovable fix menüje helyett ragadós belső menü.
  - Koktélsor: natív, végtelen, húzható/nyilazható (Embla helyett); a képek a betöltés után előtöltődnek (mobilon különben lapozáskor villant).
  - Koktélok oldal: link a landingre („Don Cherry világa…”).
- Tartalmi oldal **83** („Don Cherry meggyvermut”, SEO-URL `don-cherry`, a 80-as beállításaival; SEO-cím: `DON CHERRY – prémium édes meggyvermut | Kontyos`).
  Először Letiltottként, a téma aktiválása után Engedélyezett.
- Kiadás 1 (14:15): „Kontyos 12” (`paris_14`, a `paris_13` másolata): új `ky-page-doncherry`, `ky-page-koktelok` (élő = repó előző verziója, bd1bff6…),
  `information.tpl` mindkét `ky_imap`-be `"don-cherry": "ky-page-doncherry"`. Kiadás 2 (14:28): „Kontyos 13” (`paris_15`, a `paris_14` másolata) – csak a
  `ky-page-doncherry` (képelőtöltés). Mindkettő szerverről visszaolvasva bájtra egyezett. Cache-törlés nem kellett.
- Mérés: 132/132 anonim lekérés (66 oldal × asztali/iPhone) 200 + `paris_15` (gyors sorozatnál a szerver 201-es, ~2 KB-os fojtó választ ad – lassítva újrapróbálva mind OK);
  Playwright élesben asztali + iPhone: minden kép betölt, videó megy, lapozás azonnali, „Kosárba” valódi kosárba tesz (0 → 1) + mini-kosár; új JS-hiba nincs (a régi 2 marad).
- doncherry.hu: Netlify `doncherry-atiranyitas` (site 3dcab147-46a7-45df-8739-c2d209fefd7c, `/*` → `https://www.kontyos.hu/don-cherry` 301!, SSO csak a nem-élesen),
  domainek felvéve (doncherry.hu elsődleges + www). **DNS (Artúr, webdns.integrity.hu): A `@` és A `www` → 75.2.60.5** – utána tanúsítvány + mérés.
- Tanulság: a fájlszerkesztőben egy már megnyitott fül „Mentés” gombja néha nem reagál JS-es tartalomcserére → valódi billentyűleütés (x + Backspace) után a valódi kattintás ment.
- Következő kiadás alapja: friss másolat a `paris_15`-ből.

## ÉLESÍTVE – 2026-11-23 15:25: kiegészítők színválasztója, szövettáska, gin-szöveg (aktív téma: „Kontyos 11”, `paris_13`)
- Kérés (Artúr, Attila 11-13-i levele alapján + kinyomtatott korrektúra):
  - Gunpowder gin: le kell venni „A készlet erejéig kék díszdobozban, ajándék pohárral érkezik.” mondatot → törölve a gin oldaláról, és a Negroni csomag
    ugyanilyen megjegyzése is (Negroni-oldal, Don Cherry + Don gyümölcse oldal koktélcsomag-kártyája, Csomagok oldal). A Shoprenter-termékleírásokban nem volt benne.
  - Meggymag párna és Kontyos borospohár: a régi oldalon a vevő színt választott. **A Shoprenterben megvannak a termékopciók**, csak a saját termékoldalunk nem küldte:
    párna `option[6]` = 15 Fehér / 20 Virágos / 18 Piros; pohár `option[1]` = 1 kék / 3 piros; szövettáska `option[4]` = 10 „kék – indákkal” (egyetlen érték).
  - Szövettáska: a „További képek” fülön lévő kép (`product/Kiegészítők/Indas_szovettaska.jpg`) lett a főkép (a hibás Kontyos2026-kép törölve a termékből), és felkerült a
    Csomagok oldal „Egész évben” sorába (a Kiegészítők kategóriában eddig is ott volt).
- Megoldás (commit 4676867): `catalog.json` „opts” mező; a termékoldalon színválasztó (képes választógombok, a főkép vált), `name="option[ID]"`;
  a **pagehead.tpl-ben egy kis szkript** a kosárba tételhez (`fetch` POST `product_id`) hozzáteszi az `option[ID]` mezőt – a termékoldalon a kiválasztott,
  máshol (kártyák, ajánlók, mini-kosár) az első értéket. Így a globális JS-hez (élesben `ky-live-bw1129m.js` a fájlkezelőből) nem kellett nyúlni.
  Térkép: `cdn_pin.py` generálja a catalog „opts” + `live_pid.json` alapján (398, 388, 392). Új képek: `img/p/meggymag-parna-{viragos,piros}.webp`,
  `img/p/kontyos-borospohar-388-piros.webp` (fehér háttér kivágva), szövettáska `img/p|t/kontyos-szovettaska-392.webp` (Indas).
- Kiadás: „Kontyos 11” (`paris_13`, a `paris_11` másolata): 8 snippet (a `ky-page-csomagok` élőben eltért a repótól → célzott javítás az élő tartalmon:
  megjegyzés törlése + szövettáska-kártya beszúrása) + `pagehead.tpl` (CSS 890d0b9 → 4676867, opció-szkript). `footer_scripts.tpl` változatlan.
- Mérés: Playwright élesben, asztali + iPhone: párna 3 színgomb, választáskor vált a főkép; kosár: párna „Szín: Piros” (választott) / „Fehér” (alap),
  pohár a Csomagok kártyájáról „Szín: kék”; gin/Negroni oldalon nincs „díszdoboz”; szövettáska új kép + „Grafika: Kék, indás minta”. Új JS-hiba nincs.
- Tanulság (fájlszerkesztő): ha a megnyitott fül „Mentés” gombja szürke marad, a szerkesztő a tartalmat már mentettnek hiszi → előbb egy +„\n”-es
  változat mentése, utána a pontos tartalomé (két valódi kattintás). A fülek bezárásakor felugró „Nem mentett változtatás” ablakokra mindig „Nem”.
- Nyitott: a saját kosároldalunk (adapter) nem írja ki a kiválasztott színt a tétel alá (a Shoprenter-kosárban, a rendelésben és a visszaigazoló levélben benne van).
- Következő kiadás alapja: friss másolat a `paris_13`-ból. (A `paris_12` „Kontyos 10” néven soha nem volt aktív.)

## ÉLESÍTVE – 2026-11-19 09:05: PIRI Mama reklámfilmek + Széchenyi-badge (aktív téma: „Kontyos 10”, `paris_11`)
- Kérés (Artúr): a /pirimama hangulatvideója helyére a hosszú, fekvő HERO-film; a PIRI termékoldalak videója helyére a split screen, fekvőben;
  a Széchenyi-badge a főoldalon maradjon fix jobb lent, minden más oldalon elég a láblécben.
- Források (Vision Studio, SwissTransfer, Artúr Letöltések mappája): `PIRI_Mama_FINAL_16x9.mov` (51 mp, 1080p) és a javított
  `PR_Split screen16_9_final.mov` (nov. 18. 10:31, 17 mp, 4K). Webre: H.264 CRF 24/25, +faststart; 1080p + 720p (`<source media="(max-width:900px)">`),
  poster = 0. képkocka (webp). HERO: `img/pirimama/hero-film-{1080,720}.mp4` (6,8 / 3,4 MB, AAC hang); split: `img/video/piri_split-{1080,720}.mp4` (2,6 / 1,1 MB, hang nélkül).
- Commit 890d0b9: `.pm-video` / `.pd-video` 16:9 (`height:min(56.25vw,100svh)`, `object-fit:contain` – nincs vágás); a HERO némán, ismétlődve indul
  látótérben, „Hang be / Némítás” gomb (`.pm-snd`; első hangosításkor elölről indul). A régi `piri_hangulat.mp4` / `hangulat-720.mp4` a repóban maradt.
- Széchenyi (`pagehead.tpl`, cdn_pin.py): `body.home-body` → fix jobb lent (200×140, telefonon 120×84, a jogi sor jobbról 210 px-et hagy);
  `body:not(.home-body)` → a `.ky-legal-logos` sorban, saját sorban (200×140, telefonon 180×126).
- Kiadás: „Kontyos 10” (`paris_11`, a `paris_10` másolata): 5 snippet (`ky-page-pirimama`, 4× `ky-p-…piri…`) – az élő tartalom mind egyezett a d336d6c-vel;
  `pagehead.tpl`: a Széchenyi-blokk csere + CSS-hash 495d965 → 890d0b9. **A `footer_scripts.tpl` nem változott**: élesben NEM a jsDelivr-es
  `kontyos.live.js` töltődik, hanem `/custom/kontyos/image/data/ky-live-bw1129.js` (a 495d965 másolata módosított SEASON_DATES/PHASE_FROM-mal,
  Black Week nov. 23–29.) – ez a változás nincs a repóban, a `cdn_pin.py` footer-kimenete ezért élesben nem használható vakon.
- A témamásolás kétszer futott le (lassú visszajelzés) → a második „Kontyos 10” (`paris_12`) soha nem volt aktív, tiszta `paris_10`-másolat.
- Tanulság: a fájlszerkesztőben a JS-ből hívott `Mentés`-kattintás nem mentett; a valódi kattintás igen. Ellenőrzés a szerverről:
  `GET theme-api.shoprenter.com/shops/kontyos/themes/<téma>/files/template/<útvonal>` (X-JWT-Token fejléc) – a szerkesztő megnyitott fülei elavult tartalmat mutathatnak.
- Mérés: 24/24 anonim lekérés (12 oldal × asztali/iPhone) `paris_11` + 890d0b9; a /pirimama-n HERO, a 4 PIRI termékoldalon split screen.
  Playwright élesben: a videók játszanak (asztalon 1080p, iPhone-on 720p), a hanggomb működik; badge: főoldal fix (200 / 120 px), /pirimama,
  termékoldal: lábléc (static); új JS-hiba nincs (a régi 2 marad). Cache-törlés nem kellett (a főoldal azonnal `paris_11`).
- Következő kiadás alapja: friss másolat a `paris_11`-ből.

## ÉLESÍTVE – 2026-11-18 19:20: hópelyhek a PIRI Mama oldalakon (aktív téma: „Kontyos 9”, `paris_10`)
- Kérés (Artúr): a Graphasel Lovable-landingjén az egész oldalon végig hulló hópelyhek – a /pirimama-ra és a forralt termékoldalakra is.
- Commit 495d965: `snowfall()` (src/build.py) – fix, kattintás-átengedő réteg, 32 pehely (telefonon 18), a Graphasel arany hópehely-formája
  (`img/pirimama/hopehely.svg`) maszkként, törtfehér színnel; `prefers-reduced-motion` esetén kikapcsol. CSS: `.page-snow` a `kontyos.css`-ben.
  Oldalak: /pirimama + a 4 PIRI Mama termékoldal (klasszikus, epres, narancsos, 0%) – a többi oldal változatlan.
- Kiadás: „Kontyos 9” (`paris_10`, a `paris_9` másolata): 5 snippet (`ky-p-piri-mama-forralt-bora`, `ky-p-epres-…`, `ky-p-narancsos-…`,
  `ky-p-piri-mama-forro-itala-0`, `ky-page-pirimama`) – mindegyik élő tartalma egyezett a repó előző verziójával (5977cc5), csak utána csere;
  `pagehead.tpl` + `footer_scripts.tpl`: d9e30a7 → 495d965 (a JS azonos, csak a CSS változott) → aktiválva, cache törölve.
- Előtte élesben injektálva tesztelve (kontyos.css helyi fájlra cserélve + réteg beszúrva): fix réteg, maszk és animáció rendben.
  Utána: 18 lekérés (9 oldal × asztali/iPhone) mind `paris_10` + 495d965; pehely csak a 5 PIRI-oldalon; Playwright: 32/18 pehely, mini-kosár
  továbbra is működik, az értékelő űrlap megvan, új JS-hiba nincs.
- Következő kiadás alapja: friss másolat a `paris_10`-ből.


## ÉLESÍTVE – 2026-11-18 12:22: termékértékelés írása (aktív téma: „Kontyos 8”, `paris_9`)
- Hiba (Siket Gábor továbbította, 11-18): az értékelést kérő levélből érkező vásárló nem talált értékelő űrlapot. A Kontyos-termékoldal
  a Párizs teljes tartalmát lecseréli, így a gyári `productreview` modul (`position_4`) is eltűnt; a vélemények statikusak (catalog.json).
- Javítás (commit d6a7747): `shoprenter/snippets/ky-review.tpl` – a gyári modul rejtve renderelődik (product_id + CSRF), a látható űrlap
  az `#ertekelesek` szekcióba kerül, és a gyári végpontra küld (`/index.php?route=product/productreview/addreview`) → admin › Termék értékelések, jóváhagyásra.
  Koktélcsomagoknál (nincs vélemény-szekció) saját szekciót rajzol. Horgony: `#ertekeles-irasa` (a `#review_form` / `#review` is ide visz).
- Élesben a snippet tartalma a `product/product.tpl` ky-ágába van beillesztve (`KY-REVIEW START/END`), mert a fájlszerkesztőben új fájl nem hozható létre.
- Tesztelve élesben injektálva (asztali + iPhone): megjelenés, kliens-ellenőrzés, szerver-hibaág (hiányos adat → Shoprenter-hiba, friss token) –
  valódi vélemény nem lett beküldve. JS/CSS (jsDelivr d9e30a7) változatlan.
- 11-18 12:15: a **„Vélemény ösztönző”** automatikus levél (Marketing › Automatikus események, id 2, HU; 7 nappal a rendelés után) új arculatot kapott:
  `shoprenter/email/velemeny-osztonzo.html` (a régi: `velemeny-osztonzo.EREDETI.html`). Minden régi szöveg és változó maradt; új „Írj véleményt”
  szekció a `[PRODUCT_LIST_REVIEW]` változóval; javítva: logó-link, webshop@ e-mail-link (a fele zoltan.bencsik@-re mutatott), adatkezelési URL.
  Az EN változat érintetlen. A `[PRODUCT_LIST_REVIEW]` tényleges kimenete élő levélben még nem látott.
- Az értékelések a boltban **automatikusan elfogadódnak** (Termék értékelések › Mind) – a köszönőszöveg ehhez igazítva (commit bbfa0e7, `paris_9`-ben is).
- Aktiválva (Artúr jóváhagyásával) + Labor › Cache törlés. Mérés: 106/106 Kontyos-termékoldal (53 × asztali/iPhone) 200, mind `paris_9`,
  mindegyiken a gyári űrlap + a Kontyos-űrlap; az „Édes ünnepek” csomag (522) nincs a térképben → a Párizs gyári űrlapja jelenik meg (működik).
  Playwright élesben: PIRI (asztali), Kajszi `#review_form` horgonnyal (iPhone – az űrlap nyitva, fancybox nincs), Negroni (iPhone – saját szekció);
  kliens-ellenőrzés OK, új JS-hiba nincs (a régi 2 marad). Valódi vélemény nem lett beküldve.
- Nyitott: az új (automatikusan elfogadott) vélemények a Kontyos-oldalon csak a katalógus frissítése után látszanak (pl. nov. 3/8 PIRI Mama vélemények).
- Következő kiadás alapja: friss másolat a `paris_9`-ből.

## ÉLESÍTVE – 2026-11-17 18:25: kosárba tétel visszajelzése (aktív téma: „Kontyos 7”, `paris_8`)
- Hiba: élesben a „Kosárba” után semmi nem látszott – az adapter (`src/shoprenter_adapter.js`) elnyelte a kattintást, a demó mini-kosara nem futott.
- Javítás (commit d9e30a7): a gomb azonnal „dolgozik” (`ky-adding`), a Shoprenter-kosár frissítése után felugrik a mini-kosár
  (termék, a valódi kosárösszegből számolt „még X Ft az ingyenes szállításig”, Tovább a kosárhoz / Vásárolok még, Illik mellé),
  a fejléc kosár-számlálója ugrik egyet (`bump`). A felugró ablak `.ky`-burkolóban van (a stíluslap `.ky` alá zárt). Hiba esetén a termékoldalra visz.
- Kiadás: `cdn_pin.py d9e30a7` → „Kontyos 7” (`paris_8`, a `paris_7` másolata): a `pagehead.tpl` és a `footer_scripts.tpl` jsDelivr-hivatkozásában
  csak a commit-hash cserélve (219c1df → d9e30a7) → aktiválva, cache törölve. 219c1df óta a CSS/JS-ben más változás nem volt.
- Előtte élesben próbálva (Playwright, a jsDelivr-kérés helyi fájlra cserélve), utána élesben valódi kattintással: /pirimama, /gyumolcsbor,
  termékoldal (iPhone), főoldal (iPhone), Csomagajánlatok – mindenhol azonnali gombállapot, mini-kosár, számláló 0 → 1.
- Következő kiadás alapja: friss másolat a `paris_8`-ból.


## ÉLESÍTVE – 2026-11-17 este: PIRI Mama landing – `/pirimama` (aktív téma: „Kontyos 6”, `paris_7`)
A Graphasel Lovable-landingjének statikus átültetése (forrás: `src/pirimama.py`, demó: `pirimama.html`).
A stílus és a JS az oldal snippetjében él → a jsDelivr-re rögzített `kontyos.css` / `kontyos.live.js` **változatlan** maradt.
A képek a GitHub Pages-ről jönnek (`img/pirimama/`), mint a termékképek.
- Tartalmi oldal **80** („PIRI Mama forralt bor”, SEO-URL `pirimama`, menü/lábléc nélkül, Engedélyezett).
  SEO-cím: `PIRI Mama forralt bor – a tél fűszereivel | Kontyos`; meta-leírás a 80-as oldalon.
- **Fontos:** a `paris_5` NEM tiszta alap – a `paris_3`-ból készült a `paris_4`-gyel egy időben, és hiányoznak belőle a „Kontyos 4” módosításai
  (pl. a lábléc régi telefonszáma). Ezért friss másolat készült: „Kontyos 5” (`paris_6`) = `paris_4` másolata.
  - `paris_6`: új `snippets/ky-page-pirimama.tpl`, frissült `snippets/ky-page-forralt.tpl` (link a PIRI Mama oldalra), az `information/information.tpl`
    mindkét `ky_imap` térképébe bekerült a `"pirimama": "ky-page-pirimama"` → aktiválva, cache törölve, oldal Engedélyezett.
  - Élesben derült ki: a Webshop-doboz `.card` osztályát a generátor `k-card`-ra nevezte (Párizs-ütközés), az oldal saját stílusa viszont `.card`-ot várt
    → javítás `pm-sc` osztállyal (commit 14b0462) + build-ellenőrzés; kiadás: „Kontyos 6” (`paris_7`) = `paris_6` másolata a javított snippettel → aktiválva, cache törölve.
  - Következő kiadás alapja: friss másolat a `paris_7`-ből (a `paris_5` ne legyen alap).
- Mérés (anonim, asztali + iPhone, 12 oldal × 2 kör): mind `paris_7`, a `/pirimama` 200, 22 belső link és 38 kép/videó él;
  Playwright: sötét fejléc arany logóval, vásár-dátumok élnek, „Kosárba” valódi Shoprenter-kosárba tesz (0 → 1).
  A konzol 2 JS-hibája (`addEventListener` / `offsetHeight` null) minden oldalon megvan, nem a landingtől jön.
- Nyitott: pirimama.hu → `https://www.kontyos.hu/pirimama` 301 (Artúr); og:image; sitemap / Search Console; Joules et Jaques font és hero-fotó licence (Graphasel).

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
- **23:35-től az aktív téma: „Kontyos 2” (`paris_2`).** A `paris_1`-ben mentett utólagos módosítások is csak a kiszolgálók egy részén
  jelentek meg (a jelenség minden már lefordított témánál fennáll), ezért a **módosítások élesítése = témamásolás**:
  1. a módosítást a még soha nem aktív témapéldányba (vagy egy friss másolatba) írjuk – inaktív témában nincs gyorsítótár;
  2. a másolatot aktiváljuk (Téma kiválasztás › Műveletek › Aktivál);
  3. kívülről mérünk (`/tmp`-s chk4-szkript mintájára: kontyos.live.js, Kampányok, készítő-sor, Széchenyi-arány, korhatár-ablak, testvér-linkek).
  A korábbi témák (`paris_global`, `paris_1`) inaktív tartalékok.
- 23:35-ös kiadás: termékoldali testvér-linkek (17 snippet, 404 volt), lábléc (Kampányok: csak Vásárok + Koktélok; „Weboldalt készítette
  és karbantartja: Stratos Webdesign” a fizetési logók sorában), Széchenyi-badge arány (200×140, mobilon 140×98), a Shoprenter beépített
  korhatár-ablaka elrejtve (a Kontyos-kapu marad). Mérés: 269/269 lekérés hibátlan, 0 db 404 a renderelt linkek között.
- **2026-11-11 09:35-től az aktív téma: „Kontyos 3” (`paris_3`).** Kiadás: mobilon (≤760 px) a Széchenyi-badge termék-
  és aloldalakon a láblécbe kerül (static, 180×126), így nem takarja a ragadós „Kosárba” sávot; a főoldalon marad fix
  jobb lent 120×84; asztalin változatlan 200×140, a jogi sor jobbról 210 px-et hagy neki. Mérés: 276 lekérés (69 oldal ×
  asztali/iPhone × 2) hibátlan (az első, párhuzamos körben 15 időtúllépés a téma első fordítása miatt, egyenként újra: mind OK);
  Playwright iPhone 13: „Kosárba” látható, nincs vízszintes görgetés.
- **2026-11-11 10:05-től az aktív téma: „Kontyos 4” (`paris_4`).** (A másoláskor egy második „Kontyos 4” is létrejött,
  `paris_5` – soha nem volt aktív, ez a következő kiadás tiszta alapja.) Kiadás:
  - telefonszám mindenhol **+36 30 094 5042** (`tel:+36300945042`): ky-footer, ky-page-aszf/-info/-adatkezeles; adatbázisban:
    Kapcsolat oldal (egyedi tartalom HU/EN, Siket Gábor sora is), tartalmi oldalak 5, 43, 48, 49, 64; `llms.txt`.
    A bolt `config_telephone` már az új szám volt; a rendelési levelekben (26 állapot) nem szerepelt szám.
  - mobilmenüből (drawer) kikerült a FRISS;
  - Széchenyi-badge telefonon: csak a termékoldalon (`body.product-page-body`) a láblécben, minden más oldalon fix jobb lent 120×84;
  - `sections/contact_paris.tpl` kikapcsolva (`{% if false and … %}`) – a rejtett régi Párizs-menüben Shoprenter-mintaadatok
    voltak (Debrecen, info@shoprenter.hu, +36-1/234-5012).
  - Aktiválás után a főoldal ~13%-a még `paris_2`-t adott (teljes oldalas gyorsítótár) → Labor › Cache törlés → 60/60 `paris_4`.
  - `llms.txt`: a fájlkezelő nem ír felül (törlés + feltöltés kell: `fileconnector?mode=delete&path=/llms.txt`), és a
    `/custom/…` statikus fájlokat a szerver 30 napig cache-eli → a 301 célja `custom/kontyos/image/data/llms.txt?v=2`
    (következő frissítéskor `v=3`).
  - Mérés: 150/150 lekérés (asztali + iPhone) hibátlan; Playwright iPhone 13: Kosárba látható, menü FRISS nélkül.
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
