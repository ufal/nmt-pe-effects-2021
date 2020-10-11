#!/usr/bin/env python3
import os

FILES = ['audit_i', 'audit_r', 'china', 'hole',
         'leap', 'lease', 'turner', 'whistle']
MTS = ['m' + ('0' if x < 10 else '') + str(x) for x in range(1, 13+1)]
BOUNDARIES = {
    'audit_i': (3, 19),
    'audit_r': (22, 27),
    'china': (48, 59),
    'hole': (77, 86),
    'leap': (89, 99),
    'lease': (102, 130),
    'turner': (146, 153),
    'whistle': (179, 184)
}

for dname in FILES:
    for mtname in MTS:
        cname = f'docs/data/{dname}-{mtname}'
        print(cname)
        # os.remove(cname)

        boundary = BOUNDARIES[dname]
        with open(f'docs/translations/clean/{mtname}.sgm') as f:
            dcontent = f.readlines()[(boundary[0]-1):(boundary[1])]

        with open(cname, 'w') as f:
            f.write(''.join(dcontent).rstrip('\n'))
