#!/usr/bin/env python3
"""
Scan `images/albums/` for image files named like `artist__title.ext` and update
`data/bands.json` album `image` fields to point to these files.
"""
import os
import json
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(ROOT, 'data', 'bands.json')
IMAGES_DIR = os.path.join(ROOT, 'images', 'albums')

def load_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(d):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def parse_filename(fname):
    # expected: artist__title.ext
    name = os.path.splitext(fname)[0]
    if '__' not in name:
        return None, None
    artist, title = name.split('__', 1)
    artist = artist.replace('-', ' ').strip()
    title = title.replace('-', ' ').strip()
    return artist, title

def normalize(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def main():
    data = load_data()
    files = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR,f))]
    mapping = {}
    for f in files:
        artist, title = parse_filename(f)
        if not artist:
            continue
        key = (normalize(artist), normalize(title))
        existing = mapping.get(key)
        # prefer non-SVG (jpg/png) over svg if both exist
        ext = os.path.splitext(f)[1].lower()
        if existing:
            extext = os.path.splitext(existing)[1].lower()
            if extext == '.svg' and ext in ('.jpg', '.jpeg', '.png'):
                mapping[key] = os.path.join('images','albums', f).replace('\\','/')
        else:
            mapping[key] = os.path.join('images','albums', f).replace('\\','/')

    updated = False
    for band in data.get('bands', []):
        a_norm = normalize(band.get('name',''))
        for album in band.get('albums', []):
            t_norm = normalize(album.get('title',''))
            key = (a_norm, t_norm)
            if key in mapping:
                newpath = mapping[key]
                if album.get('image') != newpath:
                    print('Updating', band.get('name'), '-', album.get('title'), '→', newpath)
                    album['image'] = newpath
                    updated = True

    if updated:
        save_data(data)
        print('data/bands.json updated')
    else:
        print('No updates found')

if __name__ == '__main__':
    main()
