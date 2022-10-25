<script>

	import _ from "lodash"
	import Card from "./Card.svelte"
	import Download from "./Download.svelte"
	import NavigationVertical from "./NavigationVertical.svelte"
	import NavigationHorisontal from "./NavigationHorisontal.svelte"
	import Search from "./Search.svelte"
	import BigPicture from "./BigPicture.svelte"
	import Infinite from "./Infinite.svelte"

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

	let path  = [Home] // used for navigation
	let stack = ["Home"]
	
	let res=[]
	let stat={}
	let total=0

	let sokruta = ""
	let big = {file:""}
	
	let text0 = ""
	let text1 = ""
	let images = []

	const is_jpg = (file) => file.includes('.jpg') || file.includes('.JPG')
	const round = (x,n) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)

	function consumeFolder(folder) {
		sokruta = ""
		stack = folder.split("\\")
		console.log('stack',stack)
		path = [Home]
		let pointer = Home
		for (const key of stack.slice(1)) {
			pointer = pointer[key]
			path.push(pointer)
			console.log('')
			console.log('key',key)
			console.log('pointer',pointer)
			console.log('path',path)
		}
		path = path
		stack = stack 
	}

	consumeParameters()

	function consumeParameters() {
		const queryString = window.location.search
		const urlParams = new URLSearchParams(queryString)
		if (urlParams.has("image")) {
			visaBig(urlParams.get("bs"), urlParams.get("bw"), urlParams.get("bh"), urlParams.get("image"))
		} else {
			if (urlParams.has("folder")) consumeFolder(urlParams.get("folder"))
			if (urlParams.has("query")) sokruta = urlParams.get("query")
		}
	}

	$: [text0,text1,images] = search(_.last(path), sokruta, stack.join('\\'))

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
		console.log('visaBig')
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
		if (is_jpg(key)) {
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

	function search(node,words,path) {
		cards = []
		count = 0
		if (words.length == 0) {
			words = []
		}else{
			words = words.split(" ")
		}

		res=[]
		stat={}
		total=0
		const start = new Date()

		recursiveSearch(node,words,path)

		res.sort(comp)

		const keys = Object.keys(stat)
		keys.sort(comp2) 
		const st = []
		let antal = 0
		for (const key of keys) {
			st.push(`${key}:${stat[key]}`) 
			antal += stat[key]
		}
		return [st.join(' '),`${antal} of ${total} images in ${new Date() - start} ms`,res]
	}

	// rekursiv pga varierande djup i trädet
	function recursiveSearch (node,words,path) { // node är nuvarande katalog. words är de sökta orden
		for (const key in node) {
			const newPath = path + "\\" + key
			if (is_jpg(key)) {
				total += 1
				let s = ''
				for (const i in range(words.length)) {
					const word = words[i]
					if (word.length == 0) continue
					count += 1
					if (newPath.includes(word)) s += ALFABET[i]
				}
				if (s.length > 0 || words.length == 0) {
					const [sw,sh,bs,bw,bh] = node[key] // small/big width/height/size
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

		for (const i in range(COLS)) cols.push(345)
		const textHeights = 50-6
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

{#if big.file == ""}
	<Search bind:sokruta bind:text0 bind:stack {_} />
	<Download bind:selected {images} bind:text1 />
	<NavigationHorisontal {stack} {pop} />
	<NavigationVertical {path} {push} {is_jpg}/>
	<Infinite {WIDTH} {GAP} {getPath} {selected} {cards} {round} />
{:else}
	<BigPicture {big} />
{/if}

