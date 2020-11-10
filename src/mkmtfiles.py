#!/usr/bin/env python3
import os

MTmap = {
    'sent-25385': 'm01',
    'sent-29022': 'm02',
    'sent-29333': 'm03',
    'sent-32966': 'm04',
    'sent-72836': 'm05',
    'sent-997083': 'm06',
    'sent-1015168': 'm07',
    'sent-1022401': 'm08',
    'sent-1054981': 'm09',
    'sent-1058593': 'm10',
    'doc-698515': 'm11',
    'google': 'google',
    'microsoft': 'microsoft',
    'REFERENCE': 'ref',
    'SOURCE': 'src'
}

BOUNDARIES = {
    'audit_i': (1, 17),
    'audit_r': (18, 23),
    'china': (24, 35),
    'hole': (36, 45),
    'leap': (46, 56),
    'lease': (57, 85),
    'turner': (86, 93),
    'whistle': (94, 99)
}

for dname in BOUNDARIES.keys():
    for mtsrc, mtname in MTmap.items():
        cname = f'docs/data/{dname}-{mtname}'
        print(cname)
        # os.remove(cname)

        boundary = BOUNDARIES[dname]
        with open(f'docs/translations/txt/{mtsrc}.txt') as f:
            dcontent = f.readlines()[(boundary[0]-1):(boundary[1])]

        with open(cname, 'w') as f:
            f.write(''.join(dcontent).rstrip('\n'))
