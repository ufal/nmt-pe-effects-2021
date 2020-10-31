#!/usr/bin/env bash

for f in ./{doc,sent}-cubbitt-2020/*; do
	BLEU=`sacrebleu -b -w 2 ref-cs.txt < $f`
	b=`basename $f`
	echo "$BLEU $f";
done
