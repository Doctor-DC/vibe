#!/usr/bin/env python3
"""
Fetch album covers from MusicBrainz (release-group search) and Cover Art Archive.
Updates data/bands.json image paths when a cover is downloaded.

Run from project root: python3 scripts/fetch_covers.py
"""
import json
import os
import time
import urllib.parse
import urllib.request
import ssl

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(ROOT, 'data', 'bands.json')
IMAGES_DIR = os.path.join(ROOT, 'images', 'albums')
os.makedirs(IMAGES_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'VibeSite/0.1 (contact: you@example.com)'
}

# Create an unverified SSL context to allow insecure fetching when requested.
# WARNING: this disables certificate verification and is not recommended for
# production. You allowed insecure fetch for convenience.
CTX = ssl._create_unverified_context()

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

def mb_search_release_group(artist, title):
    q = 'release:"{}" AND artist:"{}"'.format(title.replace('"','\"'), artist.replace('"','\"'))
    params = {'query': q, 'fmt': 'json', 'limit': 3}
    url = 'https://musicbrainz.org/ws/2/release-group/?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
            return json.load(resp)
    except Exception as e:
        print('MusicBrainz request failed for', artist, '-', title, e)
        return None

def get_coverart_for_rg(mbid):
    url = f'https://coverartarchive.org/release-group/{mbid}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
            return json.load(resp)
    except Exception as e:
        # print('No cover art for', mbid, e)
        return None

def download_image(url, dest_path):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as resp:
            data = resp.read()
            with open(dest_path, 'wb') as f:
                f.write(data)
        return True
    except Exception as e:
        print('Failed to download', url, e)
        return False

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
            # skip if image already points to a real image (not svg placeholder)
            img = album.get('image', '')
            if img and not img.endswith('.svg') and os.path.splitext(img)[1].lower() in ('.jpg', '.jpeg', '.png'):
                print('Skip existing image for', artist, '-', album.get('title'))
                continue

            title = album.get('title')
            print('\nSearching for:', artist, '-', title)
            res = mb_search_release_group(artist, title)
            time.sleep(1.0)
            mbid = None
            if res and 'release-groups' in res and len(res['release-groups'])>0:
                # choose first
                mbid = res['release-groups'][0].get('id')
                print('Found release-group MBID:', mbid)
            else:
                print('No release-group found for', title)
                continue

            ca = get_coverart_for_rg(mbid)
            time.sleep(1.0)
            if not ca or 'images' not in ca:
                print('No cover art found for', title)
                continue

            # choose front image
            front = None
            for im in ca['images']:
                if im.get('front'):
                    front = im
                    break
            if not front:
                front = ca['images'][0]

            img_url = front.get('image')
            if not img_url:
                print('No image URL in coverart data')
                continue

            ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1]
            if not ext:
                ext = '.jpg'
            filename = f"{slugify(artist)}__{slugify(title)}{ext}"
            dest = os.path.join(IMAGES_DIR, filename)
            print('Downloading', img_url, '→', dest)
            ok = download_image(img_url, dest)
            if ok:
                album['image'] = os.path.join('images', 'albums', filename).replace('\\','/')
                updated = True
                got += 1

    if updated:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('\nUpdated', DATA_PATH)

    print(f'Finished. {got}/{total} covers downloaded or updated.')

if __name__ == '__main__':
    main()
