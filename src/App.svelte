<script>

	import _ from "lodash"
	import Card from "./Card.svelte"
	import Download from "./Download.svelte"
	import NavigationVertical from "./NavigationVertical.svelte"
	import NavigationHorisontal from "./NavigationHorisontal.svelte"
	import Search from "./Search.svelte"
	import BigPicture from "./BigPicture.svelte"

	const range = _.range

  let cards = [] // Varje bild tillsammans med tre rader text utgör ett Card.
	let y = 0 // Anger var scrollern befinner sig just nu.
	let ymax = 0 // Anger var senast laddade bild befinner sig.

	$: { // infinite scroll
		// Om y + skärmens dubbla höjd överstiger senaste bilds underkant läses 20 nya bilder in.
		if (y + 2 * screen.height > ymax) {
			const n = cards.length
			cards = cards.concat(images.slice(n, n + 20))
			const latest = _.last(cards)
			if (n > 0) {
				ymax = latest[4] + latest[6] // y + h
			}
		}
	}

	let selected = []
	let skala = 1
	// let Home = {}

	// async function readJSON(file) {
	// 	fetch(file)
	// 		.then(response => response.json())
	// 		.then(json => {
	// 			Home = json
	// 			console.log('reading JSON',_.size(Home))
	// 		})
	// }
	
	let count = 0
	
	const SCROLLBAR = 12
	const WIDTH = 475
	const GAP = 2
	const ALFABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	$: COLS = Math.floor((innerWidth-SCROLLBAR-GAP)/WIDTH)

	$: path  = [Home] // used for navigation
	const stack = ["Home"]
	
	let res=[]
	let stat={}
	let total=0

	let sokruta = "Numa"
	let big = {file:""}
	
	let text0 = ""
	let text1 = ""
	let images = []

	const queryString = window.location.search
	const urlParams = new URLSearchParams(queryString)
	if (urlParams.has("image")) {
		visaBig(urlParams.get("bs"), urlParams.get("bw"), urlParams.get("bh"), urlParams.get("image"))
	} else if (urlParams.has("query")) {
		sokruta = urlParams.get("query")
		// readJSON('./Home/bilder.json')
	}

	$: [text0,text1,images] = search(Home,sokruta)

	// $: history.replaceState(null, '', `\?query=${sokruta}`)

	$: { 
		placera(images)
		images = images
	}

	function resize() {
		placera(images)
		images = images
	}

	window.onresize = resize

	function assert(a,b) {
		if (!_.isEqual(a,b)) console.log("Assert failed",a,'!=',b)
	}

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

	function f(skala,left,x,width) {return Math.round((1-skala) * (x-left))} //         
	//           skala left x   width
	assert(  0,f(1.1,  200, 200,400))
	assert(-20,f(1.1,  200, 400,400))
	assert(-40,f(1.1,  200, 600,400))
	assert(  0,f(1.1,    0,   0,400))
	assert(-20,f(1.1,    0, 200,400))
	assert(-40,f(1.1,    0, 400,400))

	function getPath(arr,dir="small") {
		if (dir.length > 0) arr.splice(arr.length-1, 0, dir);
		return arr.join("\\")
	}

	function visaBig(bs, bw, bh, src) {
		document.title = _.last(src.split("\\"))
		document.body.style = "overflow:hidden"

		big.exifState = 0
		big.mouseState = 0

		big.bs = bs
		big.bw = bw
		big.bh = bh

		big.skala = Math.min(innerHeight/bh, innerWidth/bw)
		big.width = bw * big.skala
		big.height = bh * big.skala
		big.left = (innerWidth-big.width)/2
		big.top = (innerHeight-big.height)/2

		big.file = src
		big = big
	}

	function push(key) {
		if (key.includes('.jpg')) {
			const t5 = _.last(path)[key]
			visaBig(t5[2],t5[3],t5[4],stack.concat(key).join("\\"))
		} else {
			path.push(_.last(path)[key])
			stack.push(key)
			path = path
			stack = stack
		}
	}

	function pop(key) {
		while (_.last(stack) != key) {
			path.pop()
			stack.pop()
		}
		path = path
		stack = stack
	}

	function search(Home,words,path="Home") {
		cards = []
		count = 0
		words = words.split(" ")

		res=[]
		stat={}
		total=0

		recursiveSearch(Home,words,path)

		res.sort(comp)

		const keys = Object.keys(stat)
		keys.sort(comp2) 
		const st = []
		let antal = 0
		for (const key of keys) {
			st.push(`${key}:${stat[key]}`) 
			antal += stat[key]
		}
		return [st.join(' '),`${antal} of ${total} pictures`,res]
	}

	// rekursiv pga varierande djup i trädet
	function recursiveSearch (node,words,path="Home") { // node är nuvarande katalog. words är de sökta orden
		for (const key in node) {
			const newPath = path + "\\" + key
			if (key.includes('.jpg')) {
				total += 1
				let s = ''
				for (const i in range(words.length)) {
					const word = words[i]
					if (word.length == 0) continue
					count += 1
					if (newPath.includes(word)) s += ALFABET[i]
				}
				if (s.length > 0) {
					const [sw,sh,bs,bw,bh] = node[key] // small/big width/height
					res.push([-s.length, s, newPath, sw, sh, 0, 0, 0, false, bs, bw, bh])
					stat[s] = (stat[s] || 0) + 1
				}
			} else {
				recursiveSearch(node[key], words, newPath)
			}
		}
	}

	// Räknar ut vilken swimlane som är lämpligast.
	// Uppdaterar x och y för varje bild
	// Uppdaterar listan cols som håller reda på nästa lediga koordinat för varje kolumn
	function placera(images) {
		COLS = Math.floor((window.innerWidth-SCROLLBAR-GAP)/WIDTH)
		const cols = []
		for (const i in range(COLS)) cols.push(80)
		const textHeights = 60
		const res = images
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
		images = images
	}

</script>

<svelte:window bind:scrollY={y}/>

<div>
	{#if big.file == ""}
		<Search bind:sokruta bind:text0 bind:text1 />
		{#if sokruta == ""}
			<NavigationHorisontal {stack}{pop} />
			<NavigationVertical {stack}{path}{getPath}{push} />
		{:else}
			<Download bind:selected {images} />
			{#each cards as card,index}
				<Card {WIDTH}{GAP}{getPath}{card}{selected}{index} />
			{/each}
		{/if}
	{:else}
		<BigPicture bind:big />
	{/if}
</div>

<style>
	div {
		font-size: 0.9em;
	}
</style>
