import App from './App.svelte';

//import * as data from 'bilder.json';

async function getDirs() {
	let response = await fetch("bilder.json");
	let dirs = await response.json();
	return dirs;
}

const app = new App({
	target: document.body,
	props: {
		dirs : getDirs()
	}
});

export default app;