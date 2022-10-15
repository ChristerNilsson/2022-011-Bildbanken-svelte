<!-- https://member.schack.se/ShowTournamentServlet?id=10370 -->

<script>
	import _ from "lodash"

	const INITIAL = 0
	const SMALL = 2
	const BIG = 3
	const BIGGER = 4


	let state = INITIAL

	const SCROLLBAR = 12
	const WIDTH = 432
	const GAP = 5
	const ALFABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	$: COLS = Math.floor((innerWidth-SCROLLBAR-GAP)/WIDTH)

	console.log(data)

	const path = [data] // used for navigation
	const stack = ["Home"]
	
	const dirs = data
	let trippel = {res:[], stat:{}, total:0}
	const range = _.range
	let bigfile = ""
	let sokruta="Numa"
	$: result = search(data,sokruta)
	
	$: placera(result)

	function assert(a,b) {
		if (!_.isEqual(a,b)) console.log("Assert failed",a,'!=',b)
	}

	function resize() {
		result = result
		placera(result)
	}

	window.onresize = resize;
	
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

	function search(data,words,path=[]) {
		words = words.split(" ")
		trippel = {res:[], stat:{}, total:0}

		recursiveSearch(data,words,path)

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

	// nu rekursiv pga varierande djup i trädet
	function recursiveSearch (data,words,path=[]) { // words är de sökta orden
		for (const key in data) {
			const newPath = path.concat([key])
			if (key.includes('.jpg')) {
				trippel.total += 1
				const [width,height] = data[key]
				const newPath2 = newPath
				let s = ''
				for (const i in range(words.length)) {
					const word = words[i]
					if (word == "") continue
					let found = false
					for (const p of newPath2) {
						if (p.includes(word)) found = true
					}
					if (found) s += ALFABET[i]
				}
				if (s.length > 0) {
					trippel.res.push([-s.length, s, newPath2, width, height])
					trippel.stat[s] = (trippel.stat[s] || 0) + 1
				}
			} else {
				recursiveSearch(data[key], words, newPath)
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
		const textHeights = 75
		const res = result[2] 
		for (const bild of res) {
			let index = 0 // sök fram index för minsta kolumnen
			for (const j in range(COLS)) {
				if (cols[j] < cols[index]) index = j
			}
			bild[5] = GAP + WIDTH*index // x
			bild[6] = cols[index]       // y
			cols[index] += Math.round(WIDTH*bild[4]/bild[3]) + textHeights // h/w
		}
	}

	function getPath(arr,dir="small") {
		const arr2 = _.clone(arr)
		arr2[1] = arr2[1].slice(11) // datum bort
		if (dir.length>0) arr2.splice(arr2.length-1, 0, dir);
		return arr2.join("\\")
	}

	function prettyFilename(arr) {
		// console.log('prettyFilename',_.last(arr))
		let s = _.last(arr)
		s = s.replace('.jpg','')
		s = s.replace(/Klass_./i,'')
		s = s.replace(/\d\d\d\d-\d\d-\d\d-X-\d/,'')
		s = s.replace(/\d\d\d\d-\d\d-\d\d-\d/,'')
		s = s.replace(/\d\d\d\d-\d\d-\d\d/,'')
		s = s.replace(/Vy-/g,'')
		s = s.replaceAll(/_/ig,' ')
		s = s.replaceAll('KSK-JGP','')
		s = s.replaceAll('Minior-Lag-DM','') // kan tas från tournament
		return s
	}
	function prettyPath(arr) {
		arr = arr.slice(1,arr.length-1) 
		const s = arr.join(" ")
		return s.replaceAll('_', ' ') // .replace('\\',' ')
	}
	function visa(event) {bigfile = event.target.src.replace('small','')}
	function göm(event) {bigfile = ""}
 
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

</script>

<div>
	<input bind:value={sokruta} placeholder="Sök" style='width:50%'>
	<button>All</button>
	<button>None</button>
	<button>Download</button>
	<button>Share</button>
	{result[0]}
	<button>Prev</button>
	<button>Next</button>
	{result[1]}
	<button>Play</button>
	<button>Result</button>
</div>

{#if state == INITIAL}

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
		<img src={getPath(stack.slice(1),"")} alt='big' />
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

{:else if state == SMALL}

	{#each result[2] as {ignore,letters,path,filename,ignore,x,y}}
		<div class="item" style="position:absolute; left:{x}px; top:{y}px">
			<img src={getPath(path,"small")} width={WIDTH-GAP} alt="small" on:click={visa} on:keydown={visa}/>
			<div class="info">{prettyFilename(path)}</div>
			<div class="info">{prettyPath(path)}</div>
			<div class="info">{letters} © Lars OA Hedlund</div>
		</div>
	{/each}

{:else if state == BIG}
	<img src={bigfile} alt="X" on:click={göm} on:keydown={göm}/>
{:else if state == BIGGER}
	<div></div>
{/if}
