from flask import current_app

import requests

GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"


def searcher(term):
    if not term.startswith('*'):
        url = None
    else:
        term = term[1:]
        search_terms = {
            'start': 1,
            'num': 1,
            'q': ' '.join(['stock photo', term[:-1]]),
            'cx': current_app.config['GSE_CX_ID'],
            'key': current_app.config['GSE_API_KEY'],
            'searchType': 'image'
        }
        result = requests.get(GOOGLE_API_URL, params=search_terms).json()
        url = result['items'][0]['link']
    return {'term': term, 'url': url}


def storyze(title, text, author):
    lines = text.split('\n')
    lines = dict([(str(line[0]), searcher(line[1])) for line in enumerate(lines)])
    story = {'title': title, 'lines': lines, 'author': author}
    return story


def format_story(story):
    # ensure order
    try:
        title = story['title']
    except:
        title = ''
    try:
        author = story['author']
    except:
        author = ''
    lines = [(k, story['lines'][k]) for k in sorted(story['lines'].keys())]
    return {'title': title, 'lines': lines, 'author': author}
