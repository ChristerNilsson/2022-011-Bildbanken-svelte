<script>
	import _ from "lodash"
	export let stack
	export let pop
</script>

<div style="height:30px">
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
	div {
		margin:1px;
		padding:1px;
		font-size: 0.9em;
	}
</style>

