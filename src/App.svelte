<script>

  let cards = [] // Varje bild tillsammans med tre rader text utgör ett Card.
	let y = 0 // Anger var scrollern befinner sig just nu.
	let ymax = 0 // Anger var senast laddade bild befinner sig.

	$: { // infinite scroll
		// Om y + skärmens dubbla höjd överstiger senaste bilds underkant läses 20 nya bilder in.
		if (y + 2 * screen.height > ymax) {
			const n = cards.length
			cards = cards.concat(result[2].slice(n, n + 20))
			const latest = _.last(cards)
			if (n > 0) ymax = latest[4] + latest[6] // y + h
		}
	}

	let selected = []

	import _ from "lodash"
	import JSZip from "jszip"
	import axios from "axios"
	import { saveAs } from "file-saver"

	const INITIAL = 0
	const SMALL = 2
	const BIG = 3
	const BIGGER = 4

	let state = INITIAL
	let count = 0
	
	const SCROLLBAR = 12
	const WIDTH = 432
	const GAP = 2
	const ALFABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	$: COLS = Math.floor((innerWidth-SCROLLBAR-GAP)/WIDTH)

	const path  = [Home] // used for navigation
	const stack = ["Home"]
	
	let trippel = {res:[], stat:{}, total:0}
	const range = _.range
	let bigfile = ""
	let sokruta=""
	$: result = search(Home,sokruta)
	
	$: { 
		placera(result)
		result = result
	}

	function assert(a,b) {
		if (!_.isEqual(a,b)) console.log("Assert failed",a,'!=',b)
	}

	function resize() {
		result = result
		placera(result)
	}

	window.onresize = resize

	function spaceShip (a,b) {
		if (a < b) return -1
		else if (a == b) return 0
		return 1 
	}
	assert(spaceShip(1,2),-1)
	assert(spaceShip(1,1),0)
	assert(spaceShip(1,0),1)
	assert(_.range(3),[0,1,2])

	function comp (a,b) { if (a[0] == b[0]) {return spaceShip(a[1], b[1])} else {return spaceShip(a[0], b[0])}}
	function comp2(a,b) { if (a.length == b.length) {return spaceShip(a,b)} else {return -spaceShip(a.length,b.length)}}
	assert(comp2("A","B"),-1)
	assert(comp2("AB","AB"),0)
	assert(comp2("B","A"),1)
	assert(comp2("BC","A"),-1)

	function search(Home,words,path="Home") {
		cards = []
		count = 0
		words = words.split(" ")
		trippel = {res:[], stat:{}, total:0}

		recursiveSearch(Home,words,path)

		trippel.res.sort(comp)

		const keys = Object.keys(trippel.stat)
		keys.sort(comp2) 
		const st = []
		let antal = 0
		for (const key of keys) {
			st.push(`${key}:${trippel.stat[key]}`) 
			antal += trippel.stat[key]
		}
		return [st.join(' '),`${antal} av ${trippel.total} bilder`,trippel.res]
	}

	// rekursiv pga varierande djup i trädet
	function recursiveSearch (node,words,path="Home") { // node är nuvarande katalog. words är de sökta orden
		for (const key in node) {
			const newPath = path + "\\" + key
			if (key.includes('.jpg')) {
				trippel.total += 1
				let s = ''
				for (const i in range(words.length)) {
					const word = words[i]
					if (word.length == 0) continue
					count += 1
					if (newPath.includes(word)) s += ALFABET[i]
				}
				if (s.length > 0) {
					const [width,height] = node[key]
					trippel.res.push([-s.length, s, newPath, width, height, 0, 0, 0, false])
					trippel.stat[s] = (trippel.stat[s] || 0) + 1
				}
			} else {
				recursiveSearch(node[key], words, newPath)
			}
		}
	}

	// Räknar ut vilken swimlane som är lämpligast.
	// Uppdaterar x och y för varje bild
	// Uppdaterar listan cols som håller reda på nästa lediga koordinat för varje kolumn
	function placera(result) {
		COLS = Math.floor((window.innerWidth-SCROLLBAR-GAP)/WIDTH)
		const cols = []
		for (const i in range(COLS)) cols.push(100)
		const textHeights = 75-15
		const res = result[2]
		for (const i in res) {
			const bild = res[i]
			let index = 0 // sök fram index för minsta kolumnen
			for (const j in range(COLS)) {
				if (cols[j] < cols[index]) index = j
			}
			bild[5] = GAP + WIDTH*index // x
			bild[6] = cols[index]       // y
			bild[7] = i
			bild[8] = true // kryssruta
			cols[index] += Math.round(WIDTH*bild[4]/bild[3]) + textHeights // h/w
		}
	}

	function getPath(arr,dir="small") {
		if (dir.length > 0) arr.splice(arr.length-1, 0, dir);
		return arr.join("\\")
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
	function visa(event) {bigfile = event.target.src.replace('small','')}
	function göm(event) {bigfile = ""}

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
 
	function push(key) {
		path.push(_.last(path)[key])
		stack.push(key)
		path = path
		stack = stack
	}

	function pop(key) {
		while (_.last(stack) != key) {
			path.pop()
			stack.pop()
		}
		path = path
		stack = stack
	}

	function make(value) {
		console.log('make',selected.length)
		for (const i in range(selected.length)) {
			selected[i] = value
		}
		console.log('make',selected.length)
		selected = selected
	}

	function all() {make(true)}
	function none() {make(false)}

	function download(item) {
		return axios.get(item.url, { responseType: "blob" }).then((resp) => {zip.file(item.name, resp.data)})
	}

	let zip = new JSZip()

	function downloadAll() { // download all files as ZIP archive
		zip = new JSZip()
		const fileArr = []
		for (const i in range(selected.length)) {
			if (selected[i]==true) {
				const path = result[2][i][2]
				const p = path.lastIndexOf("\\")
				fileArr.push({name:path.slice(p+1), url:path})
			}
		}
		if (fileArr.length == 0) return

		const arrOfFiles = fileArr.map((item) => download(item)) //create array of promises
		Promise.all(arrOfFiles)
			.then(() => {zip.generateAsync({ type: "blob" }).then(function (blob) { saveAs(blob, "Bildbanken.zip") })})
			.catch((err) => {console.log(err)})
}

</script>

<svelte:window bind:scrollY={y} />

<div>
	<input bind:value={sokruta} placeholder="Sök" style='width:50%'>
	{result[0]}
	{result[1]}
</div>

{#if sokruta == ""}

	<div style="height:50px">
		{#each stack as key }
			{#if key == _.last(stack)}
				{key}
			{:else}
				<button on:click = {() => pop(key)}>{key}</button>
			{/if}
			&nbsp;
		{/each}
	</div>

	{#if _.last(stack).includes('.jpg')}
		<img src={getPath(stack,"")} alt='big' />
	{:else}
		{#each _.keys(_.last(path)) as key }
			<div>
				{#if _.isNumber(key)}
					<button on:click = {() => push(key)}>{_.last(path)[key]}</button>
				{:else}
					<button on:click = {() => push(key)}>{key}</button>
				{/if}
			</div>
		{/each}
	{/if}

{:else}

	<div>
		<button on:click = {all}>All</button>
		<button on:click = {none}>None</button>
		<button on:click = {downloadAll}>Download</button>
	</div>

	<div>
		{#each cards as card,i}
			<div class="card" style="position:absolute; left:{card[5]}px; top:{card[6]}px">
				<img src={getPath(card[2].split("\\"),"small")} width={WIDTH-GAP} alt="small" on:click={visa} on:keydown={visa}/>
				<div class="info">{card[7] + ' ' + prettyFilename(card[2])}
					<a target="_blank" href="https://member.schack.se/ViewPlayerRatingDiagram?memberid={getNumber(card[2],'M')}">{getNumber(card[2],'M')}</a>
				</div>
				<div class="info">{prettyPath(card[2])}
					<a target="_blank" href="https://member.schack.se/ShowTournamentServlet?id={getNumber(card[2],'T')}">{getNumber(card[2],'T')}</a>
				</div>
				<div class="info">
					<input type="checkbox" value="" bind:checked={selected[i]}/>
					
					{card[1]} © Lars OA Hedlund
				</div>
			</div>
		{/each}
	</div>

	<!-- <button>Share</button>
	<button>Prev</button>
	<button>Next</button>
	<button>Play</button>
	 -->

	<!-- {#each result[2].slice(0,500) as [ignore,letters,path,w,h,x,y]}
		<div class="card" style="position:absolute; left:{x}px; top:{y}px">
			<img src={getPath(path,"small")} width={WIDTH-GAP} alt="small" on:click={visa} on:keydown={visa}/>
			<div class="info">{prettyFilename(path)}</div>
			<div class="info">{prettyPath(path)}</div>
			<div class="info">{letters} © Lars OA Hedlund</div>
		</div>
	{/each} -->
{/if}

<!-- {:else if state == BIG}
	<img src={bigfile} alt="X" on:click={göm} on:keydown={göm}/>
{:else if state == BIGGER}
	<div></div> -->

<style>
	div {
		font-size: 0.9em;
	}
	.card {
		font-size: 0.9em;
    width: 432px; 
    max-height: 800px;
    /* overflow-x: scroll; */
	}
</style>
