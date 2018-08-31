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
    return [{'text': ent.text, 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_}
            for ent in doc.ents]

if __name__ == '__main__':
    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=os.getenv('PORT', 8000))
