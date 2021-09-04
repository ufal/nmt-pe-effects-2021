#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU, MT_TER, MAX_WORD_TIME, MT_BERTSCORE

MT_BERTSCORE["ref"] = 0
MT_BERTSCORE["src"] = 0

parser = argparse.ArgumentParser()
parser.add_argument('--ter', action='store_true')
parser.add_argument('--bert', action='store_true')
parser.add_argument('-m', '--mt-only', action='store_true')
args = parser.parse_args()

if args.ter:
    MT_BLEU = {k:(v,None) for k,v in MT_TER.items()}
if args.bert:
    MT_BLEU = {k:(v,None) for k,v in MT_BERTSCORE.items()}

data = load_mx()
SKIP_SRC_REF = args.mt_only

# compute per-model data
mt_times = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x])}
for doc in data:
    if doc.mt_name in {"refr", "m11r"}:
        continue
    # microaverage
    mt_times[doc.mt_name] += [
        x.revision_edit_time_word - x.revision_think_time_word + min(MAX_WORD_TIME, x.revision_think_time_word)
        for x in doc.lines for _ in x.source.split()]

def top_n(n, points=False):
    # actual value plotting
    bleu_time = []
    for mt_name in list(mt_times.keys())[-n:]:
        bleus = MT_BLEU[mt_name]
        if SKIP_SRC_REF and mt_name in {'src', 'ref'}:
            continue
        print(bleus)
        bleu_time += [(bleus[0], v) for v in mt_times[mt_name]]

    xval = [x[0] for x in bleu_time]
    yval = [x[1] for x in bleu_time]

    # linear fit
    coef = np.polyfit(xval, yval, 1)
    poly1d_fn = np.poly1d(coef)

    if points:
        plt.plot(xval, yval, '.', alpha=0.005, markersize=5)
    plt.plot(xval, poly1d_fn(xval), label=f'Top {n:02}, {coef[0]:>6.3f}')


# misc. plot parameters
plt.figure(figsize=(5, 4))
top_n(15, points=True)
top_n(13)
top_n(10)
top_n(8)
plt.legend()
plt.title(
    ('time per word ') +
    ('(without src, ref)' if SKIP_SRC_REF else '(with src, ref)')
)
plt.xlabel('BLEU')
perwhat = 'sentence'
plt.ylabel(f'average (per {perwhat}) word edit time')
plt.show()

# print model averages
print('\n'.join([
    f'{name:>10} {np.average(v):6.2f}'
    for name, v
    in sorted(mt_times.items(), key=lambda x: np.average(x[1]))
]))
