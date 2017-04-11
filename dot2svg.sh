#!/usr/bin/env bash

mkdir -p graphviz/png
cd graphviz/dot
files=(*.dot)
i=0

for name in *.dot; do
    ((i++))
    trap break SIGINT
    python ../../cmd_utils.py progress $i ${#files[@]} &&
    dot -Tsvg "$name" > "../svg/$name.svg"
done