#!/bin/bash

# clean out working directory of generated files based on .gitignore

topdir=$(dirname $(dirname $(readlink -f $BASH_SOURCE)))
for pattern in $(cat $topdir/.gitignore)
do
    echo $pattern
    rm -f $pattern
done
