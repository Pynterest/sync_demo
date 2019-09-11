from flask import Flask, jsonify
import requests
import feedparser

import time
import json

app = Flask(__name__)


def normalize_reddit_webdev(url, category):
    """
    Takes in a URL string to WebDev Subreddit.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    headers = {
        'User-Agent': 'Heroku:42:1.0.0 (by /u/sburger)'
    }
    print('url start', url)
    response = requests.get(url, headers=headers).json()
    print('url done', url)
    
    entries = response['data']['children']
    normalized_entries = {
        'source': 'reddit',
        'category': category,
        'data':[]
    }

    for entry in entries:
        normalized_entries['data'].append({
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
            #some results have thumbnail urls
            'thumbnail': entry['data'].get('thumbnail', None),
        })

    return normalized_entries


def normalize_reddit_programmerhumor(url, category):
    """
    Takes in a URL string to Programmer Humor Subreddit.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    headers = {
        'User-Agent': 'Heroku:42:1.0.0 (by /u/sburger)'
    }
    print('url start', url)
    response = requests.get(url, headers=headers).json()
    print('url done', url)

    entries = response['data']['children']
    normalized_entries = {
        'source': 'reddit',
        'category': category,
        'data':[]
    }

    for entry in entries:

        normalized_entries['data'].append({
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
            'image': entry['data'].get('url', None),
        })

    return normalized_entries


def normalize_reddit_no_image(url, category):
    """
    Takes in a URL string to Python Subreddit and a category string.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    headers = {
        'User-Agent': 'Heroku:42:1.0.0 (by /u/sburger)'
    }
    print('url start', url)
    response = requests.get(url, headers=headers).json()
    print('url done', url)

    entries = response['data']['children']
    normalized_entries = {
        'source': 'reddit',
        'category': category,
        'data':[]
    }

    for entry in entries:
        normalized_entries['data'].append({
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
        })

    return normalized_entries


def normalize_pypi(url, category):
    """
    Takes in a URL string to PyPI and a category string.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    r = requests.get(url)
    feed_data = feedparser.parse(r.content)
    print('url done', url)
    entries = feed_data.entries
    
    normalized_entries = {
        'source': 'pypi',
        'category': category,
        'data':[]
    }

    for entry in entries:
        normalized_entries['data'].append({
            'title': entry['title'],
            'link': entry['link'],
            'desc': entry['summary']
        })

    return normalized_entries


def normalize_github(url, category):
    """
    Takes in a URL string to GitHub and a category string.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = requests.get(url).json()
    print('url done', url)
    entries = response['items']
    
    normalized_entries = {
        'source': 'github',
        'category': category,
        'data':[]
    }

    for entry in entries:
        normalized_entries['data'].append({
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
    entries.append(normalize_reddit_programmerhumor('https://www.reddit.com/r/programmerhumor/.json?', 'programmerhumor'))
    entries.append(normalize_reddit_no_image('https://www.reddit.com/r/python/.json?', 'python'))
    entries.append(normalize_reddit_no_image('https://www.reddit.com/r/learnprogramming/.json?', 'learnprogramming'))
    entries.append(normalize_pypi('https://pypi.org/rss/updates.xml', 'updated'))
    entries.append(normalize_pypi('https://pypi.org/rss/packages.xml', 'newest'))

    elapsed_time = time.perf_counter() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f}')
    
    return jsonify(entries)