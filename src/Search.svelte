<script>
	export let sokruta
	export let result
</script>

<div>
	<button on:click={() => sokruta = ""}>Clear</button>
	{result[1]}
	<input bind:value={sokruta} placeholder="Enter case sensitive words separated by spaces. Combine_words_like_this." style='width:50%'>
	{result[0]}
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
	::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
		color: lightgray;
		opacity: 1; /* Firefox */
	}
</style>
