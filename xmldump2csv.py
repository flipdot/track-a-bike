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


if __name__ == '__main__':
    if not os.path.exists(CSV_DIRECTORY):
        os.makedirs(CSV_DIRECTORY)
    track_a_bike = TrackABike()
    create_stations()
    # for timestamp, data in read_xml_dumps():
    #     track_a_bike.load_xml(data)
    #     print(track_a_bike.stations)
