### Minneshantering
* Just nu läses bilder.js in varje gång sidan öppnas, dvs även när man bara ska titta på en bild.
* För att hindra att JSON-filen läses in varj gång, kan man villkorligt läsa in den mha fetch.

### Scrollhantering

Jag skulle vilja att bara en flik används för många bilder och en bild. Fick dock problem med att man tappar scrollpositionen efter att ha återvänt från BigPicture. Min workaround blev att visa BigPicture i eget fönster. Positiv sidoeffekt är att man kan ha flera bilder öppna i var sitt fönster.

Det som komplicerar är att infinite scroll används för framsökta bilder.

### Info-knappen

Den har ersatts av att man klickar eller använder hjulet.

Av samma anledning används filen bilder.js istället för [bilder.json](https://stackoverflow.com/questions/60779816/how-to-access-local-json-file-via-svelte)

Min lösning:
```
<script src='./Home/bilder.js'></script>

Home={"2022":{"2022-09-17_Kristallens_JGP":{"Klass_AB_T10368":{"1.FM_Edvin_Trost_Klass_A_2022-09-17-X.jpg":[475,267,224639,1600,1200],...

pixlar,pixlar,bytes, pixlar,pixlar
[475,  267,   224639,1600,  1200]
[sw,   sh,    bs,    bw,    bh]    s/b = small/big s/w/h = size/width/height
sw och sh används för att bygga swimlanes
bs är rena information
bw och bh anväds för att placera ut stora bilder initialt maximerade.
 
Dessa skulle alternativt kunna tas fram genom att läsa från filsystemet, men det skulle ta längre tid.
Ponera att 47.000 thumbnails sökts fram och man vill placera dem i rätt swimlane, beroende på bildernas höjder.
```

### Fliknamn

Dessa visar filens namn. Tyvärr innehåller filnamnen redundans och denna står först och därmed blir fliknamnen ganska ointressanta.
```
Vy-Damallsvenskan_Julia_Östensson_2022-09-24-X.jpg [filnamnet]
Vy-Damallsvenskan_Ju [är]
Julia_Östensson_2022 [bör]
```

### Annorlunda hantering av swimlanes

Dessa borde flyttas söderut, beroende på tidigare divars height.
Utan behov av omräkning av koordinaterna, eftersom de räknas från parents origo.

```
<div class="container" style = "left:0px; border: solid green 1px">
	<div class="item" style="top:20px" >Pelle</div>
	<div class="item" style="top:40px" >Quintus</div>
</div>

<div class="container" style = "left:60px; border: solid red 1px">
	<div class="item" style="top:20px" >Rudolf</div>
	<div class="item" style="top:40px" >Sigurd</div>
</div>

<style>
	.container {
		position:absolute;
	}
	.item {
 		border: solid black 2px;
		position:absolute;
	}
</style>
```

### Använda html element (substantiv)
För att underlätta anpassning till mobiler och paddor, begränsas antalet olika element:
* div (generell nod)
* img (bilder)
* span (texter på samma rad)
* button
* input (text)
* input (checkbox)

## Händelser (verb)
* click
* mousedown
* mousemove
* mouseup
* scroll
* wheel
* resize

## Egenskaper (adjektiv)
* width,height,left,top
* position
* margin
* padding
* font-size
* max-height
* text-align
* padding-top
* white-space:nowrap
* overflow:hidden
* background-color
* display
* flex

### Tvingades placera knapparna för search och download med position:absolute.

Browsern har ett gap mellan knapparna som ej kan förklaras.
Känns som att en vit rand utanför knappen ingår.
Knappar med 25%+50%+25% fick ej plats på 100%.

### Deploy till Google Storage

* Skapa projektet benämnt t ex Bildbanken2
* Installera gsutil.
* Kopiera över hela projektet med kommandot:
```
gsutil -m rsync -r C:\github\2022-011-Bildbanken-svelte\public gs://bildbanken2
```
* -m innebär att flera processer arbetar.
* -r innebär rekursiv traversering av katalogerna.

Prestanda: 2.4GB tog fem minuter. Nästa synk tog 13 sekunder.

Skapa rättigheter för alla användare:
* Edit Access
* +Add Principal
* Skriv in "allUsers"
* Skriv in "Storage Object Viewer"
* Save
* Allow Public Access

* Därefter kan man efter någon minut se access ändrad till "Public to Internet".
* Då kan man välja filen index.html och klicka på "Copy URL"
* Denna ska då vara "https://storage.googleapis.com/bildbanken2/index.html"

Kostnad: 100GB kostar $24 per år.
