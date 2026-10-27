"""Lecture technique des calculs vivants, sans modifier le monde ni lancer d'agent."""
import json
from agents.expose import runtime

print(json.dumps({"actifs": runtime.activites_vivantes()}))
