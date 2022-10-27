<script>
	import _ from "lodash"
	export let path
	export let push
	export let is_jpg
	export let WIDTH
</script>

<div style="width:{WIDTH}px">
	{#each _.keys(_.last(path)) as key } 
		<div>
			{#if ! is_jpg(key)}
				<button value={key} on:click = {() => push(key)}>
					{key}
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
	}
</style>
