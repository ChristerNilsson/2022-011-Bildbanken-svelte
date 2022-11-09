<script>
	import _ from "lodash"
	export let visibleKeys
	export let push
	export let is_jpg
	export let WIDTH
	export let spaceShip
	export let stack
	export let spreadWidth

	function sortera(i) {
		sortIndex = i
		let index = i==1 ? 11 : 0
		// keys = _.keys(visibleKeys)
		keys.sort((a,b) => spaceShip(a.slice(index),b.slice(index)))
		if (i==0) keys.reverse()
		// keys = keys
	}

	$: n = stack.length
	let sortIndex = n==2 ? 1 : 0
	let keys
	$: {
		keys = _.keys(visibleKeys)
		sortera(sortIndex)
		// keys = keys 
	}
	
	function clean(s) {
		s = s.replace(/_T\d+/,'')
		s = s.replace(/_M\d+/,'')
		s = s.replace(/_V\d+/,'')
		s = s.replace(/_F\d+/,'')
		s = s.replaceAll("_"," ")
		return s
	}
	
</script>

<div style="width:{WIDTH}px">

{#if n==2}
	<div style="width:{WIDTH}px">
		<button class="header" style="left:{0.000*WIDTH}px; width:{spreadWidth(0.115,WIDTH)}px" on:click = {()=>sortera(0)}>Date</button>
		<button class="header" style="left:{0.115*WIDTH}px; width:{spreadWidth(0.888,WIDTH)}px" on:click = {()=>sortera(1)}>Event</button>
	</div>
{/if}

	{#each keys as key }
		<div>
			<span>
				{#if ! is_jpg(key)}
					<button class="row" value={key} on:click = {() => push(key)}>
						{clean(key)} ({visibleKeys[key]})
					</button>
				{/if}
			</span>
		</div>
	{/each}
</div>

<style>
	span {
		flex:1;
		overflow:hidden;
		white-space:nowrap;
	}
	div {
		margin:0px
	}
	.header {
		margin:0.5px;
		height:30px;
	}
	.row {
		margin:2px;
		height:30px;
		width:99.5%;
		text-align:left;
		flex:1;
		overflow:hidden;
		white-space:nowrap;
	}

</style>
