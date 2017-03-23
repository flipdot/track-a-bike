#!/usr/bin/env python3

import os
import sys
from configparser import ConfigParser
from datetime import datetime

from TrackABike import TrackABike

DUMP_DIRECTORY = sys.argv[1] if len(sys.argv) > 1 else 'dumps'

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

filename = datetime.now().strftime('%Y-%m-%d_%H.%M')

with open(os.path.join(DUMP_DIRECTORY, '{}.xml'.format(filename)), 'wb') as f:
    f.write(track_a_bike.raw_data)
