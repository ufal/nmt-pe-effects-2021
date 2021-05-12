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

plt.figure(figsize=(4, 3.5))

mt_times = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
for doc in data:
    if doc.mt_name not in MT_BLEU.keys():
        continue
    mt_times[doc.mt_name] += [x.chrf_p1_p2() for x in doc.lines]
def top_n(n, points=False):
# compute per-model data

    bleu_time = []
    for mt_name in list(mt_times.keys())[-n:]:
    # for mt_name in mt_times.keys():
        bleus = MT_BLEU[mt_name]
        if SKIP_SRC_REF and mt_name in {'src', 'ref'}:
            continue
        bleu_time.append([v for v in mt_times[mt_name]])

    xval = [x[0] for x in bleu_time]
    yval = [x[1] for x in bleu_time]

    plt.boxplot(bleu_time)

top_n(15)

# misc. plot parameters
plt.xlabel('BLEU')
plt.ylabel('ChrF2')

plt.tight_layout(rect=(-0.02, -0.01, 1, 1))
plt.show()
