import requests
import readability
from bs4 import BeautifulSoup
from textacy.preprocess import preprocess_text
import json


def cleaning(text):
    text = preprocess_text(text, fix_unicode=True)
    return text


def cleaning_text(text):
    text = preprocess_text(text, no_numbers=True, fix_unicode=True, lowercase=True, no_punct=True)
    text = " ".join(text.replace("number", "").split())
    return text


response = requests.get('https://nasional.kompas.com/read/2018/08/08/14553351/maruf-amin-sambangi-istana-ada-apa')

negative_keywords = [
    "sum", "strong", "credits"
]

positive_keywords = [
    "detail", "page"
]

unlikely_candidates = [
    "sum",
    "related",
    "baca",
    "juga",
    "video",
    "inner-link-baca-juga"
]

p_exclude = [
    'saksikantayanganvideomenarikberikutini:',
    'simakvideomenarikberikutdibawah:',
    'simakjugavideoberikutini:',
    'bacaselengkapnya:',
    'bacajuga',
    'baca:',
    'videopilihan',
    'laporanwartawan',
    'editor:',
    'copyright',
    'tags',
    'sumber:',
    'penulis:',
    'pewarta:'
]

p_exclude = readability.compile_pattern(p_exclude)

doc = readability.Document(response.text,
               negative_keywords=negative_keywords,
               positive_keywords=positive_keywords,
               unlikely_candidates=unlikely_candidates
)

soup = BeautifulSoup(doc.summary(), "html5lib")
content = []

for p in soup.select("p"):
    text = cleaning(p.get_text())
    if len(text) > 0:
        try:
            if not p_exclude.search(text.lower().replace(" ", "")):
                content.append(text)
        except Exception:
            content.append(text)

content = "\n\n".join(content)
result = {
    "title": doc.title(),
    "short_title": doc.short_title(),
    "content": content,
    "content_lower": cleaning_text(content)
}
print(json.dumps(result))
