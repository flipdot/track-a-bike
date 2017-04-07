#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TrackABike import TrackABike, read_xml_dumps
from neo4j.v1 import GraphDatabase, basic_auth


def wipe_database(session):
    session.run('MATCH (a)-[r]->(b) DELETE r')
    session.run('MATCH (a) DELETE a')


def create_stations(session):
    track_a_bike = TrackABike()
    timestamp, data = next(read_xml_dumps())
    track_a_bike.load_xml(data)
    for k, station in track_a_bike.stations.items():
        # print(station['id'])
        session.run('MERGE (a:Station {name: {name}, id: {id}})', {'id': k, 'name': station['name']})


def bike_is_at_station(station, bike_number):
    bike_numbers = map(lambda x: x['number'], station['free_bikes'])
    return bike_number in bike_numbers


def find_bike_station(stations, bike_number):
    for id_, station in stations.items():
        if bike_is_at_station(station, bike_number):
            return id_


def create_moving_bikes_relations(session):
    bike_positions = {}
    track_a_bike = TrackABike()
    for timestamp, data in read_xml_dumps():
        print(timestamp)
        track_a_bike.load_xml(data)
        for station_id, station in track_a_bike.stations.items():
            for bike in station['free_bikes']:
                bike_id = bike['number']
                prev_station = bike_positions.get(bike_id, None)
                session.run("MERGE (a:Bike {id: {bike}})", {'bike': bike_id})
                session.run("""
                    MATCH (a:Bike {id: {bike}})
                    MATCH (b:Station {id: {station}})
                    CREATE (a)-[r:LOCATED_AT {
                        timestamp: {timestamp},
                        timestamp_str: {timestamp_str}
                    }]->(b)""", {
                        'bike': bike_id,
                        'station': station_id,
                        'timestamp': timestamp.timestamp(),
                        'timestamp_str': timestamp.strftime('%Y-%m-%d %H:%M')
                })
                if prev_station is not None and prev_station['id'] != station_id:
                    # print(f'{prev_station_id}->{station_id}')
                    bike_positions[bike_id] = station_id
                    session.run("""
                             MATCH (a:Station {id: {station_a}})
                             MATCH (b:Station {id: {station_b}})
                             CREATE (a)-[r:BIKE_MOVED {
                                timestamp: {timestamp},
                                timestamp_str: {timestamp_str},
                                bike_id: {bike_id},
                                duration: {duration}
                            }]->(b)""",
                                {
                                    'station_a': prev_station['id'],
                                    'station_b': station_id,
                                    'timestamp': timestamp.timestamp(),
                                    'timestamp_str': timestamp.strftime('%Y-%m-%d %H:%M'),
                                    'duration': (timestamp - prev_station['timestamp']).total_seconds(),
                                    'bike_id': bike_id,
                                })
                bike_positions[bike_id] = {'id': station_id, 'timestamp': timestamp}


if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "Eiqu3soh"))
    session = driver.session()
    wipe_database(session)
    create_stations(session)
    create_moving_bikes_relations(session)
    session.close()
