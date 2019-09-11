from flask import Flask, jsonify
import requests

import time
import json

app = Flask(__name__)








def normalize_github(url, category):
    """
    Takes in a ClientSession and a URL string to GitHub.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = requests.get(url).json()
    print('url done', url)
    entries = response['items']
    normalized_entries = []

    for entry in entries:
        normalized_entries.append({
            'source': 'github',
            'category': category,
            'title': entry['name'],
            'link': entry['html_url'],
            'desc': entry['description'],
            'stars': entry['stargazers_count']
        })
  
    return normalized_entries


# ======
# ROUTES
# ======

@app.route('/')
def main():
    start_time = time.perf_counter()
    entries = []

    entries.append(normalize_github('https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc', 'popular'))
    entries.append(normalize_github('https://api.github.com/search/repositories?q=language:python&sort=updated&order=desc', 'updated'))
    # entries.append(normalize_reddit_webdev('https://www.reddit.com/r/webdev/.json?', 'webdev'))
    # entries.append(normalize_reddit_programmerhumor('https://www.reddit.com/r/programmerhumor/.json?', 'programmerhumor'))
    # entries.append(normalize_reddit_no_image('https://www.reddit.com/r/python/.json?', 'python'))
    # entries.append(normalize_reddit_no_image('https://www.reddit.com/r/learnprogramming/.json?', 'learnprogramming'))
    # entries.append(normalize_pypi('https://pypi.org/rss/updates.xml', 'updated'))
    # entries.append(normalize_pypi('https://pypi.org/rss/packages.xml', 'newest'))

    elapsed_time = time.perf_counter() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f}')
    
    return jsonify(entries)