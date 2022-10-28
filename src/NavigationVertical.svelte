<script>
	import _ from "lodash"
	export let path
	export let push
	export let is_jpg
	export let WIDTH

	const digit = (d) => '0' <= d && d <= '9'

	let keys 

	$: { 
		keys = _.keys(_.last(path))
		let numbers = true
		for (const key of keys) {
			if ( ! (digit(key[0]) && digit(key[1]) && digit(key[2]) && digit(key[3]))) numbers = false
		}
		keys.sort()
		if (numbers) keys.reverse()
		// console.log('keys',numbers,keys)
		keys = keys
	}

</script>

<div style="width:{WIDTH}px">
	{#each keys as key } 
		<div>
			{#if ! is_jpg(key)}
				<button value={key} on:click = {() => push(key)}>
					{key.replaceAll("_"," ")}
				</button>
			{/if}
		</div>
	{/each}
</div>

<style>
	div {
		margin:0px
	}
	button {
		margin:2px;
		height:30px;
		width:99%;
		text-align:left;
	}
</style>
