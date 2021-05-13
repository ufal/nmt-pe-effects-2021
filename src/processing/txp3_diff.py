#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from utils import MT_BLEU, MAX_WORD_TIME, pretty_mt_name_2, confidence_change
from difflib import SequenceMatcher

data = load_mx(p1_only=True)
# compute per-model data
doc_rep = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
doc_del = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
doc_ins = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
for doc in data:
    for line in doc.lines:
        matcher = SequenceMatcher(None, line.provided.split(), line.target.split())
        matcher = matcher.get_opcodes()
        doc_rep[doc.mt_name].append(sum([(i2-i1+j2-j1)/2 for tag, i1, i2, j1, j2 in matcher if tag == 'replace']))
        doc_del[doc.mt_name].append(sum([i2-i1 for tag, i1, i2, j1, j2 in matcher if tag == 'delete']))
        doc_ins[doc.mt_name].append(sum([j2-j1 for tag, i1, i2, j1, j2 in matcher if tag == 'insert']))

# print model averages
print('\n'.join([
    f'{pretty_mt_name_2(x_rep[0]):>10} & ${np.average(x_rep[1]):6.2f}$ & ${np.average(x_del[1]):6.2f}$ & ${np.average(x_ins[1]):6.2f}$  \\\\'
    for (x_rep, x_del, x_ins)
    in zip(doc_rep.items(), doc_del.items(), doc_ins.items())
]))

print("\\midrule")
global_rep = [x for subl in doc_rep.values() for x in subl]
global_del = [x for subl in doc_del.values() for x in subl]
global_ins = [x for subl in doc_ins.values() for x in subl]
print("\\textbf{Average} &" + f'${np.average(global_rep):6.2f}$ & ${np.average(global_del):6.2f}$ & ${np.average(global_ins):6.2f}$  \\\\')
