from flask import Flask, request
from flask_cors import cross_origin
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    url = book["goodReads"]
    book["id"] = len(books)

    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'BookCover__image'))
        WebDriverWait(browser, timeout).until(element_present)
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'Text__title1'))
        WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    
    soup = BeautifulSoup(browser.page_source,  'html.parser')
    title = soup.find_all("h1")[0]
    image = soup.find_all("div", {"class": "BookCover__image"})[0].find_all("img")[0]

    book["title"] = title.contents[0]
    book["image"] = image["src"]
    book["status"] = "suggested"

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
