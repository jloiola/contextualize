# coding: utf8
import os

import hug
from hug_middleware_cors import CORSMiddleware

import spacy

# https://marshmallow.readthedocs.io/en/3.0/
# http://www.hug.rest/website/learn
nlp = spacy.load('en_core_web_sm')

@hug.get('/')
def ok():
    return {'ok': True}

@hug.get('/entities')
def entities(text: str):
    doc = nlp(text)
    return [{'text': ent.text, 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_}
            for ent in doc.ents]

if __name__ == '__main__':
    import waitress
    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=os.getenv('PORT', 8000))
