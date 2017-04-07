#!/usr/bin/env python3
from neo4j.v1 import GraphDatabase, basic_auth
import matplotlib.pyplot as plt
from numpy.random import rand
from datetime import datetime

from TrackABike import read_xml_dumps, TrackABike
from pprint import pprint

if __name__ == '__main__':
    track_a_bike = TrackABike()
    timestamp, data = next(read_xml_dumps())
    track_a_bike.load_xml(data)
    stations = track_a_bike.stations
    for id_, station in stations.items():
        print(id_, station['name'], station['free_bikes'])
    empty_stations = filter(lambda x: len(x['free_bikes']) == 0, stations.values())
    sorted_stations = sorted(stations.values(), key=lambda x: len(x['free_bikes']))
    pprint(list(map(lambda x: (x['name'], len(x['free_bikes'])), sorted_stations)))
    for station in empty_stations:
        print(station)
        # nstations.items():
        #     print(len(station['free_bikes']))
    # fig, ax = plt.subplots()
    #
    # driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "Eiqu3soh"))
    # session = driver.session()
    # result = list(session.run("MATCH (a) RETURN a.name as name"))
    # stations = list(map(lambda x: x['name'], result))
    # result = list(session.run("MATCH (a)-[r]->(b) RETURN a.name as name, r.timestamp as timestamp;"))
    # x = list(map(lambda x: datetime.fromtimestamp(x['timestamp']).hour, result))
    # y = list(map(lambda x: stations.index(x['name']), result))
    # # scale =
    # ax.scatter(x, y, alpha=0.05, edgecolors='none')
    #
    # result = list(session.run("MATCH (a)-[r]->(b) RETURN b.name as name, r.timestamp as timestamp;"))
    # x = list(map(lambda x: datetime.fromtimestamp(x['timestamp']).hour + 0.5, result))
    # y = list(map(lambda x: stations.index(x['name']), result))
    # # scale =
    # ax.scatter(x, y, alpha=0.05, color='red', edgecolors='none')
    #
    # ax.legend()
    # ax.grid(True)
    #
    # plt.show()
