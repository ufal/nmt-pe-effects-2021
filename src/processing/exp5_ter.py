#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU, MAX_WORD_TIME, MAX_SENT_TIME

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mt-only', action='store_true')
parser.add_argument('-a', '--aggregate-documents', action='store_true')
args = parser.parse_args()

data = load_mx()
SKIP_SRC_REF = args.mt_only
AGGREGATE_DOCUMENTS = args.aggregate_documents

# compute per-model data
mt_times = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
for doc in data:
    if AGGREGATE_DOCUMENTS:
        doc_time_avg = np.average(
            [x.ter() for x in doc.lines]
        )
        mt_times[doc.mt_name].append(doc_time_avg)
    else:
        mt_times[doc.mt_name] += [x.ter() for x in doc.lines]


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
        plt.plot(xval, yval, '.', alpha=0.2)
    plt.plot(xval, poly1d_fn(xval), label=f'Top {n:02}: {coef[0]:>6.3f}')

# misc. plot parameters
plt.figure(figsize=(4, 3.5))
top_n(15, points=True)
top_n(13)
top_n(10)
top_n(8)
plt.legend(ncol=2,handlelength=1, columnspacing=1)
plt.xlabel('BLEU')
plt.ylabel('HTER')
plt.ylim(-0.1, 1.5)
plt.tight_layout(rect=(-0.02, -0.01, 1, 1))
plt.show()

for k,v in mt_times.items():
    print(k, f'{np.average(v):.2f}')

print('mts avg', np.average([np.average(v) for k,v in mt_times.items() if k not in {'src', 'ref'}]))
print('mts std', np.std([np.average(v) for k,v in mt_times.items() if k not in {'src', 'ref'}]))