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