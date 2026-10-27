# -*- coding: utf-8 -*-
"""GUICHET MJ — le MJ tenu par une session Claude vivante (mode
« session-claude-guetteur »), au lieu d'un `claude -p` / `codex exec` par
reveil.

    python scripts/fournisseur.py --mj session-claude-guetteur
    python scripts/guichet_mj.py --guetter       # dans la session MJ, sous Monitor
    python scripts/guichet_mj.py --lire <id>
    python scripts/guichet_mj.py --rendre <id> "verdict"
    python scripts/guichet_mj.py --etat

CE FICHIER EST UNE FACADE (docs/organisation.md §2) : la matiere vit dans
agents/guichet_mj.py.
"""
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_d, _os.path.join(_d, "noyau")):
    if _p not in _sys.path:
        _sys.path.insert(0, _p)

from agents.guichet_mj import main  # noqa: E402

if __name__ == "__main__":
    main()
