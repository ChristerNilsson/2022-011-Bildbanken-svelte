<script>
  import { MasonryInfiniteGrid } from "@egjs/svelte-infinitegrid";
	import _ from "lodash"
	export let dirs

	let items = getItems(0, 10);

  function getItems(nextGroupKey, count) {
    const nextItems = [];

    for (let i = 0; i < count; ++i) {
      const nextKey = nextGroupKey * count + i;

      nextItems.push({ groupKey: nextGroupKey, key: nextKey });
    }
    return nextItems; 
  }

	function getDir (dirs,key) {return dirs[key]}

	function visa(url) {
		console.log(url)
	}

	function assert(a,b) {
		if (!_.isEqual(a,b)) console.log("Assert failed",a,'!=',b)
	}
	const range = _.range

	function spaceShip (a,b) {
		if (a < b) return -1
		else if (a == b) return 0
		return 1 
	}
	assert(spaceShip(1,2),-1)
	assert(spaceShip(1,1),0)
	assert(spaceShip(1,0),1)
	assert(_.range(3),[0,1,2])

	function comp (a,b) { if (a[0] == b[0]) {return spaceShip(a[1], b[1])} else {return spaceShip(a[0], b[0])}}
	function comp2(a,b) { if (a.length == b.length) {return spaceShip(a,b)} else {return -spaceShip(a.length,b.length)}}

	function search (data,s) {
		const alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		const res = []
		const words = s.split(' ')
		const stat = {}
		let total = 0
		for (const tournament in data) {
			//console.log(tournament)
			total += data[tournament].length
			for (const filename of data[tournament]) {
				// let count = 0  
				let s = ''
				for (const i in range(words.length)) {
					const word = words[i]
					if (word == "") continue
					//word = word.replaceAll '_',' '
					//console.log(tournament,tournament.includes(word),word)
					if (tournament.includes(word) || filename.includes(word)) s += alfabet[i]
				}
				if (s.length > 0) {
					res.push([-s.length,s,tournament,filename])
					stat[s] = (stat[s] || 0) + 1
				}
			}
		}

		// console.log('stat',stat)
		res.sort(comp)
		// console.log(res)

		const keys = Object.keys(stat)
		keys.sort(comp2) 
		const st = []
		let antal = 0
		for (const key of keys) {
			st.push(`${key}:${stat[key]}`)
			antal += stat[key]
		}
		// console.log('st',st)
		return [st.join(' '),`${antal} av ${total} bilder`,res]
	}

</script>
 
{#await dirs}
	<p>Loading...</p>
{:then dirs}

	
	{
		const sokruta = document.getElementById("sokruta")
		const result = search(dirs,sokruta.value())
		console.log(result)
	}

	<div>
		<input id='sokruta' placeholder="Sök" style='width:100%'>
	</div>

	<MasonryInfiniteGrid
		class="container"
		gap={5}
		{items}
		on:requestAppend={({ detail: e }) => {
			const nextGroupKey = (+e.groupKey || 0) + 1;
			items = [...items, ...getItems(nextGroupKey, 10)];
		}}
		let:visibleItems
	>
		{#each visibleItems as item (item.key)}
			{#if item.key < dirs["2022-10-01 Minior-Lag-DM"].length }
				<div class="item">
					<div class="thumbnail">
						<img
							src={"2022/Minior-Lag-DM_files/small/" + dirs["2022-10-01 Minior-Lag-DM"][item.key % dirs["2022-10-01 Minior-Lag-DM"].length]}
							alt=""
							width = 400
							xxxonclick="visa(1)"
						/>
					</div>
					<div class="info">{`2022/Minior-Lag-DM`}</div>
					<div class="info">{dirs["2022-10-01 Minior-Lag-DM"][item.key]}</div>
					<div class="info">{"A (C) Lars OA Hedlund"}</div>
				</div>
			{/if}
		{/each}
</MasonryInfiniteGrid>

{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
