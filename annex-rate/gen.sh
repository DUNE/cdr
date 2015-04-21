#!/bin/bash

# regenerate the latex using 
# https://github.com/DUNE/dune-params

mydir=$(dirname $(readlink -f $BASH_SOURCE))
gendir="$mydir/gen"
rm -rf $gendir
mkdir -p $gendir

export PYTHONPATH=$mydir

xls=$mydir/parameters.xls

for tmpl in templates/*.tex
do
    fname="$gendir/$(basename $tmpl)"
    dune-params render -f datarates.filter -t $tmpl -o $fname $xls
done

