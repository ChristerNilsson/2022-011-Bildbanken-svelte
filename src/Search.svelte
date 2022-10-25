<script>
	export let sokruta
	export let text0
	export let stack
	
	const placeholders = []
	placeholders.push("01 Separate words with a space")
	placeholders.push("02 Combine words with underscore (_)")
	placeholders.push("03 Share: copies a URL to the clipboard")
	placeholders.push("04 Download: fetches all marked images")
	placeholders.push("05 All: marks all images")
	placeholders.push("06 None: unmarks all images")
	placeholders.push("07 Home is a directory button, selects all images")
	placeholders.push("08 The listbox contains directories in the current directory")
	placeholders.push("09 The current directory is shown in bold")
	placeholders.push("10 Search words are named A, B and C")
	placeholders.push("11 Sort order: ABC AB AC BC A B C")
	placeholders.push("12 High resolution images are draggable and zoomable")
	placeholders.push("13 Only the current directory is searched")
	placeholders.push("14 Search is case sensitive")
	placeholders.push("15 Searching can start anywhere in a word")
	placeholders.push("16 Tournament numbers can be searched like T10370")
	placeholders.push("17 Member numbers can be searched like M585772")
	placeholders.push("18 Dates can be searched like 2022-09-17, 2022-09, 2022 or 09-17")
	
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
