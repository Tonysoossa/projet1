#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from urllib.parse import urljoin
import re
import os
import unicodedata

def clean_filename(title):
    """Nettoie un titre pour l'utiliser comme nom de fichier"""
    title = unicodedata.normalize('NFKD', title)
    title = re.sub(r'[<>:"/\\|?*]', '_', title)
    title = re.sub(r'\s+', '_', title)
    title = title.strip('_')
    if len(title) > 50:
        title = title[:50].rstrip('_')
    return title

def scrape_book_details(book_url, book_number):
    book_response = requests.get(book_url)
    book_soup = BeautifulSoup(book_response.text, 'lxml')

    data = {}

    table_rows = book_soup.select('table tr')
    for row in table_rows:
        cells = row.select('th, td')
        if len(cells) == 2:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            data[key] = value

    title = book_soup.select('h1')[0].get_text(strip=True)

    desc_elem = book_soup.select('div#product_description + p')
    description = desc_elem[0].get_text(strip=True) if desc_elem else ''

    breadcrumb_links = book_soup.select('ul.breadcrumb a')
    category = breadcrumb_links[2].get_text(strip=True) if len(breadcrumb_links) > 2 else ''

    rating_elem = book_soup.select('p.star-rating')
    rating = 0
    if rating_elem:
        classes = rating_elem[0].get('class')
        if classes:
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            for cls in classes:
                if cls in rating_map:
                    rating = rating_map[cls]

    img_elem = book_soup.select('div.item.active img')
    image_url = ''
    if img_elem:
        image_url = urljoin(book_url, str(img_elem[0]['src']))

    local_image_path = ''
    if image_url:
        try:
            img_response = requests.get(image_url)
            clean_title = clean_filename(title)
            filename = f"{book_number:03d}_{clean_title}.jpg"
            filepath = os.path.join('images', filename)
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            local_image_path = filepath
        except:
            pass

    availability = data.get('Availability', '')
    number_available = 0
    match = re.search(r'\d+', availability)
    if match:
        number_available = int(match.group())

    return {
        'upc': data.get('UPC', ''),
        'title': title,
        'price_including_tax': data.get('Price (incl. tax)', ''),
        'price_excluding_tax': data.get('Price (excl. tax)', ''),
        'number_available': number_available,
        'product_description': description,
        'category': category,
        'review_rating': rating,
        'image_url': image_url,
        'book_url': book_url,
        'local_image_path': local_image_path
    }

def scrape_books():
    base_url = "https://books.toscrape.com/catalogue/category/books/humor_30/"
    all_books_data = []
    page = 1

    if not os.path.exists('images'):
        os.makedirs('images')

    while True:
        url = base_url + "index.html" if page == 1 else base_url + f"page-{page}.html"
        response = requests.get(url)

        if response.status_code == 404:
            break

        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.select('.product_pod')

        if not books:
            break

        for book in books:
            link = book.select('h3 > a')[0]['href']
            book_url = urljoin(url, str(link))

            book_number = len(all_books_data) + 1
            book_data = scrape_book_details(book_url, book_number)
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

if __name__ == "__main__":
    scrape_books()
