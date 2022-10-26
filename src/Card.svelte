<script>
	import _ from "lodash"
	export let WIDTH
	export let getPath
	export let card
	export let selected
	export let index
	export let round
	export let offset

	$: y = card[5]==0 ? offset + card[6] : card[6]

	function getNumber(path,letter) { // Används både för T och M-nummer
		path = path.replace('.jpg','')
		const arr = path.split('\\')
		const pos = " MT".indexOf(letter)
		const cand = arr[arr.length-pos]
		const arr2 = cand.split('_')
		const tnummer = _.last(arr2)
		if (tnummer[0]==letter) return tnummer.slice(1)
		return ""
	}
 
	function prettyFilename(path) { // Tag bort eventuellt M-nummer
		let i = path.lastIndexOf('\\')
		let s = path.slice(i+1)
		s = s.replace('.jpg','')
		s = s.replace(/_M\d+/,'')
		s = s.replaceAll(/_/ig,' ')
		return s
	}

	function prettyPath(path) { // Tag bort eventuellt T-nummer
		path = path.split('\\')
		path = path.slice(2,path.length-1)
		path = path.join(" ")
		path = path.replace(/_T\d+/,'')
		return path.replaceAll('_', ' ') 
	}

</script>

<div class="card" id="images" style="position:absolute; left:{card[5]}px; top:{y}px">
	<img 
		margin:0px
		padding:0px
		src = {getPath(card[2].split("\\"),"small")}
		width = {WIDTH}
		alt = ""
		on:click = {() => {
			const host = location.origin + location.pathname
			window.open(host + `?bs=${card[9]}&bw=${card[10]}&bh=${card[11]}&image=${getPath(card[2].split('\\'),'')}`)
		}}
		on:keydown = {() =>{}}
	/>
	<div class="group">
		<div class="info" >&nbsp;{prettyFilename(card[2])}
			<a target="_blank" href="https://member.schack.se/ViewPlayerRatingDiagram?memberid={getNumber(card[2],'M')}">{getNumber(card[2],'M')}</a>
		</div>
		<div class="info" >&nbsp;{prettyPath(card[2])}
			<a target="_blank" href="https://member.schack.se/ShowTournamentServlet?id={getNumber(card[2],'T')}">{getNumber(card[2],'T')}</a>
		</div>
		<div class="info" style="display:flex; height:13px">
			&nbsp;{card[7]} • &nbsp;
			<input class="largerCheckbox" type="checkbox" value="" bind:checked={selected[index]}/> &nbsp; •&nbsp;
			{card[1]}
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
		/* margin-bottom:4px; */
	}
	.info {
		margin:0px;
		text-align:left;
		padding-top:1px;
		white-space:nowrap;
		width:475px;
		overflow:hidden;
		background-color:lightgray;
	}
	.card {
		margin:0px;
		font-size: 0.9em;
		width: 475px; 
		max-height: 800px;
	}
	div {
		margin:0px;
		padding:0px;
		font-size: 0.9em;
	}
</style>
