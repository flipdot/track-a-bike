#!/usr/bin/env python3
# -*- coding: utf-8

# This file converts the basic information we have ("csv/base/")
# into more "redundant" information which is easier to work with
# in further processing.
# TODO: `bike_movements.csv` is already a "redundant" csv. It
# TODO: should be generated here, not in `xml2csv.py`

import csv
import os

from src.utils import print_progressbar, clear_progressbar

CSV_DIRECTORY = 'csv'
OUTPUT_DIRECTORY = os.path.join(CSV_DIRECTORY, 'extra')

if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)


def get_csv(filename):
    with open(os.path.join(CSV_DIRECTORY, filename)) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def get_bike_positions():
    return get_csv('bike_positions.csv')


def get_stations():
    return get_csv('stations.csv')


if __name__ == '__main__':
    station_ids = [int(x['station_id:ID(Station)']) for x in get_stations()]
    station_ids.sort()
    number_of_rows = 0
    with open(os.path.join(CSV_DIRECTORY, 'bike_positions.csv')) as f:
        reader = csv.reader(f)
        for row in reader:
            if number_of_rows % 100000 == 0:
                print_progressbar()
            number_of_rows += 1
    with open(os.path.join(OUTPUT_DIRECTORY, 'free_bikes_at_station.csv'), 'w') as f:
        fieldnames = ['station_id:INT', 'timestamp:INT', 'free_bikes:INT']
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        current_timestamp = None
        counter = None
        i = 0
        for position in get_bike_positions():
            i += 1
            if position['timestamp:INT'] != current_timestamp:
                if counter is not None:
                    for station_id in station_ids:
                        writer.writerow({
                            'station_id:INT': station_id,
                            'timestamp:INT': current_timestamp,
                            'free_bikes:INT': counter[station_id]
                        })
                    print_progressbar(i / number_of_rows)
                current_timestamp = position['timestamp:INT']
                counter = {x: 0 for x in station_ids}
            counter[int(position[':END_ID(Station)'])] += 1
    clear_progressbar()
