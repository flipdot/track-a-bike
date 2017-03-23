#!/usr/bin/env python3

from configparser import ConfigParser
from TrackABike import TrackABike
from lxml import etree

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
print(etree.tostring(track_a_bike.xml, pretty_print=True).decode('utf-8'))