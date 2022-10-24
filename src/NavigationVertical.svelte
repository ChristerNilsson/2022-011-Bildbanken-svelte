<script>
	import _ from "lodash"
	export let path
	export let push
	export let is_jpg

	let selected = ""

</script>

<select bind:value={selected} size=10 style="width:470px" >
	{#each _.keys(_.last(path)) as key } 
		{#if ! is_jpg(key)}
			<option value={key} on:click = {() => push(key)}>
				{key}
			</option>
		{/if}
	{/each}
</select>

<style>
	select {
		font-size: inherit;
		font-family: inherit;
		padding: 0.4rem;
	}
</style>
