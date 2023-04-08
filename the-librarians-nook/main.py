from flask import Flask, request
from flask import send_from_directory
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_binary
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import firebase_admin
from firebase_admin import firestore
import anyrest

import os
os.environ['GRPC_DNS_RESOLVER'] = 'native'

firebase_app = firebase_admin.initialize_app()
db = firestore.client()

app = Flask(__name__)
anyrest.addAnyrestHandlers(app, db)

@app.route('/books', methods=["GET"])
def get_books():
    books = anyrest.anyrest_get(db, "books")
    r = []
    for id, book in books.items():
        book["id"] = id
        r.append(book)
        
    return r;

@app.route('/books', methods=["POST"])
def post_book():
    book = json.loads(request.data)
    url = book["goodReads"]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(chrome_options=chrome_options)
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

    books_ref = db.collection(u'books')
    doc = books_ref.add(book)

    book["id"] = doc[1].id

    return book;

@app.route('/books/<id>', methods=["PATCH"])
def patch_book(id):
    return anyrest.anyrest_patch(db, "books/"+id)

@app.route('/books/<id>', methods=["DELETE"])
def remove_book(id):
    return anyrest.anyrest_delete(db, "books/"+id)

@app.route('/')
def index():
    return send_from_directory("build", "index.html")

@app.route('/<path:path>')
def frontend(path):
    return send_from_directory("build", path)

if __name__ == '__main__':
    from flask_cors import CORS
    CORS(app)
    app.run(host='127.0.0.1', port=8080, debug=True)
