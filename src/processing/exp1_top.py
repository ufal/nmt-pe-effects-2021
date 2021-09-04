#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU, MAX_WORD_TIME, MAX_SENT_TIME, MT_TER

parser = argparse.ArgumentParser()
parser.add_argument('--ter', action='store_true')
parser.add_argument('-m', '--mt-only', action='store_true')
args = parser.parse_args()

data = load_mx()

if args.ter:
    MT_BLEU = {k:(v,None) for k,v in MT_TER.items()}


SKIP_SRC_REF = args.mt_only
# compute per-model data
mt_times = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0], reverse=args.ter)}
for doc in data:
    if doc.mt_name not in MT_BLEU.keys():
        continue
    # microaverage
    mt_times[doc.mt_name] += [x.edit_time_word - x.think_time_word + min(MAX_WORD_TIME, x.think_time_word) for x in doc.lines for _ in x.source.split()]
    # mt_times[doc.mt_name] += [x.edit_time_word - x.think_time_word + min(MAX_WORD_TIME, x.think_time_word) for x in doc.lines]

def top_n(n, points=False):
    # actual value plotting
    bleu_time = []
    for mt_name in list(mt_times.keys())[-n:]:
        bleus = MT_BLEU[mt_name]
        if SKIP_SRC_REF and mt_name in {'src', 'ref'}:
            continue
        bleu_time += [(bleus[0], v) for v in mt_times[mt_name]]

    xval = [x[0] for x in bleu_time]
    yval = [x[1] for x in bleu_time]

    # linear fit
    coef = np.polyfit(xval, yval, 1)
    poly1d_fn = np.poly1d(coef)

    if points:
        plt.plot(xval, yval, '.', alpha=0.005, markersize=6)
    plt.plot(xval, poly1d_fn(xval), label=f'Top {n:02}, {coef[0]:>6.3f}')

# misc. plot parameters
plt.figure(figsize=(4, 3.5))
top_n(15, points=True)
top_n(13)
top_n(10)
top_n(8)
plt.ylim(-0.8, 45)

plt.ylim(-0.5, 20)
plt.legend(ncol=2,handlelength=1, columnspacing=1, loc="upper center")
plt.xlabel('BLEU')
plt.ylabel(f'Total time per word (s)')
plt.tight_layout(rect=(-0.02, -0.01, 1, 1))
plt.show()
