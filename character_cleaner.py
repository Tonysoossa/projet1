import unicodedata
import re

def clean_filename(title):
    title = unicodedata.normalize('NFKD', title)
    title = re.sub(r'\s+', '-', title)
    title = title.strip('-')
    if len(title) > 30:
        title = title[:30].rstrip('-')
    return title

def clean_text(text):
    if not text:
        return text

    cleaned = text.replace('Â', '')
    cleaned = cleaned.replace('â', "'")

    return cleaned.strip()
