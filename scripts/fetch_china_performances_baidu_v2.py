#!/usr/bin/env python3
"""
More aggressive Baidu-based lookup: fetch search results, extract result links,
visit top result pages, and scan content for China keywords and years.

Warning: increased request volume may trigger blocking; rate-limited sleeps included.
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
CHINA_KEYWORDS = ['中国','来华','来过中国','北京','上海','广州','深圳','大陆','香港','澳门','China','Beijing','Shanghai','Guangzhou','Shenzhen']

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20, context=CTX) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception:
        return ''

def baidu_search_html(q):
    url = 'https://www.baidu.com/s?' + urllib.parse.urlencode({'wd': q})
    return fetch(url)

def extract_result_links(html):
    # naive extraction: collect http(s) links from href attributes
    links = []
    for m in re.finditer(r'href\s*=\s*"(http[s]?://[^"<>]+)"', html):
        links.append(m.group(1))
    # also try data-tools or data-log links
    for m in re.finditer(r'data-click\s*=\s*"[^"]*?http[s]?://([^"]+)"', html):
        links.append('http://' + m.group(1))
    # dedupe and return top 8
    out = []
    for l in links:
        if l not in out:
            out.append(l)
        if len(out) >= 8:
            break
    return out

def extract_years_from_text(text):
    return sorted({m.group(0) for m in YEAR_RE.finditer(text)})

def scan_text_for_china(text):
    if not text:
        return False, []
    found = any(k in text for k in CHINA_KEYWORDS)
    years = extract_years_from_text(text) if found else []
    return found, years

def query_and_follow(name):
    # broader queries
    queries = [f"{name} 来华 演出", f"{name} 中国 巡演", f"{name} 演唱会 中国", f"{name} 中国 演出 年份", f"{name} 演出 年", f"{name} live China", f"{name} China tour"]
    found_any = False
    years = set()
    for q in queries:
        print('Search:', q)
        html = baidu_search_html(q)
        time.sleep(1.0)
        if not html:
            continue
        # scan the snippet text first
        f, ys = scan_text_for_china(html)
        if f:
            found_any = True
            years.update(ys)
        # extract result links and follow a few
        links = extract_result_links(html)
        for link in links[:6]:
            print('  follow:', link)
            page = fetch(link)
            time.sleep(0.9)
            if not page:
                continue
            f2, ys2 = scan_text_for_china(page)
            if f2:
                found_any = True
                years.update(ys2)
            # early stop if we have concrete years
            if years:
                break
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
        if b.get('played_in_china') and b.get('china_years'):
            print('Skip exists:', name)
            continue
        print('Aggressive Baidu lookup for:', name)
        found, years = query_and_follow(name)
        if found:
            b['played_in_china'] = True
            b['china_years'] = years
            updated = True
            print('  Found via Baidu v2:', years)
        else:
            b['played_in_china'] = b.get('played_in_china', False)
            b['china_years'] = b.get('china_years', [])
            print('  Not found in Baidu v2:', name)

    if updated:
        out = {'bands': bands}
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print('Updated', DATA_PATH)
    else:
        print('No updates')

if __name__ == '__main__':
    main()
