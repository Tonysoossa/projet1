# Books Scraper Project

A Python web scraping project that extracts book information from the humor category of [Books to Scrape](https://books.toscrape.com/catalogue/category/books/humor_30/).

## Features

- Scrapes all books from the humor category across multiple pages
- Extracts comprehensive book details including:
  - UPC, title, prices (with and without tax)
  - Product description and category
  - Star rating and availability count
  - Book URL and image URL
- Downloads book cover images locally
- Exports data to both CSV and JSON formats
- Automatic pagination handling
- Clean filename generation for images that match the book title

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd projet1
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scraper to extract all humor books:
```bash
python3 main.py
```

The script will:
- Create an `images/` directory for book covers
- Scrape all pages in the humor category
- Download cover images with numbered filenames
- Generate `books.csv` and `books.json` files with all book data
- Display progress as it processes each book

### Sample Output
```
✓ The Long Haul (Diary of a Wimpy Kid #9)
✓ Old School (Diary of a Wimpy Kid #10)
✓ I Know What I'm Doing -- and Other Lies I Tell Myself
...
Terminé! 10 livres récupérés.
```

## Output Files

- `books.csv` - Spreadsheet format with all book data
- `books.json` - JSON format with all book data
- `images/` - Directory containing downloaded book cover images (numbered with cleaned titles)

## Data Fields

Each book record includes:
- `number` - Sequential book number
- `upc` - Universal Product Code
- `title` - Book title
- `price_including_tax` - Price with tax
- `price_excluding_tax` - Price without tax
- `number_available` - Stock availability count
- `product_description` - Book description
- `category` - Book category (Humor)
- `review_rating` - Star rating (1-5)
- `image_url` - Original image URL
- `book_url` - Book detail page URL
- `local_image_path` - Path to downloaded image

## Dependencies

- `requests` - For making HTTP requests
- `beautifulsoup4` - For HTML parsing
- `lxml` - Fast XML/HTML parser

## Notes

- The scraper includes a 0.5-second delay between requests to be respectful to the server
- Images are automatically downloaded and stored with cleaned filenames
- The script handles pagination automatically until all pages are scraped
- Generated files (`books.csv`, `books.json`, `images/`) are ignored by git
- This project scrapes from the humor category but you can simply change the url to any category you want.
