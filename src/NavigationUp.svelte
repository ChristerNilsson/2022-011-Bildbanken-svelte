<script>
	import _ from "lodash"
	export let stack
	export let pop
</script>

<div style="height:50px">
	{#each stack as key }
		{#if key == _.last(stack)}
			{key}
		{:else}
			<button on:click = {() => pop(key)}>{key}</button>
		{/if}
		&nbsp;
	{/each}
</div>

<style>
	button {
		margin:1px;
		padding:1px;
	}
	div {
		font-size: 0.9em;
		color:white;
		background-color: black;
	}
</style>

