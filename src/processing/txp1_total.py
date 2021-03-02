#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from utils import MT_BLEU, MAX_WORD_TIME, pretty_mt_name_2, confidence_change

data = load_mx()
# compute per-model data
all_times = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
think_times = {k: [] for k in sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])}
for doc in data:
        # microaverage
        all_times[doc.mt_name] += [x.edit_time_word - x.think_time_word + min(MAX_WORD_TIME, x.edit_time_word) for x in doc.lines for _ in x.source.split()]
        think_times[doc.mt_name] += [min(MAX_WORD_TIME, x.edit_time_word) for x in doc.lines for _ in x.source.split()]

# print model averages
print('\n'.join([
    f'{pretty_mt_name_2(x_all[0]):>10} & {np.average(x_all[1]):6.2f}s$\\pm${confidence_change(x_all[1]):.2f}s & {np.average(x_think[1]):6.2f}s$\\pm${confidence_change(x_think[1]):.2f}s \\\\'
    for (x_all, x_think)
    in sorted(zip(all_times.items(), think_times.items()), key=lambda x: np.average(x[0][1]))
]))
