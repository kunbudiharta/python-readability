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


response = requests.get('https://www.medcom.id/olahraga/sports-lainnya/GKdWa2dk-dua-emas-jadi-target-timnas-bridge-di-asian-games-2018?utm_source=all&utm_medium=allfeed&utm_campaign=allpartnership')

negative_keywords = [
    "sum",
    "strong",
    "credits",
    "header"
]

positive_keywords = [
    "detail",
    "page",
    "content-article"
]

unlikely_candidates = [
    "sum",
    "related",
    "baca",
    "juga",
    "video",
    "inner-link-baca-juga",
    "iframe",
    "caption"
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
    'pewarta:',
    'followinstagramkami'
]

p_exclude = readability.compile_pattern(p_exclude)

doc = readability.Document(
    response.text,
    negative_keywords=negative_keywords,
    positive_keywords=positive_keywords,
    unlikely_candidates=unlikely_candidates
)

soup = BeautifulSoup(doc.summary(), "html5lib")
content = []
all_p = []
for p in soup.select("p"):
    text_p = cleaning(p.get_text())
    if text_p.find("\n") > 0:
        all_p.extend(text_p.split("\n"))
    else:
        all_p.append(text_p)

for text_p in all_p:
    if len(text_p) > 0:
        try:
            if not p_exclude.search(text_p.lower().replace(" ", "")):
                content.append(text_p)
        except Exception:
            content.append(text_p)

content = "\n\n".join(content)
result = {
    "title": doc.title(),
    "short_title": doc.short_title(),
    "content": content,
    "content_lower": cleaning_text(content)
}
print(json.dumps(result))
