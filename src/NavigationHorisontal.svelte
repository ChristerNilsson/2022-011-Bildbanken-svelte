<script>
	import _ from "lodash"
	export let stack
	export let pop
	export let WIDTH

	let path= ""
	$: key = _.last(stack)
	$: {
		path = stack.slice(1).join(" • ").replaceAll("_"," ")
		if (path=="") path="Home"
	}

</script>

<div style="width:{WIDTH}px">
	<div>
		<span>
			{#if key != "Home"}
				<button class="alive" on:click = {() => pop()}>Up</button>
			{/if}
			<button class="dead" on:click = {() => pop()}>{path}</button>
		</span>
	</div>
</div>

<style>
	span {
		flex:2;
		overflow:hidden;
		white-space:nowrap;
	}
	.dead {
		border:0px;
		background-color:transparent;
		margin:2px;
		height:30px;
		text-align:left;
	}
	.alive {
		margin:2px;
		height:30px;
		text-align:left;
	}
</style>
