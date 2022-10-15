# Ny hantering av Bildbanken

### Intro

För att snabba upp sökningar, skapas en fil, *bilder.js*, som innehåller katalognamn och filnamn.
Denna fil, som egentligen är en [JSON](https://en.wikipedia.org/wiki/JSON)-fil, hämtas ner till klienten.

Att krympa bilder är en långsam process, därför cachas lokala bilder.js i varje katalog *small*. 
Denna katalog innehåller även *thumbnails*, [wikipedia](https://en.wikipedia.org/wiki/Thumbnail).

Pythonprogrammet underhåller denna fil.

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
Filer har *extension* .jpg och .js, övriga är kataloger.

* Filen *bilder.js* avspeglar katalogstrukturen.
* Den är uppbyggd mha *{}*, även kallad [object](https://www.w3schools.com/js/js_objects.asp) i Javascript och [dict](https://python.fandom.com/wiki/Dictionaries) i Python.
	* En bild nås via database["2022"]["2022-09-17_Kristallens_JGP"]["Klass_D_T10370"]["7.Numa_Karlsson_klass_D_2022-09-17.jpg"] == [432,300]
	* Texterna i klamrarna, även kallade *nycklar* eller *keys* utgör underlaget för all sökning.
* bilder.js innehåller även *width* och *height* för varje thumbnail. Höjden används för utplacering i rätt [swimlane](https://en.wikipedia.org/wiki/Swimlane), bredderna är samma för alla thumbnails.

### Ungefärliga filstorlekar
* Högupplöst bild: 2 Mbyte (t ex 2048x1365)
* Thumbnail: 25 kbyte (t ex 432x300) (1% av högupplöst bild)
* Databas per bild: 75 byte (filnamn + överordnade katalognamn) (35 ppm av högupplöst bild)
* Databas för 50k bilder: 4 Mbyte
