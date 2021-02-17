#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU, MAX_WORD_TIME, MAX_SENT_TIME, pretty_mt_name
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--sent', action='store_true')
args = parser.parse_args()

data = load_mx()
SENT_AVERAGE = args.sent

MT_ORDER = sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])

user_times = defaultdict(lambda: [])
for doc in data:
    user_times[doc.user_u] += [
        x.edit_time_word + x.think_time_word -
        min(MAX_WORD_TIME, x.think_time_word)
        for x in doc.lines for _ in x.source.split()
    ]

# compute per-model data
mt_times = {k: [] for k in MT_ORDER}
for doc in data:
    if SENT_AVERAGE:
        mt_times[doc.mt_name] += [x.edit_time_word for x in doc.lines]
    else:
        #  - np.average(user_times[doc.user_u])) / np.std(user_times[doc.user_u]
        mt_times[doc.mt_name] += [
            (x.edit_time_word + x.think_time_word -
            min(MAX_WORD_TIME, x.think_time_word))
            for x in doc.lines for _ in x.source.split()
        ]

for mt_name, mt_vals in mt_times.items():
    mt_times[mt_name] = sorted(mt_vals, reverse=False)[:int(0.85*len(mt_vals))]

# misc. plot parameters
fig, ax1 = plt.subplots(figsize=(5, 4))
ax2 = ax1.twinx()

ax1.boxplot(mt_times.values())
ax2.plot(range(1, len(mt_times.keys())+1),
         [MT_BLEU[x][0] for x in MT_ORDER], '*', alpha=1, markersize=7)
ax1.set_xticks(range(1, len(mt_times.keys())+1))
ax1.set_xticklabels([pretty_mt_name(x) for x in mt_times.keys()], rotation=45)

#plt.title('Time per word')
ax1.set_ylabel('Word edit time')
ax2.set_ylabel('BLEU')
plt.tight_layout()
plt.show()


# print model averages
print('\n'.join([
    f'{name:>10} {np.average(v):6.2f}'
    for name, v
    in sorted(mt_times.items(), key=lambda x: np.average(x[1]))
]))
