#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU, MAX_WORD_TIME, MAX_SENT_TIME

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mt-only', action='store_true')
args = parser.parse_args()

data = load_mx()
SKIP_SRC_REF = args.mt_only

# compute per-model data
mt_times = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
for doc in data:
    mt_times[doc.mt_name] += [len(x.provided.split())-len(x.target.split()) for x in doc.lines]

for k, v in mt_times.items():
    print(f'{k:>10} {np.average(v):.2f}')

our_mts = {k:np.average(v) for k,v in mt_times.items() if k not in {'src', 'ref'}}
print(f'our mts {np.average(list(our_mts.values())):.2f}+-{np.std(list(our_mts.values())):.2f}')