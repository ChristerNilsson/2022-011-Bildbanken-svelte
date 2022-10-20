<script>
	export let big

	document.body.style = "height:100%; overflow:hidden; background-color:black; font-family:-apple-system, BlinkMacSystemFont, Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;"

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
		document.body.style ="margin:0; padding:0; background-color:black; margin:1; padding:0; background-color:black; font-family:-apple-system, BlinkMacSystemFont, Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;"
		// todo Återställ även scrollposition!
	}

</script>

<div>

	<div>
		{big.file}
	</div>

	<button style = "left:0%;  top:5%;">&lt;</button>
	<button style = "left:33%; top:5%;">play</button>
	<button style = "left:66%; top:5%;">&gt;</button>
	
	<img src={big.file} alt=""
		on:wheel={wheel}
		on:mousedown={mousedown}
		on:mousemove={mousemove}
		on:mouseup={mouseup}
		width = {big.width}
		style = "position:absolute; left:{big.left}px; top:{big.top}px;"
	>
	<button style = "left:95%; top:5%;" on:click={close}>exit</button>


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
		color : white;
	}
</style>

