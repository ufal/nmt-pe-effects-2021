#!/usr/bin/env python3

from utils import MT_BLEU
from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--per-sent', action='store_true')
args = parser.parse_args()

data = load_mx()
PER_SENT = args.per_sent
MAX_WORD_TIME = 20
MAX_SENT_TIME = MAX_WORD_TIME*20

MT_ORDER = sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])

# compute per-model data
mt_times = {k: [] for k in MT_ORDER}
for doc in data:
    if PER_SENT:
        mt_times[doc.mt_name] += [x.edit_time for x in doc.lines if x.edit_time <= MAX_SENT_TIME]
    else:
        mt_times[doc.mt_name] += [x.edit_time_word for x in doc.lines if x.edit_time_word <= MAX_WORD_TIME]


def top_all():
    # actual value plotting
    bleu_time = []
    for i, mt_name in enumerate(mt_times.keys()):
        bleus = MT_BLEU[mt_name]
        bleu_time += [(i, v) for v in mt_times[mt_name]]

    xval = [x[0] for x in bleu_time]
    yval = [x[1] for x in bleu_time]

    # linear fit
    coef = np.polyfit(xval, yval, 1)
    poly1d_fn = np.poly1d(coef)
    plt.plot(xval, yval, 'o', alpha=0.1)
    plt.plot(xval, poly1d_fn(xval), label=f'Coef: {coef[0]:>6.3f}')
    plt.xticks(range(len(MT_ORDER)), MT_ORDER, rotation=90)
    explanation = (
        ('time per line = ' if PER_SENT else 'time per word = ') +
        str(poly1d_fn).strip().replace(' x', '*BLEU') + '\n' +
        '(with src, ref)'
    )


# misc. plot parameters
plt.figure(figsize=(5, 4))
top_all()
plt.legend()
TITLE = ('time per line ' if PER_SENT else 'time per word ') + '(with src, ref)'
plt.title(TITLE)
plt.ylabel('line edit time' if PER_SENT else 'word edit time')
plt.tight_layout()
plt.show()


# print model averages
print(TITLE)
print('\n'.join([
    f'{name:>10} {np.average(v):6.2f}'
    for name, v
    in sorted(mt_times.items(), key=lambda x: np.average(x[1]))
]))
