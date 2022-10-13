<script>
	import _ from "lodash"

	const SCROLLBAR = 12
	const COLS = 4
	const GAP = 5
	const WIDTH = Math.floor((innerWidth-SCROLLBAR-GAP)/COLS)

	let bigfile = ""
	
	function assert(a,b) {
		if (!_.isEqual(a,b)) console.log("Assert failed",a,'!=',b)
	}
	const range = _.range

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

	function search (s) {
		const data = dirs
		const alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		const res = []
		const words = s.split(' ')
		const stat = {}
		let total = 0
		for (const tournament in data) {
			total += data[tournament].length
			for (const [filename,width,height] of data[tournament]) {
				let s = ''
				for (const i in range(words.length)) {
					const word = words[i]
					if (word == "") continue
					if (tournament.includes(word) || filename.includes(word)) s += alfabet[i]
				}
				if (s.length > 0) {
					res.push([-s.length,s,tournament,filename,width,height])
					stat[s] = (stat[s] || 0) + 1
				}
			}
		}

		res.sort(comp)

		const keys = Object.keys(stat)
		keys.sort(comp2) 
		const st = []
		let antal = 0
		for (const key of keys) {
			st.push(`${key}:${stat[key]}`) 
			antal += stat[key]
		}
		return [st.join(' '),`${antal} av ${total} bilder`,res]

	}

	// Räknar ut vilken swimlane som är lämpligast.
	// Uppdaterar x och y för varje bild
	// Uppdaterar listan cols som håller reda på nästa lediga koordinat för varje kolumn
	function placera(result) {
		const cols = _.map(range(COLS), function () {return 100} )
		const textHeights = 75
		const res = result[2] 
		for (const bild of res) {
			let index = 0 // sök fram index för minsta kolumnen
			for (const j in range(COLS)) {
				if (cols[j] < cols[index]) index = j
			}
			bild[6] = GAP + WIDTH*index // x
			bild[7] = cols[index]             // y
			cols[index] += Math.round(WIDTH*bild[5]/bild[4]) + textHeights // h
		}
	}

	const dirs = data
	let sokruta="JGP"
	const result = search(sokruta)
	placera(result)

	function tournament(s) {
		return '2022\\' + s.slice(11).replaceAll('_',' ')
	}
	function filename(s) {
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
	function pretty(s) {
		return s.replaceAll('_', ' ').replace('\\',' ')
	}

	function visa(event) {
		bigfile = event.target.src.replace('small','big')
		console.log(bigfile)
	}

	function göm(event) {
		bigfile = ""
	}

</script>

{#if bigfile != ""}
	<img src={bigfile} alt="" on:click={göm} />
{:else}

	<input bind:value={sokruta} placeholder="Sök" style='width:100%'>
	<div>{result[0]}</div>
	<div>{result[1]}</div>

	{#each result[2] as item}
		<div class="item" style="position:absolute; left:{item[6]}px; top:{item[7]}px">
			<!-- {memory = {tournament(item[2]) + "_files/big/" + item[3]}} -->
			<!-- <img src={tournament(item[2]) + "_files/small/" + item[3]} alt="" width={WIDTH-GAP} on:click={function () {console.log('visa')}} /> -->

			<img src={tournament(item[2]) + "_files/small/" + item[3]} alt="" width={WIDTH-GAP} on:click={visa} />
			<div class="info">{filename(item[3])}</div>
			<div class="info">{pretty(item[2])}</div>
			<div class="info">{item[1]} © Lars OA Hedlund</div>
		</div>
	{/each}

{/if}
