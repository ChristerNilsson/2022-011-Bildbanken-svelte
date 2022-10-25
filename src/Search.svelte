<script>
	export let sokruta
	export let text0
	export let stack

	function push(s) {
		let n = helpTexts.length
		if (n < 10) n = '0' + n
		helpTexts.push(n + ' ' + s)
	}
 	
	const helpTexts = []
	push("[Clear] shows next help text")
	push("[Share] shows previous help text")
	push("Separate words with a space")
	push("Combine words with underscore (_)")
	push("Search words are named A, B and C")
	push("Sort order: ABC AB AC BC A B C")
	push("Only the Current directory is searched")
	push("Search is case sensitive")
	push("Searching can start anywhere in a word")
	push("Search Tournament numbers like T10370")
	push("Search Member numbers like M585772")
	push("Search dates like 2022-09-17, 2022-09, 2022 or 09-17")
	push("[Share] copies a URL to the clipboard")
	push("[Download] zips marked images")
	push("[All] marks images")
	push("[None] unmarks images")
	push("[Home] makes the Home directory the Current directory")
	push("The Current directory is shown in bold")
	push("The listbox contains directories in the Current directory")
	push("High resolution images are draggable and zoomable")
	push("Contact: janchrister_punkt_nilsson_alfakrull_gmail_punkt_com")
	
	helpTexts[0] += " of " + helpTexts.length
	
	function clear() {
		sokruta = ""
		document.getElementById("search").focus()
		helpTexts.push(helpTexts.shift())
		helpTexts = helpTexts
	}

	function share () {
		const q1 = "folder=" + stack.join("\\") 
		const q2 = "query=" + sokruta
		navigator.clipboard.writeText(location.origin + location.pathname + "?" + q1 + "&" + q2)
		helpTexts.unshift(helpTexts.pop())
		helpTexts = helpTexts
	}

	window.onload = () => document.getElementById("search").focus()

</script>

<div>
	<button on:click={share}> Share </button>
	<button on:click={clear}> Clear </button>
	<input autocomplete="off" id="search" bind:value={sokruta} placeholder={helpTexts[0]} style='width:50%'>
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
