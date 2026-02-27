#!/usr/bin/env python3
"""
Fetch whether bands have performed in China and which years by querying
Wikipedia (en / zh) and scanning page extracts for China-related mentions.

Writes `played_in_china` (bool) and `china_years` (list) into data/bands.json.
"""
import json
import re
import ssl
import sys
from urllib import request, parse, error

BASE_EN = 'https://en.wikipedia.org/w/api.php'
BASE_ZH = 'https://zh.wikipedia.org/w/api.php'
HEADERS = {'User-Agent': 'vibe-fetcher/1.0 (contact: local)'}

def urlopen_json(url, data=None, ctx=None):
    req = request.Request(url, headers=HEADERS)
    try:
        with request.urlopen(req, context=ctx, timeout=20) as resp:
            return json.load(resp)
    except Exception as e:
        raise

def search_wikipedia(api_base, query):
    params = {'action': 'query', 'list': 'search', 'srsearch': query, 'format': 'json'}
    url = api_base + '?' + parse.urlencode(params)
    try:
        return urlopen_json(url)
    except Exception:
        # retry with unverified SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return urlopen_json(url, ctx=ctx)

def fetch_extract(api_base, title):
    params = {'action': 'query', 'prop': 'extracts', 'explaintext': 1, 'titles': title, 'format': 'json'}
    url = api_base + '?' + parse.urlencode(params)
    try:
        return urlopen_json(url)
    except Exception:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return urlopen_json(url, ctx=ctx)

YEAR_RE = re.compile(r'\b(19|20)\d{2}\b')
CHINA_KEYWORDS = ['China', 'Chinese', 'PRC', 'Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen',
                  '中国', '来华', '来过中国', '北京', '上海', '广州', '深圳']

def extract_years_from_text(text):
    years = set()
    # split into sentences by common terminators
    parts = re.split(r'[\.\!?。！？\n]', text)
    for p in parts:
        if any(k in p for k in CHINA_KEYWORDS):
            for m in YEAR_RE.findall(p):
                # m is prefix in this regex; rebuild full match via search
                for full in YEAR_RE.finditer(p):
                    years.add(full.group(0))
    return sorted(years)

def find_on_wikipedia(name):
    # try English first
    try:
        res = search_wikipedia(BASE_EN, name)
        hits = res.get('query', {}).get('search', [])
        if hits:
            title = hits[0]['title']
            ex = fetch_extract(BASE_EN, title)
            pages = ex.get('query', {}).get('pages', {})
            for p in pages.values():
                text = p.get('extract', '')
                years = extract_years_from_text(text)
                found = any(k in text for k in CHINA_KEYWORDS)
                return found, years
    except Exception:
        pass

    # try Chinese wiki
    try:
        res = search_wikipedia(BASE_ZH, name)
        hits = res.get('query', {}).get('search', [])
        if hits:
            title = hits[0]['title']
            ex = fetch_extract(BASE_ZH, title)
            pages = ex.get('query', {}).get('pages', {})
            for p in pages.values():
                text = p.get('extract', '')
                years = extract_years_from_text(text)
                found = any(k in text for k in CHINA_KEYWORDS)
                return found, years
    except Exception:
        pass

    return False, []

def main():
    DATA = 'data/bands.json'
    try:
        with open(DATA, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print('Cannot read', DATA, e)
        sys.exit(1)

    # support both { "bands": [...] } and [...]
    if isinstance(data, dict) and 'bands' in data:
        bands = data['bands']
        out_as_object = True
    else:
        bands = data
        out_as_object = False

    updated = 0
    for b in bands:
        name = b.get('name')
        # skip if already has a non-empty result
        if b.get('played_in_china') and b.get('china_years'):
            print('Skip exists:', name)
            continue
        print('Searching:', name)
        found, years = find_on_wikipedia(name)
        if found:
            b['played_in_china'] = True
            b['china_years'] = years
            print(' Found China mentions, years:', years)
        else:
            b['played_in_china'] = False
            b['china_years'] = []
            print(' No China mentions found')
        updated += 1

    # write back as an object with 'bands' to match frontend expectations
    out = {'bands': bands}
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('Finished. Updated entries:', updated)

if __name__ == '__main__':
    main()
