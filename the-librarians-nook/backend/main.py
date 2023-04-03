from flask import Flask, request
from flask_cors import cross_origin
import json

app = Flask(__name__)

books = [
		{
            "id": "0",
			"image":
				'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1170803558l/72193.jpg',
			"title": 'Harry Potter and the Philosopher’s Stone',
			"goodReads":
				'https://www.goodreads.com/book/show/72193.Harry_Potter_and_the_Philosopher_s_Stone?from_search=true&from_srp=true&qid=vHgcnNSuGC&rank=1',
			"status": 'suggested'
		},
		{
            "id": "1",
			"image":
				'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1574199214i/52767659.jpg',
			"title": 'The End of Everything',
			"goodReads":
				'https://www.goodreads.com/book/show/52767659-the-end-of-everything?ref=nav_sb_ss_1_21',
			"status": 'suggested'
		}
	]

@app.route('/books', methods=["GET"])
@cross_origin()
def get_books():
    global books
    return books;

@app.route('/books', methods=["POST"])
@cross_origin()
def post_book():
    global books
    book = json.loads(request.data)
    book["id"] = len(book)
    books.append(book)
    return book;

@app.route('/books/<id>', methods=["PATCH"])
@cross_origin()
def patch_book(id):
    for i, book in enumerate(books):
        if book["id"] == id:
            books[i] = json.loads(request.data)
            return {"id": id, "result": 200};
    return {"result": 400}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
