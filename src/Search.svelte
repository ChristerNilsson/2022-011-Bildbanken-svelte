<script>
	export let sokruta
	export let result
</script>

<div>
	<input bind:value={sokruta} placeholder="Sök" style='width:50%'>
	{result[0]}
	{result[1]}
</div>