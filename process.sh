#!/usr/bin/env bash
PATH="$PATH:$(dirname $0)"
set -e

# Error color
ce=1 # red
# Success color
cs=2 # green

# Echo colorful
ec() {
    tput setaf "$1"
    echo "$2"
    tput sgr0
}

# Echo error
ee() {
    ec "$ce" "$@"
}

# Echo success
es() {
    ec "$cs" "$@"
}

silent() {
    "$@" > /dev/null 2>&1
}
export NEO4J_DIR="$(pwd)/neo4j"
mkdir -p "$NEO4J_DIR"

es "Creating CSV files…"
src/preprocess/xml2csv.py
es "Removing old graph.db…"
sudo rm -rf $NEO4J_DIR/databases/graph.db/
es "Creating Neo4J graph.db…"
./csv2neo4j.sh
es "Starting Neo4J…"
if ! sudo docker ps -f name=neo4j | silent grep neo4j; then
    sudo docker run -d \
        -p 7687:7687 -p 7474:7474 \
        -v "$NEO4J_DIR:/data" \
        --name neo4j \
        neo4j

fi
sleep 10 # Make sure the database is ready
es "Finding and marking bike transports…"
python mark_transporters.py
es "Generating dot files…"
python neo4j2dot.py
es "Generating svg files…"
dot2svg.sh
es "Generating png files…"
dot2png.sh

es "Done! Please note that the neo4j db is still running at localhost:7474"
