"""Interface locale du moteur Esprit, liée uniquement à 127.0.0.1."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

from moteur import simuler
from scorer import lire, applicable

ICI = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    def envoyer(self, code, contenu, mime="application/json; charset=utf-8"):
        if not isinstance(contenu, bytes):
            contenu = json.dumps(contenu, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(contenu)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(contenu)

    def do_GET(self):
        if self.path == "/":
            return self.envoyer(200, (ICI / "index.html").read_bytes(), "text/html; charset=utf-8")
        if self.path == "/api/catalogue":
            b = lire(ICI / "bareme.json")
            mod_actions = {cle: [k for k, m in b["modificateurs"].items() if applicable(m, a)]
                           for cle, a in b["actions"].items()}
            return self.envoyer(200, {"bareme": b, "cas": lire(ICI / "cas.json"),
                                     "mod_actions": mod_actions})
        self.envoyer(404, {"erreur": "Adresse inconnue."})

    def do_POST(self):
        if self.path != "/api/simuler":
            return self.envoyer(404, {"erreur": "Adresse inconnue."})
        origin = self.headers.get("Origin")
        if origin and origin != f"http://{self.headers.get('Host')}":
            return self.envoyer(403, {"erreur": "Origine non autorisée."})
        try:
            taille = int(self.headers.get("Content-Length", "0"))
            if not 0 < taille <= 500000:
                raise ValueError("Taille de requête invalide.")
            data = json.loads(self.rfile.read(taille))
            if not isinstance(data, dict):
                raise ValueError("Requête invalide.")
            self.envoyer(200, simuler(lire(ICI / "bareme.json"), data.get("passes")))
        except (ValueError, TypeError, KeyError) as exc:
            self.envoyer(400, {"erreur": str(exc)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=3208)
    args = parser.parse_args()
    print(f"Atelier Esprit : http://127.0.0.1:{args.port}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
