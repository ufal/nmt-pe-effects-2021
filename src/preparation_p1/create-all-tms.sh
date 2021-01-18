#!/bin/bash

mydir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docs_dir="$mydir/../docs/out"

for srcfile in $docs_dir/a*.src ; do
  tgtfile="$docs_dir/$(basename $srcfile .src).tgt"
  outfile="$(basename $srcfile .src).tmx"
  python3 $mydir/create_tm.py $srcfile $tgtfile > $outfile
done
