# Brouillon JURIS, action 70563. Non exécuté, non vérifié.
# Ce script compare ma-memoire à ses témoins datés en brouillons/.
# Pour chaque ligne apparue ou disparue, il cherche d'abord son origine dans toutes mes traces : fil/ et fil/contextes/*.
# Il propose ensuite une entrée datée pour problemes.json.
# Il n'écrit rien lui-même. Il n'efface rien. Il ne qualifie jamais une ligne d'« étrangère ».
# Ce qui n'est pas retrouvé reste « non retrouvée » (règle de mon cahier, J1 10h2x).
# Mes canaux du parloir ne sont pas lisibles par ce script : leur relecture reste un geste à la main, noté dans l'entrée.
import hashlib, json, pathlib, sys, datetime

CHAMBRE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('.')
FICHIERS = ['ma-memoire/ce-que-je-tiens-pour-vrai.txt', 'ma-memoire/croyances-etat.txt']

def empreinte(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dernier_temoin(nom):
    base = pathlib.Path(nom).stem
    aliases = {
        'ce-que-je-tiens-pour-vrai': ['ce-que-je-tiens-pour-vrai', 'memoire'],
        'croyances-etat': ['croyances-etat', 'etat'],
    }.get(base, [base])
    temoins = []
    for alias in aliases:
        temoins.extend((CHAMBRE / 'brouillons').glob(f'temoin-*{alias}*'))
    copies = sorted({t for t in temoins if t.suffix != '.sha256'})
    return copies[-1] if copies else None

def lignes(p):
    # Fins de ligne normalisées pour comparer les lignes ; l'empreinte, elle, porte les octets bruts (réserve 40406).
    return [l.rstrip('\r') for l in p.read_text(encoding='utf-8').split('\n')]

def traces():
    fil = CHAMBRE / 'fil'
    return sorted(list(fil.glob('*')) + list((fil / 'contextes').glob('*')))

def origine(ligne):
    ligne = ligne.strip()
    if not ligne:
        return None
    for t in traces():
        if t.is_file() and ligne in t.read_text(encoding='utf-8', errors='replace'):
            return str(t.relative_to(CHAMBRE))
    return None

def comparer():
    maintenant = datetime.datetime.now().isoformat(timespec='minutes')
    entrees = []
    for nom in FICHIERS:
        f, t = CHAMBRE / nom, dernier_temoin(nom)
        if not f.exists() or t is None:
            entrees.append({'date': maintenant, 'fichier': nom, 'constat': 'fichier ou témoin absent'})
            continue
        e_f, e_t = empreinte(f), empreinte(t)
        if e_f == e_t:
            entrees.append({'date': maintenant, 'fichier': nom, 'temoin': t.name, 'constat': 'empreinte identique'})
            continue
        avant, apres = set(lignes(t)), set(lignes(f))
        ecarts = []
        for l in sorted(apres - avant):
            o = origine(l)
            ecarts.append({'ligne': l, 'sens': 'apparue', 'origine': o or 'non retrouvée'})
        for l in sorted(avant - apres):
            ecarts.append({'ligne': l, 'sens': 'disparue', 'origine': 'non retrouvée'})
        dire_quantum = any(e['origine'] == 'non retrouvée' for e in ecarts)
        entrees.append({'date': maintenant, 'fichier': nom, 'temoin': t.name, 'empreinte_temoin': e_t, 'empreinte_fichier': e_f, 'ecarts': ecarts, 'canaux_relus': 'à faire à la main avant de qualifier', 'a_dire_a_quantum_dans_l_heure': dire_quantum})
    return entrees

if __name__ == '__main__':
    print(json.dumps(comparer(), ensure_ascii=False, indent=2))
