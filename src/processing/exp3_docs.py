#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from utils import MT_BLEU, MAX_WORD_TIME, MAX_SENT_TIME

data = load_mx()

# compute per-doc data
doc_times = defaultdict(lambda: [])
for doc in data:
    doc_times[doc.doc_name] += [x.edit_time_word - x.think_time_word + min(MAX_WORD_TIME, x.think_time_word) for x in doc.lines]

def top_all():
    # actual value plotting
    bleu_time = []
    for i, doc_name in enumerate(doc_times.keys()):
        bleu_time += [(i, v) for v in doc_times[doc_name]]

    xval = [x[0] for x in bleu_time]
    yval = [x[1] for x in bleu_time]

    plt.plot(xval, yval, 'o', alpha=0.1)
    plt.xticks(
        range(len(doc_times.keys())),
        [f'{k}\n{np.average(v):.2f}s' for k, v in doc_times.items()],
        rotation=0)

# misc. plot parameters
plt.figure(figsize=(5, 4))
top_all()
plt.title('time per word (with src, ref)')
plt.ylabel('word edit time')
plt.tight_layout()
plt.show()