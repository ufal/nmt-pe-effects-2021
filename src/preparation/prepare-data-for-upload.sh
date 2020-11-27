#!/bin/bash

mydir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docs_dir="$mydir/../docs/out"

mkdir -p upload-to-memsource

idx=1
for srcfile in $docs_dir/a*.src ; do
  tgtfile="$docs_dir/$(basename $srcfile .src).tgt"
  python3 $mydir/src/create_tm.py $srcfile $tgtfile > upload-to-memsource/tm-$idx.tmx
  cp $srcfile upload-to-memsource/input-file-$idx.txt
  idx=$(( $idx + 1))
done
