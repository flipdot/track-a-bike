#!/usr/bin/env bash
set -e
mkdir -p graphviz/svg
cd graphviz/dot

function do_se_sing() {
    dot -Tsvg -Ksfdp \
        -Goverlap=prism -Gnodesep=4 \
        -Gsplines=true -Goverlap_scaling=3 \
        -Nshape=none \
        "$1" -o "../svg/$1.svg"
}

files=(*.dot)
i=0
for f in "${files[@]}"; do
    i=$((i+1))
    trap break SIGINT
    ../../cmd_utils.py progress $i ${#files[@]} &&
    do_se_sing "$f"
done
../../cmd_utils.py clear_progress