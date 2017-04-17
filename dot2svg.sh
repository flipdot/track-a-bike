#!/usr/bin/env bash
set -e
DATA_DIR=$PWD/graphviz
mkdir -p graphviz/svg
cd graphviz/dot

function do_se_sing() {
    dot -Tsvg -Kdot \
        -Goverlap=scale \
        -Gnodesep=0.5 \
        -Goverlap_scaling=4 \
        -Gremincross=true \
        -Nshape=box \
        "/data/dot/$1" -o "/data/svg/$1.svg"
}

files=(*.dot)
i=0
for f in "${files[@]}"; do
    i=$((i+1))
    trap break SIGINT
    ../../src/utils.py progress $i ${#files[@]} &&
    do_se_sing "$f"
done
../../src/utils.py clear_progress