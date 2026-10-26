# Kontyos webshop – kattintható demó

Statikus, szerver nélkül működő webshop-demó a **kontyos.hu** újratervezéséhez (Stratos Webdesign).

**Élő demó:** https://stratoswebdesign.github.io/kontyos/

## Mit tud
- Főoldal 4 szezonális heróval (forralt / újbor / Black Friday / karácsony – a felső DEMO sávban váltható), hover-widget a palackokon, gyümölcsválasztó
- Kategória (édes/száraz szűrő), FRISS & Secco, Pálinka lista
- 38 termékoldal a kontyos.hu valós adataival (leírás, paraméterek, értékelések), soronként saját arculattal, 1/3/6 palackos kiszereléssel és mennyiségi árral
- Kampányoldalak: Újbor-válogatás, Black Friday (várólista/aktív fázis), Karácsonyi ajándék bor (előzetes/aktív)
- Működő kosár (localStorage), mini-kosár, ingyenes-szállítás csík, pénztár validációval (18+ és ÁSZF nyilatkozat), köszönőoldal

## Fontos
- **Nem valódi bolt:** a rendelés nem megy el sehová, fizetés nincs.
- A `[SZÖGLETES]` részek helykitöltők (díjak, dátumok, címek, ÁSZF), ezeket a Kontyos adja meg.
- A szezonális csomagok tartalma és ára demó javaslat.
- Az élő bolt Shoprenteren fut; ez a demó a design és a vásárlási folyamat bemutatására szolgál.

## Fejlesztés
```
python3 src/build.py      # src/catalog.json → *.html, termek/*.html, assets/catalog.js
python3 -m http.server    # helyi előnézet: http://localhost:8000
```
