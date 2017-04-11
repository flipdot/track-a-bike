#!/usr/bin/env bash
PATH="$PATH:$(dirname $0)"

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

es "Creating CSV files…" &&
python xmldump2csv.py &&
es "Removing old graph.db…" &&
sudo rm -rf $HOME/neo4j/databases/graph.db/ &&
es "Creating Neo4J graph.db…" &&
sudo ./csv2neo4j.sh &&
es "Starting Neo4J…" &&
sudo docker run -d -p 7687:7687 -p 7474:7474 -v $HOME/neo4j:/data --name neo4j neo4j &&
sleep 10 && # Make sure the database is ready
es "Finding and marking bike transports…" &&
python mark_transporters.py &&
es "Generating dot files…" &&
python neo4j2dot.py &&
es "Generating svg files…" &&
dot2svg.sh &&
es "Generating png files…" &&
dot2png.sh &&
es "Done! Please note that the neo4j db is still running at localhost:7474"
