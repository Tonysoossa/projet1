import csv
import json

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
