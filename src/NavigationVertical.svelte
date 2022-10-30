<script>
	import _ from "lodash"
	export let path
	export let push
	export let is_jpg
	export let WIDTH

	// const digit = (d) => '0' <= d && d <= '9'

	let keys 
	const regex1 = new RegExp(/^\d\d\d\d/)
	const regex2 = new RegExp(/^\d\d-\d\d/)

	$: { 
		keys = _.keys(_.last(path))
		let numbers = true
		for (const key of keys) {
			if ( ! (regex1.test(key) || regex2.test(key))) numbers = false 
		}
		keys.sort()
		if (numbers) keys.reverse()
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
		border:1px black solid; 
		color:white;
		background-color:green;
	}
</style>
