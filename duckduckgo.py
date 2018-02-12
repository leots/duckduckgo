import time

import requests
from lxml import html


def search(keywords, max_results=None):
    url = 'https://duckduckgo.com/html/'
    params = {
        'q': keywords,
        's': '0',
    }

    yielded = 0
    while True:
        res = requests.post(url, data=params)
        doc = html.fromstring(res.text)
        if 'If this error persists, please let us know' in doc.text_content():
            time.sleep(20)
            continue

        results = [(a.text_content(), a.get('href'))
                   for a in doc.cssselect('.result__a')]
        for result in results:
            yield result
            time.sleep(0.1)
            yielded += 1
            if max_results and yielded >= max_results:
                return

        try:
            form = doc.cssselect('.nav-link form')[-1]
        except IndexError:
            return
        params = dict(form.fields)
