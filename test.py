import requests
from readability import Document
from bs4 import BeautifulSoup


def cleaning(text):
    text = text.replace("\n", "").replace("\r", "").replace("\t", "").strip()
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


doc = Document(response.text,
               negative_keywords=negative_keywords,
               positive_keywords=positive_keywords,
               unlikely_candidates=unlikely_candidates
)

soup = BeautifulSoup(doc.summary(), "html5lib")
content = []

for p in soup.select("p"):
    content.append(cleaning(p.get_text()))

print(content)