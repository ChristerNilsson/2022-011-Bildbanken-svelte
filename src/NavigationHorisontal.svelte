<script>
	import _ from "lodash"
	export let stack
	export let pop
</script>

<div>
	{#each stack as key }
		{#if key == _.last(stack)}
			<button style="border:0px; background-color:transparent;">{key}</button>
		{:else}
			<button on:click = {() => pop(key)}>{key}</button>
		{/if}
	{/each}

</div>

<style>
	button {
		margin-right:3px;
	}
</style>
