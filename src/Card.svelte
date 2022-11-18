<script>
	import _ from "lodash"
	export let WIDTH
	export let getPath
	export let card
	export let selected
	export let index
	export let round
	export let fileWrapper
	export let prettyFilename

	$: filename = card[2] + "\\" + card[12]

	$: M = getNumber(filename,'M')
	$: T = getNumber(filename,'T')
	$: V = getNumber(filename,'V')
	$: F = getNumber(filename,'F')

	function getNumber(path,letter) { // Används för filnummer = MTVP
		let matches 
		if (letter=='M') matches = path.match(/[M]\d+/)
		if (letter=='T') matches = path.match(/[T]\d+/)
		if (letter=='V') matches = path.match(/[V]\d+/)
		if (letter=='F') matches = path.match(/[F]\d+/)
		return matches ? matches[0].slice(1) : ""
	}

	function prettyPath(path) { // Tag bort eventuellt T-nummer
		path = path.split('\\')
		path = path.slice(2,path.length-1)
		path = path.join(" • ")
		path = path.replace(/_V\d+/,'')
		path = path.replace(/_T\d+/,'')
		path = path.replace(/_F\d+/,'')
		return path.replaceAll('_', ' ')
	}

</script>

<div class="card" id="images" style="position:absolute; width:{WIDTH}px; left:{card[5]}px; top:{card[6]}px">
	<img
		margin:0px
		padding:0px
		src = {getPath(filename,"small")}
		width = {WIDTH}px
		alt = ""
		on:click = {() => {
			const host = location.origin + location.pathname
			window.open(host + `?bs=${card[9]}&bw=${card[10]}&bh=${card[11]}&image=${getPath(filename,'')}`)
		}}
		on:keydown = {() =>{}}
	/>
	<div class="group">
		<div class="info" style="width:{WIDTH}px">
			&nbsp;{prettyFilename(filename)}
		</div>
		<div class="info" style="width:{WIDTH}px">
			&nbsp;{prettyPath(filename)}
		</div>
		<div class="info" style="display:flex; height:13px; width:{WIDTH}px">
			&nbsp;{card[7]}

			{#if card[1]}
				&nbsp;&nbsp;{card[1]}
			{/if}

			&nbsp;&nbsp;<input class="largerCheckbox" type="checkbox" value="" bind:checked={selected[index]}/> 

			{#if M}
				&nbsp;&nbsp;<a target="_blank" href="https://member.schack.se/ViewPlayerRatingDiagram?memberid={M}">M</a>
			{/if}
			{#if V}
				&nbsp;&nbsp;<a target="_blank" href="https://player.vimeo.com/video/{V}">V</a>
			{/if}
			{#if F}
				&nbsp;&nbsp;<a target="_blank" href="{fileWrapper[0][F]}">F</a>
			{/if}
			{#if T}
				&nbsp;&nbsp;<a target="_blank" href="https://member.schack.se/ShowTournamentServlet?id={T}&listingtype=2">T</a>
			{/if}

			<span style="flex:2; text-align:center; white-space:nowrap;"> © Lars OA Hedlund </span>
			<span style="flex:1; text-align:right; white-space:nowrap;"> {round(card[10]*card[11]/1024/1024,1)} MP • {card[10]} x {card[11]} • {round(card[9]/1024,0)} kB &nbsp;</span>
		</div>	
	</div>
</div>

<style>
	input.largerCheckbox {
		width: 12px;
		height: 12px;
	}	
	.group {
		margin-top:-3px;
	}
	.info {
		margin:0px;
		text-align:left;
		padding-top:1px;
		white-space:nowrap;
		overflow:hidden;
		background-color:lightgray;
	}
	.card {
		margin:0px;
		font-size: 0.9em;
		max-height: 800px;
	}
	div {
		margin:0px;
		padding:0px;
		font-size: 0.9em;
	}
</style>
