#!/usr/bin/env bash
sudo docker run -it --rm -v $PWD/csv:/csv -v $NEO4J_DIR:/data neo4j \
    /var/lib/neo4j/bin/neo4j-admin import \
    --id-type integer \
    --nodes:Station /csv/stations.csv \
    --nodes:Bike /csv/bikes.csv \
    --relationships:LOCATED_AT /csv/bike_positions.csv \
    --relationships:BIKE_MOVED /csv/bike_movements.csv
