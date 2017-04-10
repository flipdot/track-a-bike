#!/usr/bin/env bash
#echo -e "\033[0;32mCreating CSV files…\033[0m" &&
#python xmldump2csv.py &&
#echo -e "\033[0;32mRemoving old graph.db…\033[0m" &&
#rm -rf $HOME/neo4j/databases/graph.db/ &&
#echo -e "\033[0;32mCreating Neo4J graph.db…\033[0m" &&
#sudo ./csv2neo4j.sh &&
echo -e "\033[0;32mStarting Neo4J…\033[0m" &&
sudo docker run -d -p 7687:7687 -p 7474:7474 -v /home/soeren/neo4j:/data --name neo4j neo4j &&
sleep 10 && # Make sure the database is ready
echo -e "\033[0;32mFinding and marking bike transports…\033[0m" &&
python mark_transporters.py &&
echo -e "\033[0;32mGenerating dot files…\033[0m" &&
python neo4j2dot.py &&
echo -e "\033[0;32mGenerating svg files…\033[0m" &&
./dot2svg.sh &&
echo -e "\033[0;32mGenerating png files…\033[0m" &&
./dot2png.sh &&
echo -e "\033[0;32mDone! Please note that the neo4j db is still running at localhost:7474 \033[0m"