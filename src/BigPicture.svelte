<script>
	import _ from "lodash"
	export let big

	let exif
	let state = 0

	const round = (x,n) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)

	function getExif() {
		const img = document.getElementById("picture")
		big.bigWidth  = img.naturalWidth
		big.bigHeight = img.naturalHeight
		console.log('getExif',big)
		big = big
		state = 1
		EXIF.getData(img, function() {
			exif = EXIF.getAllTags(this)
			if (exif.ExifVersion) {
				state = 2
				exif.DateTimeOriginal = exif.DateTimeOriginal.replace(":","-").replace(":","-")
	//		} else {
//				exif = null
			}
			console.log(exif)
		})
	}

	document.body.style = "height:100%; overflow:hidden; font-family:-apple-system, BlinkMacSystemFont, Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;"

	window.onscroll = (e)=> {
		e.preventDefault()
		e.stopPropagation()
		return false 
	}

	function wheel(e) {
		e.preventDefault()
		e.stopPropagation()

		const x = e.x // musens position
		const y = e.y

		function f(skala,left,x) {return (1-skala) * (x-left)}
	
		let faktor = 1.1
		if (e.deltaY > 0) faktor = 1/1.1

		big.left += f(faktor,big.left,x)
		big.top  += f(faktor,big.top,y)

		big.skala *= faktor

		big.width  = big.skala * big.bigWidth
		big.height = big.skala * big.bigHeight

		big = big
		return false 
	}

	function mousedown(e) {
		e.preventDefault()
		e.stopPropagation()

		if (e.x<10 && e.y<10) return

		big.state = 1
		big.startX = e.x
		big.startY = e.y
		big = big
	}

	function mousemove(e) {
		if (big.state == 0) return 
		big.left += e.x - big.startX
		big.top += e.y - big.startY
		big.startX = e.x
		big.startY = e.y
		big = big
	}

	function mouseup(e) {
		big.state = 0
		big = big
	}

	function close() {
		big.file = ""
		big = big
		document.body.style ="margin:0; padding:0; margin:1; padding:0; font-family:-apple-system, BlinkMacSystemFont, Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;"
		// todo Återställ även scrollposition!
	}

</script>

<div>

	{#if state >= 1}
		<span style="top:3%"> {round(big.bigWidth * big.bigHeight/1000000,1)} MP • {big.bigWidth} x {big.bigHeight} • {round(big.bigSize/1000000,1)} MB </span>
	{/if}
		<span style="top:5%">{big.file.replaceAll('\\',' • ').replaceAll("_"," ")}</span>
	{#if state == 2}
		<span style="top:1%;"> {exif.DateTimeOriginal.replace(" "," • ")} </span>
		<span style="top:7%;"> {exif.Model} • f/{exif.FNumber} • 1/{1/exif.ExposureTime} • {exif.FocalLength} mm • ISO {exif.ISOSpeedRatings} </span>
		<span style="top:9%;"> © {exif.Copyright} </span>
	{/if}

	<button style = "left:0%;  top:1%;" on:click={()=>getExif()}>info</button>
	<button style = "left:0%;  top:8%;">&lt;</button>
	<button style = "left:50%; top:1%;">play</button>
	<button style = "left:95%; top:8%;">&gt;</button>
	
	<img id='picture' src={big.file} alt=""
		on:wheel={wheel}
		on:mousedown={mousedown}
		on:mousemove={mousemove}
		on:mouseup={mouseup}
		width = {big.width}
		style = "position:absolute; left:{big.left}px; top:{big.top}px;"
	>
	<button style = "left:95%; top:1%;" on:click={close}>exit</button>

</div>

<style>
	button {
		border: 1px solid grey;
		color : grey;
		background-color: transparent; 
		position:absolute; 
		font-size:1em;
		width:4%;
	}

	div {
		/* color : white; */
	}

	span {
		position:absolute;
		left:5%;
	}

</style>

