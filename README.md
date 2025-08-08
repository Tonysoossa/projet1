# Scraper de Livres - Books.toscrape.com

Ce projet permet de scraper automatiquement des livres par catégorie disponibles sur le site [books.toscrape.com](https://books.toscrape.com).

## Fonctionnalités

- Récupération automatique de toutes les catégories
- Scraping complet de tous les livres de chaque catégorie
- Téléchargement des images avec noms de fichiers propres
- Nettoyage des caractères parasites dans les textes
- Export des données en CSV et JSON
- Gestion des erreurs et reprise automatique

## Prérequis

- Python 3.7+
- Les dépendances listées dans `requirements.txt`

## Installation

1. **Cloner le projet** (ou télécharger les fichiers)

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

### Scraping complet (recommandé)

Pour scraper **tous les livres de toutes les catégories** :

```bash
python main.py
```

Le programme va :
- Récupérer toutes les catégories disponibles
- Scraper tous les livres de chaque catégorie
- Télécharger toutes les images
- Sauvegarder les données en CSV et JSON

 **Attention** : Le scraping complet peut prendre plusieurs heures !


## Structure du projet

```
projet1/
├── main.py                 # Script principal
├── scrape_books.py         # Logique de scraping des catégories
├── scrape_book_details.py  # Scraping des détails de chaque livre
├── character_cleaner.py    # Nettoyage des caractères parasites
├── requirements.txt        # Dépendances Python
├── images/                 # Dossier des images téléchargées
├── all_books.csv          # Données en format CSV
└── all_books.json         # Données en format JSON
└── save_data.py            # Sauvegarde des données
```

## Données récupérées

Pour chaque livre, le scraper récupère :

| Champ | Description |
|-------|-------------|
| `number` | Numéro séquentiel du livre |
| `upc` | Code UPC unique |
| `title` | Titre du livre (nettoyé) |
| `price_including_tax` | Prix TTC |
| `price_excluding_tax` | Prix HT |
| `number_available` | Nombre d'exemplaires disponibles |
| `product_description` | Description du livre (nettoyée) |
| `category` | Catégorie du livre |
| `review_rating` | Note sur 5 étoiles |
| `image_url` | URL de l'image originale |
| `book_url` | URL de la page du livre |
| `local_image_path` | Chemin de l'image téléchargée |

## Images

Les images sont automatiquement :
- Téléchargées dans le dossier `images/`
- Nommées avec le format : `XXX_titre-nettoyer.jpg`
- Nettoyées des caractères spéciaux dans le nom

## Nettoyage des données

Le module `character_cleaner.py` nettoie automatiquement :
- Les caractères Unicode problématiques
- Les caractères de contrôle
- Les espaces multiples
- Les caractères spéciaux dans les noms de fichiers

### Erreur de dépendances
```bash
# Réinstallez les dépendances
pip install -r requirements.txt --force-reinstall
```

### Dossier images manquant
Le dossier `images/` est créé automatiquement, mais vous pouvez le créer manuellement :
```bash
mkdir images
```
