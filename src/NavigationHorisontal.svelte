<script>
	import _ from "lodash"
	export let stack
	export let WIDTH

	let path= ""
	$: key = _.last(stack)
	$: {
		path = stack.slice(1).join(" • ").replaceAll("_"," ")
		if (path=="") path="Home"
	}

</script>

<div style="width:{WIDTH-1}px">
	<div>
		<span>
			<button style="width:{WIDTH-1}px">{path}</button>
		</span>
	</div>
</div>

<style>
	span {
		flex:1;
		overflow:hidden;
		white-space:nowrap;
	}
	button {
		border:0px;
		background-color:transparent;
		margin:2px;
		height:30px;
		text-align:left;
		flex:1;
		overflow:hidden;
		white-space:nowrap;
	}
</style>
