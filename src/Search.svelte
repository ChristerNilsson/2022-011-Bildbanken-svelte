<script>
	export let sokruta
	export let text0
	export let text1
	export let stack

	function clear() {
		sokruta = ""
		document.getElementById("search").focus()
	}

	function share () {
		const extra = (sokruta == "") ? "folder=" + stack.join("\\") : "query=" + sokruta
		navigator.clipboard.writeText(location.origin + location.pathname + "?" + extra)
	}

</script>

<div>
	<button tabindex=0 on:click={share}> Share </button>
	<button tabindex=0 on:click={clear}> Clear </button>
	{text0}
	<input id="search" tabindex=0 bind:value={sokruta} placeholder="Enter case sensitive words separated by spaces. Combine_words_like_this. Share stores a link to the clipboard." style='width:50%'>
	{text1}

</div>

<style>
	div,input {
		font-size: 0.9em;
	}
	input {
		margin:4px;
	}
	::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
		color: lightgray;
		opacity: 1; /* Firefox */
	}
</style>
