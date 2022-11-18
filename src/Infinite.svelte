<script>
	import Card from './Card.svelte'
	export let WIDTH
	export let getPath
	export let selected
	export let cards
	export let round
	export let fileWrapper
	// export let retro
	export let prettyFilename
</script>

{#each cards as card,index}
	<Card {WIDTH} {getPath} {card} bind:selected {index} {round} {fileWrapper} {prettyFilename} />
{/each}
