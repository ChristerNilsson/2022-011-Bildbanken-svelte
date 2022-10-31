<script>
	import _ from "lodash"
	export let path
	export let push
	export let is_jpg
	export let WIDTH

	let keys 
	const regexYYYY = new RegExp(/^\d\d\d\d/)
	// const regexMMDD = new RegExp(/^\d\d-\d\d/)

	$: { 
		keys = _.keys(_.last(path))
		let numbers = true
		for (const key of keys) {
			// if ( ! (regexYYYY.test(key) || regexMMDD.test(key))) numbers = false 
			if (key.includes('.jpg') || key.includes('.JPG')) continue
			if ( ! regexYYYY.test(key)) numbers = false 
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
		/* border:1px black solid;  */
		/* color:white; */
		/* background-color:green; */
	}
</style>
