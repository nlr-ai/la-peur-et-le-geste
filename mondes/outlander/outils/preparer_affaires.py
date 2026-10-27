"""Modèles et cahiers personnels Outlander ; aucun contenu stratégique inventé."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def table(title, columns, rows=()):
    return {'titre': title, 'colonnes': columns,
            'lignes': [{'cellules': row} for row in rows]}

CATEGORIES = ['fins-et-doctrine', 'personnes-et-relations', 'pouvoir-et-acces',
              'moyens-materiels', 'savoirs-et-secrets', 'engagements-et-temps',
              'strategie-et-alternatives', 'zones-a-peindre']
THINGS = ['lieux-et-passages', 'objets-et-documents', 'ressources-et-populations',
          'organisations-et-dispositifs', 'usages-et-institutions', 'situations-et-processus']

def affaire(pid):
    return {
        'id': 'affaire-' + pid, 'titre': 'Les affaires de ' + pid,
        'sous_titre': 'Cahier stratégique personnel — préparation du monde et conduite de mes affaires',
        'type': 'affaire', 'tenu_par': pid, 'acteur_id': pid, 'prive': True,
        'pages': [
            'Une affaire durable par PNJ qui porte une stratégie. Plusieurs fins peuvent y coexister. '
            'Les catégories décrivent les dimensions à peindre, pas huit objectifs obligatoires. '
            'Ce cahier de simulation n’est pas la preuve d’un carnet physiquement fabriqué.',
            'Je peux établir en préparation les détails ordinaires, personnes secondaires, objets, '
            'lieux, habitudes et ressources plausibles nécessaires à mon implantation, sans contredire '
            'le canon ni les faits acquis. Je marque chaque ajout comme peint. Un ajout conséquent '
            'doit avoir une provenance, des limites, des liens et des conséquences cohérents ; '
            'je ne fais pas surgir le moyen décisif qui efface mon problème. Un autre personnage '
            'reçoit sa fiche et sa propre session avant toute parole, décision ou action jouée.',
            'Établi, peint, hypothèse, inconnu sont des statuts distincts. Peindre un état initial '
            'n’accomplit pas une action future. Fabriquer pendant le jeu exige matériaux, outils, '
            'compétence et durée ; une issue dépendant d’autrui reste ouverte. Mes croyances restent '
            'distinctes de la réalité, même si ma session contribue à préparer le monde.',
            'Les adresses C.1, V.1, K.1 et P.1 sont locales à ce cahier. Ne pas inventer de numéro '
            'global ; utiliser les outils d’adressage si un contexte global est nécessaire. '
            'Les trous ci-dessous sont écrits par moi ; ils ne remplacent pas les trous calculés du graphe.'
        ],
        'tables': [
            table('Ouverture', ['Champ', 'Contenu'], [
                ['Porteur', pid], ['Périmètre', 'Mes intérêts, mon implantation et les affaires que je poursuis.'],
                ['État de préparation', 'À remplir par mon incarnation.'],
                ['Registre compagnon', 'registre-etats-' + pid]]),
            table('Dimensions à peindre', ['Catégorie', 'Ce que je pose', 'Statut', 'Source ou provenance', 'Renvois'],
                  [[category, '', 'inconnu', '', ''] for category in CATEGORIES]),
            table('🎯 États cibles', ['N°', "L'état visé", 'Ce qui doit être vrai', 'La preuve', 'Jour dû', 'Importance']),
            table('🔒 Verrous', ['N°', 'Le verrou', 'Bloque', 'La preuve']),
            table('🗝️ Clefs', ['N°', 'La clef', 'Ouvre', 'Prix et limites']),
            table('⚔️ Actions', ['N°', "L'action", 'Réalise', 'Dépend de', 'Qui', 'Où', 'La preuve', 'État', 'Jour dû', 'Jour fait', 'Note']),
            table('Stratégie et alternatives', ['Fin', 'Approche', 'Pourquoi', 'Alternative', 'Changer si', 'Moyens engagés']),
            table('Moyens disponibles', ['Référence', 'Nature', 'Accès réel', 'Quantité ou portée', 'Limites', 'Provenance']),
            table('Trous de préparation', ['Trou', 'Catégorie', 'Ce qui en dépend', 'Traitement', 'Qui', 'Échéance', 'État', 'Résultat']),
            table('Connaissances et croyances', ['Sujet', 'Ce que je crois', 'Source reçue', 'Ce que j’ignore', 'Référence de réalité']),
            table('Résultats et révisions', ['Date', 'Fait ou découverte', 'Preuve', 'Ce que je change', 'Renvois'])
        ]}

def registre(pid):
    return {'id': 'registre-etats-' + pid, 'titre': 'Les choses suivies par ' + pid,
            'sous_titre': 'États initiaux peints et états matériels établis ; aucune omniscience accordée au porteur',
            'type': 'registre', 'tenu_par': pid, 'acteur_id': pid, 'prive': True,
            'pages': ['Catégories : ' + ', '.join(THINGS) + '. Une ligne par chose ou situation. '
                      'L’identité est une référence stable ; plusieurs PNJ citent la même chose au lieu de la recréer. '
                      'Quand une table canonique du moteur porte déjà le fait, elle garde autorité : la ligne '
                      'renvoie à cette adresse. Les évolutions arithmétiques vont dans les mains de leur maison. '
                      'Les lignes purement descriptives sont leur propre autorité jusqu’à matérialisation. '
                      'Accès au cahier technique n’est pas connaissance du personnage : Qui sait quoi doit être respecté.'],
            'colonnes': ['Référence', 'Catégorie', 'Identité et fonction', 'Où', 'Détenteur ou responsable',
                         'État présent', 'Quantité ou propriétés', 'Usages et limites', 'Liens',
                         'Évolution et échéances', 'Statut', 'Source ou provenance', 'Qui sait quoi',
                         'Date de mise à jour', 'Autorité existante'], 'lignes': []}

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = json.loads(path.read_text(encoding='utf-8'))
        if existing != value:
            raise SystemExit('Cahier déjà modifié : préservé, ' + str(path))
        return
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    write(ROOT / 'modeles' / 'affaire-pnj.json', affaire('porteur'))
    write(ROOT / 'modeles' / 'registre-etats.json', registre('porteur'))
    people = json.loads((ROOT / 'etat' / 'personnages.json').read_text(encoding='utf-8-sig'))
    seats = json.loads((ROOT / 'etat' / 'joueurs.json').read_text(encoding='utf-8-sig'))
    pj = {s['personnage_id'] for s in seats}
    count = 0
    for person in people:
        if person['etat'] != 'actif' or person['id'] in pj:
            continue
        pid = person['id']
        write(ROOT / 'chambres' / pid / 'books' / ('affaire-' + pid + '.json'), affaire(pid))
        write(ROOT / 'chambres' / pid / 'books' / ('registre-etats-' + pid + '.json'), registre(pid))
        count += 1
    print(f'{count} cahiers stratégiques et {count} registres compagnons préparés ; aucune stratégie remplie.')
