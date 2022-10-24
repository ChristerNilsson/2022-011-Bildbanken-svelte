# Ny hantering av Bildbanken

### Intro

För att snabba upp sökningar, skapas en fil, *bilder.js*, som innehåller katalognamn och filnamn.
Denna fil, som egentligen är en [JSON](https://en.wikipedia.org/wiki/JSON)-fil, hämtas ner till klienten.

Att krympa bilder är en långsam process, därför cachas lokala bilder.js i varje katalog *small*. 
Denna katalog innehåller även *thumbnails*, [wikipedia](https://en.wikipedia.org/wiki/Thumbnail).

Pythonprogrammet bilder.py underhåller denna fil.

### Format

* Alla blanktecken byts mot _ (underscore)
* Första speldatum anges först i turneringens namn (yyyy-mm-dd).
* Turneringens nummer enligt member.schack.se, T10368, anges sist i katalognamnet för bilderna.
	* Klass_AB_[T10368](https://member.schack.se/ShowTournamentServlet?id=10368) Kristallens JGP/Klass AB
* Förslagsvis kan medlemsnummer (member.schack.se) användas i framtiden för att spara plats och tid.
	* Dessa skulle även ge snabb access till personlig information, typ rating och andra turneringar.
	* Exempel: M430365 och M585772 i spänd väntan på startsignalen.jpg
		* [M430365](https://member.schack.se/ViewPlayerRatingDiagram?memberid=430365) Edvin Trost
		* [M585772](https://member.schack.se/ViewPlayerRatingDiagram?memberid=585772) Numa Karlsson

```
database
	bilder.js
	2022
		2022-09-17_Kristallens_JGP
			Klass_AB_T10368
				1.FM_Edvin_Trost_Klass_A_2022-09-17-X.jpg
				small
					bilder.js
					1.FM_Edvin_Trost_Klass_A_2022-09-17-X.jpg
			Klass_D_T10370
				7.Numa_Karlsson_klass_D_2022-09-17.jpg
				small
					bilder.js
					7.Numa_Karlsson_klass_D_2022-09-17.jpg
	2021
	2020
```
Filer har *extension* [.jpg](https://en.wikipedia.org/wiki/JPEG) och .js, övriga är kataloger.

* Filen *bilder.js* avspeglar katalogstrukturen.
* Den är uppbyggd mha *{}*, även kallad [object](https://www.w3schools.com/js/js_objects.asp) i Javascript och [dict](https://python.fandom.com/wiki/Dictionaries) i Python.
	* En bild nås via Home["2022"]["2022-09-17_Kristallens_JGP"]["Klass_D_T10370"]["7.Numa_Karlsson_klass_D_2022-09-17.jpg"] == [432,300,256000,1600,900]
	* Texterna i klamrarna, även kallade *nycklar* eller *keys* utgör underlaget för all sökning.
* bilder.js innehåller även *width* och *height* för varje thumbnail. Höjden används för utplacering i rätt [swimlane](https://en.wikipedia.org/wiki/Swimlane), bredderna är samma för alla thumbnails. De tre sista talen i listan, står för högupplösta bildens storlek i bytes, bredd och höjd i pixlar.

### Ungefärliga filstorlekar

* Högupplöst bild: 2 Mbyte (t ex 2048x1365)
* Thumbnail: 25 kbyte (t ex 432x300) (1% av högupplöst bild)
* Söktext per bild: 75 byte (filnamn + överordnade katalognamn) (35 ppm av högupplöst bild)
* Storlek av bilder.js för 50k bilder: cirka 4 Mbyte

### Sökning

Sökning genomförs genom att fylla i sökrutan. Dessa ord, avgränsade av blanktecken, matchas mot texterna i kataloger och filnamn. De kombineras automatiskt med OCH och ELLER. Underscore, _, kan användas för att binda ihop ord, t ex Numa_Karlsson, för att slippa en mängd falska Karlsson. (Falska Numor lär det vara mindre risk för).

Sökningen kräver att man anger rätt VERSALER och gemener, t ex ger varken "KARLSSON" eller "karlsson" någon träff, däremot "Karlsson".
De ord man anger kan vara delord, även enstaka tecken, och de kan stå var som helst i orden. T ex kommer "sson" att matcha ett antal Karlsson och Nilsson.

### Knappar

#### Horisontala Navigeringsknappar
Dessa utgörs av Home, 2022 osv. Man hoppar till en katalog närmare *roten* (Home).

#### Vertikala Katalogknappar och Filknappar
Dessa utgörs av 2022, 2021 osv. Man hoppar till en katalog närmare *löven* (bilderna)

#### T-nummer
För de turneringar där man angett Turneringsnummer, kan man klicka på denna länk och se resultatsidan direkt.

#### M-nummer
För de bildfiler där man angett Medlemsnummer, kan man klicka på denna länk och se personinfo direkt. T ex rating och spelade turneringar.

#### Download
De bilder man markerat laddas ner till klientens Download-katalog.

#### All
Alla bilder markeras.

#### None
Alla bilder avmarkeras.

#### Share
Aktuell avgränsning, dvs både strukturellt och med sökord, kan hämtas på klippbordet som en [URL](https://en.wikipedia.org/wiki/URL)
Det finns tre typer: 
* query - länk innehållande söktext
* folder - länk till aktuell katalog
* image - länk till en bild med full upplösning

#### Prev (Not implemented)
I storbildsläget visas föregående bild.

#### Next (Not implemented)
I storbildsläget visas nästa bild.

#### Play/Pause (Not implemented)
Markerade bilder visas i ett evigt bildspel.

### Vad innebär ABC?

* Sökningen visar bilderna med flest träffar först
* I andra hand prioriteras ord tidigt i söksträngen högre än senare ord
* T ex visar sökningen "A B" bilder i denna ordning
	* AB = Båda orden är med
	* A  = Endast första ordet, A, är med
	* B  = Endast andra ordet, B, är med
* AB:2 A:1 B:3 innebär att endast två bilder innehåller båda orden.
* Totalt har 6 bilder hittats, varav fyra med enbart A eller B.

Sökningen "A B C" visar träffarna i denna ordning:
```
ABC = Vitt
AB  = Gult
AC  = Magenta
BC  = Cyan
A   = Rött
B   = Grönt
C   = Blått
Ingen träff = Svart
```
![RGB](RGB.PNG)

### bilder.py

Så här uppdaterar man databasen med nya bildsamlingar.

* Skapa de kataloger som behövs. Namnge korrekt. Inga mellanslag.
* public
	* Home
		* 2022
			* 2022-09-17_Kristallens_JGP
				* Klass_AB_T12345
					* 7.Numa_Karlsson_M123456.jpg

Starta Pythonprogrammet bilder.py. Följande kommer att ske:
* small-katalogerna skapas. Dessa ligger i samma katalog som de stora .jpg-filerna.
* Thumbnails skapas och läggs i small-katalogen.
* Cache av bilder.js (med bredd och höjd för varje bild) läggs i katalogen small.
* Alla bilder.js sammanställs till den totala public/Home/bilder.js
* Cacharna finns pga att det tar cirka 100 ms att skapa en thumbnail.
* Att skapa om alla cachar tar drygt en timme.
	* Detta kan framtvingas genom att sätta USE_CACHE = False i bilder.py
	* Vill man bara skapa om vissa kataloger tar man bort filen bilder.js i dessa

### Tidsuppskattningar.

Att söka genom texten för en bild, inklusive path + bildtext, tar cirka 4 mikrosekunder.
Att hämta en bild tar längre tid. Har man sökt fram flera tusen bilder, vill man inte att browsern ska börja ladda hem alla dessa omedelbart.
Tekniken för att hantera detta benämns *infinite scroll* och bygger på att fånga scroll-händelsen och läsa in några bilder till om bufferten börjar ta slut.
Två skärmhöjder med bilder är lagom framförhållning för att ligga lite före användaren. Infinite scroll uppfanns av Aza Raskin 2006.
Just nu läser man in fler och fler bilder. Egentligen bör man kasta bort bilder efterhand som man scrollar neråt, samt läsa in dem på nytt, då användaren scrollar uppåt. Detta är INTE genomfört.

### Bildvisaren

* Genom att klicka på en thumbnail kommer man till Bildvisaren. 
* Med denna kan man zooma in och ut i en bild, mha mushjulet.
* Även förflyttning fungerar.
* Knappar:
	* Share. Skapar en URL och lägger på klippbordet

### FAQ
```
Q: Varför utnyttjas inte hela skärmen för bilderna?
A: Kontrollera att browserns Zoom är inställd på 100%
```
