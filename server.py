# coding: utf8
import os
import logging

import hug
import waitress
from hug_middleware_cors import CORSMiddleware

import spacy

# https://marshmallow.readthedocs.io/en/3.0/
# http://www.hug.rest/website/learn

import en_core_web_sm
nlp = en_core_web_sm.load()

# quick 'can i do this'...
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

# not everyone is semantic but instead div.paragraph ... wooo
def tag_visible(element):
    return element.parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'article', 'b', 'a']

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

logging.basicConfig()

log = logging.getLogger('waitress')
log.setLevel(logging.DEBUG)

@hug.get('/')
def ok():
    log.debug('asdasdasd')
    return {'ok': True}

@hug.post('/entities')
def entities(text: str):
    doc = nlp(text)
    return [{'text': ent.text.strip(), 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_}
            for ent in doc.ents]

@hug.get('/entities')
def entities(url: str):
    html = urllib.request.urlopen(url).read()
    text = text_from_html(html)
    doc = nlp(text)
    return [{'text': ent.text.strip(), 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_}
            for ent in list(doc.ents) if ent.label_ in ['ORG', 'PERSON']]

if __name__ == '__main__':
    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=os.getenv('PORT', 8000))
