#!/usr/bin/env python3

from utils import MT_BLEU
from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--per-sent', action='store_true', default=False)
parser.add_argument('-m', '--mt-only', action='store_true', default=False)
parser.add_argument('-a', '--aggregate-documents', action='store_true', default=False)
args = parser.parse_known_args()[0]

data = load_mx()
SKIP_SRC_REF = args.mt_only
AGGREGATE_DOCUMENTS = args.aggregate_documents
PER_SENT = args.per_sent
MAX_WORD_TIME = 40 
MAX_SENT_TIME = MAX_WORD_TIME*20

mt_times = {k:[] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
for doc in data:
    if not AGGREGATE_DOCUMENTS:
        mt_times[doc.mt_name] += [x.edit_time_word for x in doc.lines if x.edit_time_word <= MAX_WORD_TIME]
    else:
        if PER_SENT:
            doc_time_avg = np.average([x.edit_time for x in doc.lines])
            if doc_time_avg <= MAX_SENT_TIME:
                mt_times[doc.mt_name].append(doc_time_avg)
        else:
            doc_time_avg = np.average([x.edit_time_word for x in doc.lines])
            if doc_time_avg <= MAX_WORD_TIME:
                mt_times[doc.mt_name].append(doc_time_avg)

def top_n(n, points=False):
    bleu_time = []
    for mt_name in list(mt_times.keys())[-n:]:
        bleus = MT_BLEU[mt_name]
        if SKIP_SRC_REF and mt_name in {'src', 'ref'}:
            continue
        bleu_time += [(bleus[0], v) for v in mt_times[mt_name]]


    xval = [x[0] for x in bleu_time]
    yval = [x[1] for x in bleu_time]

    # linear fit
    coef = np.polyfit(xval,yval,1)
    poly1d_fn = np.poly1d(coef) 

    if points:
        plt.plot(xval, yval, '.', alpha=0.5)
    plt.plot(xval, poly1d_fn(xval), label=f'Top {n:02}, {coef[0]:>6.3f}')
    explanation = (
        ('time per line = ' if PER_SENT else 'time per word = ') +
        str(poly1d_fn).strip().replace(' x', '*BLEU') + '\n' +
        ('(without src, ref)' if SKIP_SRC_REF else '(with src, ref)')
    )

plt.figure(figsize=(5,4))
top_n(15, points=True)
top_n(13)
top_n(10)
top_n(8)
plt.legend()
plt.title(
        ('time per line ' if PER_SENT else 'time per word ') +
        ('(without src, ref)' if SKIP_SRC_REF else '(with src, ref)')
)
plt.xlabel('BLEU')
perwhat = 'document' if AGGREGATE_DOCUMENTS else 'sentence'
plt.ylabel(f'average (per {perwhat}) line edit time' if PER_SENT else f'average (per {perwhat}) word edit time')
plt.show()