"""Relations de préparation Outlander, additives, sans action ou parole jouée."""
import json
import os
from pathlib import Path
os.environ['CONSEIL_MONDE']='outlander'
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'etat'
def lire(n): return json.loads((STATE/(n+'.json')).read_text(encoding='utf-8'))

# A, B, liens A→B, opinion A→B, liens B→A, opinion B→A.
# Les opinions sont des paramètres interprétés de préparation, pas des chiffres canoniques.
FAMILLE = [
 ('colum-mackenzie','dougal-mackenzie',['frere','chef-de-clan'],40,['frere','subordonne'],55),
 ('colum-mackenzie','letitia-mackenzie',['epoux'],65,['epouse'],65),
 ('colum-mackenzie','hamish-mackenzie',['pere-reconnu'],85,['fils-reconnu'],85),
 ('letitia-mackenzie','hamish-mackenzie',['mere'],90,['fils'],90),
 ('dougal-mackenzie','hamish-mackenzie',['oncle-reconnu'],70,['neveu-reconnu'],65),
 ('dougal-mackenzie','letitia-mackenzie',['beau-frere'],30,['belle-soeur'],30),
 ('colum-mackenzie','jamie-fraser',['oncle'],45,['neveu'],40),
 ('dougal-mackenzie','jamie-fraser',['oncle'],35,['neveu'],30),
 ('colum-mackenzie','jenny-murray',['oncle'],45,['niece'],40),
 ('dougal-mackenzie','jenny-murray',['oncle'],35,['niece'],30),
 ('jamie-fraser','jenny-murray',['frere'],85,['soeur'],80),
 ('jenny-murray','ian-murray',['epouse'],90,['epoux'],90),
 ('jamie-fraser','ian-murray',['ami','beau-frere'],85,['ami','beau-frere'],85),
 ('murtagh-fraser','jamie-fraser',['parrain','protecteur'],90,['filleul'],85),
 ('mrs-fitz','laoghaire-mackenzie',['grand-mere'],80,['petite-fille'],75),
]
LEOCH = [
 ('colum-mackenzie','ned-gowan',['employeur','conseil-juridique'],70,['juriste','service'],75),
 ('colum-mackenzie','mrs-fitz',['employeur'],70,['intendante','service'],70),
 ('colum-mackenzie','alec-mackenzie',['chef-de-clan','employeur'],65,['maitre-des-chevaux','service'],70),
 ('dougal-mackenzie','rupert-mackenzie',['commandement','compagnon'],65,['service','compagnon'],75),
 ('dougal-mackenzie','angus-mhor',['commandement','compagnon'],55,['service','compagnon'],70),
 ('rupert-mackenzie','angus-mhor',['ami','compagnon'],85,['ami','compagnon'],85),
 ('colum-mackenzie','rupert-mackenzie',['chef-de-clan'],55,['service'],70),
 ('colum-mackenzie','angus-mhor',['chef-de-clan'],45,['service'],60),
 ('dougal-mackenzie','ned-gowan',['collaborateur'],50,['collaborateur'],45),
 ('mrs-fitz','alec-mackenzie',['collegue'],60,['collegue'],60),
 ('letitia-mackenzie','mrs-fitz',['maisonnee'],65,['service','maisonnee'],65),
 ('jamie-fraser','alec-mackenzie',['travail-aux-ecuries'],60,['encadrement-aux-ecuries'],60),
 ('jamie-fraser','rupert-mackenzie',['compagnon'],65,['compagnon'],65),
 ('jamie-fraser','angus-mhor',['compagnon'],55,['compagnon'],60),
 ('murtagh-fraser','rupert-mackenzie',['compagnon'],45,['compagnon'],50),
 ('murtagh-fraser','angus-mhor',['compagnon'],35,['compagnon'],45),
 # Claire est déjà à Leoch dans le départ retenu ; confiance encore limitée.
 ('claire-randall','jamie-fraser',['connaissance'],35,['connaissance'],40),
 ('claire-randall','mrs-fitz',['accueil'],45,['accueil'],40),
 ('claire-randall','colum-mackenzie',['hospitalite-surveillee'],10,['hospitalite-surveillee'],5),
 ('claire-randall','dougal-mackenzie',['connaissance'],0,['connaissance'],5),
]
# Peinture locale déclarée : aucune parenté ou affiliation politique déduite des noms.
INVERNESS = [
 ('mairi-macleod','finlay-ross',['collaborateur','hebergement-et-ecuries'],55,['collaborateur','hebergement-et-ecuries'],60),
 ('mairi-macleod','alasdair-cameron',['relation-professionnelle'],45,['relation-professionnelle'],45),
 ('finlay-ross','alasdair-cameron',['relation-professionnelle','soins-des-chevaux'],60,['relation-professionnelle','soins-des-chevaux'],55),
 ('mairi-macleod','elspeth-munro',['relation-professionnelle'],50,['relation-professionnelle'],45),
 ('ewan-macrae','elspeth-munro',['voisinage','aide-aux-habitants'],35,['voisinage','aide-aux-habitants'],35),
 ('ewan-macrae','robert-ainslie',['interlocuteur-local'],35,['interlocuteur-local'],35),
 ('robert-ainslie','william-forbes',['interlocuteur-local'],40,['interlocuteur-local'],45),
 ('robert-ainslie','mairi-macleod',['interlocuteur-local'],25,['interlocuteur-local'],20),
 ('william-forbes','alasdair-cameron',['relation-professionnelle'],40,['relation-professionnelle'],40),
]

if __name__=='__main__':
    gens=lire('personnages'); ids={p['id'] for p in gens}; pjs={p['personnage_id'] for p in lire('joueurs')}
    relations=lire('relations'); presents={(r['source_id'],r['cible_id']) for r in relations}
    ajouts=[]
    for a,b,ab,oab,ba,oba in FAMILLE+LEOCH+INVERNESS:
        assert a in ids and b in ids and a!=b
        assert a not in pjs and b not in pjs
        for source,cible,liens,opinion in [(a,b,ab,oab),(b,a,ba,oba)]:
            if (source,cible) in presents: continue
            ajouts.append(dict(source_id=source,cible_id=cible,opinion=opinion,liens=liens,connue_du_joueur=False))
            presents.add((source,cible))
    relations.extend(ajouts)
    assert len(presents)==len(relations), 'Relations directionnelles dupliquées'
    assert all(-100<=r['opinion']<=100 for r in ajouts)
    (STATE/'relations.json').write_text(json.dumps(relations,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(ajouts)} relations directionnelles ajoutées ; {len(relations)} au total ; {len(FAMILLE+LEOCH+INVERNESS)} paires préparées.')
