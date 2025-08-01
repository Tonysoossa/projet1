import os
import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from urllib.parse import urljoin
import scrape_book_details as sbd

def scrape_books_categories():
    base_url = "https://books.toscrape.com/catalogue/category/books/classics_6/"
    all_books_data = []
    page = 1

    if not os.path.exists('images'):
        os.makedirs('images')

    while True:
        url = base_url + "index.html" if page == 1 else base_url + f"page-{page}.html"
        response = requests.get(url)

        if response.status_code == 404:
            pass

        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.select('.product_pod')

        if not books:
            pass

        for book in books:
            link = book.select('h3 > a')[0]['href']
            book_url = urljoin(url, str(link))

            book_number = len(all_books_data) + 1
            book_data = sbd.scrape_book_details(book_url, book_number)
            book_data['number'] = book_number

            all_books_data.append(book_data)
            print(f"✓ {book_data['title']}")
            time.sleep(0.5)

        page += 1

    fieldnames = ['number', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                  'number_available', 'product_description', 'category', 'review_rating',
                  'image_url', 'book_url', 'local_image_path']

    with open('books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_books_data)

    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(all_books_data, f, ensure_ascii=False, indent=2)

    print(f"Terminé! {len(all_books_data)} livres récupérés.")
