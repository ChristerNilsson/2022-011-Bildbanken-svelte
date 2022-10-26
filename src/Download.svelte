<script>
	import _ from "lodash"
	import JSZip from "jszip"
	import axios from "axios"
	import { saveAs } from "file-saver"

	export let selected
	export let images

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

<div style="width:475px" >
	<button style="width:115px" on:click = {none}>None</button>
	<button style="width:229px" on:click = {downloadAll}>Download {n} image(s)</button>
	<button style="width:115px" on:click = {all}>All</button>
</div>

<style>
button{
	margin:1px;
	height:33px;
}
div {
	margin:0px
}
</style>

