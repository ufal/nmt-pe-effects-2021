#!/usr/bin/env bash

for f in `ls -v [sdgm]*.txt*`; do
	BLEU=`sacrebleu -b -w 2 REFERENCE.txt < $f`
	b=`basename $f`
	echo "$BLEU $f";
done
