# -*- coding: utf-8 -*-
"""Worker interne des appels CAST. Ne constitue pas une facade publique."""
import io
import json
import os
import sys

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from agents import runtime, work_identity  # noqa: E402


def main():
    requete = sys.argv[1]
    if len(sys.argv) > 2:
        # Lance par WMI (agents/detache.py) : aucun flux herite, il ouvre son
        # journal lui-meme.
        journal = io.open(sys.argv[2], "a", encoding="utf-8", buffering=1)
        sys.stdout = sys.stderr = journal
    with io.open(requete, encoding="utf-8") as f:
        charge = json.load(f)
    # Ni l'environnement n'est herite : il voyage dans la requete.
    os.environ.update(charge.get("environnement") or {})
    try:
        # La bascule globale peut changer apres le spawn : ce CAST garde le
        # fournisseur annonce a son depart, sans course avec l'operateur.
        os.environ["LE_CONSEIL_FOURNISSEUR"] = charge["fournisseur"]
        rep = runtime.appeler(**charge["appel"])
        artifact = None
        trace = charge.get("trace") or {}
        if trace:
            try:
                from agents import trace as vecu
                artifact = vecu.deposer(
                    trace["qui"], charge["appel"]["session_id"],
                    etiquette=trace.get("etiquette"),
                    transcript=rep.get("transcript_path"),
                    provider=rep.get("provider"),
                    contexte_id=trace.get("contexte_id"),
                    ref=trace.get("ref"))
            except Exception:
                pass
        identity = rep.get("continuous_work_identity")
        if identity:
            work_identity.terminer_attempt(
                identity, rep.get("compute_event_id"), "succeeded",
                term=bool(artifact), artifact=artifact)
        print(json.dumps(rep, ensure_ascii=False), flush=True)
        return 0
    except BaseException:
        identity = (charge.get("appel") or {}).get("work_identity")
        if identity:
            try:
                work_identity.terminer_attempt(
                    identity, None, "failed", term=False)
            except Exception:
                pass
        raise
    finally:
        try:
            os.unlink(requete)
        except OSError:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
