#!/usr/bin/env python3

import argparse
from random import shuffle
from glob import glob
from os import makedirs

parser = argparse.ArgumentParser(
    description='Shuffle documents for annotators in NMT-PE-Effects.')
parser.add_argument('docs_dir',
                    help='Path to the root document directory')
parser.add_argument('out_dir',
                    help='Path to the output directory (doesn\'t have to exist)')
parser.add_argument('-s', '--shuffle-order',
                    default=False, action='store_true', help='Shuffle base order')
parser.add_argument('-d', '--shuffle-order-annotator',
                    default=False, action='store_true', help='Shuffle order for every annotator')
args = parser.parse_args()

MT_ORDER = ['mt1', 'mt2', 'mt3']
MT_NUMBER = len(MT_ORDER)
# doc_order = ['hole', 'whistle', 'china', 'turner',
#              'leap', 'lease', 'audit_i', 'audit_r']
DOC_ORDER = ['hole', 'whistle', 'china']
RELAX_MESSAGE = "# U této věty je možnost udělat si přestávku mezi překlady."

print('Creating annotator queues')

shuffle(MT_ORDER)
if args.shuffle_order:
    shuffle(DOC_ORDER)

mt_buckets = [{} for _ in range(MT_NUMBER)]

for doc_name in DOC_ORDER:
    for mt_index, mt_name in enumerate(MT_ORDER):
        filename = f'{args.docs_dir}/{doc_name}-{mt_name}'
        with open(filename, 'r') as f:
            data = f.read()
            mt_buckets[mt_index][doc_name] = data

annotator_buckets = [{} for _ in range(MT_NUMBER)]

offset = 0
for doc_name in DOC_ORDER:
    for mt_index, mt_name in enumerate(MT_ORDER):
        annotator_index = (mt_index + offset) % MT_NUMBER
        annotator_buckets[annotator_index][doc_name] = mt_buckets[mt_index][doc_name]
    offset = (offset+1) % MT_NUMBER


print('Serializing data')

annotator_serial = [""] * MT_NUMBER

for annotator_index, annotator_bucket in enumerate(annotator_buckets):
    for doc_index, doc_name in enumerate(DOC_ORDER):
        if doc_index != 0:
            annotator_serial[annotator_index] += RELAX_MESSAGE + '\n'  
        annotator_serial[annotator_index] += annotator_buckets[annotator_index][doc_name]

print('Storing data')

makedirs(args.out_dir, exist_ok=True)
for annotator_index, annotator_bucket in enumerate(annotator_buckets):
    with open(f'{args.out_dir}/a{annotator_index}', 'w') as f:
        f.write(annotator_serial[annotator_index])