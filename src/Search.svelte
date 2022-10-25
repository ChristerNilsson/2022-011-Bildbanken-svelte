<script>
	export let sokruta
	export let text0
	export let stack

	function push(s) {
		let n = placeholders.length
		if (n < 10) n = '0' + n
		placeholders.push(n + ' ' + s)
	}
 	
	const placeholders = []
	push("[Clear] Show next help text")
	push("[Share] Show previous help text")
	push("Separate words with a space")
	push("Combine words with underscore (_)")
	push("Search words are named A, B and C")
	push("Sort order: ABC AB AC BC A B C")
	push("Only the current directory is searched")
	push("Search is case sensitive")
	push("Searching can start anywhere in a word")
	push("Search Tournament numbers like T10370")
	push("Search Member numbers like M585772")
	push("Search dates like 2022-09-17, 2022-09, 2022 or 09-17")
	push("[Share] copies a URL to the clipboard")
	push("[Download] fetches all marked images")
	push("[All] marks all images")
	push("[None] unmarks all images")
	push("[Home] selects images in all directories")
	push("The current directory is shown in bold")
	push("The listbox contains directories in the current directory")
	push("High resolution images are draggable and zoomable")
	placeholders[0] += " of " + placeholders.length
	
	function clear() {
		sokruta = ""
		document.getElementById("search").focus()
		placeholders.push(placeholders.shift())
		placeholders = placeholders
	}

	function share () {
		const q1 = "folder=" + stack.join("\\") 
		const q2 = "query=" + sokruta
		navigator.clipboard.writeText(location.origin + location.pathname + "?" + q1 + "&" + q2)
		placeholders.unshift(placeholders.pop())
		placeholders = placeholders
	}

</script>

<div>
	<button tabindex=0 on:click={share}> Share </button>
	<button tabindex=0 on:click={clear}> Clear </button>
	<input autocomplete="off" id="search" tabindex=0 bind:value={sokruta} placeholder={placeholders[0]} style='width:50%'>
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
