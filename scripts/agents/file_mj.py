"""File FIFO inter-processus d'une session MJ ; la mort libère le verrou OS."""
import contextlib
import os
import time
import uuid

from agents import runtime


class Interrompu(RuntimeError):
    def __init__(self, evenements):
        super().__init__("MJ interrompu par un nouveau message")
        self.evenements = list(evenements)


def plus_recent(ticket):
    """Un autre message vivant attend après le calcul courant."""
    dossier, courant = os.path.split(ticket)
    try:
        for nom in os.listdir(dossier):
            if not nom.endswith(".json") or nom <= courant:
                continue
            d = runtime._lire_json(os.path.join(dossier, nom), {})
            if d.get("processus") and runtime._identite_processus(d.get("pid")) == d["processus"]:
                return True
    except (OSError, ValueError):
        pass
    return False


@contextlib.contextmanager
def attendre(session):
    dossier = os.path.join(runtime.DOSSIER_RUNTIME, "mj-files", str(session))
    os.makedirs(dossier, exist_ok=True)
    ticket = os.path.join(dossier, "%020d-%s.json" % (time.time_ns(), uuid.uuid4().hex))
    identite = runtime._identite_processus(os.getpid())
    runtime._ecrire_json(ticket, {"pid": os.getpid(), "processus": identite})
    verrou = open(os.path.join(dossier, "session.lock"), "a+b")
    if os.fstat(verrou.fileno()).st_size == 0:
        verrou.write(b"0")
        verrou.flush()
    pris = False
    try:
        while not pris:
            tickets = []
            for nom in sorted(os.listdir(dossier)):
                if not nom.endswith(".json"):
                    continue
                chemin = os.path.join(dossier, nom)
                try:
                    d = runtime._lire_json(chemin, {})
                    if runtime._identite_processus(d.get("pid")) == d.get("processus") and d.get("processus"):
                        tickets.append(chemin)
                    else:
                        os.remove(chemin)
                except (OSError, ValueError):
                    continue
            if tickets and tickets[0] == ticket:
                try:
                    verrou.seek(0)
                    if os.name == "nt":
                        import msvcrt
                        msvcrt.locking(verrou.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    pris = True
                except OSError:
                    pass
            if not pris:
                time.sleep(.1)
        # Compatibilité avec une session déjà lancée avant ce déploiement.
        while any(d.get("homme") == "mj" and d.get("session") == str(session)
                  for d in runtime.activites_vivantes()):
            time.sleep(.2)
        yield ticket
    finally:
        verrou.close()
        try:
            os.remove(ticket)
        except FileNotFoundError:
            pass
