import sys
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
    prev_waiting_time = 20
    while True:
        res = requests.post(url, data=params)
        doc = html.fromstring(res.text)
        if 'If this error persists, please let us know' in doc.text_content():
            # Count a failure
            time_to_w8 = min(prev_waiting_time, 600)
            prev_waiting_time *= 2
            print(
                "> DuckDuckGo error, waiting " + str(time_to_w8) + " seconds!",
                file=sys.stderr)

            # Wait
            time.sleep(time_to_w8)
            continue

        # Reset waiting time
        prev_waiting_time = 20

        # Get results
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
