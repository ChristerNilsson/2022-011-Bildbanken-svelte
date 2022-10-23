<script>
	import _ from "lodash"
	export let stack
	export let path
	export let getPath
	export let push

	const click = (key) => {
		if (key.includes('.jpg')) {
			const arr = _.last(path)[key]
			console.log('origin',location.origin)
			console.log('pathname',location.pathname)
			console.log('href',location.href)
			const host = location.origin + location.pathname//.replace('/localhost','')
			console.log('host',host)
			// window.open(`/?bs=${arr[2]}&bw=${arr[3]}&bh=${arr[4]}&image=${getPath(stack,"")+"\\"+key}`)
			window.open(host + `/?bs=${arr[2]}&bw=${arr[3]}&bh=${arr[4]}&image=${getPath(stack,'')}\\${key}`)

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
