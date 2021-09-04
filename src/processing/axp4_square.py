#!/usr/bin/env python3

from load import *
import numpy as np
from collections import defaultdict
from utils import MT_BLEU_EXT, DOMAIN_MAP, pretty_mt_name_2

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

for mt_name in MT_BLEU_EXT.keys():
    lqa1 = np.average([x[0] for x in mt_times[mt_name]])
    lqa2 = np.average([x[1] for x in mt_times[mt_name]])
    lqa8 = np.average([x[2] for x in mt_times[mt_name]])
    lqaAvg = np.average([sum(x) for x in mt_times[mt_name]])
    print(pretty_mt_name_2(mt_name),
        "& \\blocksimple{", lqa1, "}",
        "& \\blocksimple{", lqa2, "}",
        "& \\blocksimple{", lqa8, "}",
        "& \\blocksimple{", lqaAvg, "}",
        "\\\\"
    )

print("\n\midrule\n")

for doc_name in list(domain_times.keys()):
    lqa1 = np.average([x[0] for x in domain_times[doc_name]])
    lqa2 = np.average([x[1] for x in domain_times[doc_name]])
    lqa8 = np.average([x[2] for x in domain_times[doc_name]])
    lqaAvg = np.average([sum(x) for x in domain_times[doc_name]])
    print(doc_name,
        "& \\blocksimple{", lqa1, "}",
        "& \\blocksimple{", lqa2, "}",
        "& \\blocksimple{", lqa8, "}",
        "& \\blocksimple{", lqaAvg, "}",
        "\\\\"
    )