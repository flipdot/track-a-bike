#!/usr/bin/env bash

mkdir -p graphviz/png
cd graphviz/dot
rm -rf ../png/*
for name in *.dot; do echo "$name" && dot -Tpng -Gdpi=150 "$name" -o "../png/$name.png"; done