<script>
	export let sokruta
	export let result
</script>

<div>
	<button on:click={() => sokruta = ""}>Clear</button>
	<input bind:value={sokruta} placeholder="Sök" style='width:50%'>
	{result[0]}
	{result[1]}
</div>

<style>
	div,input {
		font-size: 0.9em;
		color:white;
		background-color: black;
	}
	input {
		margin:4px;
	}
</style>
