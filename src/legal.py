# -*- coding: utf-8 -*-
"""Jogi oldalak (ÁSZF, Adatkezelési tájékoztató) – IDEIGLENES szöveg, amíg jogász által írt változat nem készül.

Forrás: a kontyos.hu 2024.10.18-i ÁSZF-jének tényadatai (cégadatok, adatfeldolgozók), a demó szállítási/fizetési
táblázata, valamint a hatályos szabályok: GDPR (2016/679 EU rendelet) 12–14. és 28. cikk, Infotv., Ptk., Fgytv.,
Ektv. (2001. évi CVIII.), 45/2014. (II. 26.) Korm. rendelet (az elállási funkcióval, 2026. június 19-től),
373/2021. (VI. 30.) Korm. rendelet. Az EU ODR-platform 2025. július 20-án megszűnt, ezért nem hivatkozunk rá.
A blokkok: ('h2', cím, horgony) · ('h3', cím) · ('p', html) · ('ul', [html…]) · ('table', fejléc, sorok) · ('dl', [(kulcs, érték)…])
"""

EFFECTIVE = '2026. november – az új webáruház indulásának napjától'

CO = [('Cégnév', 'Kontyos Borház Kft.'), ('Székhely', '6773 Klárafalva, Kossuth u. 183.'),
      ('Cégjegyzékszám', '06-09-017653 (Szegedi Törvényszék Cégbírósága)'), ('Adószám', '23503016-2-06'),
      ('Működési engedély száma', '398/2012.'), ('NÉBIH engedélyszám', '330-07-KüE-1263'),
      ('Bankszámla', 'OTP Bank 11735074-20517986'), ('Telefon', '<a href="tel:+36203492185">+36-20/349-2185</a>'),
      ('E-mail', '<a href="mailto:info@kontyos.hu">info@kontyos.hu</a> · webshop: <a href="mailto:webshop@kontyos.hu">webshop@kontyos.hu</a>')]

HOST = [('Tárhelyszolgáltató', 'ShopRenter.hu Kft.'), ('Székhely', '4028 Debrecen, Kassai út 129.'), ('Cégjegyzékszám', '09-09-020636'),
        ('Adószám', '23174108-2-09'), ('E-mail', 'info@shoprenter.hu'), ('Telefon', '+36-1/234-5011')]

SHIP = [('GLS házhozszállítás', '3–5 munkanap', '2 400 Ft', 'átutalás, utánvét (+500 Ft), bankkártya'),
        ('GLS csomagpont', '3–5 munkanap', '2 100 Ft', 'átutalás, fizetés az átadó helyen (+500 Ft), bankkártya'),
        ('MPL csomagautomata', '3–5 munkanap', '1 800 Ft', 'átutalás, bankkártya'),
        ('MPL PostaPont', '1–3 munkanap', '1 800 Ft', 'átutalás, bankkártya'),
        ('MPL postán maradó', '1–3 munkanap', '1 800 Ft', 'átutalás, bankkártya'),
        ('Személyes átvétel a klárafalvi borászatban', 'előzetes egyeztetéssel', 'ingyenes', 'átutalás, bankkártya')]

BEKELTETO = ('Csongrád-Csanád Vármegyei Békéltető Testület – 6721 Szeged, Párizsi krt. 8–12. · tel.: (62) 554-250/118 · '
             'e-mail: bekelteto.testulet@csmkik.hu · www.bekeltetes-csongrad.hu')
FOGYVED = ('Csongrád-Csanád Vármegyei Kormányhivatal, fogyasztóvédelmi hatóság – 6722 Szeged, Rákóczi tér 1. · tel.: (62) 680-530 · '
           'e-mail: fogyasztovedelem@csongrad.gov.hu')
NAIH = ('Nemzeti Adatvédelmi és Információszabadság Hatóság (NAIH) – 1055 Budapest, Falk Miksa utca 9–11. · postacím: 1363 Budapest, Pf. 9. · '
        'tel.: +36-1/391-1400 · e-mail: ugyfelszolgalat@naih.hu · www.naih.hu')

W = '<a href="{withdraw}">Elállás a szerződéstől</a>'

ASZF = [
    ('p', '<b>Hatályos:</b> ' + EFFECTIVE),
    ('p', 'Ez az Általános Szerződési Feltételek (ÁSZF) a <b>kontyos.hu</b> webáruházban történő vásárlás feltételeit tartalmazza: '
          'ki az eladó, hogyan jön létre a szerződés, mennyibe kerül a szállítás, és milyen jogok illetnek meg vásárlóként. '
          'Kérjük, rendelés előtt olvasd el. A megrendelés elküldésével elfogadod az itt leírtakat.'),
    ('h2', '1. Az eladó adatai', 'elado'),
    ('dl', CO),
    ('h3', 'A tárhelyszolgáltató adatai'),
    ('dl', HOST),
    ('h2', '2. Alapvető tudnivalók', 'alap'),
    ('ul', ['A szerződés a Kontyos Borház Kft. (a továbbiakban: Eladó) és a vásárló (a továbbiakban: Vevő) között, távollévők között, elektronikus úton jön létre. '
            'A szerződésre a magyar jog, különösen a Polgári Törvénykönyv (Ptk.), a fogyasztóvédelmi törvény (Fgytv.), az elektronikus kereskedelemről szóló '
            '2001. évi CVIII. törvény (Ektv.) és a 45/2014. (II. 26.) Korm. rendelet az irányadó.',
            'A szerződés nyelve magyar. A megkötött szerződést az Eladó nem iktatja, utólag nem hozzáférhető; a rendelés adatait a visszaigazoló e-mail tartalmazza.',
            'Az Eladó magatartási kódexnek nem veti alá magát.',
            'Az Eladó az ÁSZF-et módosíthatja; a módosítás a közzététel után leadott rendelésekre vonatkozik.']),
    ('h2', '3. Csak 18 éven felülieknek', 'eletkor'),
    ('p', 'A webáruházban kínált termékek többsége <b>alkoholtartalmú ital</b>. Alkoholtartalmú terméket kizárólag 18. életévét betöltött személy rendelhet és vehet át. '
          'A megrendeléssel a Vevő kijelenti, hogy elmúlt 18 éves. Az átadáskor a futár, az átvételi pont vagy az Eladó kérheti az életkor igazolását; '
          'ha ez nem történik meg, vagy a címzett láthatóan kiskorú, az alkoholtartalmú terméket nem adjuk át.'),
    ('h2', '4. Termékek és árak', 'arak'),
    ('ul', ['A termékek lényeges tulajdonságait a termékoldalak tartalmazzák. A fotók illusztrációk, a címke és a kiszerelés évjáratonként kissé eltérhet.',
            'Az árak magyar forintban értendők, és tartalmazzák az általános forgalmi adót (bruttó árak). A szállítási díjat a kosár és a pénztár külön mutatja.',
            '<b>Visszaváltási díj (DRS):</b> a jogszabály szerint visszaváltási díjas italcsomagolásban értékesített termékek után a kosár külön soron palackonként '
            '<b>50 Ft</b> visszaváltási díjat számol fel. A díjat az üres csomagolás visszaváltásakor bármely MOHU visszaváltó ponton visszakapod.',
            'Mennyiségi ár: egyes termékeknél 6 palacktól kedvezményes egységár érvényes, amelyet a termékoldal jelez.',
            'A csomagok, szezonális akciók és kuponok feltételeit és időtartamát az adott ajánlat oldala tartalmazza. Akciós ár csak a feltüntetett időszakban érvényes.',
            'Ha a webáruházban – gondos eljárás ellenére – nyilvánvalóan hibás ár jelenik meg (például a szokásos ár töredéke vagy 0 Ft), az Eladó nem köteles a terméket '
            'hibás áron teljesíteni. Ilyenkor felajánljuk a helyes áron történő teljesítést, amelynek ismeretében a Vevő elállhat a vásárlástól.']),
    ('h2', '5. A rendelés menete', 'rendeles'),
    ('ul', ['A kiválasztott termékeket a „Kosárba” gombbal teheted a kosárba; a kosár tartalma és a darabszám ott módosítható.',
            'A „Tovább a pénztárhoz” gombbal add meg az elérhetőségeidet, a szállítási és számlázási adatokat, majd válassz szállítási és fizetési módot. '
            'Regisztráció nélkül, vendégként is rendelhetsz.',
            'Az utolsó lépésben az összesítőn ellenőrizheted és javíthatod a megadott adatokat. A rendelést a fizetési kötelezettséggel járó megrendelés-gombbal küldöd el.',
            'A rendelés beérkezését a rendszer automatikus e-mailben azonnal visszaigazolja. Ha ez 48 órán belül nem érkezik meg, mentesülsz az ajánlati kötöttség alól. '
            'A szerződés a visszaigazoló e-mail megérkezésével jön létre.',
            'Ha rendelés közben hibát észlelsz, írj a webshop@kontyos.hu címre – a rendelést a teljesítés előtt módosítjuk vagy töröljük.']),
    ('h2', '6. Fizetés', 'fizetes'),
    ('ul', ['<b>Bankkártyás fizetés:</b> a SimplePay by OTP rendszerén keresztül (OTP Mobil Kft.). A kártyaadatok a fizetési szolgáltatóhoz kerülnek, azokat az Eladó nem látja és nem tárolja.',
            '<b>Előre utalás:</b> a rendelés visszaigazolásában szereplő adatokkal, a rendelésszám közleményként való megadásával. A csomagot a jóváírás után adjuk fel.',
            '<b>Utánvét</b> (GLS házhozszállítás) és fizetés az átadó helyen (GLS csomagpont): +500 Ft kezelési díj.',
            'Személyes átvételnél előre utalás vagy bankkártyás fizetés választható.',
            'A számlát elektronikusan, e-mailben küldjük.']),
    ('p', '<b>Adattovábbítási nyilatkozat (SimplePay):</b> tudomásul veszem, hogy a Kontyos Borház Kft. (6773 Klárafalva, Kossuth u. 183.) adatkezelő által a kontyos.hu '
          'felhasználói adatbázisában tárolt alábbi személyes adataim átadásra kerülnek az OTP Mobil Kft. (1143 Budapest, Hungária krt. 17–19.), mint adatfeldolgozó részére: '
          'név, e-mail cím, telefonszám, számlázási és szállítási cím, a rendelés száma és összege. Az adatfeldolgozó által végzett adatfeldolgozási tevékenység jellege és célja '
          'a SimplePay adatkezelési tájékoztatóban (simplepay.hu/vasarlo-aff) tekinthető meg.'),
    ('h2', '7. Szállítás', 'szallitas'),
    ('table', ['Szállítási mód', 'Szállítási idő*', 'Díj', 'Fizetési mód'], SHIP),
    ('ul', ['*A rendelés visszaigazolásától (előre utalásnál a jóváírástól) számítva. A teljesítési határidő legfeljebb 30 nap.',
            '<b>25 000 Ft feletti</b> rendelési érték (a termékek bruttó listaára alapján) esetén a szállítás ingyenes. Egyes csomagajánlatoknál a szállítás az összegtől függetlenül ingyenes – ezt az ajánlat jelzi.',
            'A csomagot átvételkor ellenőrizd. Ha sérült, kérj jegyzőkönyvet a futártól, és jelezd a webshop@kontyos.hu címen – a sérült vagy hiányzó terméket pótoljuk.',
            'A csomagponton és automatában a csomag a szolgáltató által megadott ideig vehető át, utána visszakerül a borászathoz.',
            'Külföldre (EU) egyedi ajánlat alapján szállítunk: webshop@kontyos.hu.']),
    ('h2', '8. Elállási jog', 'elallas'),
    ('p', 'Fogyasztóként a terméknek (több termék esetén az utolsó terméknek) a te vagy az általad megjelölt személy általi átvételétől számított <b>14 napon belül</b> '
          'indoklás nélkül elállhatsz a vásárlástól. Az elállási jogot a szerződés megkötése és a termék átvétele között is gyakorolhatod.'),
    ('h3', 'Hogyan állhatsz el?'),
    ('ul', ['<b>Online, az elállási funkcióval:</b> a láblécben és itt is elérhető ' + W + ' oldalon add meg a rendelésszámot, a nevedet és e-mail címedet, majd erősítsd meg az elállást. '
            'A beérkezett elállást e-mailben haladéktalanul visszaigazoljuk.',
            'E-mailben (webshop@kontyos.hu) vagy postai levélben (6773 Klárafalva, Kossuth u. 183.), egyértelmű nyilatkozattal – ehhez használhatod az alábbi nyilatkozatmintát is.',
            'Az elállás határidőben érvényes, ha a nyilatkozatot a 14. nap végéig elküldöd.']),
    ('h3', 'Az elállás következményei'),
    ('ul', ['Az elállástól számított 14 napon belül visszatérítjük a teljes kifizetett összeget, a szállítási költséget is (kivéve a legolcsóbb szokásos szállítási módnál drágább '
            'szállítás többletköltségét). A visszatérítés az eredeti fizetési móddal történik, hacsak másban nem állapodunk meg; ez többletköltséget nem jelent.',
            'A visszatérítést visszatarthatjuk, amíg a terméket vissza nem kaptuk, vagy amíg nem igazoltad, hogy visszaküldted – a kettő közül a korábbi időpontig.',
            'A terméket legkésőbb az elállás közlésétől számított 14 napon belül kell visszaküldened vagy átadnod a 6773 Klárafalva, Kossuth u. 183. címen. '
            'A visszaküldés közvetlen költsége téged terhel.',
            'A termék jellegének, tulajdonságainak és működésének megállapításához szükséges használatot meghaladó használatból eredő értékcsökkenésért felelsz '
            '(például felbontott, részben elfogyasztott ital).']),
    ('h3', 'Kivételek'),
    ('p', 'Nem illeti meg elállási jog a fogyasztót – a 45/2014. (II. 26.) Korm. rendelet 29. §-a alapján – többek között a romlandó vagy minőségét rövid ideig megőrző termék, '
          'valamint az olyan zárt csomagolású termék esetén, amely egészségvédelmi vagy higiéniai okokból az átadást követő felbontás után nem küldhető vissza.'),
    ('h3', 'Elállási nyilatkozatminta'),
    ('p', '<i>Címzett: Kontyos Borház Kft., 6773 Klárafalva, Kossuth u. 183., webshop@kontyos.hu<br>Alulírott kijelentem, hogy gyakorlom elállási jogomat az alábbi termék(ek) '
          'adásvételére irányuló szerződés tekintetében: … · Rendelésszám: … · Átvétel időpontja: … · Név: … · Cím: … · Aláírás (csak papíron történő közlés esetén) · Kelt: …</i>'),
    ('h2', '9. Szavatosság és jótállás', 'szavatossag'),
    ('h3', 'Kellékszavatosság'),
    ('p', 'Az Eladó hibás teljesítése esetén kellékszavatossági igényt érvényesíthetsz: kérheted a kijavítást vagy a kicserélést, ha ez lehetetlen vagy aránytalan, '
          'árleszállítást kérhetsz, vagy elállhatsz a szerződéstől. A hibát felfedezése után haladéktalanul jelezd; a teljesítéstől számított két éven túl az igény nem '
          'érvényesíthető. A teljesítéstől számított egy éven belül – az ellenkező bizonyításáig – vélelmezni kell, hogy a hiba már a teljesítéskor fennállt '
          '(373/2021. (VI. 30.) Korm. rendelet). A minőségét rövid ideig megőrző termékeknél a minőségmegőrzési idő az irányadó.'),
    ('h3', 'Termékszavatosság'),
    ('p', 'A saját gyártású termékeink (gyümölcsborok, Don Cherry, pálinkák) gyártója az Eladó. Termékhiba esetén termékszavatossági igényként a termék kicserélését kérheted '
          'a termék forgalomba hozatalától számított két éven belül. A hibát neked kell bizonyítanod. Ugyanazon hiba miatt kellék- és termékszavatossági igényt egyszerre nem '
          'érvényesíthetsz. Partnertermékek (pl. Campari, gin, tonik) esetén a termékszavatossági igény a gyártóval szemben érvényesíthető.'),
    ('h3', 'Jótállás'),
    ('p', 'Az értékesített termékekre jogszabály kötelező jótállást nem ír elő, és az Eladó önkéntes jótállást nem vállal.'),
    ('h2', '10. Panaszkezelés és jogérvényesítés', 'panasz'),
    ('ul', ['Panaszodat e-mailben (webshop@kontyos.hu), telefonon (+36-20/349-2185) vagy levélben (6773 Klárafalva, Kossuth u. 183.) teheted meg. '
            'Az írásbeli panaszra 30 napon belül írásban, érdemben válaszolunk; a panaszról felvett jegyzőkönyvet és a válasz másolatát 3 évig megőrizzük.',
            'Ha a panaszt elutasítjuk, vagy a válasszal nem értesz egyet, az alábbi szervekhez fordulhatsz:',
            '<b>Békéltető testület</b> (a vállalkozás székhelye szerint illetékes, ingyenes, peren kívüli eljárás): ' + BEKELTETO + '. Az Eladót a békéltető testületi eljárásban együttműködési kötelezettség terheli.',
            '<b>Fogyasztóvédelmi hatóság:</b> ' + FOGYVED + '.',
            '<b>Bíróság:</b> a polgári perrendtartás szerint illetékes bíróság.']),
    ('h2', '11. Szerzői jog', 'szerzoi'),
    ('p', 'A webáruház tartalma (szövegek, fotók, grafikák, logók, a felület kialakítása) szerzői jogi védelem alatt áll. Előzetes írásbeli engedélyünk nélkül nem másolható, nem terjeszthető.'),
    ('h2', '12. Adatkezelés', 'adatvedelem'),
    ('p', 'A személyes adatok kezeléséről az <a href="{privacy}">Adatkezelési tájékoztató</a> rendelkezik.'),
]

ADAT = [
    ('p', '<b>Hatályos:</b> ' + EFFECTIVE),
    ('p', 'Ebben a tájékoztatóban leírjuk, milyen személyes adatokat kezelünk rólad, amikor a kontyos.hu webáruházat használod, miért és meddig, kinek adjuk át, '
          'és milyen jogaid vannak. A tájékoztató az Európai Unió általános adatvédelmi rendelete (GDPR, 2016/679/EU rendelet) és az információs önrendelkezési jogról '
          'szóló 2011. évi CXII. törvény (Infotv.) alapján készült.'),
    ('h2', '1. Az adatkezelő', 'adatkezelo'),
    ('dl', [CO[0], CO[1], CO[2], CO[3], ('Adatvédelmi kérdések', '<a href="mailto:info@kontyos.hu">info@kontyos.hu</a> · +36-20/349-2185 · levélben a székhely címén')]),
    ('p', 'Adatvédelmi tisztviselő kijelölésére a Kontyos Borház Kft. nem köteles, ilyet nem jelölt ki.'),
    ('h2', '2. Milyen adatokat, mire és meddig kezelünk?', 'celok'),
    ('table', ['Cél', 'Kezelt adatok', 'Jogalap', 'Időtartam'], [
        ('Megrendelés teljesítése, kapcsolattartás a rendelésről', 'név, e-mail, telefonszám, szállítási cím, rendelés tartalma és összege, választott szállítási és fizetési mód',
         'szerződés teljesítése – GDPR 6. cikk (1) b)', 'a szerződés teljesítésétől számított 5 év (polgári jogi elévülés)'),
        ('Számlázás, könyvelés', 'név, számlázási cím, (cég esetén) adószám, a megvásárolt termékek és összegek',
         'jogi kötelezettség – GDPR 6. cikk (1) c), az áfatörvény 159. § és a számviteli törvény 169. §', '8 év'),
        ('Életkor-nyilatkozat (18+)', 'a rendeléskor tett nyilatkozat ténye',
         'jogi kötelezettség – alkoholtartalmú ital kiskorúnak nem értékesíthető; GDPR 6. cikk (1) c)', 'a rendelési adatokkal együtt, 5 év'),
        ('Vásárlói fiók (regisztráció), törzsvásárlói kedvezmény', 'név, e-mail, telefonszám, címek, jelszó (titkosítva), korábbi rendelések, törzsvásárlói szint',
         'szerződés – GDPR 6. cikk (1) b)', 'a fiók törléséig; a fiók bármikor törölhető'),
        ('Elállás, panasz, szavatossági igény kezelése', 'név, elérhetőség, rendelésszám, a kérés tartalma, a válasz',
         'jogi kötelezettség – GDPR 6. cikk (1) c), Fgytv. 17/A. §, 45/2014. Korm. rendelet', 'panasz: 3 év (Fgytv.); egyéb: a polgári jogi elévülésig, 5 év'),
        ('Hírlevél és az 5%-os feliratkozási kupon', 'e-mail cím, (ha megadod) név, a feliratkozás időpontja, a kupon felhasználása',
         'hozzájárulás – GDPR 6. cikk (1) a)', 'a hozzájárulás visszavonásáig (leiratkozás a hírlevél alján lévő linkkel vagy e-mailben)'),
        ('Vásári értesítő (adventi standjaink nyitása)', 'e-mail cím, a kiválasztott városok',
         'hozzájárulás – GDPR 6. cikk (1) a)', 'a hozzájárulás visszavonásáig, de legkésőbb a szezon végéig'),
        ('Kapcsolatfelvétel, ügyfélszolgálat', 'név, e-mail, telefonszám, az üzenet tartalma',
         'hozzájárulás – GDPR 6. cikk (1) a), illetve rendeléssel kapcsolatos kérdésnél szerződés – (1) b)', 'az ügy lezárásától számított 1 év'),
        ('Webáruház működése, biztonság (szükséges sütik, naplózás)', 'IP-cím, munkamenet-azonosító, kosár tartalma, böngésző adatai',
         'jogos érdek – GDPR 6. cikk (1) f), az elektronikus hírközlésről szóló törvény 155. § (4)', 'a munkamenet végéig, illetve legfeljebb 30 nap'),
        ('Látogatottsági statisztika (Google Analytics)', 'sütiazonosító, a látogatás adatai (megtekintett oldalak, eszköz, hozzávetőleges hely)',
         'hozzájárulás – GDPR 6. cikk (1) a), a sütibeállítások szerint', 'legfeljebb 14 hónap'),
        ('Hirdetések mérése, remarketing (Google Ads, Meta pixel)', 'sütiazonosító, a látogatás és a vásárlás eseményei',
         'hozzájárulás – GDPR 6. cikk (1) a), a sütibeállítások szerint', 'a hozzájárulás visszavonásáig, legfeljebb 13 hónap'),
    ]),
    ('p', 'A rendeléshez és a szerződés teljesítéséhez szükséges adatok megadása nélkül nem tudjuk teljesíteni a rendelést. A hozzájáruláson alapuló adatkezelésekhez adott '
          'hozzájárulásodat bármikor, indoklás nélkül visszavonhatod; ez nem érinti a visszavonás előtti adatkezelés jogszerűségét.'),
    ('h2', '3. Sütik (cookie-k)', 'sutik'),
    ('ul', ['A <b>szükséges sütik</b> a kosár, a belépés és a pénztár működéséhez kellenek – ezek nélkül a webáruház nem működik, ezért ezekhez nem kérünk hozzájárulást.',
            'A <b>statisztikai</b> (Google Analytics) és a <b>marketing</b> (Google Ads, Meta pixel) sütiket csak a hozzájárulásod után kapcsoljuk be. A választásodat az első látogatáskor '
            'megjelenő sütisávban adhatod meg, és a lábléc „Sütibeállítások” linkjén bármikor módosíthatod.',
            'A sütiket a böngésződ beállításaiban is törölheted vagy tilthatod.']),
    ('h2', '4. Kinek adjuk át az adatokat? (adatfeldolgozók és címzettek)', 'cimzettek'),
    ('table', ['Címzett', 'Feladat', 'Adatok'], [
        ('ShopRenter.hu Kft. (4028 Debrecen, Kassai út 129.)', 'webáruház-rendszer, tárhely, rendelés- és hírlevélkezelés', 'a webáruházban megadott összes adat'),
        ('OTP Mobil Kft. (1143 Budapest, Hungária krt. 17–19.)', 'bankkártyás fizetés (SimplePay)', 'név, e-mail, telefonszám, cím, rendelésszám, összeg'),
        ('GLS Hungary Kft. (2351 Alsónémedi, GLS Európa u. 2.)', 'csomagszállítás', 'név, cím, telefonszám, e-mail, utánvét összege'),
        ('Magyar Posta Zrt. (1138 Budapest, Dunavirág utca 2–6.)', 'csomagszállítás (MPL)', 'név, cím, telefonszám, e-mail'),
        ('MiniCRM Zrt. (1075 Budapest, Madách Imre út 13–14.)', 'ügyféladatok tárolása, hírlevélküldés', 'név, e-mail, (feliratkozás adatai)'),
        ('ENTER \'93 Kft. (9700 Szombathely, Veres P. u. 12.)', 'számlázó és jövedéki nyilvántartó program', 'számlázási adatok'),
        ('Könyvelő (Bicskei-Barsi Kata ev., 6724 Szeged)', 'könyvelés', 'számlázási adatok'),
        ('Google Ireland Ltd. (Dublin, Írország)', 'látogatottsági statisztika és hirdetésmérés – csak hozzájárulással', 'sütiazonosító, látogatási és konverziós adatok'),
        ('Meta Platforms Ireland Ltd. (Dublin, Írország)', 'hirdetésmérés (Meta pixel) – csak hozzájárulással', 'sütiazonosító, látogatási és konverziós adatok'),
    ]),
    ('p', 'A Google és a Meta az adatokat az Egyesült Államokba is továbbíthatja. Az adattovábbítás az EU–USA Adatvédelmi Keretrendszer (Data Privacy Framework) alapján hozott '
          'megfelelőségi határozat, illetve az általános szerződési feltételek (SCC) alapján történik. A Meta pixel használata során a Kontyos Borház Kft. és a Meta közös adatkezelőnek minősül '
          'az adatgyűjtés és -továbbítás tekintetében. Hatósági megkeresésre jogszabály alapján adatot adhatunk ki. Személyes adatot nem adunk el.'),
    ('h2', '5. Milyen jogaid vannak?', 'jogok'),
    ('ul', ['<b>Hozzáférés:</b> tájékoztatást kérhetsz arról, milyen adatot kezelünk rólad, és másolatot kérhetsz róluk.',
            '<b>Helyesbítés:</b> kérheted a pontatlan adatok javítását (a fiókodban magad is módosíthatod).',
            '<b>Törlés:</b> kérheted adataid törlését, ha már nincs szükség rájuk, vagy visszavontad a hozzájárulásodat – kivéve, ha jogszabály megőrzésüket írja elő (pl. számla).',
            '<b>Korlátozás:</b> kérheted, hogy ideiglenesen csak tároljuk az adatokat (pl. ha vitatod a pontosságukat).',
            '<b>Adathordozhatóság:</b> a szerződés vagy hozzájárulás alapján kezelt, általad megadott adatokat géppel olvasható formában megkaphatod.',
            '<b>Tiltakozás:</b> a jogos érdeken alapuló adatkezelés ellen tiltakozhatsz.',
            '<b>Hozzájárulás visszavonása:</b> bármikor, a hírlevél leiratkozó linkjével, a sütibeállításokban vagy e-mailben.']),
    ('p', 'Kérésedet az info@kontyos.hu címre küldd. A kérést legkésőbb egy hónapon belül teljesítjük (indokolt esetben ez további két hónappal meghosszabbítható, erről értesítünk). '
          'A kérés teljesítése díjmentes. A visszaélések elkerülése érdekében azonosítást kérhetünk. Automatizált döntéshozatalt (profilalkotáson alapuló, joghatással járó döntést) nem alkalmazunk; '
          'a törzsvásárlói szint a teljesített rendelések összege alapján, kizárólag kedvezményt biztosítva számolódik.'),
    ('h2', '6. Jogorvoslat', 'jogorvoslat'),
    ('ul', ['Ha úgy érzed, hogy megsértettük az adatvédelmi jogaidat, kérjük, először keress minket – igyekszünk gyorsan orvosolni.',
            'Panaszt tehetsz a felügyeleti hatóságnál: ' + NAIH + '.',
            'Bírósághoz is fordulhatsz; a per – választásod szerint – a lakóhelyed vagy tartózkodási helyed szerinti törvényszék előtt is megindítható.']),
    ('h2', '7. Adatbiztonság', 'biztonsag'),
    ('p', 'A webáruház titkosított (HTTPS) kapcsolaton működik. A személyes adatokhoz csak azok a munkatársaink és adatfeldolgozóink férnek hozzá, akiknek a feladatuk ellátásához szükséges. '
          'A bankkártyaadatokat nem látjuk és nem tároljuk. Adatvédelmi incidens esetén a GDPR szerint járunk el.'),
    ('h2', '8. Kiskorúak', 'kiskoruak'),
    ('p', 'A webáruház alkoholtartalmú termékeket kínál, ezért 18 éven aluliak nem vásárolhatnak és nem regisztrálhatnak. Kiskorú személyes adatait tudatosan nem kezeljük; '
          'ha ilyen adat tudomásunkra jut, töröljük.'),
    ('h2', '9. A tájékoztató módosítása', 'modositas'),
    ('p', 'A tájékoztatót a jogszabályok vagy az adatkezelések változásakor frissítjük; a lényeges változásokról a weboldalon tájékoztatunk.'),
]


def render(blocks, links):
    """HTML a demó arculatával (a build.py stílusaival)."""
    out = []
    for b in blocks:
        k = b[0]
        if k == 'h2':
            out.append(f'<h2 id="{b[2]}" class="serif lg-h2">{b[1]}</h2>')
        elif k == 'h3':
            out.append(f'<h3 class="lg-h3">{b[1]}</h3>')
        elif k == 'p':
            out.append(f'<p class="lg-p">{b[1]}</p>')
        elif k == 'ul':
            out.append('<ul class="lg-ul">' + ''.join(f'<li>{x}</li>' for x in b[1]) + '</ul>')
        elif k == 'dl':
            out.append('<dl class="kv lg-kv">' + ''.join(f'<div><dt>{a}</dt><dd>{v}</dd></div>' for a, v in b[1]) + '</dl>')
        elif k == 'table':
            out.append('<div class="lg-tw"><table class="lg-t"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in b[1]) + '</tr></thead><tbody>'
                       + ''.join('<tr>' + ''.join(f'<td data-l="{b[1][i]}">{c}</td>' for i, c in enumerate(row)) + '</tr>' for row in b[2]) + '</tbody></table></div>')
    return ''.join(out).replace('{withdraw}', links['withdraw']).replace('{privacy}', links['privacy'])


def toc(blocks):
    return '<nav class="chips lg-toc">' + ''.join(f'<a class="chip" href="#{b[2]}">{b[1].split(". ", 1)[-1]}</a>' for b in blocks if b[0] == 'h2') + '</nav>'
