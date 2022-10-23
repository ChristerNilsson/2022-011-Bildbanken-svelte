### Scrollhantering

Jag skulle vilja att bara en flik används för många bilder och en bild. Fick dock problem med att man tappar scrollpositionen efter att ha återvänt från BigPicture. Min workaround blev att visa BigPicture i eget fönster. Positiv sidoeffekt är att man kan ha flera bilder öppna i var sitt fönster.

Det som komplicerar ytterligare är att infinite scroll används för framsökta bilder.

För att hindra att JSON-filen läses in även när man bara ska titta på en bild, läses den mha fetch och enbart i huvudfönstret.

### Info-knappen

Vore skönt att slippa klicka på den. Dock kräver det asynkron hantering, vilket gör programmet svårare att underhålla. Nyckelord: 
* async
* await
* then
* catch
* promise
* fetch
* resolve
* reject

Detta är ett av de komplexare områdena inom Javascript.
```
{#await promise}
{:then result}
{:catch error}
{/await}
```

Av samma anledning används filen bilder.js istället för [bilder.json](https://stackoverflow.com/questions/60779816/how-to-access-local-json-file-via-svelte)

Min lösning:
```
<script src='./Home/bilder.js'></script>

Home={"2022":{"2022-09-17_Kristallens_JGP":{"Klass_AB_T10368":{"1.FM_Edvin_Trost_Klass_A_2022-09-17-X.jpg":[475,267,224639],...

[475,267,224639] står för [smallWidth,smallHeight,bigSize] (pixlar,pixlar,bytes)
Dessa skulle alternativt kunna tas fram genom att läsa från filsystemet, men det skulle ta längre tid.
Ponera att 47.000 thumbnails sökts fram och man vill placera dem i rätt swimlane, beroende på bildernas höjder.
```

