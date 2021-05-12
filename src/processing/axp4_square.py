#!/usr/bin/env python3

from load import *
import numpy as np
from collections import defaultdict
from utils import MT_BLEU_EXT, DOMAIN_MAP, pretty_mt_name

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mt-only', action='store_true')
args = parser.parse_args()

data = load_mx()
SKIP_SRC_REF = args.mt_only

# compute per-model data
mt_times = {k: [] for k in sorted(MT_BLEU_EXT.keys(), key=lambda x: MT_BLEU_EXT[x][0])}
domain_times = defaultdict(lambda:[])
for doc in data:
    # microaverage
    mt_times[doc.mt_name] += [ x.lqa_distribution() for x in doc.lines ]
    domain_times[DOMAIN_MAP[doc.doc_name]] += [ x.lqa_distribution() for x in doc.lines ]

# for mt_name in list(mt_times.keys()):
#     lqa1 = np.average([x[0] for x in mt_times[mt_name]])
#     lqa2 = np.average([x[1] for x in mt_times[mt_name]])
#     lqa8 = np.average([x[2] for x in mt_times[mt_name]])
#     lqaAvg = np.average([x for x in mt_times[mt_name]])
#     print(pretty_mt_name(mt_name),
#         "& \\blocksimple{", lqa1, "}",
#         "& \\blocksimple{", lqa2, "}",
#         "& \\blocksimple{", lqa8, "}",
#         "& \\blocksimple{", lqaAvg, "}",
#         "\\\\"
#     )

for doc_name in list(domain_times.keys()):
    lqa1 = np.average([x[0] for x in domain_times[doc_name]])
    lqa2 = np.average([x[1] for x in domain_times[doc_name]])
    lqa8 = np.average([x[2] for x in domain_times[doc_name]])
    lqaAvg = np.average([x for x in domain_times[doc_name]])
    print(doc_name,
        "& \\blocksimple{", lqa1, "}",
        "& \\blocksimple{", lqa2, "}",
        "& \\blocksimple{", lqa8, "}",
        "& \\blocksimple{", lqaAvg, "}",
        "\\\\"
    )

# print('\n'.join([
#     f'{name:>10} {np.average(v):6.2f}'
#     for name, v
#     in sorted(mt_times.items(), key=lambda x: np.average(x[1]))
# ]))


# print("\nTotal avg:", np.average([np.average(x) for k,x in mt_times.items() if k not in {"google", "m10", "m11"}]))


# print()
# # print doc averages
# print('\n'.join([
#     f'{name:>10} {np.average(v):6.2f}'
#     for name, v
#     in sorted(doc_times.items(), key=lambda x: np.average(x[1]))
# ]))

# print("audit", np.average(doc_times["audit_i"]+doc_times["audit_r"]))
# print("wmt", np.average(doc_times["hole"]+doc_times["china"]+doc_times["turner"]+doc_times["whistle"]))