<script>
	import _ from "lodash"
	export let stack
	export let path
	export let getPath
	export let push

	const click = (key) => {
		if (key.includes('.jpg')) {
			const arr = _.last(path)[key]
			const host = location.origin + location.pathname
			window.open(host + `?bs=${arr[2]}&bw=${arr[3]}&bh=${arr[4]}&image=${getPath(stack,'')}\\${key}`)
		} else {
			push(key)
		}
	}
</script>

<span>
	{#each _.keys(_.last(path)) as key } 
	<button on:click = {() => click(key)}> {key} </button>
	{/each}
</span>

<style>
	button {
		margin:1px;
		/* width:99%; */
		/* text-align:left; */
	}
</style>
