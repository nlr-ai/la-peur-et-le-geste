"""Pictogrammes des 60 actions du catalogue de résistance, sans ajout de règles."""


def dessins(path, rect, circle):
    def person(x, y, small=False):
        r=3 if small else 4
        return circle(x,y,r)+path(f'M{x-6} {y+17}v-5q0-8 6-8t6 8v5')

    def arrow(x,y,dx=13):
        return path(f'M{x} {y}h{dx}m-5-5 5 5-5 5')

    def document():
        return path('M16 8h24l8 8v39H16zM40 8v9h8M23 25h17m-17 7h17m-17 7h10')

    def home():
        return path('M6 28L32 8l26 20M13 26v28h38V26M25 54V36h14v18')

    def rail():
        return path('M22 8L9 55M42 8l13 47M20 17h24m-27 12h30m-33 13h36m-39 11h42')

    def phone():
        return path('M10 23q22-19 44 0l-5 8-9-5 1-5q-9-5-18 0l1 5-9 5z')

    def radio():
        return rect(11,27,42,26,3)+rect(17,33,16,13)+circle(42,41,4)+path('M18 27V10m4 27v5m5-5v5')

    def factory():
        return path('M8 54V30l15-9v11l15-9v12h17v19zM45 35V10h8v25M15 43h5v5h-5zM28 43h5v5h-5zM43 43h5v5h-5z')

    def burst():
        return path('M27 21l-5-8m14 7 3-9M22 30l-12-2m31 0 12-4M26 39l-6 9m17-9 6 9')

    def tree(x=18,y=10):
        return path(f'M{x} {y}l-9 14h5l-9 13h26l-9-13h5zM{x} {y+27}v10')

    def crate():
        return rect(12,26,40,27)+path('M12 33h40m-40 13h40M20 33l24 13m0-13L20 46')

    def eye():
        return path('M7 29q25-26 50 0-25 26-50 0z')+circle(32,29,9)+circle(32,29,3)

    def train():
        return rect(17,9,30,35,5)+rect(22,15,20,12)+circle(24,36,2)+circle(40,36,2)+path('M23 44l-8 12m26-12 8 12M20 50h24')

    def flame(x=32,y=31):
        return path(f'M{x-5} {y+12}q-15-9 2-28-1 10 7 13l2-8q15 20-3 24z')

    def lock():
        return rect(20,29,25,23,3)+path('M25 29V18a8 8 0 0 1 16 0v11')+circle(32,39,2)+path('M32 41v5')

    def flag():
        return path('M32 54V7l21 5-5 8-16-3M27 54h10')

    def handshake():
        return path('M6 30l9-10 12 3 11-3 20 12-7 14-13 7-18-9-6-5M26 24l-7 9 7 5 9-8 16 15M5 35l9 6m42-5-5 9M22 43l5-5m0 9 5-5m0 8 5-5')

    def route():
        return path('M8 52h13q10 0 10-11V24q0-10 12-10h12m-6-6 6 6-6 6')+circle(8,52,3)

    def tower():
        return path('M32 7L15 55m17-48 17 48M24 29h16M20 42h24M17 54h30M24 29l20 13M40 29L20 42M15 18h34M10 23v-5h5m34 0h5v5')

    def plan(inner, mark):
        return '<g transform="translate(9 9) scale(.72)">'+inner+'</g>'+rect(6,5,52,54,3)+path(mark)

    return {
        'sound_out': person(18,20)+person(46,28)+path('M28 13h24v10h-8l-5 5v-5M34 17h1m5 0h1m5 0h1'),
        'test_recruit': person(14,19)+rect(29,15,25,37)+path('M35 25l4 4 9-10M35 38h12m-12 7h9'),
        'induct': person(13,25)+person(51,25)+flame(32,20)+path('M20 47l12 6 12-6'),
        'form_cell': circle(32,13,6)+circle(13,47,6)+circle(51,47,6)+path('M29 19L16 41m22-22 10 22M19 47h26')+circle(32,34,3),
        'win_notable': handshake()+path('M23 12l9-6 9 6M27 11v7m10-7v7'),
        'shelter_refractory': path('M5 25L26 8l20 15M10 25v29h19M19 54V33h12')+person(43,32)+path('M36 49h-8m5-5-5 5 5 5'),
        'link_london': path('M9 51V23h12v28M7 23l8-13 8 13M41 51V18h13v33M39 18l8-9 9 9M15 9V5M47 8V4M23 34q9-10 18 0m-17 6q8-7 16 0')+circle(47,25,3),
        'steal_stamps': rect(11,30,24,9)+path('M17 30V18q6-10 12 0v12M8 44h30M39 36l16-14m-8 0h8v8M12 49h23'),
        'get_stamps_inside': rect(24,24,20,13)+path('M29 24v-8h10v8M6 40h17l7 5h15l11-9M6 49h17l9 6h13l12-9M7 34l8 5M17 31h5'),
        'set_workshop': rect(12,28,40,7)+path('M16 35v19m32-19v19M18 28V11h19v17M23 18h8M41 23l12-12m-5-4 9 9')+circle(45,48,5),
        'forge_papers': document()+path('M30 48l19-22 6 6-19 22-9 3zM45 31l6 5')+circle(27,18,4),
        'set_safehouse': home()+path('M35 43h20m-6-5 6 5-6 5')+circle(28,43,5),
        'change_identity': rect(6,12,22,34)+rect(36,18,22,34)+circle(17,23,4)+circle(47,29,4)+path('M11 38q0-10 6-10t6 10M41 44q0-10 6-10t6 10M24 7h21l5 5m-5-10 5 10h-9M39 57H19l-5-5'),
        'win_farm': path('M7 32l19-18 19 18M12 31v24h29V31M21 55V39h10v16M42 23V9m-5 8 5-8 5 8m-5 6 9-6M48 42l4 4 7-9'),
        'set_cover_business': factory()+path('M9 17q8-9 16 0-8 10-16 0zM12 19l10-4')+rect(10,7,16,3),
        'open_mailbox': rect(10,21,44,29,3)+path('M10 23l22 17 22-17M18 16h28M45 12h13m-6-6v12'),
        'carry_message': rect(23,16,33,23)+path('M23 18l16 11 17-11M6 25h12M4 33h13M11 44h27m-7-5 7 5-7 5M17 52h28'),
        'set_radio': radio()+path('M35 16h19m-9-9v18M10 14h8'),
        'transmit': radio()+path('M25 16q8-11 18 0m-13 3q4-5 8 0M40 7q10-1 17 9M45 12q6 0 9 6'),
        'set_press': rect(13,10,31,34)+path('M9 10h39M18 24h21v9H18M7 39h42v7H7M16 46v9m24-9v9M48 19h12m-6-6v12'),
        'print_tracts': rect(13,22,38,25,3)+path('M21 22V8h22v14M21 37h22v20H21zM26 43h12m-12 6h12M18 29h5M46 29h1'),
        'spread_tracts': path('M5 17l16-6 10 22-16 6zM34 9l22 8-8 22-15-5M9 24l11-4m20-3 9 3M17 49h29m-5-5 5 5-5 5M26 39l-1 4m11-5 2 5'),
        'watch_trains': train()+path('M8 20q-4-10 4-14M52 6q8 4 4 14M27 30h10')+circle(32,20,3),
        'scout_garrison': rect(11,30,14,19,5)+rect(39,30,14,19,5)+path('M11 33l6-14h8l4 14h6l4-14h8l6 14M25 36h14M27 12l5-5 5 5M32 7v12')+circle(18,42,4)+circle(46,42,4),
        'copy_files': path('M10 43H6V7h31v6M14 48h-3V13h31v6')+rect(19,20,33,36)+path('M25 29h20m-20 7h20m-20 7h13M25 49h16'),
        'unmask_informer': person(23,17)+circle(40,35,12)+circle(40,35,5)+path('M49 44l11 11M10 14h26M15 13l3-6h12l3 6'),
        'homologate_dz': path('M9 48l9-37 19 6 16-6-6 37-20-6zM18 11l9 31m10-25 10 31')+circle(32,30,7)+path('M43 48l6 6 10-13'),
        'receive_drop': path('M7 26a25 20 0 0 1 50 0q-8-7-16 0-9-7-18 0-8-7-16 0zM7 26l20 20m30-20L37 46M23 26l7 20m11-20-7 20M23 26q-2-17 9-20 11 3 9 20')+rect(25,46,14,12),
        'set_cache': path('M6 38h52M9 42l5 15h36l5-15M12 34l11-14 18 3 12 11')+rect(19,43,26,10)+path('M24 48h16m-16-2v4'),
        'raid_supplies': crate()+path('M9 18h22m-6-6 6 6-6 6M45 6l-8 11h8l-5 8'),
        'recover_1940_arms': path('M7 45q8-8 16 0t16 0 18 0M11 54h43M14 37l8-2 22-22-4-4-22 22-7 2zM29 27l4 4M47 24v14m-5-5 5 5 5-5'),
        'black_market': path('M8 26h48l-7-15H15zM10 26v27h44V26M9 37h46M17 16l-2 10m11-10v10m11-10v10m10-10 3 10')+circle(24,45,5)+path('M35 43h11m-5-4 5 4-5 4'),
        'meet_london_agent': person(31,25)+path('M20 22h22M24 20l3-7h10l3 7M11 48h12m-5-5 5 5-5 5M54 41H43m5-5-5 5 5 5')+rect(41,46,14,10),
        'collect_funds': circle(32,13,7)+path('M32 9v8M32 24v10m-5-5 5 5 5-5M6 41h17l7 6h14l12-8M7 51h16l10 5h12l13-10M24 40h13l4 7'),
        'gather_food': path('M12 31h40l-6 23H18zM21 31q0-23 11-23t11 23M22 38v10m10-10v10m10-10v10M7 22h10m-4-4 4 4-4 4')+circle(31,27,6),
        'open_escape_line': route()+path('M10 14V8h14v22H10M21 24l8-8m-1 8 6-8M41 42h13v12H41z'),
        'exfiltrate': person(16,18)+path('M30 8v48M35 34h22m-7-7 7 7-7 7M8 54l9-13 8 8M38 53l6-8 9 8'),
        'hide_children': path('M6 27L32 7l26 20M12 26v29h40V26')+person(25,30,True)+person(40,36,True)+path('M17 20q15-6 28 0'),
        'set_infirmary': home()+path('M27 23h10v7h7v10h-7v7H27v-7h-7V30h7z'),
        'free_prisoner': path('M7 8h30v47H7zM15 8v47m10-47v47M37 8l12 6v41l-12-1M31 33h27m-6-6 6 6-6 6'),
        'slow_work': factory()+circle(25,17,10)+path('M25 10v7l-5 3M12 8l-4 4M34 7l5 5'),
        'sabotage_rolling_stock': train()+path('M7 29l8 7-8 7M49 28l8 7-8 7M25 31l14 9m-14 0 14-9'),
        'cut_phone': phone()+path('M16 31v12h9m14 0h9V31M25 37l14 13m-14 0 14-13'),
        'unbolt_rail': rail()+path('M24 27l16 12M39 25l-7 7M42 22l6-1-1 7-5 3-5-5z'),
        'blow_rail': path('M22 7l-5 17m25-17 5 17M20 16h24M15 42l-5 14m39-14 5 14M12 51h40M21 30l7 3-4 7 10-4 5 7-1-11 8-3-10-2-3-8-4 10z'),
        'blow_pylon': path('M29 8L17 29m12-21 13 21M19 19h20M11 14h36M17 29l10 6-5 9 14-4 9 14M12 56h42M34 10l-5 7M39 22l15 9m-6 1 6-1-1-6'),
        'blow_bridge': path('M6 44h17m18 0h17M6 27h17l5 6 9-6h21M8 27V15m48 12V15M9 22h14m17 0h15M13 44V28m38 16V28M22 34l10 8 10-8M28 48l4 7 5-7M6 54q5-4 10 0m32 0q5-4 10 0'),
        'sabotage_factory': factory()+path('M26 9l-6 9h8l-5 10M7 17l5 4M34 14l5-4'),
        'burn_depot': path('M8 53V32l13-9 10 8 13-9 12 10v21zM15 41h9v12m10-12h9v12')+flame(34,17),
        'destroy_sto_files': rect(9,9,29,39)+path('M16 17h15m-15 7h15m-15 7h9M8 54h48')+flame(46,36),
        'found_maquis': tree(16,13)+path('M24 55l17-25 17 25zM41 30v25M38 55l3-10 4 10M37 27V7l17 5-5 7-12-3'),
        'train_maquis': person(12,29)+rect(29,10,27,31)+circle(42,25,9)+circle(42,25,4)+path('M29 18L19 34M33 41v13m18-13v13'),
        'execute_traitor': person(32,15)+path('M17 52l30-25m-30 0 30 25M14 9l-4 6m40-6 4 6'),
        'ambush': path('M29 7v50m6-50v50M7 23h14l-5-5m5 5-5 5M57 41H43l5-5m-5 5 5 5M6 44l7-10 7 10zM45 19l6-10 7 10z'),
        'break_contact': tree(15,9)+path('M25 52l12-18 12 18zM31 23h24m-6-6 6 6-6 6M25 59h27'),
        'plan_green': plan(rail(),'M7 12h9m-9 6h9M43 50l5 5 8-10'),
        'plan_violet': plan(phone()+path('M16 33v15h32V33'),'M7 12h9m-9 6h9M28 44l10 10m-10 0 10-10'),
        'plan_turtle': plan(path('M20 7v49m24-49v49M32 7v8m0 8v8m0 8v8M10 31h44M14 25v12m36-12v12'),'M7 12h9m-9 6h9M43 50h12'),
        'plan_blue': plan(tower(),'M7 12h9m-9 6h9M46 43l-4 7h7l-4 6'),
        'liberate_town': path('M8 55V33h13v22M43 55V27h13v28M24 55V30h16v25M7 33l8-8 8 8M42 27l8-8 8 8M28 55V43h8v12')+flag(),
    }
