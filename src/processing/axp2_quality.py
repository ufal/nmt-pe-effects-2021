#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU_EXT, MAX_WORD_TIME, MAX_SENT_TIME

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mt-only', action='store_true')
args = parser.parse_args()

data = load_mx()
SKIP_SRC_REF = args.mt_only

# compute per-model data
mt_times = {k: [] for k in sorted(MT_BLEU_EXT.keys(), key=lambda x: MT_BLEU_EXT[x][0])}
doc_times = defaultdict(lambda:[])
for doc in data:
    # microaverage
    mt_times[doc.mt_name] += [ x.lqa_count() for x in doc.lines ]
    doc_times[doc.doc_name] += [ x.lqa_count() for x in doc.lines ]

def top_n(n, points=False):
    # actual value plotting
    bleu_time = []
    for mt_name in list(mt_times.keys())[-n:]:
        bleus = MT_BLEU_EXT[mt_name]
        if SKIP_SRC_REF and mt_name in {'src', 'ref', 'refr'}:
            continue
        if mt_name == 'm11r':
            continue
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
top_n(17, points=True)
top_n(13)
top_n(10)
top_n(9)
plt.legend()
plt.title(
    ('per word ') +
    ('(without src, ref)' if SKIP_SRC_REF else '(with src, ref)')
)
plt.xlabel('BLEU')
plt.ylabel(f'average (per sentence)')
plt.show()

# print model averages
print('\n'.join([
    f'{name:>10} {np.average(v):6.2f}'
    for name, v
    in sorted(mt_times.items(), key=lambda x: np.average(x[1]))
]))


print("\nTotal avg:", np.average([np.average(x) for k,x in mt_times.items() if k not in {"google", "m10", "m11"}]))


print()
# print doc averages
print('\n'.join([
    f'{name:>10} {np.average(v):6.2f}'
    for name, v
    in sorted(doc_times.items(), key=lambda x: np.average(x[1]))
]))

print("audit", np.average(doc_times["audit_i"]+doc_times["audit_r"]))
print("wmt", np.average(doc_times["hole"]+doc_times["china"]+doc_times["turner"]+doc_times["whistle"]))