#!/usr/bin/env bash

for f in ./{doc,sent}-cubbitt-2020/* ./commercial/* ; do
	BLEU=`sacrebleu -b -w 2 ref-cs.txt < $f`
	b=`basename $f`
	echo "$BLEU $f";
done

# for f in ./{doc,sent}-cubbitt-2020/* ./commercial/* ; do
# 	BLEU=`sacrebleu --metric ter -b ref-cs.txt < $f`
# 	b=`basename $f`
# 	echo "$BLEU $b";
# done