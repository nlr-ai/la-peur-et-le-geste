import json
import io

p = json.load(io.open('mondes/charmed/etat/paroles.json', encoding='utf-8'))
p.append({
  "id": "parole-leo-retour-fondateurs-2001-10-10-0724",
  "locuteur": "leo-wyatt",
  "texte": "Rien de précis. Quand je suis monté là-haut, ils ne m'ont ouvert aucun grand registre secret. Les Fondateurs savent que la Source s'agite et qu'elle cherche à tester vos défenses, mais le nom de Kharos le Briseur ne figure sur aucun de leurs registres. Rien sur lui, ni sur qui l'envoyait ce matin.",
  "destinataires": ["phoebe-halliwell", "piper-halliwell", "paige-matthews"],
  "lieu": "grenier",
  "date": "10.10.2001, 7 h 24"
})
io.open('mondes/charmed/etat/paroles.json', 'w', encoding='utf-8').write(json.dumps(p, ensure_ascii=False, indent=2))

a = json.load(io.open('mondes/charmed/etat/actes.json', encoding='utf-8'))
a.append({
  "id": "acte-leo-revient-fondateurs-2001-10-10-0724",
  "auteur": "leo-wyatt",
  "fait": "Leo revient du plan des Fondateurs et rapporte qu'aucune mention de Kharos le Briseur n'existe dans leurs registres, confirmant seulement que la Source commence à s'agiter.",
  "temoins": ["phoebe-halliwell", "piper-halliwell", "paige-matthews"],
  "lieu": "grenier",
  "date": "10.10.2001, 7 h 24"
})
io.open('mondes/charmed/etat/actes.json', 'w', encoding='utf-8').write(json.dumps(a, ensure_ascii=False, indent=2))
print("ETAT_MIS_A_JOUR")
