#!/usr/bin/env python3

from load import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import pretty_mt_name_2, MT_BLEU_EXT

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mt-only', action='store_true')
args = parser.parse_args()

data = load_mx()
SKIP_SRC_REF = args.mt_only

# compute per-model data
mt_times_0_1 = {k: [] for k in sorted(MT_BLEU_EXT.keys(), key=lambda x: MT_BLEU_EXT[x][0])}
mt_times_1_2 = {k: [] for k in sorted(MT_BLEU_EXT.keys(), key=lambda x: MT_BLEU_EXT[x][0])}
mt_times_0_2 = {k: [] for k in sorted(MT_BLEU_EXT.keys(), key=lambda x: MT_BLEU_EXT[x][0])}
for doc in data:
    mt_times_1_2[doc.mt_name] += [x.chrf_p1_p2() for x in doc.lines]
    mt_times_0_2[doc.mt_name] += [x.chrf_p0_p2() for x in doc.lines]
    mt_times_0_1[doc.mt_name] += [x.chrf_p0_p1() for x in doc.lines]

def top_n(n, points=False):
    # actual value plotting
    bleu_time = []
    for mt_name in list(mt_times_0_1.keys())[-n:]:
        bleus = MT_BLEU_EXT[mt_name]
        if SKIP_SRC_REF and mt_name in {'src', 'ref', 'refr'}:
            continue
        if mt_name == "m11r":
            continue
        bleu_time += [(bleus[0], v) for v in mt_times_0_2[mt_name]]

    xval = [x[0] for x in bleu_time]
    yval = [x[1] for x in bleu_time]

    # linear fit
    coef = np.polyfit(xval, yval, 1)
    poly1d_fn = np.poly1d(coef)

    if points:
        plt.plot(xval, yval, '.', alpha=0.2, markersize=6)
    plt.plot(xval, poly1d_fn(xval), label=f'Top {n:02}: {coef[0]:>6.3f}')

# misc. plot parameters
plt.figure(figsize=(4, 3.5))
top_n(17, points=True)
top_n(13)
top_n(10)
top_n(9)
plt.legend(ncol=2,handlelength=1, columnspacing=1, loc="upper center")
plt.xlabel('BLEU')
plt.ylabel('ChrF6')
plt.ylim(0, 1.28)
plt.tight_layout(rect=(-0.02, -0.01, 1, 1))
plt.show()

print('mts avg', np.average([np.average(v) for k,v in mt_times_1_2.items() if k not in {'src', 'ref', 'refr'}]))
print('mts std', np.std([np.average(v) for k,v in mt_times_1_2.items() if k not in {'src', 'ref', 'refr'}]))
print("\n")


# print latex table
for (mt_name,p1_p2),(_, p0_p2),(_, p0_p1) in zip(mt_times_1_2.items(), mt_times_0_2.items(), mt_times_0_1.items()):
    print(pretty_mt_name_2(mt_name), "&", f'{np.average(p0_p1):.2f}', '&', f'{np.average(p1_p2):.2f}', '&', f'{np.average(p0_p2):.2f}', '\\\\')
print("\\midrule")
avg_p0_p1 = np.average([np.average(v) for v in mt_times_0_1.values() if np.average(v) != 0])
avg_p0_p2 = np.average([np.average(v) for v in mt_times_0_2.values() if np.average(v) != 0])
avg_p1_p2 = np.average([np.average(v) for v in mt_times_1_2.values() if np.average(v) != 0])
print("\\textbf{Average}", f" & {avg_p0_p1:.2f} & {avg_p1_p2:.2f} & {avg_p0_p2:.2f} \\\\")