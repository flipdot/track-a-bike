#!/usr/bin/env python3
import os

from neo4j.v1 import GraphDatabase, basic_auth
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from pprint import pprint

OUTPUT_DIRECTORY = os.path.join('graphviz', 'dot')

START_DATE = datetime.strptime('25.03.2017 00:00', '%d.%m.%Y %H:%M')
END_DATE = datetime.strptime('09.04.2017 00:00', '%d.%m.%Y %H:%M')
STEP = timedelta(hours=1)

def get_stations(session):
    result = session.run('MATCH (station:Station) RETURN station')
    return [x['station'] for x in result]

def render_hourly(session):
    date = START_DATE
    while date < END_DATE:
        print(date.strftime('%d.%m.%Y %H:%M'))
        graph = nx.MultiDiGraph()
        start = date
        end = (date + STEP)
        result = session.run("""
            MATCH (a:Station)-[r:BIKE_MOVED]->(b:Station)
            WHERE {start} <= r.timestamp_start < {end}
            RETURN a, r, b""", {'start': start.timestamp(), 'end': end.timestamp()})
        for record in result:
            station_a = record['a']['name'].replace('/', ' /\n')
            station_b = record['b']['name'].replace('/', ' /\n')
            bike_id = record['r']['bike_id']
            start_time = datetime.fromtimestamp(record['r']['timestamp_start']).strftime('%H\:%M')
            end_time = datetime.fromtimestamp(record['r']['timestamp_end']).strftime('%H\:%M')
            label = f'{start_time} -\n{end_time}'
            color = 'red' if record['r']['transporter'] else 'grey'
            penwidth = 2 if record['r']['transporter'] else 1
            graph.add_edge(station_a, station_b, label=label, color=color, penwidth=penwidth)
            # graph.add_edge(station_a, station_b, label=bike_id)
        filename = f"{start.strftime('%Y-%m-%d_%H_%M')} - {end.strftime('%Y-%m-%d_%H_%M')}.dot"
        write_dot(graph, os.path.join(OUTPUT_DIRECTORY, filename))
        date = end

def add_transporters(session, graph):
    min_cnt = 20
    result = session.run("""
        MATCH (a)-[r:BIKE_MOVED {transporter: true}]->(b)
        WITH a, b, count(*) AS cnt
        WHERE cnt > {min_cnt}
        RETURN a, b, cnt""", {'min_cnt': min_cnt})
    result = list(result)
    max_cnt = max(result, key=lambda x: x['cnt'])['cnt']
    for record in result:
        station_a = record['a']['name']
        station_b = record['b']['name']
        label = record['cnt']
        penwidth = ((record['cnt'] - min_cnt) / max_cnt) * 10
        graph.add_edge(station_a, station_b, label=label, penwidth=penwidth, color='#aa0000')

def add_popular_stations(session, graph):
    min_cnt = 27
    result = session.run("""
        MATCH (a)-[r:BIKE_MOVED]->(b)
        WHERE NOT EXISTS(r.transporter)
        WITH a, b, count(*) AS cnt
        WHERE cnt > {min_cnt}
        RETURN a, b, cnt""", {'min_cnt': min_cnt})
    result = list(result)
    max_cnt = max(result, key=lambda x: x['cnt'])['cnt']
    for record in result:
        station_a = record['a']['name']
        station_b = record['b']['name']
        label = record['cnt']
        penwidth = ((record['cnt'] - min_cnt) / max_cnt) * 10
        graph.add_edge(station_a, station_b, label=label, penwidth=penwidth, color='#00aa00')

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'Eiqu3soh'))
    session = driver.session()
    stations = get_stations(session)
    # render_hourly(session)
    graph = nx.MultiDiGraph()
    add_transporters(session, graph)
    add_popular_stations(session, graph)
    write_dot(graph, os.path.join(OUTPUT_DIRECTORY, 'popular.dot'))
    # nx.drawing.draw(graph)
    # plt.show()