"""Fond Natural Earth ; positions fictives de mise en page, sans distances de jeu."""
import json
import math
from pathlib import Path
from urllib.request import urlretrieve
from PIL import Image
import numpy as np
import contourpy
from shapely.geometry import Polygon
from shapely.geometry import shape, box
from shapely.ops import unary_union

ICI = Path(__file__).resolve().parent
BORNES = (-7.4, 56.45, -2.6, 58.7)
SOURCE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson'
def point(lon, lat):
    return [round((lon + 7.4) * math.cos(math.radians(57.5)) * 220, 2), round((58.7 - lat) * 220, 2)]

def chemin(g):
    if g.is_empty:
        return ''
    if g.geom_type in ('MultiPolygon', 'MultiLineString', 'GeometryCollection'):
        return ''.join(chemin(p) for p in g.geoms)
    if g.geom_type == 'LineString':
        return 'M' + 'L'.join(','.join(map(str, point(*p[:2]))) for p in g.coords)
    if g.geom_type != 'Polygon':
        return ''
    def anneau(r):
        return 'M' + 'L'.join(','.join(map(str, point(*p[:2]))) for p in r.coords) + 'Z'
    return anneau(g.exterior) + ''.join(anneau(r) for r in g.interiors)

source = ICI / 'terre-source.geojson'
if not source.exists():
    urlretrieve(SOURCE, source)
terre = unary_union([shape(f['geometry']) for f in json.loads(source.read_text())['features']]).intersection(box(*BORNES)).simplify(.002, preserve_topology=True)
def couche(nom):
    fichier = ICI / (nom+'-source.geojson')
    if not fichier.exists():
        urlretrieve(SOURCE.replace('land.geojson', nom+'.geojson'), fichier)
    morceaux = []
    for f in json.loads(fichier.read_text(encoding='utf-8'))['features']:
        g = shape(f['geometry'])
        if g.intersects(box(*BORNES)):
            morceaux.append(g.intersection(box(*BORNES)))
    print(nom, len(morceaux), 'éléments')
    return unary_union(morceaux)

eaux = couche('lakes')
rivieres = unary_union([couche('rivers_lake_centerlines'), couche('rivers_europe')])
# Relief mesuré depuis les tuiles Terrarium, seuils 300 et 700 m.
# Altitudes lissées puis isolignes interpolées : aucun contour en cellules carrées.
def tuile(lon, lat):
    return ((lon+180)/360*128, (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*128)
def inverse(x, y):
    return (x/128*360-180, math.degrees(math.atan(math.sinh(math.pi*(1-2*y/128)))))
x0, y0 = tuile(BORNES[0], BORNES[3])
x1, y1 = tuile(BORNES[2], BORNES[1])
tx0, tx1 = math.floor(x0), math.floor(x1)
ty0, ty1 = math.floor(y0), math.floor(y1)
altitudes = np.zeros(((ty1-ty0+1)*256,(tx1-tx0+1)*256))
cache = ICI/'terrain-source'
cache.mkdir(exist_ok=True)
for tx in range(math.floor(x0), math.floor(x1)+1):
    for ty in range(math.floor(y0), math.floor(y1)+1):
        fichier = cache/f'{tx}-{ty}.png'
        if not fichier.exists():
            urlretrieve(f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/7/{tx}/{ty}.png',fichier)
        rgb = np.array(Image.open(fichier).convert('RGB'),dtype=float)
        alt = rgb[:,:,0]*256+rgb[:,:,1]+rgb[:,:,2]/256-32768
        altitudes[(ty-ty0)*256:(ty-ty0+1)*256,(tx-tx0)*256:(tx-tx0+1)*256] = alt
# Filtre gaussien séparable, continu aux joints des tuiles.
rayon = 4
poids = np.exp(-np.arange(-rayon,rayon+1,dtype=float)**2/(2*1.5**2))
poids /= poids.sum()
for axe in (0,1):
    altitudes = np.apply_along_axis(lambda v: np.convolve(np.pad(v,rayon,mode='edge'),poids,mode='valid'),axe,altitudes)
longitudes = np.array([inverse(tx0+(i+.5)/256,ty0)[0] for i in range(altitudes.shape[1])])
latitudes = np.array([inverse(tx0,ty0+(i+.5)/256)[1] for i in range(altitudes.shape[0])])
contours = contourpy.contour_generator(x=longitudes,y=latitudes,z=altitudes,fill_type='OuterOffset')
relief = {}
for nom,seuil in [('collines',300),('montagnes',700)]:
    points, offsets = contours.filled(seuil,10000)
    polygones = []
    for pts, limites in zip(points,offsets):
        anneaux = [pts[a:b] for a,b in zip(limites[:-1],limites[1:])]
        polygones.append(Polygon(anneaux[0],anneaux[1:]))
    relief[nom] = chemin(unary_union(polygones).intersection(terre).simplify(.0015,preserve_topology=True))
w, h = point(-2.6, 56.45)
inverness = point(-4.224, 57.4778)
# Les lieux fictifs sont regroupés à titre indicatif près d'Inverness.
# Leurs écarts graphiques ne constituent aucune mesure ni route canonique.
lieux = {'inverness': inverness}
for nom, dx, dy in [('craigh-na-dun',-35,-26),('lisiere-craigh',-35,-22),('croisee-craigh',-35,-18),('ferme-du-ruisseau',-39,-14),('chemin-aval-ruisseau',-39,-8),('route-basse-craigh',-35,-2),('gue-route-basse',-31,4),('hameau-derriere-crete',-27,10),('leoch',-85,22),('cranesmuir',-67,35),('lallybroch',-60,70)]:
    lieux[nom] = [round(inverness[0]+dx,2), round(inverness[1]+dy,2)]
lieux['fort-william'] = point(-5.105,56.819)
lieux['fort-william-fort'] = [lieux['fort-william'][0]-3,lieux['fort-william'][1]-4]
geo = dict(viewBox=f'0 0 {w} {h}', largeur=w, hauteur=h, terre=chemin(terre), fonds={}, regions=[], eaux=chemin(eaux), rivieres=chemin(rivieres.buffer(.0015)), relief=relief, routes=[], lieux=lieux,
    bourgs=[dict(id=n.lower().replace(' ','-'),nom=n,p=point(lon,lat)) for n,lon,lat in [('Beauly — Fraser de Lovat',-4.459,57.483),('Château de Beaufort — Fraser',-4.478,57.452),('Portree',-6.195,57.412),('Ullapool',-5.159,57.897),('Dornoch',-4.028,57.881),('Thurso',-3.525,58.593),('Wick',-3.094,58.439),('Aviemore',-3.827,57.195),('Loch Ness',-4.55,57.28),('Ben Nevis',-5.004,56.797)]],
    cadres={'highlands':f'0 0 {w} {h}','inverness':f'{inverness[0]-125} {inverness[1]-65} 215 155'})
from details_inverness import enrichir
enrichir(geo, point)
(ICI/'geo.js').write_text('// Highlands — Natural Earth 1:10m. Voir README.md pour les limites des repères fictifs.\nwindow.Geo = '+json.dumps(geo,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print(f'Carte : {len(geo["terre"])} caractères de côte, {len(lieux)} lieux.')
