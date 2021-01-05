#!/usr/bin/env python3

from load import *
import argparse
import random
from os import makedirs
import json
from collections import defaultdict, Counter

DOC_ORDER = ['hole', 'whistle', 'china', 'turner',
             'leap', 'lease', 'audit_i', 'audit_r']
RELAX_MESSAGE_MT = 'U této věty je možnost udělat si přestávku mezi korekturou.'
INDEX_FILENAME = 'index.json'

print('Loading data')

parser = argparse.ArgumentParser()
parser.add_argument('--out_dir_p2', default='docs/out_p2/',
                    help='Path to the output directory (doesn\'t have to exist)')
parser.add_argument('--shuffle-doc', default=True, action='store_true')
parser.add_argument('--no-save', default=False, action='store_true')
parser.add_argument('--seed', default=306, type=int)
args = parser.parse_args()
random.seed(args.seed)

data = load_mx()
data_p1 = defaultdict(list)
doc_names = set()
mt_names = set()
u1_names = set()

data_spec_ref = []
data_spec_mt = []

for doc in data:
    if doc.mt_name == 'ref':
        data_spec_ref.append(doc)
    if doc.mt_name == 'm11':
        data_spec_mt.append(doc)
    data_p1[doc.doc_name].append(doc)
    doc_names.add(doc.doc_name)
    mt_names.add(doc.mt_name)
    u1_names.add(doc.user_a)
del data
data_new = {}

# assumptions for the input data
assert(len(doc_names) == 8)
for doc_name in data_p1.keys():
    assert(len(data_p1[doc_name]) == 15)
    random.shuffle(data_p1[doc_name])

print('Processing data')
overlap = {'m': [], 'u': [], 'mu': []}

# Pick a user for every document for every u_p2
p2_docs = [[] for _ in range(15)]
for u_p2 in range(15):
    u_p2_counter_ua = Counter()
    u_p2_counter_mt = Counter()
    u_p2_counter_mu = Counter()
    for docname in data_p1.keys():
        found = False
        backup_i = None
        for doc_i, tmp_doc in enumerate(data_p1[docname]):
            if tmp_doc.user_a not in u_p2_counter_ua and tmp_doc.mt_name not in u_p2_counter_mt:
                found = True
                break
            if tmp_doc.user_a not in u_p2_counter_ua:
                backup_i = doc_i
            if tmp_doc.mt_name not in u_p2_counter_mt:
                backup_i = doc_i
        if not found:
            if backup_i is None:
                raise Exception('Unable to compose queue')
            doc_i = backup_i

        tmp_doc = data_p1[docname].pop(doc_i)
        p2_docs[u_p2].append(tmp_doc)
        u_p2_counter_ua[tmp_doc.user_a] += 1
        u_p2_counter_mt[tmp_doc.mt_name] += 1
        u_p2_counter_mu[(tmp_doc.user_a, tmp_doc.mt_name)] += 1
    
    overlap['m'].append(list(u_p2_counter_mt.values()))
    overlap['u'].append(list(u_p2_counter_ua.values()))
    overlap['mu'].append(list(u_p2_counter_mu.values()))

print('Counter MT + User')
for u_p2, counter in enumerate(overlap['mu']):
    print(' '.join(str(x) for x in counter))
print('Counter MT')
for u_p2, counter in enumerate(overlap['u']):
    print(' '.join(str(x) for x in counter))
print('Counter User')
for u_p2, counter in enumerate(overlap['m']):
    print(' '.join(str(x) for x in counter))

# assert queue depleted
for doc_name, doc_list in data_p1.items():
    assert(len(doc_list) == 0)

print('Serializing data')

serial_tgt = [""] * (15+1+1)
serial_src = [""] * (15+1+1)
indexdata = {}
index_pointer = 0

for u_p2, doc_queue in enumerate(p2_docs):
    if args.shuffle_doc:
        random.shuffle(doc_queue)
    for doc in doc_queue:
        serial_tgt[u_p2] += f'# {RELAX_MESSAGE_MT} ({index_pointer})\n'
        serial_src[u_p2] += f'# {RELAX_MESSAGE_MT} ({index_pointer})\n'
        serial_tgt[u_p2] += doc.target()
        serial_src[u_p2] += doc.source()
        indexdata[index_pointer] = {'annotator': doc.user_a, 'corrector': u_p2, 'mt': doc.mt_name, 'doc': doc.doc_name}
        index_pointer += 1

for u_p2, doc_queue in [(15, data_spec_ref), (16, data_spec_mt)]:
    if args.shuffle_doc:
        random.shuffle(doc_queue)
    for doc in doc_queue:
        serial_tgt[u_p2] += f'# {RELAX_MESSAGE_MT} ({index_pointer})\n'
        serial_src[u_p2] += f'# {RELAX_MESSAGE_MT} ({index_pointer})\n'
        serial_tgt[u_p2] += doc.provided()
        serial_src[u_p2] += doc.source()
        indexdata[index_pointer] = {'annotator': doc.user_a, 'corrector': u_p2, 'mt': doc.mt_name, 'doc': doc.doc_name}
        index_pointer += 1

if args.no_save:
    exit(0)

print('Storing data')
makedirs(args.out_dir_p2, exist_ok=True)
for u_p2 in range(15+1+1):
    with open(f'{args.out_dir_p2}/k{u_p2}.tgt', 'w') as f:
        f.write(serial_tgt[u_p2].rstrip('\n'))
    with open(f'{args.out_dir_p2}/k{u_p2}.src', 'w') as f:
        f.write(serial_src[u_p2].rstrip('\n'))

print('Storing index')
with open(f'{args.out_dir_p2}/{INDEX_FILENAME}', 'w') as f:
    json.dump(indexdata, f, ensure_ascii=False)
