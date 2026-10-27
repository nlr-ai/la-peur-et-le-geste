"""Ressources du chantier ; couverture et sens initial restent distincts."""
NOMS = dict(money='Clous', ration_cards='Bons de livraison', stamps='Gabarits', paper_ink='Chaux', false_papers='Huisseries', tracts='Carreaux', food='Sable', fuel='Huile de chantier', weapons='Outils', ammo='Pointes', explosives='Poudre de carrière', radio_set='Sonnette', intel='Cotes', london_credit='Agrément du bureau des plans')

def dessins(path, rect, circle):
    return {
      'money': path('M16 12v28l3 7 3-7V12M11 12h16M33 8v29l3 7 3-7V8M28 8h16')+circle(45,47,10)+path('M45 41v12m-4-9h8m-8 6h8'),
      'ration_cards': path('M12 9h37v45H12zM18 16h24M18 23h18M18 32h5v5h-5zM18 43h5v5h-5zM28 35h13m-13 11h8M49 18h7v40H20v-4')+path('M40 9v45',stroke_dasharray='2 4'),
      'stamps': rect(9,10,46,43)+circle(21,24,6)+rect(35,18,12,12)+path('M17 44l8-9 8 9zM39 39h9m-9 5h9M14 57h36'),
      'paper_ink': path('M17 12h30l-5 9 9 33H13l9-33zM22 21h20M19 12V7h26v5M20 48h24M25 34h14m-14 5h14')+path('M8 43q-7-7 0-15 7 8 0 15z'),
      'false_papers': rect(12,7,40,50)+rect(18,13,28,38)+path('M12 7l6 6m28 0 6-6M12 57l6-6m28 0 6 6M23 34q0-9 9-9t9 9M23 42h18')+circle(32,21,4),
      'tracts': path('M8 10h20v20H8zM36 10h20v20H36zM8 38h20v20H8zM36 38h20v20H36zM13 16h10m-10 5h7M41 16h10m-10 5h7M13 44h10m-10 5h7M41 44h10m-10 5h7'),
      'food': path('M18 10h28l-6 10q15 16 13 34H11q-2-18 13-34zM24 20h16M19 43h26M24 38h1m6-5h1m6 5h1m-10 12h1m10-2h1M25 10l-3-5m12 5V4')+path('M8 33h8m32 0h8'),
      'fuel': path('M12 52V30q0-8 8-8h18q7 0 7 8v22zM21 22V11h15v11M25 11V7h7v4M45 31l12-13v15L45 45M18 29h20')+path('M29 32q-12 13 0 16 12-3 0-16z'),
      'weapons': path('M9 13l30 11-4 12-30-11zM22 31L14 54l7 3 8-23M43 7l9 3-10 30-6-2zM39 39l-5 16 5 2 5-16M12 19l21 8'),
      'ammo': rect(8,32,48,25)+path('M8 40h48M16 32V12h5v20M13 12h11M30 32V8h5v24M27 8h11M44 32V15h5v17M41 15h11M17 47v5m15-5v5m15-5v5'),
      'explosives': path('M17 12h29l-5 10q13 12 12 32H11q-1-20 12-32zM23 22h18M24 39l6-9 3 7 8-3-4 9 6 5H22l5-5zM46 11l5-6m-1 12h8'),
      'radio_set': path('M14 45h36l-6-9V25q0-13-12-13T20 25v11zM27 50q5 8 10 0M32 12V6M48 10q11 6 10 18M47 18q5 3 5 9M11 18q-5 3-5 9'),
      'intel': path('M8 10h9v36h39v9H8zM23 50v5m8-5v5m8-5v5m8-5v5M8 20h5m-5 9h5M24 13h31v25H24zM29 19h21m-21 6h12M29 32h16M41 12v27'),
      'london_credit': path('M10 7h33l10 10v37H10zM43 7v11h10M17 15h17M17 24h27M17 31h15M18 46V35l8-5 8 5v11zM23 46v-7h6v7')+circle(46,45,10)+path('M40 45l4 4 7-8M41 54l-2 7 7-3 5 3 1-8'),
    }
