<script>

	import _ from "lodash"
	import { tick } from 'svelte'
	import Card from "./Card.svelte"
	import Download from "./Download.svelte"
	import Help from "./Help.svelte"
	import NavigationVertical from "./NavigationVertical.svelte"
	import NavigationHorisontal from "./NavigationHorisontal.svelte"
	import Search from "./Search.svelte"
	import BigPicture from "./BigPicture.svelte"
	import Infinite from "./Infinite.svelte"
	import fileIndex from './json/file_index.json'

	let Home
	async function getJSON() {
		let response = await fetch("./json/bilder.json")
		return await response.json()
	}
	const promise = getJSON()

	const range = _.range

	const MAX_DOWNLOAD = 100 // Lars OH vill ha 500.

  let cards = [] // Varje bild tillsammans med tre rader text utgör ett Card.
	let y = 0 // Anger var scrollern befinner sig just nu.
	let ymax = 0 // Anger var senast laddade bild befinner sig.
	let offset = 0

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

	const fileWrapper = [fileIndex]
	
	let count = 0
	
	const ALFABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	const SCROLLBAR = 0 // 12+3+1
	const GAP = 1
	$: WIDTH = calcWidth(innerWidth)
	$: COLS = Math.floor((innerWidth-SCROLLBAR-GAP)/WIDTH)

	let path=[] // = [Home] // used for navigation
	let stack=[] //= ["Home"]
	
	let res=[]
	let stat={}
	let total=0
	let buttons = false

	let sokruta = ""
	let big = {file:""}
	
	let text0 = ""
	let text1 = ""
	let images = []
	let visibleKeys = {}

	// innehåller de kataloger söksträngen finns i. T ex {"2022":7,"2021":3} Innehåller antal bilder
	$: visibleKeys = getVisibleKeys(res, path.length)

	const is_jpg = (file) => file.endsWith('.jpg') || file.endsWith('.JPG')
	const round = (x,n) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)
	const spreadWidth = (share,WIDTH) => Math.floor((WIDTH-2*GAP*(1/share+1))*share) - 2

	function calcWidth(innerWidth) {
		let n = Math.floor(innerWidth/475)
		return Math.floor((innerWidth-(n+1)*GAP-SCROLLBAR-0)/n)
	}

	function consumeFolder(folder) {
		sokruta = ""
		stack = folder.split("\\")
		path.length = 0 // clear
		path.push(Home)
		let pointer = Home
		for (const key of stack.slice(1)) {
			pointer = pointer[key]
			path.push(pointer)
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

	$: [text0,text1,images] = search(_.last(path), sokruta, stack.join('\\'), Home)

	$: { 
		placera(images,visibleKeys)
		images = images
	}

	function resize() {
		WIDTH = calcWidth(innerWidth)
		placera(images,visibleKeys)
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

	// Obs: använd index++ istf 0 pga -0 == +0
	// 1 index => [-1],[1] = 2 varianter
	// 2 index => [-1,-2],[1,-2],[-1,2],[1,2], [-2,-1],[-2,1],[2,-1],[2,1] = 2!*2^2 = 8 varianter
	// 3 index => n! * 2^n = 48 varianter
	// 4 index => 24 * 16 = 384 varianter
	function multiSort (a,b,indexes) {
		for (const i in _.range(indexes.length)) {
			const index = Math.abs(indexes[i])-1 // 0..
			let res = spaceShip(a[index],b[index])
			if (res != 0) return indexes[i] < 0 ? -res : res
		}
	}
	assert([[2018, 'Noah'], [2013, 'Numa'], [1982, 'Karolina'], [1982, 'Kasper'], [1982, 'Miranda'], [1954, 'Christer'], [1954, 'Maria']],[[1954,'Christer'],[1982,'Kasper'],[1982,'Karolina'],[1982,'Miranda'],[2013,'Numa'],[2018,'Noah'],[1954,'Maria']].sort((a,b) =>  multiSort(a,b,[-1,2])) )

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

	function getPath(path,dir="small") {
		if (dir.length > 0) path = path.replace("Home",dir)
		return path
	}

	function visaBig(bs, bw, bh, src) {
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

	function pop() {
		path.pop()
		stack.pop()
		path = path
		stack = stack
	}

	// Gå igenom listan, plocka ut de knappar som ska synas.
	function getVisibleKeys(bilder,level) {
		const res = {}
		for (const bild of bilder) {
			const arr = bild[2].split("\\")
			if (level >= arr.length) break
			const key = arr[level]
			res[key] ||= 0
			res[key] += 1
		}
		return res
	}

	function search(node,words,path) {
		ymax = 0 // Viktigt! Annars syns inte nya bilder.
		cards = []
		count = 0

		words = words.toLowerCase()
		// path = path.toLowerCase()
		words = words.length == 0 ? [] : words.split(" ")

		res = []
		stat = {}
		total = 0
		selected = []

		const start = new Date()

		const levels = 99
		recursiveSearch(node, words, path, levels)
		res.sort((a,b) => multiSort(a,b,[1,2,-3,13])) // OBS: index++  [-letters.length, letters, -path, key] [-3, 'ABC', 'Home/2022/2022-09-17...', 'Pelle...jpg']

		const keys = Object.keys(stat)
		keys.sort(comp2) 
		const st = []
		let antal = 0
		for (const key of keys) {
			st.push(`${key}:${stat[key]}`) 
			antal += stat[key]
		}
		return [st.join(' '),`found ${antal} of ${total} images in ${new Date() - start} ms`,res]
	}

	// rekursiv pga varierande djup i trädet
	function recursiveSearch (node,words,path,levels) { // node är nuvarande katalog. words är de sökta orden
		tick()
		if (levels==0) return
		for (const key in node) {
			const newPath = path + "\\" + key
			if (is_jpg(key)) {
				total += 1
				let s = ''
				const newpath = newPath.toLowerCase()
				for (const i in range(words.length)) {
					const word = words[i]
					if (word.length == 0) continue
					count += 1
					if (newpath.slice(10).includes(word)) s += ALFABET[i]
				}
				if (s.length > 0 || words.length == 0) {
					const [sw,sh,bs,bw,bh] = node[key] // small/big width/height/size
					res.push([-s.length, s, path, sw, sh, 0, 0, 0, false, bs, bw, bh, key])
					stat[s] = (stat[s] || 0) + 1
				}
			} else {
				recursiveSearch(node[key], words, newPath, levels - 1)
			}
		}
	}

	// Räknar ut vilken swimlane som är lämpligast.
	// Uppdaterar x och y för varje bild
	// Uppdaterar listan cols som håller reda på nästa lediga koordinat för varje kolumn
	function placera(images,visibleKeys) {
		const rows = sokruta=="" ? 4 : 5
		let antal = rows + 1 + _.size(visibleKeys)
		if (stack.length==2) antal+=1
		if (stack.length!=2 && buttons) antal+=1

		offset = 34 * antal // 30 + 2 * margin=2

		COLS = Math.floor((window.innerWidth-SCROLLBAR-GAP)/WIDTH)

		const cols = [offset]
		for (const i in range(COLS)) cols.push(0)
		const textHeights = 50-2 //43
		const res = images
		for (const i in res) {
			tick()
			const bild = res[i]
			let index = 0 // sök fram index för minsta kolumnen
			for (const j in range(COLS)) {
				if (cols[j] < cols[index]) index = j
			}
			bild[5] = (GAP + WIDTH)*index // x
			bild[6] = cols[index]       // y
			bild[7] = i
			bild[8] = true // kryssruta
			cols[index] += Math.round(WIDTH*bild[4]/bild[3]) + textHeights // h/w
		}
		images = images
	}

	function countDirs(path) {
		let res = 0
		for (const name in path) {
			console.log('countDirs',name)
			if (! is_jpg(name)) {
				res += 1
			}
		}
		return res
	}

	function prettyFilename(path) { // Tag bort eventuella M och V-nummer
		let i = path.lastIndexOf('\\')
		let s = path.slice(i+1)
		// if (true) { // !retro
			// if (s.startsWith('Vy-')) s = s.slice(1+s.indexOf('_'))
			// const p = s.search(/\d\d\d\d-\d\d-\d\d/)
			// if (p>=0) s = s.slice(0,p)
			// s = s.replace('Pristagare ','')
			// s = s.replace(/[kK]lass [A-Z]+/,'')
		// }
		s = s.replace('.jpg','')
		s = s.replace('.JPG','')
		s = s.replace(/_M\d+/,'')
		s = s.replace(/_V\d+/,'')
		s = s.replace(/_F\d+/,'')
		s = s.replaceAll('_',' ')
		return s
	}

	function setHome(data) {
		Home = data
		path = [Home]
		stack = ["Home"]
		// console.log('path',path)
		// console.log('stack',stack)
		return ""
	}

</script>

<svelte:window bind:scrollY={y}/>

{#await promise }
	<p>Loading...</p>
{:then data}
	{setHome(data)}
	{#if big.file == ""}
		<Search bind:sokruta {text0} {text1} {stack} {WIDTH} {GAP} {spreadWidth} {path} {_} {is_jpg} />
		<Download bind:selected {images} {WIDTH} {spreadWidth} {MAX_DOWNLOAD} {stack} {pop}/>
		<NavigationHorisontal {stack} {WIDTH} />
		<NavigationVertical bind:buttons {visibleKeys} {push} {is_jpg} {WIDTH} {spaceShip} {stack} />
		<Infinite {WIDTH} {getPath} bind:selected {cards} {round} {fileWrapper} {prettyFilename} />
	{:else}
		<BigPicture {big} {prettyFilename} />
	{/if}
{/await}
