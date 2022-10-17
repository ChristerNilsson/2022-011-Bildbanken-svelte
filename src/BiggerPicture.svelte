<script>
	export let bigfile

	let state = 0

	function grow(event) {
		event.stopPropagation()
		state = 1 - state
		console.log(event)
		const src = event.srcElement
		console.log(src.naturalWidth,src.naturalHeight)
	}

</script>

{#if state==0}
	<div style="position:absolute; left:{100}px; top:0px">
		<img src={bigfile} alt="X" height={innerHeight-10} on:click={grow} on:keydown={grow}/>
	</div>
{:else}
	<div style="position:absolute; left:{100}px; top:0px">
		<img src={bigfile} alt="X" height={1.5*innerHeight} on:click={grow} on:keydown={grow}/>
	</div>
{/if}

<!-- <style>
	.center {
		top: 0;
		margin-top:0;
		display: block;
		margin-left: auto;
		margin-right: auto;
		/* width: 50%; */
	}
</style> -->
