<script>
	export let sokruta
	export let text0
	export let stack

	function clear() {
		sokruta = ""
		document.getElementById("search").focus()
	}

	function share () {
		const q1 = "folder=" + stack.join("\\") 
		const q2 = "query=" + sokruta
		navigator.clipboard.writeText(location.origin + location.pathname + "?" + q1 + "&" + q2)
	}

</script>

<div>
	<button tabindex=0 on:click={share}> Share </button>
	<button tabindex=0 on:click={clear}> Clear </button>
	<input id="search" tabindex=0 bind:value={sokruta} placeholder="Enter case sensitive words separated by spaces. Combine_words_like_this. Share stores a link to the clipboard." style='width:50%'>
	{#if (sokruta.split(" ").length <= 3) && (sokruta.length > 0)}
		&nbsp; {text0} &nbsp;
	{/if}
</div>

<style>
	::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
		color: lightgray;
		opacity: 1; /* Firefox */
	}
</style>
