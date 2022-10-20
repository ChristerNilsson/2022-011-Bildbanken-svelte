<script>
	export let sokruta
	export let text0
	export let text1
</script>

<div>
	<button on:click={() => sokruta = ""}>Clear</button>
	{text0}
	<input bind:value={sokruta} placeholder="Enter case sensitive words separated by spaces. Combine_words_like_this." style='width:50%'>
	{text1}
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
