#!/usr/bin/env bash

# first you need to `pip install bert_score`

bertscore="../../../src/processing/bert_score.py"

for f in `ls -v [sdgm]*.txt*`; do
  score=$(bert-score -r REFERENCE.txt -c $f --lang cs 2>/dev/null | sed 's/.*F1: //')
	echo "$score $f";
done
