#!/usr/bin/env bash

mkdir -p graphviz/png
cd graphviz/dot
files=(*.dot)
i=0

for f in "${files[@]}"; do
    ((i++))
    trap break SIGINT
    ../../cmd_utils.py progress $i ${#files[@]} &&
    dot -Tpng -Gdpi=150 "$f" > "../png/$f.png"
done
../../cmd_utils.py clear_progress