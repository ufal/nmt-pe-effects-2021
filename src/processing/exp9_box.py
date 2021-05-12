#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU, MAX_WORD_TIME, pretty_mt_name

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mt-only', action='store_true')
args = parser.parse_args()

data = load_mx()
SKIP_SRC_REF = args.mt_only
# compute per-model data
mt_times = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
for doc in data:
    if doc.mt_name not in MT_BLEU.keys():
        continue
    # microaverage
    mt_times[doc.mt_name] += [x.edit_time_word - x.think_time_word + min(MAX_WORD_TIME, x.think_time_word) for x in doc.lines]

def top_n(n):
    # actual value plotting
    bleu_time = []
    bleu_labels = []
    for mt_name in list(mt_times.keys())[-n:]:
        bleus = MT_BLEU[mt_name]
        if SKIP_SRC_REF and mt_name in {'src', 'ref'}:
            continue
        bleu_time.append([v for v in mt_times[mt_name]])
        bleu_labels.append(f"{pretty_mt_name(mt_name)} ({bleus[0]})")

    bleu_means = [np.average(x) for x in bleu_time]

    # linear fit
    # coef = np.polyfit(xval, yval, 1)
    # poly1d_fn = np.poly1d(coef)
    # plt.plot(xval, poly1d_fn(xval), label=f'Top {n:02}, {coef[0]:>6.3f}')
    plt.scatter(range(1, len(bleu_means)+1), bleu_means, marker="s", s=10)
    plt.boxplot(bleu_time, labels=bleu_labels)
    plt.xticks(rotation=70, fontsize=9)

# misc. plot parameters
plt.figure(figsize=(4, 4.2))
top_n(15)
plt.ylim(-0.8, 45)

plt.ylim(-0.5, 20)
# plt.legend(ncol=2,handlelength=1, columnspacing=1, loc="upper center")
plt.xlabel('BLEU')
plt.ylabel(f'Total time per word (s)')
plt.tight_layout(rect=(-0.02, -0.01, 1, 1))
plt.show()
