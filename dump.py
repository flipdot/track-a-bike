#!/usr/bin/env python3

import os
import sys
from configparser import ConfigParser
from datetime import datetime

from track_a_bike import TrackABike

DUMP_DIRECTORY = sys.argv[1] if len(sys.argv) > 1 else 'xml'

if not os.path.exists(DUMP_DIRECTORY):
    os.makedirs(DUMP_DIRECTORY)

config = ConfigParser()
config.read('config.ini')

if 'CREDENTIALS' not in config:
    sys.exit('Credentials not set.')

track_a_bike = TrackABike(
    config['CREDENTIALS']['username'],
    config['CREDENTIALS']['password'],
)

now = datetime.now()
directory_name = os.path.join(DUMP_DIRECTORY, now.strftime('%Y-%m-%d'))
filename = now.strftime('%Y-%m-%d_%H.%M')

if not os.path.exists(directory_name):
    os.makedirs(directory_name)

with open(os.path.join(directory_name, '{}.xml'.format(filename)), 'wb') as f:
    f.write(track_a_bike.raw_data)
