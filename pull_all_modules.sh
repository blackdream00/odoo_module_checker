#!/bin/sh

eval "git config --global credential.helper cache"

for d in */
do
    cd $d
    echo $d
    eval "git pull"
    cd ..
done
