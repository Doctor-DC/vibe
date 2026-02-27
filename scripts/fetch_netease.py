#!/usr/bin/env python3
"""
Fetch album covers from NetEase Cloud Music (music.163.com) using public search endpoints.
Saves images to images/albums/ and updates data/bands.json when successful.

Use with caution: this script disables SSL verification (insecure) and may fail
if the site blocks automated requests. You allowed insecure fetching.
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
IMAGES_DIR = os.path.join(ROOT, 'images', 'albums')
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

def netease_search_albums(q):
    url = 'https://music.163.com/api/search/get/?' + urllib.parse.urlencode({'s': q, 'type': 10, 'limit': 8})
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
            return json.load(resp)
    except Exception as e:
        print('NetEase search failed for', q, e)
        return None

def netease_album_detail(aid):
    url = f'https://music.163.com/api/album/{aid}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
            return json.load(resp)
    except Exception as e:
        print('Album detail failed for', aid, e)
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

def find_best_album_match(items, target_title, artist_name):
    best = None
    best_score = 0
    for it in items:
        name = it.get('name') or it.get('album') or ''
        artists = ''
        if 'artist' in it and isinstance(it['artist'], dict):
            artists = it['artist'].get('name','')
        elif 'artists' in it and isinstance(it['artists'], list) and len(it['artists'])>0:
            artists = it['artists'][0].get('name','')
        s = score(name, target_title) + score(artists, artist_name)
        if s > best_score:
            best_score = s
            best = it
    return best, best_score

def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    bands = data.get('bands', [])
    updated = False
    total = 0
    got = 0

    for band in bands:
        artist = band.get('name')
        for album in band.get('albums', []):
            total += 1
            title = album.get('title')
            # skip if already has a non-svg image
            cur = album.get('image','')
            if cur and not cur.endswith('.svg') and os.path.splitext(cur)[1].lower() in ('.jpg','.jpeg','.png'):
                print('Skip (exists):', artist, '-', title)
                continue

            queries = [f"{artist} {title}", title, f"{title} {artist}", artist]
            found = False
            for q in queries:
                print('Searching NetEase for:', q)
                res = netease_search_albums(q)
                time.sleep(0.8)
                if not res:
                    continue
                items = None
                if 'result' in res and res['result']:
                    # some responses: result.albums or result.albums['items']
                    r = res['result']
                    if isinstance(r, dict) and 'albums' in r:
                        a = r['albums']
                        if isinstance(a, dict) and 'items' in a:
                            items = a['items']
                        elif isinstance(a, list):
                            items = a
                    elif isinstance(r, list):
                        items = r

                if not items:
                    continue

                best, sc = find_best_album_match(items, title, artist)
                if not best or sc < 0.6:
                    continue

                aid = best.get('id') or best.get('albumId')
                pic = best.get('picUrl') or best.get('picUrl')
                if not pic and aid:
                    detail = netease_album_detail(aid)
                    time.sleep(0.8)
                    if detail and 'album' in detail and 'picUrl' in detail['album']:
                        pic = detail['album']['picUrl']

                if pic:
                    ext = os.path.splitext(urllib.parse.urlparse(pic).path)[1] or '.jpg'
                    fname = f"{slugify(artist)}__{slugify(title)}{ext}"
                    dest = os.path.join(IMAGES_DIR, fname)
                    print('Downloading', pic, '→', dest)
                    if download_image(pic, dest):
                        album['image'] = os.path.join('images','albums', fname).replace('\\','/')
                        updated = True
                        got += 1
                        found = True
                        break

            if not found:
                print('No NetEase cover found for', artist, '-', title)

    if updated:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('\nUpdated', DATA_PATH)

    print(f'Finished. {got}/{total} covers downloaded or updated.')

if __name__ == '__main__':
    main()
