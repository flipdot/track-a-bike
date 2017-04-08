#!/usr/bin/env python3
import os

import sys

from TrackABike import TrackABike, read_xml_dumps
import csv

CSV_DIRECTORY = 'csv'


def create_stations():
    track_a_bike = TrackABike()
    timestamp, data = next(read_xml_dumps())
    track_a_bike.load_xml(data)
    with open(os.path.join(CSV_DIRECTORY, 'stations.csv'), 'w') as f:
        fieldnames = ['id', 'name', 'lat', 'lng', 'is_outside']
        headernames = {'id': 'station_id:ID(Station)'}
        writer = csv.DictWriter(f, [headernames.get(x, x) for x in fieldnames])
        stations = map(lambda x: {headernames.get(key, key): x[key] for key in fieldnames},
                       track_a_bike.stations.values())
        writer.writeheader()
        writer.writerows(stations)


def create_bikes():
    track_a_bike = TrackABike()
    fieldnames = ['number', 'version', 'marke_id', 'marke_name', 'is_pedelec']
    headernames = {'number': 'bike_id:ID(Bike)'}
    bikes = {}
    i = 0
    for timestamp, data in read_xml_dumps():
        i += 1
        # We want to build a list of all bikes. Since some bikes may be rented or are even in maintenance,
        # it is not enough to look at a given moment. To save time, we just don't need to look at every
        # minute, so we just process a dataset every hour
        if i % 60:
            continue
        print(timestamp)
        track_a_bike.load_xml(data)
        for station in track_a_bike.stations.values():
            # print(station['free_bikes'])
            update = {}
            for bike in station['free_bikes']:
                update[bike['number']] = {headernames.get(key, key): bike[key] for key in fieldnames}
            bikes.update(update)
            # bikes.update({free_bikes['number']: free_bikes[key] for key in fieldnames})
    with open(os.path.join(CSV_DIRECTORY, 'bikes.csv'), 'w') as f:
        writer = csv.DictWriter(f, [headernames.get(x, x) for x in fieldnames])
        writer.writeheader()
        bikes_list = list(bikes.values())
        bikes_list.sort(key=lambda x: x['bike_id:ID(Bike)'])
        writer.writerows(bikes_list)


def create_bike_positions():
    track_a_bike = TrackABike()
    fieldnames = ['number', 'timestamp', 'can_be_rented', 'can_be_returned', 'station_id']
    headernames = {
        'number': ':START_ID(Bike)',
        'station_id': ':END_ID(Station)'
    }
    with open(os.path.join(CSV_DIRECTORY, 'bike_positions.csv'), 'w') as f:
        writer = csv.DictWriter(f, [headernames.get(x, x) for x in fieldnames])
        writer.writeheader()
        i = 0
        for timestamp, data in read_xml_dumps():
            i += 1
            if i % 60 == 0:
                print(timestamp)
            track_a_bike.load_xml(data)
            for station in track_a_bike.stations.values():
                bike_positions = []
                for bike in station['free_bikes']:
                    bike_position = {headernames.get(key, key): bike.get(key, None) for key in fieldnames}
                    bike_position[headernames['station_id']] = station['id']
                    bike_position['timestamp'] = timestamp.timestamp()
                    bike_positions.append(bike_position)
                writer.writerows(bike_positions)

if __name__ == '__main__':
    if not os.path.exists(CSV_DIRECTORY):
        os.makedirs(CSV_DIRECTORY)
    track_a_bike = TrackABike()
    print('Creating stations.csv…')
    create_stations()
    print('Creating bikes.csv…')
    create_bikes()
    print('Creating bike_positions.csv…')
    create_bike_positions()
    # for timestamp, data in read_xml_dumps():
    #     track_a_bike.load_xml(data)
    #     print(track_a_bike.stations)
