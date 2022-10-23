<script>
	import _ from "lodash"
	export let stack
	export let path
	export let getPath
	export let push

	const click = (key) => {
		if (key.includes('.jpg')) {
			const arr = _.last(path)[key]
			window.open(`/?bs=${arr[2]}&bw=${arr[3]}&bh=${arr[4]}&image=${getPath(stack,"")+"\\"+key}`, "_blank")
		} else {
			push(key)
		}
	}
</script>

{#each _.keys(_.last(path)) as key } 
	<button on:click = {() => click(key)}> {key} </button>
{/each}

<style>
	button {
		width:99%;
		text-align:left;
	}
</style>
