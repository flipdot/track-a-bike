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
        headernames = {
            'id': 'station_id:ID(Station)',
            'lat': 'lat:FLOAT',
            'lng': 'lng:FLOAT',
            'is_outside': 'is_outside:BOOLEAN'
        }
        writer = csv.DictWriter(f, [headernames.get(x, x) for x in fieldnames])
        stations = map(lambda x: {headernames.get(key, key): x[key] for key in fieldnames},
                       track_a_bike.stations.values())
        writer.writeheader()
        writer.writerows(stations)


def create_bikes():
    track_a_bike = TrackABike()
    fieldnames = ['number', 'version', 'marke_id', 'marke_name', 'is_pedelec']
    headernames = {
        'number': 'bike_id:ID(Bike)',
        'version': 'version:INT',
        'marke_id': 'marke_id:INT',
        'is_pedelec': 'is_pedelec:BOOLEAN'
    }
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


def create_bike_positions_and_movement():
    fieldnames_position = ['number', 'timestamp', 'can_be_rented', 'can_be_returned', 'station_id']
    headernames_position = {
        'number': ':START_ID(Bike)',
        'station_id': ':END_ID(Station)',
        'timestamp': 'timestamp:INT',
        'can_be_rented': 'can_be_rented:BOOLEAN',
    }
    fieldnames_movement = [':START_ID(Station)', ':END_ID(Station)', 'timestamp_start:INT', 'timestamp_end:INT',
                           'duration:INT', 'bike_id:INT']
    with open(os.path.join(CSV_DIRECTORY, 'bike_positions.csv'), 'w') as f:
        with open(os.path.join(CSV_DIRECTORY, 'bike_movements.csv'), 'w') as f2:
            position_writer = csv.DictWriter(f, [headernames_position.get(x, x) for x in fieldnames_position])
            movement_writer = csv.DictWriter(f2, fieldnames_movement)
            position_writer.writeheader()
            movement_writer.writeheader()
            i = 0
            track_a_bike = TrackABike()
            current_bike_positions = {}
            for timestamp, data in read_xml_dumps():
                i += 1
                if i % 60 == 0:
                    print(timestamp)
                track_a_bike.load_xml(data)
                for station in track_a_bike.stations.values():
                    bike_positions = []
                    for bike in station['free_bikes']:
                        bike_id = bike['number']
                        prev_station = current_bike_positions.get(bike_id, None)
                        if prev_station is not None and prev_station['id'] != station['id']:
                            movement_writer.writerow({
                                ':START_ID(Station)': prev_station['id'],
                                ':END_ID(Station)': station['id'],
                                'timestamp_start:INT': int(prev_station['timestamp'].timestamp()),
                                'timestamp_end:INT': int(timestamp.timestamp()),
                                'duration:INT': (timestamp - prev_station['timestamp']).total_seconds(),
                                'bike_id:INT': bike_id,
                            })
                        current_bike_positions[bike_id] = {'id': station['id'], 'timestamp': timestamp}
                        bike_position = {headernames_position.get(key, key): bike.get(key, None) for key in
                                         fieldnames_position}
                        bike_position[headernames_position['station_id']] = station['id']
                        bike_position[headernames_position['timestamp']] = int(timestamp.timestamp())
                        bike_positions.append(bike_position)
                    position_writer.writerows(bike_positions)


if __name__ == '__main__':
    if not os.path.exists(CSV_DIRECTORY):
        os.makedirs(CSV_DIRECTORY)
    track_a_bike = TrackABike()
    print('Creating stations.csv…')
    create_stations()
    print('Creating bikes.csv…')
    create_bikes()
    print('Creating bike_positions.csv and bike_movements.csv…')
    create_bike_positions_and_movement()
    # for timestamp, data in read_xml_dumps():
    #     track_a_bike.load_xml(data)
    #     print(track_a_bike.stations)
