<script lang="ts">
	import { onMount } from 'svelte';

	interface book {
		[key: string]: string | null;
		id: string | null;
		goodReads: string;
		image: string;
		status: string;
		title: string;
	}

	let books: book[] = [];

	function loadBooks() {
		fetch('http://localhost:8080/books')
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
	});

	let adding = false;

	async function add(e: SubmitEvent) {
		let form;
		if (e.target instanceof HTMLFormElement) {
			form = new FormData(e.target);
		} else {
			return;
		}
		let b: book = {
			id: null,
			title: '',
			image: '',
			status: 'suggested',
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

		await fetch('http://localhost:8080/books', {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(b)
		});
		loadBooks();
		adding = false;
	}

	function update(b: book) {
		fetch('http://localhost:8080/books/' + b.id, {
			method: 'PATCH',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(b)
		});
	}
</script>

<h1>Book List</h1>
<div class="list">
	{#each books as book}
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
		</div>
	{/each}
	{#if adding}
		<form id="add" on:submit|preventDefault={add}>
			<label>
				title
				<input name="title" type="text" />
			</label><br />
			<label
				>image link
				<input name="image" type="text" />
			</label><br />
			<label
				>goo reads link
				<input name="gooreads" type="text" />
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
		margin-top: 20px;
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
	.book {
		background-color: red;
		display: inline-block;
		width: 51vw;
		margin-top: 2vh;
		padding: 10px;
	}
	.book img {
		margin: 10px;
		float: left;
	}
</style>
