"""Ajout idempotent de fiches de préparation ; aucune scène ni connaissance PJ."""
import json
import os
from pathlib import Path

os.environ['CONSEIL_MONDE'] = 'outlander'
ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT/'etat'
def lire(n): return json.loads((STATE/(n+'.json')).read_text(encoding='utf-8'))
def sauver(n,v): (STATE/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Titres et liens : canon. Traits, manière et objectifs : interprétation de préparation.
ACTEURS = [
 ('murtagh-fraser','Murtagh Fitzgibbons Fraser','fraser','leoch','Parrain de Jamie', ['loyal','réservé','vigilant'], 'Peu de mots, observations sèches et concrètes.', 'Veiller sur Jamie et préserver sa sécurité.'),
 ('jenny-murray','Janet « Jenny » Fraser Murray','fraser','lallybroch','Sœur de Jamie, épouse d’Ian Murray', ['résolue','pragmatique','protectrice'], 'Franche, précise, peu impressionnée par le rang.', 'Préserver son foyer et la continuité du domaine de Lallybroch.'),
 ('ian-murray','Ian Murray','murray','lallybroch','Époux de Jenny, ami de Jamie', ['loyal','patient','pragmatique'], 'Calme, concret, volontiers conciliant.', 'Soutenir Jenny et préserver le foyer de Lallybroch.'),
 ('mrs-fitz','Glenna Fitzgibbons — Mrs Fitz',None,'leoch','Maisonnée de Leoch', ['pragmatique','chaleureuse','ferme'], 'Familiarité chaleureuse, consignes nettes.', 'Tenir les besoins ordinaires de la maisonnée de Leoch.'),
 ('laoghaire-mackenzie','Laoghaire MacKenzie','mackenzie','leoch','Jeune femme du clan MacKenzie', ['fière','sensible','réservée'], 'Retenue en public, attentive aux marques de considération.', 'Trouver sa place à Leoch et préserver sa considération.'),
 ('letitia-mackenzie','Letitia MacKenzie','mackenzie','leoch','Épouse de Colum', ['digne','prudente','protectrice'], 'Courtoise, attentive aux préséances.', 'Préserver son foyer et la place de Hamish à Leoch.'),
 ('hamish-mackenzie','Hamish MacKenzie','mackenzie','leoch','Fils reconnu de Colum et Letitia', ['curieux','vif'], 'Questions directes d’un enfant, sans calcul de conseil.', 'Grandir auprès des siens et découvrir ce qui l’entoure.'),
 ('rupert-mackenzie','Rupert MacKenzie','mackenzie','leoch','Homme du clan, compagnon de Dougal', ['loyal','jovial','pratique'], 'Franc, plaisante facilement, parle concret.', 'Servir le clan et préserver ses compagnons.'),
 ('angus-mhor','Angus Mhor',None,'leoch','Homme des MacKenzie, compagnon de Rupert', ['impulsif','loyal','rugueux'], 'Direct, gouailleur, peu cérémonieux.', 'Tenir sa place parmi les hommes du clan et protéger ses compagnons.'),
 ('ned-gowan','Ned Gowan',None,'leoch','Juriste au service des MacKenzie', ['méthodique','prudent','perspicace'], 'Précis, distingue faits, droits et engagements.', 'Préserver les intérêts du clan par des engagements juridiquement solides.'),
 ('alec-mackenzie','Alec MacMahon MacKenzie — le vieux Alec','mackenzie','leoch','Maître des chevaux de Leoch', ['expérimenté','exigeant','pragmatique'], 'Parle chevaux et travail avec peu de détours.', 'Maintenir les chevaux et les écuries en état de servir.'),
]

lieux=lire('lieux'); maisons=lire('maisons'); gens=lire('personnages'); tetes=lire('intentions')
if not any(l['id']=='lallybroch' for l in lieux):
    lieux.append(dict(id='lallybroch',nom='Lallybroch',region='Highlands',type='domaine',controle_id='fraser',alias=[]))
for ident,nom in [('fraser','Fraser de Lallybroch'),('murray','Murray de Lallybroch')]:
    if not any(m['id']==ident for m in maisons):
        maisons.append(dict(id=ident,nom=nom,siege_id='lallybroch',suzerain_id=None,canon=True))
jamie=next(p for p in gens if p['id']=='jamie-fraser')
if jamie.get('maison_id') is None: jamie['maison_id']='fraser'
ajoutes=[]
date=lire('monde')['date']
for ident,nom,maison,lieu,titre,traits,maniere,but in ACTEURS:
    if any(p['id']==ident for p in gens): continue
    gens.append(dict(id=ident,nom=nom,maison_id=maison,titre=titre,traits=traits,objectifs=[dict(but=but,priorite=1)],maniere=maniere,etat='actif',lieu_id=lieu,condition='libre'))
    tetes.append(dict(personnage_id=ident,croyances=[titre,f'Son implantation de départ est à {"Leoch" if lieu=="leoch" else "Lallybroch"}.'],ignore=['L’arrivée d’Aurore et Nicolas.','L’origine temporelle de Claire.'],intention=but,plan=[],declencheurs=[],attitude_joueur='Ne connaît ni Aurore ni Nicolas.',date_maj=date.copy()))
    chambre=ROOT/'chambres'/ident
    (chambre/'books').mkdir(parents=True,exist_ok=True)
    (chambre/'AGENTS.md').write_text(f'# {nom}\n\nLire ../../AGENTS.md, ../../manuel.md et ../../canon/clans.md. Lire l’état actuel dans le monde outlander. Les fiches sont une préparation ; aucune rencontre avec les PJ n’en découle. Les objectifs et traits initiaux sont des interprétations révisables. Aucune parole ou action nouvelle sans la session de son porteur.\n',encoding='utf-8')
    for modele,prefixe in [('affaire-pnj','affaire'),('registre-etats','registre-etats')]:
        s=(ROOT/'modeles'/(modele+'.json')).read_text(encoding='utf-8').replace('porteur',ident)
        (chambre/'books'/(prefixe+'-'+ident+'.json')).write_text(s,encoding='utf-8')
    ajoutes.append(ident)
for n,v in [('lieux',lieux),('maisons',maisons),('personnages',gens),('intentions',tetes)]: sauver(n,v)
assert len({p['id'] for p in gens})==len(gens)
assert all(p.get('maison_id') is None or p['maison_id'] in {m['id'] for m in maisons} for p in gens)
assert all(p.get('lieu_id') is None or p['lieu_id'] in {l['id'] for l in lieux} for p in gens)
print(f'{len(ajoutes)} PNJ ajoutés ; {len(gens)-2} PNJ au total, 2 PJ préservés.')
