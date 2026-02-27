#!/usr/bin/env python3
"""
Query NetEase Cloud Music for artist descriptions to find China performance mentions/years.

Writes results into `data/bands.json` (preserves existing played_in_china if present).
"""
import json
import os
import re
import time
import ssl
import sys
import urllib.parse
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(ROOT, 'data', 'bands.json')
CTX = ssl._create_unverified_context()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
    'Referer': 'https://music.163.com'
}

YEAR_RE = re.compile(r'\b(19|20)\d{2}\b')
CHINA_KEYWORDS = ['中国','来华','北京','上海','广州','深圳','大陆','香港','澳门','China','Beijing','Shanghai','Guangzhou','Shenzhen']

def netease_search_artist(q):
    url = 'https://music.163.com/api/search/get/?' + urllib.parse.urlencode({'s': q, 'type': 100, 'limit': 8})
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
            return json.load(resp)
    except Exception as e:
        print('NetEase artist search failed for', q, e)
        return None

def netease_artist_desc(aid):
    url = f'https://music.163.com/api/artist/desc?id={aid}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
            data = resp.read()
            try:
                return json.loads(data)
            except Exception:
                # return raw text when JSON parsing fails
                return data.decode('utf-8', errors='ignore')
    except Exception as e:
        print('Artist desc failed for', aid, e)
        return None

def extract_years(text):
    return sorted({m.group(0) for m in YEAR_RE.finditer(text)})

def scan_text_for_china(text):
    if not text:
        return False, []
    found = any(k in text for k in CHINA_KEYWORDS)
    years = extract_years(text) if found else []
    return found, years

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
        # skip if already true with years
        if b.get('played_in_china') and b.get('china_years'):
            print('Skip exists:', name)
            continue

        print('NetEase lookup:', name)
        res = netease_search_artist(name)
        time.sleep(0.7)
        if not res or 'result' not in res:
            print(' No netease result for', name)
            b.setdefault('played_in_china', False)
            b.setdefault('china_years', [])
            continue

        # unpack possible artist items
        items = None
        r = res['result']
        if isinstance(r, dict) and 'artists' in r:
            a = r['artists']
            if isinstance(a, dict) and 'items' in a:
                items = a['items']
            elif isinstance(a, list):
                items = a
        elif isinstance(r, list):
            items = r

        if not items:
            print(' No artist items for', name)
            b.setdefault('played_in_china', False)
            b.setdefault('china_years', [])
            continue

        # pick best match by simple name inclusion / length
        best = None
        for it in items:
            title = it.get('name','')
            if title.lower() == name.lower():
                best = it
                break
        if not best:
            best = items[0]

        aid = best.get('id')
        if not aid:
            print(' No artist id for', name)
            b.setdefault('played_in_china', False)
            b.setdefault('china_years', [])
            continue

        desc = netease_artist_desc(aid)
        time.sleep(0.6)
        text = ''
        if desc and isinstance(desc, dict):
            # various fields might contain description
            if 'briefDesc' in desc and desc['briefDesc']:
                text += '\n' + desc['briefDesc']
            # some responses include 'introduction' or 'artist'->'briefDesc'
            if 'introduction' in desc:
                if isinstance(desc['introduction'], list):
                    for p in desc['introduction']:
                        text += '\n' + (p.get('txt') or '')
                else:
                    text += '\n' + str(desc.get('introduction',''))
            # fallback: entire json string
            if not text:
                text = json.dumps(desc, ensure_ascii=False)

        found, years = scan_text_for_china(text)
        if found:
            b['played_in_china'] = True
            b['china_years'] = years
            updated = True
            print('  Found:', years)
        else:
            b['played_in_china'] = b.get('played_in_china', False)
            b['china_years'] = b.get('china_years', [])
            print('  Not found')

    # write back preserving object wrapper
    out = {'bands': bands}
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('Done. Updated file:', DATA_PATH)

if __name__ == '__main__':
    main()
