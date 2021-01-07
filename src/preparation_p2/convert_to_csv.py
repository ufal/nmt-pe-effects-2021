#!/usr/bin/env python3

import pandas as pd
from typing import Tuple, Iterator


def read_parallel_corpus(src_file: str, tgt_file: str) -> Iterator[Tuple[str, str]]:
    with open(src_file) as src_hdl, open(tgt_file) as tgt_hdl:
        for src_line, tgt_line in zip(src_hdl, tgt_hdl):
            yield src_line.rstrip(), tgt_line.rstrip()

for i in range(17):
    segments = read_parallel_corpus(f"docs/out_p2/k{i}.src", f"docs/out_p2/k{i}.tgt")
    df = pd.DataFrame(segments, columns=("en", "cs"))
    df.to_csv(f"revision-{i + 1}.csv", header=False, index=False)

