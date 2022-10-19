<script>
	import _ from "lodash"
	import JSZip from "jszip"
	import axios from "axios"
	import { saveAs } from "file-saver"

	export let selected
	export let result

	function make(value) { selected = _.map(result[2], () => value) }
	function download(item) { return axios.get(item.url, { responseType: "blob" }).then((resp) => {zip.file(item.name, resp.data)}) }

	let zip = null

	function all() {make(true)}
	function none() {make(false)}
	function downloadAll() { // download all files as ZIP archive
		zip = new JSZip()
		const fileArr = []
		for (const i in _.range(selected.length)) {
			if (selected[i]==true) {
				const path = result[2][i][2]
				const p = path.lastIndexOf("\\")
				fileArr.push({name:path.slice(p+1), url:path})
			}
		}
		if (fileArr.length == 0) return

		const arrOfFiles = fileArr.map((item) => download(item)) //create array of promises
		Promise.all(arrOfFiles)
			.then(() => {zip.generateAsync({ type: "blob" }).then(function (blob) { saveAs(blob, "Bildbanken.zip") })})
			.catch((err) => {console.log(err)})
	}

</script>

<button on:click = {all}>All</button>
<button on:click = {none}>None</button>
<button on:click = {downloadAll}>Download</button>
