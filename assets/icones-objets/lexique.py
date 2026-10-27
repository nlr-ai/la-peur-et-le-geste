"""Vocabulaire de couverture proposé pour le jeu, sans effet de simulation."""
ACTIONS = {
'sound_out':'Examiner une candidature','test_recruit':'Faire travailler à l’essai','induct':'Embaucher','form_cell':'Constituer une équipe','win_notable':'Gagner un maître d’ouvrage','shelter_refractory':'Loger un ouvrier de passage','link_london':'Se rattacher au bureau des plans',
'steal_stamps':'Récupérer des gabarits','get_stamps_inside':'Obtenir les gabarits du magasin','set_workshop':'Ouvrir une menuiserie','forge_papers':'Ajuster des huisseries','set_safehouse':'Louer une remise','change_identity':'Changer d’huisserie','win_farm':'Trouver une sablière','set_cover_business':'Ouvrir une enseigne',
'open_mailbox':'Ouvrir un comptoir','carry_message':'Porter un bon','set_radio':'Installer une sonnette','transmit':'Appeler le bureau des plans','set_press':'Ouvrir un atelier de peinture','print_tracts':'Préparer les carreaux','spread_tracts':'Poser les carreaux',
'watch_trains':'Mesurer les longues pièces','scout_garrison':'Relever le chantier voisin','copy_files':'Reproduire les cotes','unmask_informer':'Repérer le bois véreux',
'homologate_dz':'Faire agréer la cour','receive_drop':'Décharger les matériaux','set_cache':'Aménager le magasin d’outillage','raid_supplies':'Prélever des fournitures','recover_1940_arms':'Restaurer les anciens outils','black_market':'Acheter hors catalogue','meet_london_agent':'Recevoir le dessinateur','collect_funds':'Rassembler les clous','gather_food':'Livrer le sable',
'open_escape_line':'Ouvrir un chemin de livraison','exfiltrate':'Acheminer un ouvrier','hide_children':'Abriter les apprentis','set_infirmary':'Ouvrir l’atelier de réparation','free_prisoner':'Desserrer l’étau',
'slow_work':'Ralentir le rabotage','sabotage_rolling_stock':'Gripper les chariots','cut_phone':'Couper le cordeau','unbolt_rail':'Décheviller les traverses','blow_rail':'Rompre les traverses','blow_pylon':'Abattre un montant','blow_bridge':'Déposer une passerelle','sabotage_factory':'Dérégler l’établi','burn_depot':'Brûler le stock de bois','destroy_sto_files':'Raboter les fiches',
'found_maquis':'Ouvrir un chantier forestier','train_maquis':'Former les ouvriers forestiers','execute_traitor':'Éliminer la pièce véreuse','ambush':'Préparer un serrage','break_contact':'Démonter et déplacer l’atelier','plan_green':'Plan des traverses','plan_violet':'Plan des cordeaux','plan_turtle':'Plan des accès','plan_blue':'Plan des installations','liberate_town':'Rouvrir les grandes portes',
}

def termes(p,r,c):
    def board(): return r(10,22,44,30)+p('M10 31h44M16 38h14m9 7h9')
    def guard(): return p('M18 53V27h28v26M14 27l18-17 18 17M25 33v14m14-14v14')+c(32,10,5)
    def gate(): return p('M8 55V12h7v43M49 55V12h7v43M15 24h34v10H15zM20 24l10 10m4-10 10 10')
    def rule(): return r(10,14,44,13)+p('M17 14v6m8-6v6m8-6v6m8-6v6m8-6v6')
    return [
      ('soldat','Soldat','Ouvrier du chantier voisin','Présences',guard()),
      ('officier','Officier','Contremaître du chantier voisin','Présences',guard()+p('M10 7h9m26 0h9M23 57h18')),
      ('patrouille','Patrouille','Tournée de chantier','Présences',p('M13 22q19-22 38 0m-1-8 1 8-8-1M51 43Q32 62 13 43m1 8-1-8 8 1')+r(23,24,18,16)+p('M28 29h8m-8 6h8')),
      ('sentinelle','Sentinelle','Veilleur de chantier','Présences',p('M14 54V13h25v41M19 19h15v11H19M19 36h15M45 54V23')+c(45,16,7)),
      ('garnison','Garnison','Équipe installée au chantier voisin','Présences',board()+p('M10 22L32 7l22 15M20 31v21m12-21v21m12-21v21')),
      ('gendarme','Gendarme','Gardien du dépôt','Présences',p('M12 54V23l20-14 20 14v31zM12 30h40M21 54V37h22v17')+c(32,44,3)),
      ('indicateur','Indicateur','Bois véreux','Présences',r(10,10,44,44)+p('M17 19h16m6 27h9M18 40q-7-13 7-13t7 12 11-5M17 47h9')),
      ('barrage','Barrage','Barrière de chantier','Contrôles et alertes',gate()),
      ('controle','Contrôle des papiers','Vérification des bons','Contrôles et alertes',rule()+r(17,32,23,24)+p('M23 39h10m-10 7h7M43 45l5 5 10-14')),
      ('fouille','Fouille','Inspection de la remise','Contrôles et alertes',p('M8 29L29 10l23 19M14 28v26h25M21 35h15')+c(43,39,10)+p('M50 47l9 10')),
      ('rafle','Rafle','Fermeture du chantier','Contrôles et alertes',gate()+p('M24 12h16v9H24zM28 12V6h8v6M21 43l22 13m-22 0 22-13')),
      ('arrestation','Arrestation','Mise sous serre-joint','Contrôles et alertes',p('M46 9H15v42h31M40 9v9H24v24h16v9M44 27v30m-7-25h14M37 57h14')+r(28,24,10,15)),
      ('couvre-feu','Couvre-feu','Fermeture des ateliers','Contrôles et alertes',p('M10 56V23h33v33M16 29h21m-21 8h21m-21 8h21M45 6q-9 17 9 20-18 6-20-9 1-8 11-11z')),
      ('alerte','Alerte','Cloche de chantier','Contrôles et alertes',p('M16 46h32l-6-11V24q0-12-10-12T22 24v11zM27 51q5 8 10 0M32 12V6M7 16l7 6m36 0 7-6M5 34h8m38 0h8')),
      ('voie-ferree','Voie ferrée','Alignement de traverses','Infrastructures',p('M22 7L13 57M42 7l9 50M17 17h30v6H17zM15 33h34v6H15zM12 49h40v6H12zM24 20h8m0 16h9m-21 16h9')),
      ('ligne-telephonique','Ligne téléphonique','Cordeau tendu','Infrastructures',p('M12 55V13h6v42M46 55V13h6v42M7 19h16m18 0h16M18 19q14 8 28 0M18 26q14 8 28 0M9 8h12m22 0h12M15 8v5m34-5v5M7 55h16m18 0h16')),
    ]
