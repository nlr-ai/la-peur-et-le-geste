"""60 gestes de menuiserie : une silhouette de métier, un indice du sens initial."""

def dessins(path, rect, circle):
    def plank():
        return rect(9,25,46,15)+path('M14 30h15m10 5h11')+path('M33 29q-6 3 0 7 6-3 0-7z')
    def frame():
        return rect(13,8,38,48)+rect(19,14,26,36)+path('M13 8l6 6m26 0 6-6M13 56l6-6m26 0 6 6')
    def bench():
        return rect(7,30,50,7)+path('M13 37v19m38-19v19M13 48h38M47 37v7h10V28m-3-3v6')
    def crate():
        return rect(10,24,44,31)+path('M10 33h44M10 45h44M18 24v31m28-31v31M23 38h18')
    def mallet():
        return path('M25 27l-9 25 7 3 9-25M14 10l29 11-5 12L9 22zM13 18l24 9')
    def saw():
        return path('M8 42l32-28 13 15-5 4-4-1-1 5-5-1-1 5-5-1-1 5-5-1-1 5-5-1-1 5zM40 14l7-7 12 13-6 9M47 14l5 6')
    def plane():
        return path('M8 40h45l4 9H10zM15 40v-7q8-12 14-4v11M34 40l5-16 7 2-4 14M12 54h43M42 19q-8-10-15-3t-12 0')
    def square():
        return path('M10 10h9v35h35v9H10zM25 49v5m8-5v5m8-5v5m8-5v5M10 18h5m-5 9h5m-5 9h5')
    def clamp():
        return path('M45 10H17v39h28M40 10v8H25v23h15v8M43 27v29m-7-24h14M36 56h14')
    def bell():
        return path('M16 43h32l-5-8V24q0-12-11-12T21 24v11zM27 48q5 9 10 0M32 12V7')
    def door():
        return path('M12 55V9h38v46M20 55V16l22-5v44z')+circle(36,34,2)
    def tree():
        return path('M22 8L9 27h7L6 42h32L28 27h7zM22 42v14')
    def joint():
        return path('M6 20h20v7h12v-7h20v24H38v-7H26v7H6zM12 25h8m24 14h8')
    def nails():
        return path('M17 16v34l3 7 3-7V16M12 16h16M37 9v34l3 7 3-7V9M32 9h16')
    def template():
        return rect(12,12,40,40)+circle(23,24,5)+rect(34,19,10,11)+path('M20 42l7-8 8 8zM42 38v7')
    def cart():
        return path('M7 23h36l8 20H14zM43 23l4-10h10M16 29h23m-20 6h22')+circle(20,49,6)+circle(45,49,6)
    def grain():
        return path('M12 21q19-8 39 0M12 29q9-5 17-2m10 0 12 2M12 42q18 8 39 0')+circle(33,34,5)
    def arrow(): return path('M8 12h16m-5-5 5 5-5 5')
    def tick(): return path('M42 49l6 6 10-15')
    def waves(): return path('M46 10q12 8 10 20M44 18q6 4 5 11')
    def lift(): return path('M32 5v14m-6-6 6 6 6-6')
    def cross(): return path('M43 44l13 13m-13 0 13-13')
    def small(s,x=5,y=18,k=.7): return f'<g transform="translate({x} {y}) scale({k})">'+s+'</g>'
    def plan(s): return rect(6,5,52,54)+small(s,12,13,.62)+path('M12 11h13m-13 5h7M42 53h10')
    return {
      'sound_out': grain()+path('M49 8l-9 15m4-18 8 5M30 7v7'),
      'test_recruit': small(joint())+small(square(),25,0,.5)+tick(),
      'induct': joint()+path('M32 6v16m-5-10 5 5 5-5M29 49h6'),
      'form_cell': path('M10 10h18v18H10zM36 10h18v18H36zM23 38h18v18H23zM19 28v7h26v-7M32 35v3M15 15h8m18 8h8m-21 25h8'),
      'win_notable': joint()+path('M23 14l9-7 9 7M32 45v10'),
      'shelter_refractory': small(door(),0,0,.9)+path('M40 37h17m-6-5 6 5-6 5M43 47v9h14v-9'),
      'link_london': path('M8 45V19h15v26M41 45V19h15v26M23 23q9-12 18 0m-18 8q9-12 18 0M12 24h7m-7 7h7m26-7h7m-7 7h7M8 51h48'),
      'steal_stamps': small(template(),2,15,.72)+path('M36 21l18-14m-9 0h9v9'),
      'get_stamps_inside': small(template(),13,0,.65)+path('M6 42h17l8 8h15l12-10M6 53h15l9 6h17l11-10'),
      'set_workshop': bench()+small(mallet(),15,0,.5),
      'forge_papers': frame()+path('M27 38l28-28 5 5-28 28-9 4z'),
      'set_safehouse': door()+path('M24 22h14M24 27h14M24 44h14'),
      'change_identity': small(frame(),0,8,.65)+small(frame(),29,13,.55)+arrow()+path('M36 57H20l5-5'),
      'win_farm': path('M7 30L32 9l25 21M13 30v25h38V30M24 55V37h16v18M18 30h28')+tick(),
      'set_cover_business': bench()+path('M8 24l8-13h32l8 13zM18 15v9m10-9v9m10-9v9m10-9v9'),
      'open_mailbox': rect(10,21,44,34)+path('M14 30h36M16 26h32M14 38h36M16 51l16-10 16 10M32 5v11m-5-5 5 5 5-5'),
      'carry_message': small(plank(),15,3,.7)+path('M28 23l10 7 10-7M7 43h35m-7-6 7 6-7 6M8 52h18'),
      'set_radio': bell()+path('M5 56h54M49 41v15M44 51h10'),
      'transmit': small(bell(),1,10,.8)+waves(),
      'set_press': clamp()+path('M7 56h50M29 23h25'),
      'print_tracts': small(plane(),4,0,.85)+path('M12 48h40M12 53h40M12 58h40'),
      'spread_tracts': path('M8 15h15v23H8zM27 15h15v23H27zM46 15h10v23H46zM12 21h7m12 0h7m12 0h3M9 49h45m-6-6 6 6-6 6'),
      'watch_trains': path('M16 9v45m32-45v45M12 17h40M12 29h40M12 41h40M12 53h40')+circle(32,29,8)+path('M37 35l8 9'),
      'scout_garrison': square()+path('M28 16l13-8 13 8v24H28zM35 40V26h12v14M31 21h4m12 0h4'),
      'copy_files': small(template(),0,0,.8)+path('M22 49v8h36V22h-8M29 51h22M51 31v13'),
      'unmask_informer': grain()+circle(34,33,14)+path('M44 44l13 13M30 27l8 12m-9 0 8-12'),
      'homologate_dz': small(square(),0,0,.85)+path('M26 14h27v24H26zM26 20h27M31 14v24m16-24v24')+tick(),
      'receive_drop': crate()+lift(),
      'set_cache': path('M8 19h48v13H8zM8 40h48v15H8zM14 24h16m-16 22h15M24 32v8h17v-8')+circle(32,36,2),
      'raid_supplies': crate()+arrow()+path('M49 7l-7 10h9'),
      'recover_1940_arms': small(mallet(),17,0,.7)+path('M7 43q12-7 25 0t25 0M9 54h46M11 30V15m-5 6 5-6 5 6'),
      'black_market': small(crate(),10,0,.75)+path('M8 52h41m-7-5 7 5-7 5M53 11H26m6-5-6 5 6 5'),
      'meet_london_agent': small(square(),0,7,.75)+small(mallet(),29,4,.55)+path('M24 32h13m-6-5 6 5-6 5'),
      'collect_funds': nails()+path('M7 39v19h49V39M28 29h27m-5-5 5 5-5 5'),
      'gather_food': cart()+path('M12 18q12-16 27 0M17 18v-6m9 6V8m8 10v-6'),
      'open_escape_line': path('M10 55V10h20v45M15 15h10v35H15M36 53V27h19v26M35 15h17v7m-5-5 5 5 5-5'),
      'exfiltrate': small(door(),0,0,.8)+path('M28 39h29m-7-7 7 7-7 7M35 50h20'),
      'hide_children': path('M8 28L32 9l24 19M13 27v29h38V27')+rect(19,35,10,17)+rect(35,40,10,12)+path('M22 40h4m12 5h4'),
      'set_infirmary': small(bench(),0,15,.9)+path('M26 7h12v10h10v12H38v10H26V29H16V17h10z'),
      'free_prisoner': small(clamp(),-2,0,.85)+path('M30 36h27m-6-6 6 6-6 6M45 18v9M45 45v9'),
      'slow_work': small(plane(),0,15,.85)+circle(45,16,11)+path('M45 9v8h-6'),
      'sabotage_rolling_stock': cart()+path('M17 46l7 7m-7 0 7-7M33 16l-6-8m10 6 4-8'),
      'cut_phone': path('M7 18q12 18 23 4M37 22q12-18 20 0M24 30l20-20M33 35l-4-5')+circle(20,39,7)+circle(37,44,7)+path('M25 34l4-4m5 8-5-8'),
      'unbolt_rail': small(plank(),0,20,.9)+path('M30 37V16l8-7h10v8H36v20M26 37h8M23 13l-8 6m0-6v6h6'),
      'blow_rail': path('M8 23h19l-5 8 7 9H8zM56 23H37l5 8-7 9h21zM14 29h7m22 5h7M30 8v8m9-5-4 6M30 48v9'),
      'blow_pylon': path('M13 55l8-22 9 6-5 16M26 24l7-17 13 28-10-6M20 20h32M23 14h26M39 42l12 10M45 41l10 3'),
      'blow_bridge': path('M7 23h20l-5 7 8 8M57 23H39l4 7-8 8M7 32h13m24 0h13M13 32v21m38-21v21M9 53h9m28 0h10M29 45l4 10 5-10'),
      'sabotage_factory': bench()+path('M16 13h31v13H16zM22 13v13m19-13v13M23 40l15 15m-15 0 15-15'),
      'burn_depot': small(crate(),0,16,.9)+path('M32 33q-18-9 1-27-2 12 6 13l4-7q12 22-11 21z'),
      'destroy_sto_files': small(plane(),0,0,.85)+path('M12 51q7-9 12 0t12 0 12 0M12 58h40'),
      'found_maquis': tree()+path('M32 55V32l12-13 14 13v23M36 34h18m-13 0v21m9-21v21'),
      'train_maquis': small(bench(),0,18,.9)+small(mallet(),4,0,.6)+small(mallet(),33,5,.4)+path('M35 13h9'),
      'execute_traitor': path('M8 17h48v13H8zM12 22h13m14 3h11M20 30l-7 25m20-25 13 25M30 8v33m-5-7 5 7 5-7')+cross(),
      'ambush': path('M9 10h46v44H9zM14 16v32m36-32v32M18 28h10l-5-5m5 5-5 5M46 39H36l5-5m-5 5 5 5M18 54l5-8 5 8m8 0 5-8 5 8'),
      'break_contact': path('M6 20h17v7h7v10h-7v7H6zM58 20H41v7h-7v10h7v7h17zM24 52H8m5-5-5 5 5 5M40 12h16m-5-5 5 5-5 5'),
      'plan_green': plan(path('M16 8v48m32-48v48M10 17h44m-44 12h44m-44 12h44m-44 12h44M24 24l16 16')),
      'plan_violet': plan(path('M10 12q20 30 42 0M32 16v34M24 43l8 7 8-7M25 9l14 14')),
      'plan_turtle': plan(path('M10 12h44v12H10zM10 39h44v12H10zM18 24l28 15M46 24L18 39M15 15h10')),
      'plan_blue': plan(path('M32 9L10 54h44zM22 34h20M17 45h30M32 9v45M11 17h42')),
      'liberate_town': path('M8 55V12h48v43M14 55V19l14-7v43M50 55V19l-14-7v43M28 46h8M32 32V19m-5 5 5-5 5 5M5 7h54'),
    }
