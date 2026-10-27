"""Import initial explicite. Refuse de remplacer une partie ou un import existant."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")
SOURCE = Path(r"C:\Users\reyno\univers-magiciens")
MONDE = Path(__file__).resolve().parents[1]
DEST = MONDE / "canon" / "univers-magiciens"


def lire(p):
    return p.read_text(encoding="utf-8-sig")


def sauver(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def titre(t):
    return t.splitlines()[0].lstrip("# ").strip()


def section(t, nom):
    for bloc in re.split(r"(?m)(?=^## )", t):
        if nom in bloc.splitlines()[0]:
            return bloc.split("\n", 1)[1].strip()
    return ""


def importer():
    assert SOURCE.is_dir(), SOURCE
    assert not DEST.exists(), "Import déjà présent : aucune mise à jour automatique."
    for table in ("personnages", "maisons", "actes", "paroles", "evenements"):
        assert json.loads(lire(MONDE / "etat" / (table + ".json"))) == [], table + " non vide"
    assert not lire(MONDE / "etat/flux.jsonl").strip(), "Une scène existe déjà."
    fichiers = sorted(p for p in SOURCE.rglob("*") if p.is_file()
                      and ".git" not in p.relative_to(SOURCE).parts
                      and p.name not in {"AGENTS.md", "CLAUDE.md", ".gitignore"})
    provenance = []
    for p in fichiers:
        rel = p.relative_to(SOURCE)
        cible = DEST / rel
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, cible)
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        assert hashlib.sha256(cible.read_bytes()).hexdigest() == digest
        provenance.append({"fichier": rel.as_posix(), "octets": p.stat().st_size, "sha256": digest})

    organisations = []
    numeros = {}
    for p in sorted((DEST / "organisations").glob("[0-9]*.md")):
        t = lire(p)
        ident = p.stem.split("-", 1)[1]
        numeros[p.name[:2]] = ident
        nom = re.sub(r"^[^A-Za-zÀ-ÿ]+", "", titre(t))
        organisations.append({"id": ident, "nom": nom,
                              "devise": re.search(r"(?m)^> (.+)", t).group(1),
                              "siege_id": None, "suzerain_id": None, "canon": True})
    sauver(MONDE / "etat/maisons.json", organisations)

    personnages = []
    for p in sorted((DEST / "personnages").glob("[0-9]*.md")):
        t = lire(p)
        ident = p.stem.split("-", 1)[1]
        fonction = re.search(r"\*\*Fonction :\*\* (.+)", t).group(1).strip()
        personnages.append({"id": ident, "nom": titre(t), "maison_id": numeros[p.name[:2]],
                             "titre": fonction, "traits": [], "objectifs": [],
                             "portrait": {"physique": section(t, "Présence")},
                             "etat": "dormant", "lieu_id": None})
    sauver(MONDE / "etat/personnages.json", personnages)

    # Le corpus est de la documentation de conception, pas du savoir possédé
    # par un PNJ. La bibliothèque prévoit explicitement cette autorité.
    books = MONDE / "etat/maisons/_sans-maison/documents/books"
    ids = []
    index = []
    for p in sorted(DEST.rglob("*.md")):
        rel = p.relative_to(DEST)
        ident = "source-magies-" + slug(rel.with_suffix("").as_posix())
        t = lire(p)
        sauver(books / (ident + ".json"), {
            "id": ident, "maison_id": "_sans-maison", "titre": titre(t),
            "sous_titre": "Dossier de conception importé — " + rel.as_posix()
                + " — statuts retenu/proposé/ouvert conservés dans le texte",
            "type": "dossier", "pages": [t]})
        ids.append(ident)
        index.append({"id": ident, "source": rel.as_posix(), "titre": titre(t)})
    sauver(books / "_ordre.json", ids)
    sauver(MONDE / "etat/books/_ordre.json", [])
    sauver(MONDE / "habillage/habillage.json", {"titre": "magies — Magiciens et Non-Vivants"})
    sauver(MONDE / "import/provenance.json", {
        "source": str(SOURCE), "importe_le": datetime.now(timezone.utc).isoformat(),
        "revision": None, "revision_note": "Dépôt source sans premier commit ; empreintes des fichiers de travail.",
        "fichiers": provenance, "documents": index,
        "organisations": [x["id"] for x in organisations],
        "personnages": [x["id"] for x in personnages]})
    (MONDE / "canon/cadre.md").write_text(
        '# magies — cadre importé\n\n'
        'Source : [univers-magiciens](univers-magiciens/README.md).\n\n'
        'Le [cadre du monde](univers-magiciens/MONDE.md) fait autorité sur les choix de direction. '
        'Les [douze magies](univers-magiciens/MAGIES_ET_RELATIONS.md) et leurs fiches v1 décrivent les mécanismes. '
        'Les mentions retenu, proposé et ouvert sont conservées : importer ne vaut pas arbitrer.\n\n'
        'Civilisation médiévale originale gouvernée par des organisations polymagiques ; '
        'grandeur tragique et invention à l’échelle des forteresses vivantes. '
        'Les Non-Vivants viennent d’apparaître : instinctifs et moralement neutres, '
        'ils peuvent être supervisés par des retournés ambitieux.\n\n'
        'Aucune création d’énergie. Les gemmes stockent un travail réel. '
        'Les passages humains exigent des équipes aux deux extrémités ; '
        'l’Enchantement v1 exige au moins deux personnes distinctes. '
        'Les formulations anciennes « énergie du monde » se lisent sous cette correction.\n\n'
        'La géographie, les positions, la chronologie et le personnage joueur restent ouverts. '
        'Les deux atlas sont des propositions. La date an 1/mois 1/jour 1 à 08h00 '
        'reste un repère technique, pas une chronologie adoptée.\n', encoding='utf-8')
    (MONDE / "manuel.md").write_text(
        '# magies — manuel\n\n'
        'Sélectionner explicitement `CONSEIL_MONDE=magies` pour les outils.\n\n'
        'Lire [le cadre](canon/cadre.md), puis [MONDE.md](canon/univers-magiciens/MONDE.md), '
        '[les règles](canon/univers-magiciens/MAGIES_ET_RELATIONS.md) et les fiches concernées. '
        'Ce canon est autonome : aucun élément de Westeros, Charmed ou Lumina ne s’applique implicitement.\n\n'
        'Les six organisations sont enregistrées dans maisons.json. Les six personnages sont '
        'référencés en état dormant, sans position. Leurs biographies, motivations, techniques et '
        'liens restent des propositions comme dans leurs fiches. Les objectifs et intentions '
        'exécutables seront établis avec la situation de départ, sans inventer de priorités à cet import.\n\n'
        'Les dossiers sous `_sans-maison` sont des sources de conception, pas des objets possédés '
        'dans la fiction ni des connaissances automatiquement accessibles aux PNJ. '
        'Les scènes d’introduction et les épreuves techniques ne sont ni actes accomplis, '
        'ni paroles prononcées, ni résultats de simulation.\n\n'
        'Aucun siège joueur, lieu de départ, calendrier canonique, score de relation, '
        'effectif, stock, coût ou traité n’est fixé par cet import. '
        'La partie reste en phase de création. Respecter la Règle Zéro pour toute mise en scène ultérieure.\n', encoding='utf-8')
    contenu = ['# magies — contenu importé', '',
        f'{len(fichiers)} fichiers source copiés et vérifiés par SHA-256 ; {len(ids)} dossiers indexés.', '',
        'Six organisations et six personnages référencés dans l’état du moteur. '
        'La partie reste en création ; aucun personnage n’est activé.', '',
        '- [Cadre et décisions](canon/univers-magiciens/MONDE.md)',
        '- [Douze magies](canon/univers-magiciens/MAGIES_ET_RELATIONS.md)',
        '- [Organisations](canon/univers-magiciens/organisations/README.md)',
        '- [Personnages](canon/univers-magiciens/personnages/README.md)',
        '- [Non-Vivants](canon/univers-magiciens/non-vivants/README.md)',
        '- [Atlas 001 proposé](canon/univers-magiciens/geographie/monde-001/index.html)',
        '- [Atlas 002 proposé](canon/univers-magiciens/geographie/monde-002-portrait/index.html)',
        '- [Provenance et empreintes](import/provenance.json)', '',
        'Serveur : http://localhost:3198/ — `node serveur/serveur.js 3198 --monde magies`.', '',
        '## Dossiers importés', '']
    contenu += [f'- [{x["titre"]}](canon/univers-magiciens/{x["source"]})' for x in index]
    (MONDE / 'README.md').write_text('\n'.join(contenu)+'\n', encoding='utf-8')
    print(json.dumps({'fichiers': len(fichiers), 'dossiers': len(ids),
                      'organisations': len(organisations), 'personnages': len(personnages)}, ensure_ascii=False))


if __name__ == '__main__':
    importer()
