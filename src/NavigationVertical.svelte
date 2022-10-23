<script>
	import _ from "lodash"
	export let stack
	export let path
	export let getPath
	export let push
</script>

{#if _.last(stack).includes('.jpg')}
	<img src={getPath(stack,"")} alt='big' />
{:else}
<!-- {console.log('Cesar',path)} -->
{#each _.keys(_.last(path)) as key } 
		<!-- {console.log('Cesar',key)} -->
		<div>
			{#if _.isNumber(key)}
				<button on:click = {() => push(key,_.last(path)[key])}>{_.last(path)[key]}</button>
			{:else}
				<button on:click = {() => push(key)}>{key}</button>
			{/if}
		</div>
	{/each}
{/if}

<style>
	button {
		width:99%;
		text-align:left;
	}

	div {
		font-size: 0.9em;
	}
</style>
