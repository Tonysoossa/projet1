import unicodedata
import re

def clean_filename(title):
    """
    Nettoie un titre pour en faire un nom de fichier valide
    """

    # Normaliser les caractères Unicode
    title = unicodedata.normalize('NFKD', title)
    title = title.encode('ascii', 'ignore').decode('ascii')
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'[-\s]+', '-', title)
    title = title.strip('-')

    if len(title) > 50:
        title = title[:50].rstrip('-')

    if not title:
        title = "unknown"

    return title.lower()

def clean_text(text):
    """
    Nettoie le texte en supprimant les caractères parasites
    """
    if not text:
        return ""

    text = unicodedata.normalize('NFKD', text)
    replacements = {
        'Â': '',
        'â': "'",
        'Ã¢': "'",
        'Ã©': 'é',
        'Ã¨': 'è',
        'Ã ': 'à',
        'Ã§': 'ç',
        'Ã´': 'ô',
        'Ã»': 'û',
        'Ã®': 'î',
        'Ã¯': 'ï',
        'Ã«': 'ë',
        'Ã¼': 'ü',
        'Ã¶': 'ö',
        'Ã¤': 'ä',
        'Ã±': 'ñ',
        '\xa0': ' ',  # Non-breaking space
        '\u2019': "'",  # Right single quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2026': '...',  # Horizontal ellipsis
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[`´''‛]', "'", text)
    text = re.sub(r'[""„‟]', '"', text)

    return text.strip()

def clean_price(price_text):
    """
    Nettoie le texte de prix et extrait la valeur numérique
    """
    if not price_text:
        return ""

    cleaned = clean_text(price_text)

    price_match = re.search(r'[\d.]+', cleaned)
    if price_match:
        return price_match.group()

    return cleaned

def clean_description(description):
    """
    Nettoie spécifiquement les descriptions de livres
    """
    if not description:
        return ""

    cleaned = clean_text(description)
    cleaned = re.sub(r',+', ',', cleaned)
    cleaned = re.sub(r'\.{3,}', '...', cleaned)

    return cleaned.strip()
