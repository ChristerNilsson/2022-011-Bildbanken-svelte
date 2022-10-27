<script>
	import _ from "lodash"
	import JSZip from "jszip"
	import axios from "axios"
	import { saveAs } from "file-saver"

	export let selected
	export let images
	export let WIDTH
	export let spreadWidth

	$: n = _.sumBy(selected, (value) => value ? 1 : 0)

	function make(value) { selected = _.map(images, () => value) }
	function download(item) { return axios.get(item.url, { responseType: "blob" }).then((resp) => {zip.file(item.name, resp.data)}) }

	let zip = null

	function all() {make(true)}
	function none() {make(false)}
	function downloadAll() { // download all files as ZIP archive
		zip = new JSZip()
		const fileArr = []
		for (const i in _.range(selected.length)) {
			if (selected[i]==true) {
				const path = images[i][2]
				const p = path.lastIndexOf("\\")
				fileArr.push({name:path.slice(p+1), url:path})
			}
		}
		n = fileArr.length
		if (fileArr.length == 0) return

		const arrOfFiles = fileArr.map((item) => download(item)) //create array of promises
		Promise.all(arrOfFiles)
			.then(() => {zip.generateAsync({ type: "blob" }).then(function (blob) { saveAs(blob, "Bildbanken.zip") })})
			.catch((err) => {console.log(err)})
	}

</script>

<!-- <div style="width:{WIDTH}px; height:34px">
	<button on:click={share} style="left:0px;           width:{spreadWidth(1/3,WIDTH)}px">Share</button>
	<button on:click={clear} style="left:{WIDTH/3}px;   width:{spreadWidth(1/3,WIDTH)}px">Clear</button>
	<button on:click={help}  style="left:{2*WIDTH/3}px; width:{spreadWidth(1/3,WIDTH)}px">Help</button>
</div> -->


<div style="width:{WIDTH}px; height:34px">
	<button style="left:0px;           width:{spreadWidth(0.25,WIDTH)}px" on:click = {none}>None</button>
	<button style="left:{WIDTH/4}px;   width:{spreadWidth(0.50,WIDTH)}px" on:click = {downloadAll}>Download {n} image(s)</button>
	<button style="left:{3*WIDTH/4}px; width:{spreadWidth(0.25,WIDTH)}px" on:click = {all}>All</button>
</div>

<style>
	button {
		position:absolute;
		height:30px;
		margin:2px;
	}
	div {
		margin:0px
	}
</style>

