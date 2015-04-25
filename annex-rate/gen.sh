#!/bin/bash

# regenerate the latex using 
# https://github.com/DUNE/dune-params

mydir=$(dirname $(readlink -f $BASH_SOURCE))
topdir=$(dirname $mydir)
gendir="$topdir/generated"
rm -rf $gendir
mkdir -p $gendir

export PYTHONPATH=$mydir

xls=$mydir/parameters.xls

for tmpl in templates/*.tex
do
    fname="$gendir/annex-rate-$(basename $tmpl)"
    echo "generating $fname"
    dune-params render -f datarates.filter -t $tmpl -o $fname $xls || exit 1
done

