<script>
	import _ from "lodash"
	export let path
	export let push
	export let is_jpg
	export let WIDTH

	let keys 
	const regexYYYY = new RegExp(/^\d\d\d\d/)

	$: { 
		keys = _.keys(_.last(path))
		console.log('keys',keys)
		let numbers = true
		for (const key of keys) {
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
			<span>
				{#if ! is_jpg(key)}
					<button value={key} on:click = {() => push(key)}>
						{key.replaceAll("_"," ")}
					</button>
				{/if}
			</span>
		</div>
	{/each}
</div>

<style>
	span {
		flex:1;
		overflow:hidden;
		white-space:nowrap;
	}
	div {
		margin:0px
	}
	button {
		margin:2px;
		height:30px;
		width:99%;
		text-align:left;
		flex:1;
		overflow:hidden;
		white-space:nowrap;
	}
</style>
