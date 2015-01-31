# coding: utf-8
from urllib.request import build_opener
import json

URL_TEMPLATE = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={0}&start=0"

def searcher(term):
    if not term.startswith('*'):
        url = None
    else:
        term = term[1:]
        search_term = ' '.join(['stock photo', term[:-1]])
        fetcher = build_opener()
        url = URL_TEMPLATE.format(search_term.replace(' ', '%20'))
        result = fetcher.open(url)
        result = json.load(result)
        try:
            url = result['responseData']['results'][0]['unescapedUrl']
        except:
            url = None
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
