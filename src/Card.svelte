<script>
	import _ from "lodash"
	export let WIDTH
	export let GAP
	export let getPath
	export let card
	export let selected
	export let index
	export let big

	function getNumber(path,letter) { // Används både för T och M-nummer
		path = path.replace('.jpg','')
		const arr = path.split('\\')
		const pos = " MT".indexOf(letter)
		const cand = arr[arr.length-pos]
		const arr2 = cand.split('_')
		const tnummer = _.last(arr2)
		if (tnummer[0]==letter) return tnummer.slice(1)
		return ""
	}
 
	function prettyFilename(path) { // Tag bort eventuellt M-nummer
		let i = path.lastIndexOf('\\')
		let s = path.slice(i+1)
		s = s.replace('.jpg','')
		s = s.replace(/_M\d+/,'')

		// s = s.replace(/Klass_./i,'')
		// s = s.replace(/\d\d\d\d-\d\d-\d\d-X-\d/,'')
		// s = s.replace(/\d\d\d\d-\d\d-\d\d-\d/,'')
		// s = s.replace(/\d\d\d\d-\d\d-\d\d/,'')

		s = s.replace('Vy-Veckans-bild-','')
		s = s.replace('Vy-Veckans-bild_','')
		s = s.replace('Vy-Veckans-Bild_','')
		s = s.replace('Vy-Vexkans_Bild_','')
		s = s.replace('Vy-Veckans_Bild_','')
		s = s.replace('Vy-Veckans_bild_','')
		s = s.replace('Vy-veckans_bild_','')
		s = s.replace('Vy-veckans-bild_','')
		s = s.replace('Vy-Veckans-Bild _','')
		s = s.replace('Vy-','')

		s = s.replace('schakläger','schackläger')
		s = s.replace('sgnerer','signerar')
		s = s.replace('Salongerrna','Salongerna')
		
		s = s.replaceAll(/_/ig,' ')
		// s = s.replaceAll('KSK-JGP','')
		// s = s.replaceAll('Minior-Lag-DM','') // kan tas från tournament
		return s
	}

	function prettyPath(path) { // Tag bort eventuellt T-nummer
		path = path.split('\\')
		path = path.slice(2,path.length-1)
		path = path.join(" ")
		path = path.replace(/_T\d+/,'')
		return path.replaceAll('_', ' ') 
	}

	function visaBig(card) {
		console.log('urban')
		big.state = 0
		big.smallWidth = card[3] // width
		big.smallHeight = card[4] // height

		big.bigWidth = 2000 //naturalWidth //innerWidth //1600
		big.bigHeight = 1000 //naturalHeight //innerHeight //1311
		console.log(big)
		big.bigSize = card[9]

		big.skala = 1
		big.width  = big.bigWidth  * big.skala
		big.height = big.bigHeight * big.skala

		big.left = 0
		big.top = 0

		big.file = card[2].replace("small","")

		big = big
	}

</script>

<div class="card" id="images" style="position:absolute; left:{card[5]}px; top:{card[6]}px">
	<img 
		src = {getPath(card[2].split("\\"),"small")}
		width = {WIDTH-GAP}
		alt = ""
		on:click = {() => visaBig(card)}
		on:keydown = {() => visaBig(card)}
	/>
	<div class="info">{prettyFilename(card[2])}
		<a target="_blank" href="https://member.schack.se/ViewPlayerRatingDiagram?memberid={getNumber(card[2],'M')}">{getNumber(card[2],'M')}</a>
	</div>
	<div class="info">{prettyPath(card[2])}
		<a target="_blank" href="https://member.schack.se/ShowTournamentServlet?id={getNumber(card[2],'T')}">{getNumber(card[2],'T')}</a>
	</div>
	<div class="info">
		{card[7]}
		<input type="checkbox" value="" bind:checked={selected[index]}/>
		{card[1]} © Lars OA Hedlund
	</div>
</div>

<style>
	.card {
		font-size: 0.9em;
		width: 475px; 
		max-height: 800px;
	}
	div {
		font-size: 0.9em;
	}
</style>
