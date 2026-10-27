"""Repères géographiques arrondis et axes schématiques : aucune route de jeu."""
def enrichir(geo, point):
    def trace(coords):
        return 'M'+'L'.join(','.join(map(str,point(*p))) for p in coords)
    axes = [
      ('beauly','Chemin vers Beauly', [(-4.224,57.478),(-4.28,57.48),(-4.34,57.47),(-4.40,57.46),(-4.459,57.483)]),
      ('dores','Chemin de Dores', [(-4.224,57.478),(-4.245,57.445),(-4.29,57.41),(-4.333,57.382)]),
      ('drumnadrochit','Chemin de la rive du Loch Ness', [(-4.224,57.478),(-4.28,57.445),(-4.36,57.405),(-4.42,57.365),(-4.48,57.335)]),
      ('clava','Chemin vers Culloden et Clava', [(-4.224,57.478),(-4.15,57.475),(-4.10,57.47),(-4.075,57.455),(-4.074,57.438)]),
      ('nairn','Chemin côtier vers Nairn', [(-4.224,57.478),(-4.15,57.49),(-4.07,57.505),(-3.96,57.54),(-3.875,57.585)]),
      ('kiltarlity','Chemin de Kiltarlity', [(-4.459,57.483),(-4.478,57.452),(-4.49,57.436)])]
    geo['routes']=[dict(id='inverness-'+i,nom=n+' — tracé indicatif',d=trace(c)) for i,n,c in axes]
    reperes=[('dores','Dores',-4.333,57.382),('drumnadrochit','Drumnadrochit',-4.48,57.335),('kiltarlity','Kiltarlity',-4.49,57.436),('nairn','Nairn',-3.875,57.585),('clava','Cairns de Clava',-4.074,57.438),('culloden','Lande de Culloden',-4.094,57.477),('dochfour','Loch Dochfour',-4.337,57.417),('ness','Rivière Ness',-4.259,57.452),('nairn-riviere','Rivière Nairn',-4.03,57.429),('beauly-firth','Beauly Firth',-4.325,57.51),('craig-phadrig','Craig Phadrig',-4.273,57.484),('urquhart','Château d’Urquhart',-4.442,57.324)]
    ids={b['id'] for b in geo['bourgs']}
    geo['bourgs'] += [dict(id=i,nom=n,p=point(x,y)) for i,n,x,y in reperes if i not in ids]
    # Cours d’eau locaux simplifiés, rubans vectoriels continus.
    for coords in [[(-4.333,57.424),(-4.30,57.436),(-4.266,57.449),(-4.246,57.465),(-4.229,57.479),(-4.221,57.495)], [(-4.23,57.36),(-4.15,57.40),(-4.074,57.438),(-4.02,57.46),(-3.95,57.51),(-3.875,57.585)]]:
        from shapely.geometry import LineString
        poly=LineString(coords).buffer(.0009)
        geo['rivieres'] += trace(list(poly.exterior.coords))+'Z'
