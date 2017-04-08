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
        writer = csv.DictWriter(f, fieldnames)
        stations = map(lambda x: {key: x[key] for key in fieldnames}, track_a_bike.stations.values())
        writer.writeheader()
        writer.writerows(stations)


def create_bikes():
    track_a_bike = TrackABike()
    fieldnames = ['number', 'version', 'marke_id', 'marke_name', 'is_pedelec']
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
                update[bike['number']] = {key: bike[key] for key in fieldnames}
            bikes.update(update)
            # bikes.update({free_bikes['number']: free_bikes[key] for key in fieldnames})
    with open(os.path.join(CSV_DIRECTORY, 'bikes.csv'), 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        bikes_list = list(bikes.values())
        bikes_list.sort(key=lambda x: x['number'])
        writer.writerows(bikes_list)


if __name__ == '__main__':
    if not os.path.exists(CSV_DIRECTORY):
        os.makedirs(CSV_DIRECTORY)
    track_a_bike = TrackABike()
    create_stations()
    create_bikes()
    # for timestamp, data in read_xml_dumps():
    #     track_a_bike.load_xml(data)
    #     print(track_a_bike.stations)
