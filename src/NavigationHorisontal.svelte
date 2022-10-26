<script>
	import _ from "lodash"
	export let stack
	export let pop
</script>

<div style="width:470px">
	{#each stack as key }
		<div>
			{#if key == _.last(stack)}
				<button style="border:0px; background-color:transparent;"><b>{key}</b></button>
			{:else}
				<button on:click = {() => pop(key)}>{key}</button>
			{/if}
		</div>
	{/each}
</div>

<style>
	button {
		margin:1px;
		height:33px;
		width:473px;
		text-align:left;
	}
</style>
