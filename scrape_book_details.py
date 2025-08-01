import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import character_cleaner as cc

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

    title = cc.clean_text(book_soup.select('h1')[0].get_text(strip=True))

    desc_elem = book_soup.select('div#product_description + p')
    description = desc_elem[0].get_text(strip=True) if desc_elem else ''
    description = cc.clean_text(description.replace(',', '').strip())

    breadcrumb_links = book_soup.select('ul.breadcrumb a')
    category = cc.clean_text(breadcrumb_links[2].get_text(strip=True)) if len(breadcrumb_links) > 2 else ''

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
            clean_title = cc.clean_filename(title)
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
        'price_including_tax': cc.clean_text(data.get('Price (incl. tax)', '')),
        'price_excluding_tax': cc.clean_text(data.get('Price (excl. tax)', '')),
        'number_available': number_available,
        'product_description': description,
        'category': category,
        'review_rating': rating,
        'image_url': image_url,
        'book_url': book_url,
        'local_image_path': local_image_path
    }
