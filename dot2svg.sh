#!/usr/bin/env bash

mkdir -p graphviz/svg
cd graphviz/dot
for name in *.dot; do echo "$name" && dot -Tsvg "$name" -o "../svg/$name.svg"; done