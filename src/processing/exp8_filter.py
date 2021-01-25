#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import MT_BLEU, MAX_WORD_TIME, MAX_SENT_TIME

parser = argparse.ArgumentParser()
#parser.add_argument('-s', '--per-sent', action='store_true')
args = parser.parse_args()

data = load_mx()
#PER_SENT = args.per_sent

MT_ORDER = sorted(MT_BLEU.keys(), key=lambda x: MT_BLEU[x][0])

doc_times = {}
for doc in data:
    #if doc.mt_name in {'src', 'ref'}:
    #    continue
    if doc.doc_name not in doc_times.keys():
        doc_times[doc.doc_name] = [[] for _ in doc.lines] 
    for line_i,line in enumerate(doc.lines):
        doc_times[doc.doc_name][line_i].append(line.edit_time_word)
doc_times = {k:[np.median(line) for line in doc_lines] for k,doc_lines in doc_times.items()}

faulty_count = 0
total_count = 0
# compute per-model data
mt_times = {k: [] for k in MT_ORDER}
for doc in data:
    condition1 = lambda line_i, line: line.edit_time_word <= MAX_WORD_TIME
    condition2 = lambda line_i, line: line.edit_time_word <= 3 * doc_times[doc.doc_name][line_i]
    condition3 = lambda line_i, line: line.edit_time_word <= 3 * doc_times[doc.doc_name][line_i] or line.edit_time_word <= 10
    condition = condition3
    positive = [line.edit_time_word for (line_i, line) in enumerate(doc.lines) if condition(line_i, line)]

    for line_i, line in enumerate(doc.lines):
        if condition(line_i, line):
            continue
        faulty_count += 1
        print(doc_times[doc.doc_name][line_i], line.edit_time_word, line.target, sep=' | ')

    mt_times[doc.mt_name] += positive
    total_count += len(doc.lines)

print('Faulty:', faulty_count, f'({faulty_count/total_count:.2f})')
print('Total:', total_count)
print('--')

# print model averages
print('\n'.join([
    f'{name:>10} {np.average(v):6.2f}'
    for name, v
    in sorted(mt_times.items(), key=lambda x: np.average(x[1]))
]))
