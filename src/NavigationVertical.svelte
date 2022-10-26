<script>
	import _ from "lodash"
	export let path
	export let push
	export let is_jpg
</script>

<div>
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
		margin:1px;
		height:33px;
		width:473px;
		text-align:left;
	}
</style>


<!-- <select bind:value={selected} size=10 style="width:470px;" >
	{#each _.keys(_.last(path)) as key } 
		{#if ! is_jpg(key)}
			<option value={key} on:click = {() => push(key)}>
				{key}
			</option>
		{/if}
	{/each}
</select> -->
