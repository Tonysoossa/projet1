import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import character_cleaner as cc

def extract_table_data(soup):
    """Extract data from the book details table"""
    data = {}
    table_rows = soup.select('table tr')
    for row in table_rows:
        cells = row.select('th, td')
        if len(cells) == 2:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            data[key] = value
    return data

def extract_rating(soup):
    rating_elem = soup.select('p.star-rating')
    if not rating_elem:
        return 0

    classes = rating_elem[0].get('class')
    if not classes:
        return 0

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    for cls in classes:
        if cls in rating_map:
            return rating_map[cls]
    return 0

def extract_image_url(soup, book_url):
    img_elem = soup.select('div.item.active img')
    if not img_elem:
        return ""

    src_attr = img_elem[0].get('src')
    if not src_attr:
        return ""

    return urljoin(book_url, str(src_attr))

def download_image(image_url, title, book_number):
    if not image_url:
        return ""

    try:
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        clean_title = cc.clean_filename(title)
        filename = f"{book_number:03d}_{clean_title}.jpg"
        filepath = os.path.join('images', filename)

        os.makedirs('images', exist_ok=True)

        with open(filepath, 'wb') as f:
            f.write(img_response.content)
        return filepath

    except Exception as img_error:
        print(f"Erreur lors du téléchargement de l'image: {img_error}")
        return ""

def extract_availability_count(availability_text):
    if not availability_text:
        return 0

    match = re.search(r'(\d+)', availability_text)
    return int(match.group(1)) if match else 0

def scrape_book_details(book_url, book_number):
    """
    Scrape les détails d'un livre à partir de son URL
    """
    try:
        book_response = requests.get(book_url)
        book_response.raise_for_status()
        book_soup = BeautifulSoup(book_response.text, 'lxml')

        # Extract table data
        data = extract_table_data(book_soup)

        # Extract title
        title_elem = book_soup.select('h1')
        title = cc.clean_text(title_elem[0].get_text(strip=True)) if title_elem else "Titre inconnu"

        # Extract description
        desc_elem = book_soup.select('div#product_description + p')
        description = ""
        if desc_elem:
            description = cc.clean_description(desc_elem[0].get_text(strip=True))

        # Extract category from breadcrumb
        breadcrumb_links = book_soup.select('ul.breadcrumb a')
        category = ""
        if len(breadcrumb_links) > 2:
            category = cc.clean_text(breadcrumb_links[2].get_text(strip=True))

        rating = extract_rating(book_soup)

        image_url = extract_image_url(book_soup, book_url)
        local_image_path = download_image(image_url, title, book_number)

        availability = data.get('Availability', '')
        number_available = extract_availability_count(availability)

        price_incl = cc.clean_price(data.get('Price (incl. tax)', ''))
        price_excl = cc.clean_price(data.get('Price (excl. tax)', ''))

        # Return structured data
        return {
            'upc': cc.clean_text(data.get('UPC', '')),
            'title': title,
            'price_including_tax': price_incl,
            'price_excluding_tax': price_excl,
            'number_available': number_available,
            'product_description': description,
            'category': category,
            'review_rating': rating,
            'image_url': image_url,
            'book_url': book_url,
            'local_image_path': local_image_path
        }

    except Exception as e:
        print(f"❌ Erreur lors du scraping du livre {book_url}: {e}")
        return {
            'upc': '',
            'title': f'Erreur livre #{book_number}',
            'price_including_tax': '',
            'price_excluding_tax': '',
            'number_available': 0,
            'product_description': '',
            'category': '',
            'review_rating': 0,
            'image_url': '',
            'book_url': book_url,
            'local_image_path': ''
        }
