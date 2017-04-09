#!/usr/bin/env python3
import os

from neo4j.v1 import GraphDatabase, basic_auth
from datetime import datetime
from pprint import pprint

OUTPUT_DIRECTORY = os.path.join('graphviz', 'dot')

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'Eiqu3soh'))
    session = driver.session()
    result = session.run("""
        MATCH (a:Station)-[r:BIKE_MOVED]->(b:Station)
        WHERE 1490778000 + 3600 * 3 <= r.timestamp_start < 1490781600 + 3600 * 3
        RETURN a, r, b""")
    with open(os.path.join(OUTPUT_DIRECTORY, 'test.dot'), 'w') as f:
        f.write('digraph g {\n')
        for record in result:
            station_a = record['a']['name']
            station_b = record['b']['name']
            bike_id = record['r']['bike_id']
            f.write(f'"{station_a}" -> "{station_b}" [label="{bike_id}"]\n')
        f.write('}')