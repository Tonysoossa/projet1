import os
import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from urllib.parse import urljoin
import scrape_book_details as sbd

def get_all_categories():
    """
    Récupère toutes les catégories disponibles sur le site books.toscrape.com
    """
    base_url = "https://books.toscrape.com/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'lxml')

    categories = {}

    category_links = soup.select('div.side_categories ul li ul li a')

    for link in category_links:
        category_name = link.get_text(strip=True)
        category_url = urljoin(base_url, str(link['href']))
        categories[category_name] = category_url

    return categories

def scrape_category_books(category_name, category_url, global_book_counter):
    """
    Scrape tous les livres d'une catégorie donnée
    """
    print(f"\nScraping de la catégorie: {category_name}")
    print(f"URL: {category_url}")

    all_books_data = []
    page = 1

    while True:
        if page == 1:
            url = category_url
        else:
            url = category_url.replace('index.html', f'page-{page}.html')

        print(f"Page {page}...")
        response = requests.get(url)

        if response.status_code == 404:
            print(f"Fin de la catégorie {category_name} (page {page-1})")
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.select('.product_pod')

        if not books:
            print(f"Fin de la catégorie {category_name} (aucun livre sur la page {page})")
            continue

        for book in books:
            try:
                link = book.select('h3 > a')[0]['href']
                book_url = urljoin(url, str(link))

                book_data = sbd.scrape_book_details(book_url, global_book_counter[0])
                book_data['number'] = global_book_counter[0]
                book_data['category'] = category_name  # Forcer la catégorie

                all_books_data.append(book_data)
                print(f"[{global_book_counter[0]:03d}] {book_data['title']}")
                global_book_counter[0] += 1

                time.sleep(0.2)

            except Exception as e:
                print(f"❌ Erreur lors du scraping d'un livre: {e}")
                continue

        page += 1

    return all_books_data

def scrape_all_categories():
    """
    Fonction principale qui scrape toutes les catégories
    """
    if not os.path.exists('images'):
        os.makedirs('images')
        print("📁 Dossier 'images' créé")

    print("📋 Récupération de la liste des catégories...")
    categories = get_all_categories()

    if not categories:
        print("❌ Aucune catégorie trouvée!")
        return

    print(f"📊 {len(categories)} catégories trouvées:")
    for i, category_name in enumerate(categories.keys(), 1):
        print(f"  {i:2d}. {category_name}")

    all_books_data = []
    global_book_counter = [1]

    for i, (category_name, category_url) in enumerate(categories.items(), 1):
        print(f"\n{'='*60}")
        print(f"Catégorie {i}/{len(categories)}: {category_name}")
        print(f"{'='*60}")

        try:
            category_books = scrape_category_books(category_name, category_url, global_book_counter)
            all_books_data.extend(category_books)

            print(f"Catégorie '{category_name}' terminée: {len(category_books)} livres")

        except Exception as e:
            print(f"❌ Erreur lors du scraping de la catégorie '{category_name}': {e}")
            continue

        time.sleep(0.5)

    save_data(all_books_data)

    print("\n SCRAPING TERMINÉ!")
    print(f"Total: {len(all_books_data)} livres récupérés")

def save_data(all_books_data):
    """
    Sauvegarde les données dans des fichiers CSV et JSON
    """
    if not all_books_data:
        print("Aucune donnée à sauvegarder")
        return

    fieldnames = ['number', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                  'number_available', 'product_description', 'category', 'review_rating',
                  'image_url', 'book_url', 'local_image_path']

    print("💾 Sauvegarde en CSV...")
    with open('all_books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_books_data)

    print("💾 Sauvegarde en JSON...")
    with open('all_books.json', 'w', encoding='utf-8') as f:
        json.dump(all_books_data, f, ensure_ascii=False, indent=2)

    print("Données sauvegardées dans 'all_books.csv' et 'all_books.json'")
