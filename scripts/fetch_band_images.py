#!/usr/bin/env python3
"""
Fetch band images from NetEase Cloud Music and update data/bands.json.

Usage: python3 scripts/fetch_band_images.py
"""
import json
import os
import time
import urllib.parse
import urllib.request
import ssl
from difflib import SequenceMatcher

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(ROOT, 'data', 'bands.json')
IMAGES_DIR = os.path.join(ROOT, 'images', 'bands')
os.makedirs(IMAGES_DIR, exist_ok=True)

CTX = ssl._create_unverified_context()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
    'Referer': 'https://music.163.com'
}

def slugify(s):
    s = s.lower()
    keep = []
    for c in s:
        if c.isalnum():
            keep.append(c)
        elif c.isspace() or c in ('-','_'):
            keep.append('-')
    out = ''.join(keep)
    out = out.replace('--','-')
    return out.strip('-')

def score(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def netease_search_artist(q):
    url = 'https://music.163.com/api/search/get/?' + urllib.parse.urlencode({'s': q, 'type': 100, 'limit': 8})
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
            return json.load(resp)
    except Exception as e:
        print('NetEase artist search failed for', q, e)
        return None

def download_image(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            data = r.read()
            with open(dest, 'wb') as f:
                f.write(data)
        return True
    except Exception as e:
        print('Download failed:', url, e)
        return False

def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    bands = data.get('bands', [])
    updated = False
    got = 0

    for band in bands:
        name = band.get('name')
        cur = band.get('image','')
        # skip if already a jpg/png
        if cur and cur.lower().endswith(('.jpg','.jpeg','.png')):
            print('Skip exists:', name)
            continue

        print('Searching NetEase artist for:', name)
        res = netease_search_artist(name)
        time.sleep(0.8)
        if not res or 'result' not in res:
            print('No result for', name)
            continue

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
            print('No artists list for', name)
            continue

        # find best match
        best = None
        best_score = 0
        for it in items:
            title = it.get('name','')
            s = score(title, name)
            if s > best_score:
                best_score = s
                best = it

        if not best or best_score < 0.5:
            print('No good artist match for', name)
            continue

        pic = best.get('picUrl') or (best.get('img1v1Url') if 'img1v1Url' in best else None)
        if not pic:
            print('No picUrl for', name)
            continue

        ext = os.path.splitext(urllib.parse.urlparse(pic).path)[1] or '.jpg'
        fname = f"{slugify(name)}{ext}"
        dest = os.path.join(IMAGES_DIR, fname)
        print('Downloading', pic, '→', dest)
        if download_image(pic, dest):
            band['image'] = os.path.join('images','bands', fname).replace('\\','/')
            updated = True
            got += 1

    if updated:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('\nUpdated', DATA_PATH)

    print('Finished. Downloaded or updated band images:', got)

if __name__ == '__main__':
    main()
