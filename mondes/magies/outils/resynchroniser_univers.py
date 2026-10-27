# -*- coding: utf-8 -*-
"""Remet le canon du monde au niveau de la source. À blanc par défaut.

L'import initial (`importer_univers.py`) refuse toute mise à jour : il est fait
pour ne jamais écraser une partie. Ce script fait l'autre moitié du travail —
il resynchronise `canon/univers-magiciens/` sur la source, dit ce qu'il change,
et ne touche à rien sans `--vraiment`.

    python outils/resynchroniser_univers.py              # le rapport
    python outils/resynchroniser_univers.py --vraiment   # la copie

Il ne touche jamais à `etat/`, ni aux fichiers propres du monde (`canon/cadre.md`,
`canon/implantations.md`, `canon/doctrine.md`…) : seule l'arborescence copiée
depuis la source est concernée.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")

SOURCE = Path(r"C:\Users\reyno\le-conseil2\import\univers-magiciens")
MONDE = Path(__file__).resolve().parents[1]
DEST = MONDE / "canon" / "univers-magiciens"
PROVENANCE = MONDE / "import" / "provenance.json"

# Mêmes exclusions que l'import initial : les consignes de collaboration du
# dépôt source ne sont pas du canon de monde.
HORS = {"AGENTS.md", "CLAUDE.md", ".gitignore"}


def empreinte(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fichiers_source():
    return sorted(p for p in SOURCE.rglob("*") if p.is_file()
                  and ".git" not in p.relative_to(SOURCE).parts
                  and p.name not in HORS)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def relivrer():
    """Les volumes `source-magies-*` que les gens peuvent ouvrir, refaits depuis le canon.

    Un livre laissé en arrière est pire qu'un livre absent : quelqu'un le lit et
    le croit. Les volumes propres au monde (ceux qui ne portent pas le préfixe)
    ne sont jamais touchés, et l'ordre du coffret les conserve.
    """
    books = MONDE / "etat/maisons/_sans-maison/documents/books"
    ordre_ancien = json.loads((books / "_ordre.json").read_text(encoding="utf-8")) if (books / "_ordre.json").exists() else []
    propres = [i for i in ordre_ancien if not i.startswith("source-magies-")]

    neufs, changes, ids, index = [], [], [], []
    for p in sorted(DEST.rglob("*.md")):
        rel = p.relative_to(DEST)
        ident = "source-magies-" + slug(rel.with_suffix("").as_posix())
        texte = p.read_text(encoding="utf-8-sig")
        titre = texte.splitlines()[0].lstrip("# ").strip()
        volume = {
            "id": ident, "maison_id": "_sans-maison", "titre": titre,
            "sous_titre": "Dossier de conception importé — " + rel.as_posix()
                          + " — statuts retenu/proposé/ouvert conservés dans le texte",
            "type": "dossier", "pages": [texte],
        }
        cible = books / (ident + ".json")
        avant = json.loads(cible.read_text(encoding="utf-8")) if cible.exists() else None
        if avant is None:
            neufs.append(rel.as_posix())
        elif avant.get("pages") != volume["pages"] or avant.get("titre") != titre:
            changes.append(rel.as_posix())
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(json.dumps(volume, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ids.append(ident)
        index.append({"id": ident, "source": rel.as_posix(), "titre": titre})

    (books / "_ordre.json").write_text(
        json.dumps(propres + ids, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return neufs, changes, index


def main():
    vraiment = "--vraiment" in sys.argv
    assert SOURCE.is_dir(), SOURCE
    assert DEST.is_dir(), "Pas d'import à resynchroniser : lancer importer_univers.py."

    neufs, changes, inchanges, provenance = [], [], [], []
    for p in fichiers_source():
        rel = p.relative_to(SOURCE)
        cible = DEST / rel
        digest = empreinte(p)
        if not cible.exists():
            neufs.append(rel.as_posix())
        elif empreinte(cible) != digest:
            changes.append(rel.as_posix())
        else:
            inchanges.append(rel.as_posix())
        provenance.append({"fichier": rel.as_posix(), "octets": p.stat().st_size, "sha256": digest})
        if vraiment and (not cible.exists() or empreinte(cible) != digest):
            cible.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, cible)
            assert empreinte(cible) == digest, rel

    # Ce que le monde a et que la source n'a plus : on le SIGNALE, on ne le supprime jamais.
    connus = {f["fichier"] for f in provenance}
    orphelins = sorted(p.relative_to(DEST).as_posix() for p in DEST.rglob("*")
                       if p.is_file() and p.relative_to(DEST).as_posix() not in connus)

    print("Source : %s" % SOURCE)
    print("Canon  : %s" % DEST)
    print("%d inchangé(s) · %d à mettre à jour · %d à ajouter · %d orphelin(s)"
          % (len(inchanges), len(changes), len(neufs), len(orphelins)))
    for titre, liste in (("À AJOUTER", neufs), ("À METTRE À JOUR", changes), ("ORPHELINS (jamais supprimés)", orphelins)):
        if liste:
            print("\n== %s (%d) ==" % (titre, len(liste)))
            for f in liste:
                print("  " + f)

    if not vraiment:
        print("\nÀ blanc. Rien n'a été écrit. Relancer avec --vraiment.")
        return

    neufs_l, changes_l, index = relivrer()
    print("\nLivres de source : %d ajouté(s), %d mis à jour." % (len(neufs_l), len(changes_l)))
    for f in neufs_l:
        print("  + " + f)

    ancienne = json.loads(PROVENANCE.read_text(encoding="utf-8")) if PROVENANCE.exists() else {}
    ancienne["source"] = str(SOURCE)
    ancienne["fichiers"] = provenance
    ancienne["documents"] = index
    ancienne.setdefault("resynchronisations", []).append({
        "le": datetime.now(timezone.utc).isoformat(),
        "source": str(SOURCE),
        "ajoutes": neufs, "mis_a_jour": changes,
        "inchanges": len(inchanges), "orphelins": orphelins,
    })
    PROVENANCE.write_text(json.dumps(ancienne, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\nCopié. Provenance et empreintes remises à jour.")


if __name__ == "__main__":
    main()
