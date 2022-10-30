<script>
	import _ from "lodash"
	export let stack
	export let pop
	export let WIDTH
</script>

<div style="width:{WIDTH}px">
	{#each stack as key }
		<div>
			{#if key == _.last(stack)}
				<button style="border:1px black solid; background-color:yellow;"><b>{key.replaceAll("_"," ")}</b></button>
			{:else}
				<button style="color:white; border:1px black solid; background-color:red;"on:click = {() => pop(key)}>{key}</button>
			{/if}
		</div>
	{/each}
</div>

<style>
	button {
		margin:2px;
		height:30px;
		width:99%;
		text-align:left;
	}
</style>
