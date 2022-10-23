<script>
	import _ from "lodash"
	export let big

	let exif = null
	
	const round = (x,n) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)

	function getExif() {
		const img = document.getElementById("picture")
		big.bw = img.naturalWidth
		big.bh = img.naturalHeight
		big.exifState = 1
		big = big
		EXIF.getData(img, function() {
			exif = EXIF.getAllTags(this)
			if (exif.ExifVersion) {
				big.exifState = 2
				big = big
				exif.DateTimeOriginal = exif.DateTimeOriginal.replace(":","-").replace(":","-")
			}
		})
	}

	window.onscroll = (e)=> {
		e.preventDefault()
		e.stopPropagation()
		return false 
	}

	function wheel(e) {
		e.preventDefault()
		e.stopPropagation()
		if (exif == null) getExif()

		const x = e.x // musens position
		const y = e.y

		function f(skala,left,x) {return (1-skala) * (x-left)}
	
		let faktor = 1.1
		if (e.deltaY > 0) faktor = 1/1.1

		big.left += f(faktor,big.left,x)
		big.top  += f(faktor,big.top,y)

		big.skala *= faktor

		big.width  = big.skala * big.bw
		big.height = big.skala * big.bh

		big = big
		return false 
	}

	function mousedown(e) {
		e.preventDefault()
		e.stopPropagation()
		if (exif == null) getExif()
		big.mouseState = 1
		big.startX = e.x
		big.startY = e.y
		big = big
	}

	function mousemove(e) {
		if (big.mouseState == 0) return 
		big.left += e.x - big.startX
		big.top += e.y - big.startY
		big.startX = e.x
		big.startY = e.y
		big = big
	}

	function mouseup(e) {
		big.mouseState = 0
		big = big
	}

	function mouseout(e) {
		big.mouseState = 0
		big = big
	}
</script>

<div>

	<span style="top:1%">{big.file.replaceAll('\\',' • ').replaceAll("_"," ")}</span>
	{#if big.exifState >= 1}
		<span style="top:3%"> {round(big.bw * big.bh/1000000,1)} MP • {big.bw} x {big.bh} • {round(big.bs/1000000,1)} MB </span>
	{/if}
	{#if big.exifState == 2}
		<span style="top:5%;"> {exif.DateTimeOriginal.replace(" "," • ")} </span>
		<span style="top:7%;"> {exif.Model} • f/{exif.FNumber} • 1/{1/exif.ExposureTime} • {exif.FocalLength} mm • ISO {exif.ISOSpeedRatings} </span>
		<span style="top:9%;"> © {exif.Copyright} </span>
	{/if}
	
	<img id='picture' src={big.file} alt=""
		on:wheel={wheel}
		on:mousedown={mousedown}
		on:mousemove={mousemove}
		on:mouseup={mouseup}
		on:mouseout={mouseout}
		on:blur={blur}
		width = {big.width}
		style = "position:absolute; left:{big.left}px; top:{big.top}px;"
	>

</div>

<style>
	span {
		position:absolute;
		left:1%;
	}
</style>

