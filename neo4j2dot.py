#!/usr/bin/env python3
import os

from neo4j.v1 import GraphDatabase, basic_auth
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from matplotlib import pyplot as plt
from datetime import datetime
from pprint import pprint

OUTPUT_DIRECTORY = os.path.join('graphviz', 'dot')

def get_stations(session):
    result = session.run('MATCH (station:Station) RETURN station')
    return [x['station'] for x in result]

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'Eiqu3soh'))
    session = driver.session()
    graph = nx.DiGraph()
    stations = get_stations(session)
    min_lat = min(stations, key=lambda x: x['lat'])['lat']
    min_lng = min(stations, key=lambda x: x['lng'])['lng']
    max_lat = max(stations, key=lambda x: x['lat'])['lat']
    max_lng = max(stations, key=lambda x: x['lng'])['lng']
    for station in stations:
        name = station['name']
        lat = station['lat']
        lng = station['lng']
        x = (lat - min_lat) / (max_lat - min_lat)
        y = (lng - min_lng) / (max_lng - min_lng)
        # graph.add_node(station['name'], id=station['station_id'], lat=station['lat'], lng=station['lng'])

    result = session.run("""
    MATCH (a:Station)-[r:BIKE_MOVED]->(b:Station)
    WHERE 1490778000 + 3600 * 3 <= r.timestamp_start < 1490781600 + 3600 * 3
    RETURN a, r, b""")
    for record in result:
        station_a = record['a']['name']
        station_b = record['b']['name']
        bike_id = record['r']['bike_id']
        graph.add_edge(station_a, station_b)
    write_dot(graph, os.path.join(OUTPUT_DIRECTORY, 'test.dot'))
    plt.show()