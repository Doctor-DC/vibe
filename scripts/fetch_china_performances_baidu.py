#!/usr/bin/env python3
"""
Search Baidu for band performance evidence in China and extract years.

Notes:
- This performs simple HTML fetching and text scanning; it's not using an API.
- It uses an unverified SSL context like other scripts.
"""
import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(ROOT, 'data', 'bands.json')
CTX = ssl._create_unverified_context()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
}

YEAR_RE = re.compile(r'\b(19|20)\d{2}\b')
CHINA_KEYWORDS = ['中国','来华','来过中国','北京','上海','广州','深圳','大陆','香港','澳门']

def fetch_baidu(query):
    url = 'https://www.baidu.com/s?' + urllib.parse.urlencode({'wd': query})
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print('Fetch failed for', query, e)
        return ''

def extract_context_years(html):
    # search for China keywords and collect nearby years
    years = set()
    for kw in CHINA_KEYWORDS:
        for m in re.finditer(re.escape(kw), html):
            start = max(0, m.start() - 200)
            end = min(len(html), m.end() + 200)
            snippet = html[start:end]
            for y in YEAR_RE.findall(snippet):
                # YEAR_RE uses group, so finditer to get full match
                pass
            for full in YEAR_RE.finditer(snippet):
                years.add(full.group(0))
    return sorted(years)

def scan_band(name):
    queries = [f"{name} 来华 演出", f"{name} 中国 演出", f"{name} 演出 年", f"{name} live China", name]
    found_any = False
    years = set()
    for q in queries:
        print('Baidu search:', q)
        html = fetch_baidu(q)
        time.sleep(1.0)
        if not html:
            continue
        if any(kw in html for kw in CHINA_KEYWORDS):
            found_any = True
            ys = extract_context_years(html)
            years.update(ys)
        # also check snippets like '演出时间' '巡演' nearby
        if '巡演' in html or '演出' in html:
            if any(kw in html for kw in CHINA_KEYWORDS):
                found_any = True
                ys = extract_context_years(html)
                years.update(ys)
        # small early exit if we already found years
        if years:
            break
    return found_any, sorted(years)

def main():
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            doc = json.load(f)
    except Exception as e:
        print('Cannot read', DATA_PATH, e)
        sys.exit(1)

    bands = doc.get('bands') if isinstance(doc, dict) and 'bands' in doc else doc
    updated = False
    for b in bands:
        name = b.get('name')
        if not name:
            continue
        # skip if already has years
        if b.get('played_in_china') and b.get('china_years'):
            print('Skip exists:', name)
            continue

        found, years = scan_band(name)
        if found:
            b['played_in_china'] = True
            b['china_years'] = years
            updated = True
            print(' Found via Baidu:', name, years)
        else:
            b['played_in_china'] = b.get('played_in_china', False)
            b['china_years'] = b.get('china_years', [])
            print(' Not found via Baidu:', name)

    out = {'bands': bands}
    if updated:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print('Updated', DATA_PATH)
    else:
        print('No updates made')

if __name__ == '__main__':
    main()
