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
		const q1 = "folder=" + stack.join("\\") 
		const q2 = "query=" + sokruta
		navigator.clipboard.writeText(location.origin + location.pathname + "?" + q1 + "&" + q2)
	}

	window.onload = () => document.getElementById("search").focus()

</script>

<input autocomplete="off" id="search" bind:value={sokruta} placeholder='Search' >
<div class="center">
	{text1}
</div>
<div style="width:475px">
	<button on:click={share} style="width:233px"> Share </button>
	<button on:click={clear} style="width:233px"> Clear </button>
</div>
{#if (sokruta.split(" ").length <= 3) && (sokruta.length > 0)}
	<div class="center">
		{text0}
	</div>
{/if}

<style>
	.center {
		margin-top:7px;
		width:475px;
		text-align:center;
		height:25px
	}
	div {
		margin:0px;
	}
	button {
		margin:1px;
	}
	input {
		width:473px;
		margin:1px;
	}
	::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
		color: lightgray;
		opacity: 1; /* Firefox */
	}
</style>
