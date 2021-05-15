#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from utils import MT_BLEU, MT_BERTSCORE, pretty_mt_name_2

ordering = sorted([x for x in MT_BLEU.keys() if x not in {"src", "ref"}], key=lambda k: MT_BLEU[k][0])
data_bleu = [MT_BLEU[k][0] for k in ordering]
data_bertscore = [MT_BERTSCORE[k] for k in ordering]

plt.plot(data_bleu, data_bertscore)
plt.xlabel("BLEU")
plt.ylabel("bertscore")
plt.show()

print(np.corrcoef(data_bleu, data_bertscore)[0,1])
