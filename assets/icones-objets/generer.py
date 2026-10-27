"""Icônes vectorielles originales : actions de résistance, biens et équipements."""
from pathlib import Path
import html
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r"C:\Users\reyno\Modern Front\content")
OUT = ROOT / "svg"
OUT.mkdir(parents=True, exist_ok=True)


def path(d, **attrs):
    extra = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="{d}" {extra}/>'


def rect(x, y, w, h, rx=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'


def circle(x, y, r):
    return f'<circle cx="{x}" cy="{y}" r="{r}"/>'


def line(x, y, a, b):
    return path(f'M{x} {y} L{a} {b}')


def wheel(x, y, r=5):
    return circle(x, y, r) + circle(x, y, 1)


def table(small=False):
    x, w = (20, 24) if small else (10, 44)
    return rect(x, 25, w, 6) + path(f'M{x+4} 31v19m{w-8} 0V31')


def radio(kind="mains"):
    if kind == "crystal":
        return rect(10, 33, 39, 15) + path('M16 33V22h19v11m-16-12v12m5-12v12m5-12v12M39 33l9-18M47 14h7v18h-7m-1-17v-3a8 8 0 0 0-16 0') + circle(18, 41, 2)
    s = rect(10, 20, 44, 29, 4) + rect(16, 26, 17, 16, 2) + path('M20 27v14m5-14v14m4-14v14') + rect(38, 27, 10, 4) + circle(40, 40, 2) + circle(48, 40, 2)
    if kind == "battery":
        s += rect(23, 9, 18, 7) + path('M28 9V6m8 3V6M32 10v5m-2-2h4')
    elif kind == "mains_shortwave":
        s += path('M42 20L51 7M20 14q12-9 21 0m-17 1q7-5 12 0')
    else:
        s += path('M19 20v-6h26v6')
    return s


def car(kind):
    tops = {
        'car': 'M17 30l7-12h19l7 12',
        'citroen_traction': 'M17 30l8-13h15l8 13',
        'peugeot_202': 'M18 30q5-16 20-13l10 13',
        'renault_juvaquatre': 'M17 30l6-13h19v13',
        'old_car': 'M19 30V15h23v15',
    }
    s = path(tops[kind]) + path('M8 39v-7l9-2h32l7 4v8h-5M18 42h23M8 42h1') + wheel(14, 43) + wheel(46, 43)
    if kind == 'old_car':
        s += path('M21 12h23M24 18v11m12-11v11M51 31v-7h4')
    elif kind == 'citroen_traction':
        s += path('M25 21h13l6 8H21m10-8v8M51 34l2 2-2 2')
    elif kind == 'peugeot_202':
        s += path('M24 23q6-7 13-2l6 8H21M51 34v5m3-4v4')
    elif kind == 'renault_juvaquatre':
        s += path('M25 21h13v8H21m9-8v8M18 34h21')
    else:
        s += path('M25 22h15l4 7H21M31 22v7')
    return s


def truck(kind):
    s = wheel(17, 47) + wheel(48, 47) + path('M7 42v-4h49v8h-3M23 46h19M7 46h4M38 38V22h11l7 10v6M43 27v7h9l-5-7z')
    if kind == 'van':
        s += path('M8 38V18h29v20M13 23h17v9H13z')
    elif kind == 'gazogene_lorry':
        s += rect(7, 18, 23, 20) + path('M33 38V14h7v24M33 17h7m-7 15h7M35 14V8h6')
    else:
        s += rect(7, 23 if kind == 'truck' else 17, 29, 15 if kind == 'truck' else 21) + path('M12 26v10m8-10v10m8-10v10')
    return s


def bicycle(kind):
    if kind == 'delivery_bicycle':
        return wheel(13, 44, 9) + wheel(50, 44, 7) + path('M13 44l11-20 10 20H13m11-20h10l6 20M23 23l-2-6m-4 0h10M37 25l-3-10h7') + rect(40, 25, 18, 12)
    s = wheel(14, 44, 10) + wheel(50, 44, 10) + path('M14 44l12-21 9 21H14m21 0 10-22 5 22M25 23l-3-7m-5 0h11M45 22l-3-9h9')
    s += path('M26 24l14 7') if kind in ('bicycle', 'mens_bicycle') else path('M25 26q4 14 15 4')
    return s


def cart(kind):
    s = wheel(22, 44, 8) + path('M8 34h33l16-10M12 34l-4-15h31l-3 15M15 23h19')
    if kind == 'wagon':
        s += wheel(43, 44, 7) + path('M37 34h13V19H39M16 19V12h32v7')
    elif kind == 'trap':
        s += path('M12 19v-7q12-9 23 0v7M23 19v-7M9 35h29')
    elif kind == 'farm_cart':
        s += path('M10 28h28M17 19v14m12-14v14')
    return s


def gun(kind):
    if kind == 'revolver':
        return path('M10 19h33v9H25l-4 8 6 13H15L9 31l-4-3v-8h5M31 20v7m-5-7v7M43 21h13v5H43M21 34q15 5 13-7M12 15h4v4') + circle(20, 24, 3)
    s = path('M7 48l11-3 9-12 6 1 22-23-3-3-22 22-7-1-9 9-7 3zM26 34l-3 8h-7')
    if kind == 'shotgun':
        s += path('M33 30L54 9m-24 24 4 4')
    elif kind == 'rifle_22':
        s += path('M23 30l-3-4 12-12 3 4M36 27l3 3')
    elif kind == 'lebel':
        s += path('M49 12l8-8M30 28l4-4 4 4M10 44l6-1')
    else:
        s += path('M34 24l3 3M13 41l4 3')
    return s


def ammo(kind):
    h = {'shotgun_cartridge': 25, 'cartridge_22lr': 17, 'revolver_8mm': 22, 'lebel_8mm': 30}[kind]
    s = ''
    for x, y in [(15, 49), (29, 44), (43, 49)]:
        s += rect(x, y-h, 8, h) + line(x, y-5, x+8, y-5)
        if kind == 'lebel_8mm':
            s += path(f'M{x+1} {y-h}v-4l3-6 3 6v4')
        elif kind != 'shotgun_cartridge':
            s += path(f'M{x} {y-h}q4-7 8 0')
    return s


def coin(kind):
    s = circle(32, 32, 20) + circle(32, 32, 15)
    emblems = {
        'gold': 'M24 37l8-15 8 15zM27 41h10',
        'napoleon': 'M24 38l6-6-3-8 8 3 7-5-2 9-6 5v6m-4-7-7-2',
    }
    if '10' in kind:
        s += path('M25 27l4-4v18m7-18q10-1 6 18h-6z')
    elif 'louis' in kind:
        s += path('M22 36l-2-12 8 7 4-10 4 10 8-7-2 12zM23 41h18')
    elif 'emp' in kind or kind == 'napoleon_head':
        s += path('M26 42v-7l-4-3 4-3v-7l7-3 6 6-2 12 4 5M26 23l14 3')
    else:
        s += path(emblems['gold' if kind == 'gold' else 'napoleon'])
    return s


def jewel(kind):
    if kind in ('wedding_ring', 'alliance'):
        return circle(32, 34, 17) + circle(32, 34, 12) + path('M20 16l-4-4m16 1V7m12 9 4-4')
    if 'chain' in kind:
        return path('M14 11q-5 26 18 29 23-3 18-29M14 11q18-8 36 0M29 40v5h-5v5h5v8h6v-8h5v-5h-5v-5')
    if 'brooch' in kind:
        return path('M12 32q7-25 20-9 13-16 20 9-7 25-20 9-13 16-20-9zM16 32h32') + circle(32, 32, 6)
    if 'earring' in kind:
        return path('M13 20c-8-14 18-17 12-2l-6 9M39 20c-8-14 18-17 12-2l-6 9M19 27q-16 17 0 26 16-9 0-26zM45 27q-16 17 0 26 16-9 0-26z')
    if 'watch' in kind:
        return circle(32, 37, 18) + circle(32, 37, 13) + circle(32, 13, 5) + path('M32 26v11l8 5M27 19v-3h10v3M12 23Q3 11 15 8')
    if 'signet' in kind:
        return circle(32, 37, 16) + circle(32, 37, 10) + rect(21, 10, 22, 16, 4) + path('M27 21l5-7 5 7')
    if 'bracelet' in kind:
        return path('M10 32a22 15 0 1 0 44 0 22 15 0 1 0-44 0M10 32v7a22 15 0 0 0 44 0v-7M16 24l4 6m9-12v8m12-5-3 6m11 1-5 5')
    if 'pearl' in kind:
        return ''.join(circle(x,y,4) for x,y in [(13,16),(12,26),(15,36),(21,45),(31,50),(41,46),(48,37),(51,27),(50,17)]) + path('M17 12h29')
    return circle(24, 39, 12) + path('M18 28l-5-10 10-9 11 9-5 10M13 18h21m-11-9v18') + circle(45, 43, 7)


def good(key, family):
    if family == 'car': return car(key)
    if family == 'truck': return truck(key)
    if family == 'bicycle': return bicycle(key)
    if family == 'cart': return cart(key)
    if family == 'hunting_gun': return gun(key)
    if family == 'jewellery': return jewel(key)
    if family == 'gold': return coin(key)
    if family == 'fuel': return rect(14,16,36,40,4)+path('M22 16V8h16v8M43 16l5-7 8 5-5 7M21 26l22 22m0-22L21 48')
    if family == 'cash': return rect(7,18,45,27,2)+rect(12,23,35,17)+circle(30,31,6)+path('M12 49h44V23M18 29v5m23-5v5')
    raise ValueError((key, family))


def load(file): return json.loads((SOURCE/file).read_text(encoding='utf-8-sig'))


entries = []


def add(key, name, group, drawing, source, source_key):
    entries.append(dict(id=key, nom=name, categorie=group, fichier=f'svg/{key}.svg', source=source, cle_source=source_key, drawing=drawing))


from lexique import ACTIONS, termes
from actions import dessins
resistance = load('resistance_actions.json')
action_drawings = dessins(path, rect, circle)
assert set(action_drawings) == {a['key'] for a in resistance['actions']}, 'Catalogue des actions incomplet'
assert set(ACTIONS) == set(action_drawings)
categories = {c['key']: c['name'] for c in resistance['categories']}
for action in resistance['actions']:
    key = action['key']
    add('action-'+key, action['name'], 'Actions — '+categories[action['category']], action_drawings[key], 'resistance_actions.json', key)
    entries[-1].update(nom_original=action['name'], nom_couvert=ACTIONS[key])
# Les actions ajoutées pour le jeu, sans toucher au fichier Modern Front.
from actions_locales import actions as actions_locales
locales = actions_locales(path, rect, circle)
for action in locales:
    key = action['key']
    assert key not in action_drawings, key
    add('action-'+key, action['name'], 'Actions — '+categories[action['category']], action['code'], 'actions_locales.py', key)
    entries[-1].update(nom_original=action['name'], nom_couvert=action['couvert'])

from ressources import dessins as dessins_ressources, NOMS
resource_drawings = dessins_ressources(path, rect, circle)
assert set(resource_drawings) == set(NOMS) == {r['key'] for r in resistance['resources']}
for resource in resistance['resources']:
    key = resource['key']
    add('ressource-'+key, NOMS[key]+' — '+resource['name'], 'Chantier — ressources', resource_drawings[key], 'resistance_actions.json', key)
    entries[-1].update(nom_couvert=NOMS[key], nom_original=resource['name'], unite_originale=resource['unit'])

from biens_atelier import dessins as dessins_biens
atelier = dessins_biens(path, rect, circle)
for item in load('belongings.json')['items']:
    key = item['key']
    if key == 'horse': continue
    couvert, dessin = atelier['bien-'+key]
    groupe = 'Biens — transport' if key in ('car','truck','cart','bicycle') else 'Biens — outillage et valeurs'
    add('bien-'+key, item['name'], groupe, dessin, 'belongings.json', key)
    entries[-1].update(nom_original=item['name'], nom_couvert=couvert)
# Un seul pictogramme pour chaque famille, sans marques ni calibres.
for key, original, couvert, dessin, source in [
    ('munition','Munitions','Pointes',resource_drawings['ammo'],'resistance_actions.json'),
    ('radio','Radio','Sonnette',atelier['radio-mains'][1],'radios.json'),
    ('telephone','Téléphone','Tube porte-voix',atelier['telephone'][1],'telephones.json'),
    ('tabac','Tabac','Crayons d’atelier',atelier['tabac-gauloises'][1],'tobacco.json'),
]:
    add(key,original,'Biens — fournitures et communications',dessin,source,'ammo' if key=='munition' else key)
    entries[-1].update(nom_original=original,nom_couvert=couvert)
for key, original, couvert, groupe, dessin in termes(path,rect,circle):
    add('terme-'+key, original, 'Vocabulaire — '+groupe, dessin, 'lexique.py', key)
    entries[-1].update(nom_original=original, nom_couvert=couvert, statut='proposition de vocabulaire')

STYLE = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
from icones_claires import dessins as dessins_clairs
clairs = dessins_clairs(path, rect, circle, good, radio, ammo)
clairs.update({'action-'+a['key']: a['clair'] for a in locales})
assert set(clairs) == {e['id'] for e in entries}
(ROOT/'svg-clair').mkdir(exist_ok=True)
symboles_clairs=[]
for e in entries:
    e['fichier_clair']='svg-clair/'+e['id']+'.svg'
    titre=html.escape(e.get('nom_original',e['nom']))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img"><title>{titre}</title><g {STYLE}>{clairs[e["id"]]}</g></svg>\n'
    ET.fromstring(svg)
    (ROOT/e['fichier_clair']).write_text(svg,encoding='utf-8')
    symboles_clairs.append(f'<symbol id="{e["id"]}" viewBox="0 0 64 64"><title>{titre}</title><g {STYLE}>{clairs[e["id"]]}</g></symbol>')
(ROOT/'objets-clairs.sprite.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">'+''.join(symboles_clairs)+'</svg>',encoding='utf-8')
symbols=[]
for e in entries:
    title=html.escape(e['nom'])
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-labelledby="title"><title id="title">{title}</title><g {STYLE}>{e["drawing"]}</g></svg>\n'
    ET.fromstring(svg)
    (ROOT/e['fichier']).write_text(svg,encoding='utf-8')
    symbols.append(f'<symbol id="{e["id"]}" viewBox="0 0 64 64"><title>{title}</title><g {STYLE}>{e["drawing"]}</g></symbol>')
(ROOT/'objets.sprite.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">'+''.join(symbols)+'</svg>\n',encoding='utf-8')
manifest=[{k:v for k,v in e.items() if k!='drawing'} for e in entries]
etapes=json.loads((ROOT/'etapes-actions.json').read_text(encoding='utf-8'))
for entry in manifest:
    if entry['id'] in etapes:
        entry['etapes_suggerees']=etapes[entry['id']]
types=json.loads((ROOT/'noeuds-types.json').read_text(encoding='utf-8'))
for entry in manifest:
    entry['type_noeud']='action' if entry['id'].startswith('action-') else 'ressource' if entry['categorie']=='Chantier — ressources' else 'objet'
    if entry['id'] in types['actions']:
        entry['noeuds_associes']=types['actions'][entry['id']]
manifest.extend(types['metiers'])
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

cards=[]
for categorie in dict.fromkeys(e['categorie'] for e in entries):
    cartes=[]
    for e in (e for e in entries if e['categorie']==categorie):
        original=e.get('nom_original',e['nom']); couvert=e['nom_couvert']
        recherche=html.escape(original+' '+couvert+' '+e['id'])
        cartes.append(f'<a class="card" href="{e["fichier"]}" data-group="{html.escape(categorie)}" data-search="{recherche}" title="Ouvrir le SVG : {html.escape(original)}"><div class="sample"><svg viewBox="0 0 64 64" aria-hidden="true"><g {STYLE}>{e["drawing"]}</g></svg></div><span>{html.escape(original)}</span><strong class="couvert">{html.escape(couvert)}</strong></a>')
    cards.append(f'<section class="category"><h2>{html.escape(categorie)}</h2><div class="grid">'+''.join(cartes)+'</div></section>')
groups=''.join(f'<option>{html.escape(g)}</option>' for g in dict.fromkeys(e['categorie'] for e in entries))
page='''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>La peur et le geste — Actions et objets</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f1eee5;color:#282d29;font:16px/1.5 system-ui,sans-serif}header,main{max-width:1440px;margin:auto;padding:32px 40px}header{padding-bottom:24px;border-bottom:1px solid #c7c9be}.eyebrow{font:12px ui-monospace,monospace;letter-spacing:.18em;color:#626b58}h1{font:52px/1.05 Georgia,serif;margin:18px 0 12px}p{max-width:740px;color:#62665e;margin:0 0 20px}.controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center}input,select,button{font:inherit;padding:10px 14px;border:1px solid #b1b7a5;border-radius:4px;background:transparent;color:inherit}input{min-width:240px}button{cursor:pointer}a{color:inherit}.count{margin-left:auto;font:13px ui-monospace,monospace}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:1px;background:#c7c9be;border:1px solid #c7c9be}.card{display:flex;flex-direction:column;align-items:center;padding:20px 12px 16px;min-height:174px;background:#f8f6f0;text-align:center;text-decoration:none}.card:hover,.card:focus-visible{background:#e4e9da;outline:2px solid #5d704d;outline-offset:-2px}.sample{height:83px;display:flex;align-items:center;justify-content:center}.sample svg{width:64px;height:64px}.card span{font-size:13px;line-height:1.3}.card small{font:9px/1.3 ui-monospace,monospace;overflow-wrap:anywhere;color:#777f6d;margin-top:8px}.card[hidden],.category[hidden],[hidden]{display:none!important}.category{margin-bottom:36px}.category h2{font:25px Georgia,serif;margin:0 0 14px}.couvert{font:italic 15px/1.4 Georgia,serif;margin-top:10px;color:#586842}body.dark .couvert{color:#c0cfaa}body.dark{background:#222923;color:#eceddf}body.dark .grid{background:#424d40}body.dark .card{background:#2a332c}body.dark .card:hover{background:#3e4b3c}body.dark p,body.dark small,body.dark .eyebrow{color:#b5bfaa}body.dark option{background:#222923}.downloads{font-size:13px;display:flex;gap:20px;margin-top:20px}@media(max-width:600px){header,main{padding:24px 18px}h1{font-size:38px}.count{margin-left:0}.grid{grid-template-columns:repeat(2,1fr)}}
</style><header><div class="eyebrow">LA PEUR ET LE GESTE / COLLECTION 01</div><h1>À l’atelier.<br>Le geste à double sens.</h1><p>61 actions, 14 ressources, 13 types de biens et 16 termes de présence, de contrôle et d’infrastructure. Chaque nom est suivi de sa traduction de chantier. Les variantes ont été retirées ; les nouveaux termes sont des propositions pour le jeu.</p><div class="controls"><input id="search" aria-label="Chercher une action ou un objet" placeholder="Chercher une action ou un objet…"><select id="group" aria-label="Catégorie"><option value="">Toutes les catégories</option>__GROUPS__</select><label>Taille <select id="size"><option>64</option><option>32</option><option>24</option></select></label><button id="theme">Fond sombre</button><span class="count" id="count"></span></div><div class="downloads"><a href="objets.sprite.svg" download>Sprite SVG</a><a href="manifest.json" download>Catalogue JSON</a><a href="icones-objets.zip" download>Télécharger les SVG</a></div></header><main>__CARDS__<p id="empty" hidden>Aucun résultat pour cette recherche.</p></main><script>
const cards=[...document.querySelectorAll('.card')],search=document.querySelector('#search'),group=document.querySelector('#group');const fold=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();function filter(){let n=0;for(const card of cards){card.hidden=!(fold(card.dataset.search).includes(fold(search.value))&&(!group.value||card.dataset.group===group.value));if(!card.hidden)n++}document.querySelectorAll('.category').forEach(s=>{s.hidden=![...s.querySelectorAll('.card')].some(c=>!c.hidden)});document.querySelector('#empty').hidden=n>0;document.querySelector('#count').textContent=n+' / '+cards.length+' icônes'}search.value=new URLSearchParams(location.search).get('q')||'';search.addEventListener('input',filter);group.addEventListener('change',filter);document.querySelector('#size').addEventListener('change',e=>{document.querySelectorAll('.sample svg').forEach(s=>{s.style.width=s.style.height=e.target.value+'px'})});document.querySelector('#theme').onclick=e=>{const dark=document.body.classList.toggle('dark');e.target.textContent=dark?'Fond clair':'Fond sombre'};filter();
</script></html>'''.replace('__COUNT__',str(len(entries))).replace('__GROUPS__',groups).replace('__CARDS__',''.join(cards))
(ROOT/'index.html').write_text(page,encoding='utf-8')
# Deux planches avec les mêmes catégories, identifiants et filtres.
page_claire=page.replace('À l’atelier.<br>Le geste à double sens.','Langage clair.<br>Les gestes et les moyens.')
for e in entries:
    page_claire=page_claire.replace(f'<g {STYLE}>{e["drawing"]}</g>',f'<g {STYLE}>{clairs[e["id"]]}</g>')
    page_claire=page_claire.replace('href="'+e['fichier']+'"','href="'+e['fichier_clair']+'"')
page_claire=page_claire.replace('Chaque nom est suivi de sa traduction de chantier.', 'Dessins littéraux : personnes, équipements et infrastructures. La traduction de chantier reste indiquée sous chaque nom.')
page_claire=page_claire.replace('href="objets.sprite.svg"','href="objets-clairs.sprite.svg"')
page_claire=page_claire.replace('<div class="downloads">','<div class="downloads"><a href="index.html">Voir les icônes codées</a>')
(ROOT/'index-clair.html').write_text(page_claire,encoding='utf-8')
(ROOT/'index.html').write_text(page.replace('<div class="downloads">','<div class="downloads"><a href="index-clair.html">Voir les icônes claires</a>'),encoding='utf-8')

readme='''# Icônes des actions et objets

Dessins SVG originaux pour La peur et le geste. Les 60 actions ont une silhouette de menuiserie et un indice du sens initial (assemblage, trajet, contrôle, rupture). Les 14 ressources ont aussi leur pictogramme de chantier : clous, bons de livraison, gabarits, chaux, huisseries, carreaux, sable, huile, outils, pointes, poudre, sonnette, cotes et agrément. Le manifeste conserve leur nom couvert, leur sens initial et leur unité réelle sans inventer de conversion. Les identifiants et chemins sont conservés. La première version est conservée dans actions-resistance-original.py. Source des types : fichiers de contenu Modern Front. Les 60 actions viennent de resistance_actions.json, sans ajout ni modification de règles ; une action propre au jeu, Organiser une réunion, s’y ajoute depuis actions_locales.py. Les 67 icônes de mobilier et de décor ont été retirées ; les biens sont réduits à 13 types principaux, sans variantes de marque, de bijou, de pièce, de calibre ou de radio. Seize termes de présence, de contrôle et d’infrastructure sont ajoutés comme propositions dans lexique.py. Les noms de couverture sont des propositions graphiques ; les clés source restent inchangées. Ce sont des pictogrammes, pas des reproductions historiques précises de modèles ou de marques.

- `index.html` : planche autonome, recherche, filtres, fond clair/sombre et tailles 64/32/24 px.
- `svg-clair/` : les 104 dessins littéraux, raccordés au langage clair du tableau.
- `index-clair.html` et `objets-clairs.sprite.svg` : planche et sprite en langage clair.
- `svg/` : un fichier autonome par type, action ou terme, transparent, viewBox 0 0 64 64.
- `manifest.json` : identifiants stables, libellés, chemins et clés des données source.
- `objets.sprite.svg` : symboles utilisables avec `<svg><use href="objets.sprite.svg#action-print_tracts"/></svg>`.
- `generer.py` : génération reproductible depuis les fichiers source locaux.

Le trait utilise `currentColor` (2 unités). En SVG inline ou sprite, la couleur suit la propriété CSS `color`; dans une balise `img`, elle reste noire. Les animaux ne font pas partie du catalogue d’objets. Les fichiers sont créés dans le nouveau dépôt, sans modification de Modern Front. Les icônes ne changent pas la simulation ; leur présence ne signifie pas qu’une action est actuellement disponible.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
import zipfile
with zipfile.ZipFile(ROOT/'icones-objets.zip','w',zipfile.ZIP_DEFLATED) as z:
    for file in [ROOT/e['fichier'] for e in entries]+[ROOT/e['fichier_clair'] for e in entries]+[ROOT/'index-clair.html',ROOT/'objets-clairs.sprite.svg']+[ROOT/'objets.sprite.svg',ROOT/'manifest.json',ROOT/'index.html',ROOT/'README.md']:
        z.write(file,file.relative_to(ROOT))
print(f'{len(entries)} SVG, sprite, catalogue, planche et archive créés dans {ROOT}')
