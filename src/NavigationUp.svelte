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
