"""Vectorise les données WorldEngine, sans incorporer d'image matricielle."""
from pathlib import Path
from html import escape
import cv2
import numpy as np
from worldengine.model.world import World

ROOT = Path(__file__).resolve().parent
w = World.open_protobuf(str(ROOT / 'monde-002-portrait.world'))
ocean = w.layers['ocean'].data.astype(bool)
land = ~ocean
height, width = land.shape
biome = w.layers['biome'].data

def contours(mask, tolerance=0.65):
    # Doubler préserve les îlots et cours d'eau d'un seul pixel.
    big = cv2.resize(mask.astype('uint8'), None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    rings, _ = cv2.findContours(big, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    pieces = []
    for ring in rings:
        p = cv2.approxPolyDP(ring, tolerance, True).reshape(-1, 2) / 2
        if len(p) >= 3:
            pieces.append('M' + 'L'.join(f'{x:g},{y:g}' for x,y in p) + 'Z')
    return ''.join(pieces)

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1024" height="2048" viewBox="0 0 {width} {height}">',
 '<title>Monde 002 — carte vectorielle portrait</title>',
 '<desc>Contours extraits des données WorldEngine, graine 1609. Biomes regroupés pour la lisibilité. Aucun fond matriciel. Géographie proposée, sans échelle kilométrique.</desc>']
def group(key, label):
    parts.append(f'<g id="{key}" inkscape:groupmode="layer" inkscape:label="{escape(label)}">')
def shape(mask, color, tolerance=.65, extra=''):
    d = contours(mask, tolerance)
    if d:
        parts.append(f'<path d="{d}" fill="{color}" fill-rule="evenodd" {extra}/>')

group('ocean', '01 · Océan')
parts.append(f'<rect width="{width}" height="{height}" fill="#244f63"/>')
parts.append('</g>')
group('terres','02 · Terres et côtes')
shape(land, '#c5bb88', extra='stroke="#142f36" stroke-width="0.6" stroke-linejoin="round"')
parts.append('</g>')
families = [('glaces','#edf2ec'),('toundra','#afb9a7'),('deserts','#d5bd89'),('prairies','#a1ac72'),('forets-seches','#889864'),('forets','#597b60'),('forets-humides','#365e53')]
classes = np.full(biome.shape, 'prairies', dtype='<U20')
for name in np.unique(biome):
    n = str(name)
    category = ('glaces' if 'ice' in n else 'toundra' if ('tundra' in n or 'polar' in n) else 'deserts' if 'desert' in n else 'forets-humides' if ('rain forest' in n or 'wet forest' in n) else 'forets-seches' if ('dry forest' in n or 'woodland' in n or 'scrub' in n) else 'forets' if 'forest' in n else 'prairies')
    classes[biome == name] = category
for key, color in families:
    group(key, '03 · Biomes / '+key)
    shape((classes == key) & land, color)
    parts.append('</g>')
group('relief','04 · Relief — courbes relatives')
elev = w.layers['elevation'].data
for percentile in (65, 80, 92, 97):
    level = np.percentile(elev[land], percentile)
    shape((elev >= level) & land, '#384237', extra='fill-opacity="0.12" stroke="#48523e" stroke-opacity="0.35" stroke-width="0.3"')
parts.append('</g>')
group('hydrographie','05 · Rivières et lacs')
for key in ('river_map','lake_map'):
    if key in w.layers:
        shape((w.layers[key].data > 0) & land, '#64abc1', tolerance=0.15)
parts.append('</g>')
for key,label in [('villes','06 · Villes — à placer'),('territoires','07 · Territoires — à concevoir'),('passages','08 · Passages — à concevoir')]:
    group(key,label)
    parts.append('</g>')
parts.append('</svg>')
target = ROOT / 'monde-002-portrait.svg'
target.write_text('\n'.join(parts), encoding='utf-8')
print(f'{target} : {target.stat().st_size:,} octets ; {len(parts)} éléments')
