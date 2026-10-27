"""Lecture littérale des icônes : personnes, équipements et infrastructures."""
from pathlib import Path
import importlib.util

def dessins(p,r,c,good,radio,ammo):
    spec=importlib.util.spec_from_file_location('actions_litterales',Path(__file__).with_name('actions-resistance-original.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    a=module.dessins(p,r,c)
    out={'action-'+k:v for k,v in a.items()}
    for k in ('car','truck','fuel','hunting_gun','cart','bicycle','cash','jewellery','gold'):out['bien-'+k]=good(k,k)
    telephone=p('M10 41l8-15h28l8 15v10H10zM14 22q18-13 36 0l3-7Q32 1 11 15zM49 23q14 8 7 15')+c(32,37,9)+c(32,37,3)
    out.update(munition=ammo('shotgun_cartridge'),radio=radio('mains'),telephone=telephone,tabac=r(14,20,36,36)+p('M14 31h36M20 20V8h6v12m7 0V5h6v15M21 43h22m-22 6h22'))
    doc=r(12,8,40,48)+p('M20 18h24m-24 8h24m-24 8h16')
    out.update({
      'ressource-money':good('cash','cash'),
      'ressource-ration_cards':r(10,11,44,42)+p('M10 23h44M19 23v30m12-30v30m12-30v30M10 33h44m-44 10h44M17 17h20'),
      'ressource-stamps':p('M18 34V21q0-15 14-15t14 15v13M11 34h42v9H11zM8 51h48M21 56h23'),
      'ressource-paper_ink':p('M8 45V9h30v31H14M8 45h28M14 16h17m-17 7h17m-17 7h12')+r(38,36,18,20)+p('M42 36v-6h10v6M41 44h12M47 24l8-17'),
      'ressource-false_papers':r(7,14,50,36)+r(13,20,17,24)+c(21,26,4)+p('M16 40v-4q5-7 10 0v4M36 24h15m-15 7h15m-15 7h9')+c(47,43,5),
      'ressource-tracts':p('M8 46V9h35v38H8M14 15h22v9H14zM14 30h22m-22 6h22m-22 6h12M16 52h35V16M23 58h34V22'),
      'ressource-food':p('M8 38q0-22 24-22t24 22v12H8zM18 30l7-7m4 7 7-7m4 8 6-6M8 44h48M20 55h24'),
      'ressource-fuel':good('fuel','fuel'),
      'ressource-weapons':good('hunting_gun','hunting_gun'),
      'ressource-ammo':ammo('shotgun_cartridge'),
      'ressource-explosives':r(10,25,12,29,3)+r(26,25,12,29,3)+r(42,25,12,29,3)+p('M10 35h44m-44 10h44M16 25V14h32v11M32 14V7m-5-1 5 1 5-1'),
      'ressource-radio_set':radio('mains_shortwave'),
      'ressource-intel':doc+c(39,40,11)+p('M47 48l10 10'),
      'ressource-london_credit':doc+p('M18 44l6 6 10-14')+c(45,43,9)+p('M40 52l-2 7 7-3 7 3-2-7'),
    })
    def soldier():return p('M18 22q0-15 14-15t14 15M14 22h36M22 22v9q10 12 20 0v-9M13 56V45q19-14 38 0v11M32 39v17M18 45l25 11')
    rail=p('M22 6L10 58M42 6l12 52M18 18h28m-31 12h34m-37 12h40m-43 12h46')
    wire=p('M15 7v50m34-50v50M6 17h18m16 0h18M9 12v5m12-5v5m22-5v5m12-5v5M15 17q17 12 34 0M15 24q17 12 34 0M8 57h14m20 0h14')
    def person(x,y):return c(x,y,4)+p(f'M{x-7} {y+22}v-9q7-9 14 0v9')
    out.update({
      'terme-soldat':soldier(),
      'terme-officier':soldier()+p('M20 15h24M26 48l6-5 6 5-6 4z'),
      'terme-patrouille':person(17,19)+person(42,25)+p('M9 13q20-18 43 0m-6-7 6 7h-9M14 52h36m-6-5 6 5-6 5'),
      'terme-sentinelle':person(28,20)+p('M17 15q11-14 22 0M44 9v46m-4-14h8M18 55l10-13 10 13'),
      'terme-garnison':p('M8 54V23h48v31M8 23l24-14 24 14M16 30h7v8h-7zM41 30h7v8h-7zM27 54V36h10v18M32 9V3h15v7H32'),
      'terme-gendarme':person(32,27)+p('M19 19h26l-4-10H23zM16 19h32M23 42l18 11M18 57h28'),
      'terme-indicateur':person(25,22)+p('M12 18h26M17 17l3-9h12l3 9M39 24h18v13h-8l-6 6v-6M44 29h8'),
      'terme-barrage':p('M7 24h50v13H7zM13 37v19m38-19v19M10 24l12 13m1-13 12 13m1-13 12 13M17 8h30v10H17z'),
      'terme-controle':r(8,16,35,29)+c(19,26,4)+p('M13 39q0-10 6-10t6 10M30 24h7m-7 7h7M36 47l8 8 14-19'),
      'terme-fouille':a['unmask_informer']+p('M8 55h22'),
      'terme-rafle':person(17,25)+person(44,25)+p('M7 16h50M7 8v8l6-5m44-3v8l-6-5M8 52h48M26 23h12v23H26z'),
      'terme-arrestation':c(19,35,11)+c(45,35,11)+p('M27 31h10m-10 8h10M14 31h10v8H14M40 31h10v8H40'),
      'terme-couvre-feu':p('M42 8q-13 20 10 24-26 10-28-11Q24 9 42 8M8 56V36h13v20M25 56V42h13v14M43 56V37h13v19M12 42h5m30 1h5'),
      'terme-alerte':p('M32 7L5 55h54zM32 23v15')+c(32,46,2),
      'terme-voie-ferree':rail,
      'terme-ligne-telephonique':wire,
    })
    return out
