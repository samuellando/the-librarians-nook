from flask import Flask, request
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import firebase_admin
from firebase_admin import firestore

import os
os.environ['GRPC_DNS_RESOLVER'] = 'native'

firebase_app = firebase_admin.initialize_app()
db = firestore.client()

app = Flask(__name__)

@app.route('/books', methods=["GET"])
def get_books():
    books = []
    books_ref = db.collection(u'books')
    docs = books_ref.stream()
    for doc in docs:
        book = doc.to_dict()
        book["id"] = doc.id
        books.append(book)
        
    return books;

@app.route('/books', methods=["POST"])
def post_book():
    book = json.loads(request.data)
    url = book["goodReads"]

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

    books_ref = db.collection(u'books')
    doc = books_ref.add(book)

    book["id"] = doc[1].id

    return book;

@app.route('/books/<id>', methods=["PATCH"])
def patch_book(id):
    books_ref = db.collection(u'books')
    doc = books_ref.document(id)
    book = json.loads(request.data)
    doc.set(book)
    return {"result": 200}

@app.route('/books/<id>', methods=["DELETE"])
def remove_book(id):
    books_ref = db.collection(u'books')
    doc = books_ref.document(id)
    doc.delete()
    return {"result": 200}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
