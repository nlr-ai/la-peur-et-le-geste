"""Biens déguisés en outillage, quincaillerie et fournitures d'atelier."""
def dessins(p, r, c):
    out={}
    def add(key,name,svg): out[key]=(name,svg)
    def grain(): return p('M18 29h12m8 6h9')
    def wheels(xs,y=49): return ''.join(c(x,y,5)+c(x,y,1) for x in xs)
    for i,(key,name) in enumerate([('car','Servante roulante'),('citroen_traction','Servante à chevrons'),('peugeot_202','Servante arrondie'),('renault_juvaquatre','Servante carrée'),('old_car','Servante ancienne')]):
        tops=[p('M13 20h38v21H13z'),p('M13 20h38v21H13zM26 26l6-4 6 4m-12 6 6-4 6 4'),p('M13 41V28q0-13 19-13t19 13v13z'),p('M13 16h38v25H13zM32 16v25'),p('M13 20h38v21H13zM10 15h44M20 20v21m24-21v21')][i]
        add('bien-'+key,name,tops+p('M8 41h48M13 20V9h10')+wheels([18,46]))
    for i,(key,name) in enumerate([('truck','Chariot à bois'),('van','Chariot couvert'),('lorry','Chariot de charge'),('gazogene_lorry','Chariot à chaudière')]):
        s=r(7,26,43,16)+p('M7 33h43M13 26v16m30-16v16M50 42l6-24')+wheels([16,42])
        s += [p('M15 26V13h29v13M19 19h20'),p('M10 26V12h37v14M10 18h37'),p('M10 20h40M10 14h40M10 8h40'),r(35,7,15,18,4)+p('M40 7V3m5 4V3M16 13h13v13H16z')][i]
        add('bien-'+key,name,s)
    add('bien-fuel','Réserve d’huile',r(13,17,36,38,3)+p('M22 17V8h17v9M49 25l9-11v16l-9 8M21 25h20M30 31q-12 16 1 17 13-2-1-17z'))
    for key,name,s in [
        ('hunting_gun','Outillage de coupe',p('M10 12h30v13H10zM23 25v31h6V25M43 9l10 4-12 33-6-3zM35 43l-3 11 6 2 3-10')),
        ('shotgun','Ciseau double',p('M20 8h8v27h-8zM36 8h8v27h-8zM24 35v8h16v-8M28 43v13h8V43M20 13h8m8 0h8')),
        ('rifle_22','Ciseau fin',p('M29 6h6v32h-6zM26 38h12v18H26zM29 10h6M30 43v8')),
        ('revolver','Vilebrequin',p('M38 9v12H21v22h17v12M30 9h16M33 55h10')+r(15,26,12,13,4)+c(38,15,4)),
        ('lebel','Ciseau ancien',p('M27 5h10v35H27zM24 40h16v17H24zM27 12h10M24 46h16M32 5v35'))]: add('bien-'+key,name,s)
    for i,(key,name) in enumerate([('cart','Plateau roulant'),('farm_cart','Plateau à deux roues'),('wagon','Plateau à quatre roulettes'),('trap','Plateau à dossier')]):
        s=p('M8 36h43v7H8zM51 39l7-22')+wheels([15,45])
        s += [p('M15 36V22h29v14M19 28h21'),p('M8 30h43M14 30v6m30-6v6'),c(27,49,4)+c(35,49,4)+p('M12 27h34v9H12z'),p('M14 36V14h8v22M22 29h20v7')][i]
        add('bien-'+key,name,s)
    for i,(key,name) in enumerate([('bicycle','Diable d’atelier'),('mens_bicycle','Diable à traverse'),('ladies_bicycle','Diable ouvert'),('delivery_bicycle','Diable à caisse')]):
        s=p('M17 10h24v39H17zM17 10V5h8M41 49h15M17 49H9')+wheels([17,41],54)
        s += [p('M17 24h24m-24 14h24'),p('M17 18l24 24M41 18L17 42'),p('M17 21q12 22 24 0'),r(10,22,38,21)+p('M10 29h38M16 22v21m26-21v21')][i]
        add('bien-'+key,name,s)
    add('bien-cash','Clous en réserve',r(8,25,48,30)+p('M8 34h48M19 25V9m-5 0h10M32 25V6m-5 0h10M45 25V12m-5 0h10')+c(32,44,6))
    jewel={
      'jewellery':('Quincaillerie fine',r(8,20,48,35)+p('M8 29h48M8 20l9-11h30l9 11')+c(20,41,6)+r(31,36,15,10)),
      'wedding_ring':('Bague de serrage',c(32,31,19)+c(32,31,12)+p('M46 44l8 8M42 48l8 8M49 48l5-5M12 10l4-4m-4 0 4 4')),
      'gold_chain':('Chaînette de suspension',p('M10 14h44M17 14v7m30-7v7M17 34q15 17 30 0M32 44v9')+r(12,20,10,15,5)+r(42,20,10,15,5)+c(32,55,4)),
      'brooch':('Rosace de fixation',c(32,31,17)+c(32,31,7)+p('M12 31h40M32 11v40M20 19l24 24M44 19L20 43M14 54h36')),
      'earrings':('Crochets jumelés',p('M13 15a7 7 0 0 1 14 0v14q0 11-11 11V26M37 15a7 7 0 0 1 14 0v14q0 11-11 11V26')+c(20,47,7)+c(44,47,7)),
      'gold_watch':('Cadran d’établi',c(32,33,20)+c(32,33,15)+p('M27 13V6h10v7M32 22v12l9 5M13 51l-5 5m43-5 5 5M11 14l-5-5')),
      'signet_ring':('Bague à tête carrée',c(32,37,16)+c(32,37,10)+r(20,8,24,19,3)+p('M26 14h12v7H26z')),
      'bracelet':('Collier de serrage',p('M16 17q-14 33 16 36 30-3 16-36M22 20q-11 24 10 27 21-3 10-27')+r(17,11,30,10)+p('M23 11v10m6-10v10m6-10v10m6-10v10')),
      'pearl_necklace':('Chapelet de chevilles',p('M11 14v12q0 29 21 29t21-29V14M11 14h42')+''.join(c(x,y,4) for x,y in [(12,28),(16,40),(24,48),(36,49),(46,41),(52,28)])),
    }
    for key,(name,s) in jewel.items(): add('bien-'+key,name,s)
    for i,(key,name) in enumerate([('gold','Rondelles de laiton'),('napoleon_20','Grande rondelle'),('napoleon_10','Petite rondelle'),('napoleon_head','Rondelle poinçonnée'),('louis_or','Rondelle ancienne')]):
        radius=15 if i==2 else 21
        s=c(32,32,radius)+c(32,32,7)
        s += [p('M12 47q20 20 40 0M16 53q16 12 32 0'),p('M19 18l3 3m20-3-3 3M18 43l4-3m20 3-3-3'),p('M29 11h6M29 53h6'),p('M22 17h20M26 12v10m12-10v10'),p('M32 11v11m0 20v11M11 32h11m20 0h11M18 18l8 8m12 12 8 8')][i]
        add('bien-'+key,name,s)
    for i,(key,name) in enumerate([('shotgun_cartridge','Pointes larges'),('cartridge_22lr','Pointes fines'),('revolver_8mm','Pointes courtes'),('lebel_8mm','Pointes longues')]):
        width=[7,3,6,5][i]; top=[15,8,23,6][i]
        s=r(7,45,50,12)+p('M12 51h40')
        for x in [16,30,44]: s+=p(f'M{x} {top}h{width}v{40-top}l-{width/2} 5-{width/2}-5zM{x-2} {top}h{width+4}')
        add('munition-'+key,name,s)
    for i,(key,name) in enumerate([('crystal','Sonnette à contact'),('battery','Sonnette autonome'),('mains','Sonnette filaire'),('mains_shortwave','Sonnette à longue portée')]):
        s=p('M14 44h32l-5-9V25q0-12-11-12T19 25v10zM26 49q4 8 8 0M30 13V8')
        s += [p('M8 55h45M48 44V24l8-10M52 11l7 4'),r(46,31,12,23)+p('M49 31v-4h6v4M49 39h6m-3-3v6M49 48h6'),p('M46 44h8V16h-7V9m7 7V9M44 9h13'),p('M46 8q15 8 12 23M45 17q8 4 7 13M8 15q-7 8-3 16')][i]
        add('radio-'+key,name,s)
    add('telephone','Tube porte-voix',p('M13 10h15v9H13zM17 19v18q0 14 15 14t15-14V24M41 24h12l7-12H34zM13 6v4m15-4v4M24 35h16M28 30v10'))
    for i,(key,name) in enumerate([('gauloises','Crayons d’atelier'),('gitanes','Crayons de traçage'),('celtiques','Crayons de précision'),('boyards','Crayons de charpentier'),('gris','Copeaux en sachet')]):
        if i==4:
            s=p('M14 13h36l-5 9 7 32H12l7-32zM19 22h26M20 34q12-10 21 0t-21 7m3 6h17M16 8h32')
        else:
            s=r(13,28,38,28)+p('M13 36h38M18 51h27')
            for j,x in enumerate([20,30,40]):
                y=7+((i+j)%3)*4
                s+=p(f'M{x} 28V{y+7}l3-7 3 7v{21-y}M{x} {y+7}h6')
            s += [p('M21 42h21'),p('M21 44q10-8 21 0'),c(32,45,5),p('M22 42h20v6H22z')][i]
        add('tabac-'+key,name,s)
    return out
