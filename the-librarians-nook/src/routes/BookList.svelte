<script lang="ts">
	let url = window.location.origin;
	//let url = 'http://localhost:8080';
	import { onMount } from 'svelte';

	interface book {
		[key: string]: string | null;
		id: string | null;
		goodReads: string;
		image: string | null;
		status: string | null;
		title: string | null;
	}

	let books: book[] = [];

	function loadBooks() {
		fetch(url + '/books')
			.then((response) => response.json())
			.then((data) => {
				books = data;
			})
			.catch((error) => {
				console.log(error);
				return [];
			});
	}

	onMount(async () => {
		loadBooks();
		loading = false;
	});

	let adding = false;

	async function add(e: SubmitEvent) {
		loading = true;
		let form;
		if (e.target instanceof HTMLFormElement) {
			form = new FormData(e.target);
		} else {
			return;
		}
		let b: book = {
			id: null,
			title: null,
			image: null,
			status: null,
			goodReads: ''
		};
		for (let field of form) {
			const [key, value] = field;
			if (!(value instanceof File)) {
				b[key.toString()] = value;
			} else {
				return;
			}
		}

		await fetch(url + '/books', {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(b)
		})
			.then((response) => response.json())
			.then((data) => {
				books = [...books, data];
			})
			.catch((error) => {
				console.log(error);
				return [];
			});

		loading = false;
		adding = false;
	}

	function update(b: book) {
		fetch(url + '/books/' + b.id, {
			method: 'PATCH',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(b)
		});
	}

	function del(b: book) {
		books = books.filter((book) => book.id != b.id);
		fetch(url + '/books/' + b.id, {
			method: 'DELETE',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			}
		});
	}

	let filter = 'none';
	let fbooks: book[] = [];
	$: {
		fbooks = books;
		if (filter != 'none') {
			fbooks = books.filter((book) => book.status == filter);
		}
	}
	let loading = true;
</script>

<h1>Book List</h1>
{#if loading}
	<div class="loader-container">
		<div class="loader" />
	</div>
{/if}
<div class="list">
	Filter:
	<select id="filter" bind:value={filter}>
		<option value="none">none</option>
		<option value="suggested">suggested</option>
		<option value="will read">will read</option>
		<option value="reading">reading</option>
		<option value="read">done</option>
	</select>
	<br />
	{#each fbooks as book}
		<div class="book">
			<img src={book.image} alt="{book.title} cover" />
			<h2>{book.title}</h2>
			<p><a href={book.goodReads}>good reads</a></p>
			<select bind:value={book.status} on:change={() => update(book)}>
				<option value="suggested">suggested</option>
				<option value="will read">will read</option>
				<option value="reading">reading</option>
				<option value="read">done</option>
			</select>
			<button on:click={() => del(book)}>remove</button>
		</div>
	{/each}
	{#if adding}
		<form on:submit|preventDefault={add}>
			<label
				>GoodReads link<br /><br />
				<input name="goodReads" type="text" />
			</label><br />
			<input type="submit" />
		</form>
	{:else}
		<br />
		<button id="add" on:click={() => (adding = true)}>add</button>
	{/if}
</div>

<style>
	#add {
		background-color: #cc00ff65;
		border-radius: 10px;
		border: none;
		padding: 10px;
		margin-top: 20px;
		margin-bottom: 200px;
	}
	h1 {
		text-align: center;
	}
	img {
		height: 200px;
	}
	.list {
		text-align: center;
	}
	form {
		background-color: #cc00ff65;
		border-radius: 25px;
		display: inline-block;
		width: 51vw;
		margin-top: 2vh;
		padding: 20px;
		margin-bottom: 200px;
	}
	input {
		margin-bottom: 20px;
	}
	button {
		background-color: #ccffff;
		border-radius: 10px;
		border: none;
		padding: 10px;
	}
	input {
		background-color: #ccffff;
		border-radius: 10px;
		border: none;
		padding: 10px;
	}
	select {
		background-color: #ccffff;
		border-radius: 10px;
		border: none;
		padding: 10px;
	}
	.book {
		background-color: #cc00ff65;
		border-radius: 25px;
		display: inline-block;
		width: 51vw;
		margin-top: 2vh;
		padding: 10px;
	}
	.book img {
		margin: 10px;
		float: left;
	}
	@media only screen and (max-width: 600px) {
		.book img {
			float: none;
		}
	}
	#filter {
		background-color: #cc00ff65;
	}

	.loader-container {
		background-color: #cc00ff35;
		position: fixed;
		width: 100vw;
		height: 100vh;
		top: 0;
		left: 0;
		display: flex;
		justify-content: center;
		align-items: center;
		text-align: center;
	}
	.loader {
		border: 16px solid #ccffff; /* Light grey */
		border-top: 16px solid #cc00ff; /* Blue */
		border-radius: 50%;
		width: 120px;
		height: 120px;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
