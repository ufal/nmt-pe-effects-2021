#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU, MAX_WORD_TIME, MAX_SENT_TIME
import scipy.stats as st

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mt-only', action='store_true')
args = parser.parse_args()

data = load_mx()
SKIP_SRC_REF = args.mt_only

# compute per-model data
mt_times_1 = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
mt_times_2 = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
for doc in data:
    if doc.mt_name not in MT_BLEU.keys():
        continue
    mt_times_1[doc.mt_name] += [len(x.provided.split()) for x in doc.lines]
    mt_times_2[doc.mt_name] += [len(x.target.split()) for x in doc.lines]

for k in mt_times_1.keys():
    print(f'{k:>10} {np.average(mt_times_1[k]):.2f} -> {np.average(mt_times_2[k]):.2f}')

our_mts_1 = list({k:np.average(v) for k,v in mt_times_1.items() if k not in {'src', 'ref'}}.values())
our_mts_2 = list({k:np.average(v) for k,v in mt_times_2.items() if k not in {'src', 'ref'}}.values())

ci_1_x, ci_1_y = st.t.interval(alpha=0.95, df=len(our_mts_1)-1, loc=np.mean(our_mts_1), scale=st.sem(our_mts_1)) 
ci_2_x, ci_2_y = st.t.interval(alpha=0.95, df=len(our_mts_2)-1, loc=np.mean(our_mts_2), scale=st.sem(our_mts_2)) 

ci_size_1 = (ci_1_y-ci_1_x)/2
ci_size_2 = (ci_2_y-ci_2_x)/2

print(
    f'MTs only',
    f'{np.average(our_mts_1):.2f}+-{ci_size_1:.2f}',
    f'->',
    f'{np.average(our_mts_2):.2f}+-{ci_size_2:.2f}',
)