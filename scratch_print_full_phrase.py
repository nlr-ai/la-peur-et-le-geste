import os, sys
import scripts.depecher as d
orig_depecher = d.depecher
def my_depecher(*args, **kwargs):
    import agents.depeche.mission as m
    orig_appeler = m.appeler
    def my_appeler(*a, **k):
        rep = orig_appeler(*a, **k)
        with open('leo_full_phrase.txt', 'w', encoding='utf-8') as f:
            f.write(str(rep.get('result')))
        return rep
    m.appeler = my_appeler
    return orig_depecher(*args, **kwargs)
d.depecher = my_depecher
d.main()
