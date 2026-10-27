"""Actions propres à La peur et le geste, hors du catalogue Modern Front."""

def actions(path, rect, circle):
    def person(x, y):
        return circle(x, y, 5)+path(f'M{x-8} 34v-4q8-10 16 0v4')
    return [
        dict(key='hold_meeting', name='Organiser une réunion', category='recruit',
             couvert='Tenir une réunion de chantier',
             # Code : l'établi, le plan déroulé dessus, le crayon qui y pointe.
             code=rect(7,30,50,7)+path('M13 37v19m38-19v19M13 48h38')
                  +path('M15 30l5-12h24l5 12M22 24h20M27 18v12m10-12v12M46 10l-6 10'),
             # Clair : trois personnes autour d'une table.
             clair=person(18,20)+person(32,16)+person(46,20)
                   +rect(8,34,48,6)+path('M14 40v16m36-16v16')),
    ]
