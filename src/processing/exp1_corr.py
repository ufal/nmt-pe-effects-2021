#!/usr/bin/env python3

from utils import MT_BLEU
from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = load_mx()
SKIP_SRC_REF = False
PER_SENT = False
MAX_WORD_TIME = 40 
MAX_SENT_TIME = MAX_WORD_TIME*20

mt_times = {k:[] for k in MT_BLEU.keys()}

for doc in data:
    if PER_SENT:
        doc_time_avg = np.average([x.edit_time for x in doc.lines])
        if doc_time_avg <= MAX_SENT_TIME:
            mt_times[doc.mt_name].append(doc_time_avg)
    else:
        doc_time_avg = np.average([x.edit_time_word for x in doc.lines])
        if doc_time_avg <= MAX_WORD_TIME:
            mt_times[doc.mt_name].append(doc_time_avg)


bleu_time = []
for mt_name, bleus in MT_BLEU.items():
    if SKIP_SRC_REF and mt_name in {'src', 'ref'}:
        continue
    bleu_time += [(bleus[0], v) for v in mt_times[mt_name]]


xval = [x[0] for x in bleu_time]
yval = [x[1] for x in bleu_time]

# linear fit
coef = np.polyfit(xval,yval,1)
poly1d_fn = np.poly1d(coef) 

plt.figure(figsize=(5,4))
plt.plot(xval, yval, '.', xval, poly1d_fn(xval))
plt.title(
    ('time per line = ' if PER_SENT else 'time per word = ') +
    str(poly1d_fn).strip().replace(' x', '*BLEU') + '\n' +
    ('(without src, ref)' if SKIP_SRC_REF else '(with src, ref)')
)
plt.xlabel('BLEU')
plt.ylabel('average (per document) line edit time' if PER_SENT else 'average (per document) word edit time')
plt.show()