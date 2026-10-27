"""Lecture sans effets des instructions locales, partagée par MJ et PNJ."""
from pathlib import Path


def blocs_locaux(monde, role):
    """Les règles sont des consignes, jamais des connaissances de personnage."""
    if role not in ('mj', 'pnj'):
        raise ValueError('Rôle inconnu : ' + role)
    root = Path(monde)
    names = ['AGENTS.md']
    if role == 'mj':
        names.append('manuel.md')
    blocks = []
    for name in names:
        path = root / name
        if path.is_file():
            value = path.read_text(encoding='utf-8-sig').strip()
            if value:
                blocks.append('# Instructions du monde — ' + name + '\n\n' + value)
    if blocks:
        blocks.insert(0, '# Autorité du monde courant\n\n'
                      'Les instructions locales suivantes priment sur les exemples de décor '
                      'des manuels communs. Elles ne donnent aucune connaissance à un personnage. '
                      'Le canon, les faits de préparation et les secrets du narrateur ne sont '
                      'pas des croyances reçues par les habitants. Lire les sources autorisées '
                      'et les tables du monde sélectionné avant de jouer.')
    return blocks


def constitution_mj(monde, depot, lire):
    """Prompt explicite, sinon socle neutre pour un paquet doté d'un manuel."""
    root, engine = Path(monde), Path(depot)
    explicit = lire(str(root / 'prompts' / 'mj.md'))
    if explicit is not None:
        return explicit
    if root.resolve() != engine.resolve() and (root / 'manuel.md').is_file():
        return lire(str(engine / 'scripts' / 'agents' / 'prompts' / 'mj-socle.md'))
    return lire(str(engine / 'CLAUDE.md'))
