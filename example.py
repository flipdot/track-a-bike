#!/usr/bin/env python3

from configparser import ConfigParser
from TrackABike import TrackABike
from lxml import etree
from pprint import pprint

config = ConfigParser()

config.read('config.ini')

while not 'CREDENTIALS' in config \
        or not config['CREDENTIALS']['username'] \
        or not config['CREDENTIALS']['password']:
    print('Credentials not set.')
    username = input('Username: ')
    password = input('Password: ')
    config['CREDENTIALS'] = {
        'username': username,
        'password': password,
    }
    with open('config.ini', 'w') as f:
        config.write(f)

username = config['CREDENTIALS']['username']
password = config['CREDENTIALS']['password']
track_a_bike = TrackABike(username, password)
track_a_bike.refresh()
# print(etree.tostring(track_a_bike.xml, pretty_print=True).decode('utf-8'))

stations = track_a_bike.stations
stations.sort(key=lambda x: len(x['free_bikes']), reverse=True)
fn = lambda x: f"{x['name']:50} {len(x['free_bikes'])}"
print('\n'.join(map(fn, stations)))
total_bikes = sum(map(lambda x: len(x['free_bikes']), stations))
print(f'Gesamtzahl Fahrräder: {total_bikes}')