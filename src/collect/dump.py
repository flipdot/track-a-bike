#!/usr/bin/env python3

import os
from datetime import datetime
from constants import XML_DIRECTORY
import logging

from track_a_bike import TrackABike


def run():
    logging.info('Dumping XML')
    track_a_bike = TrackABike()
    track_a_bike.refresh()

    now = datetime.now()
    directory_name = os.path.join(XML_DIRECTORY, now.strftime('%Y-%m-%d'))
    filename = now.strftime('%Y-%m-%d_%H.%M')

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    with open(os.path.join(directory_name, '{}.xml'.format(filename)), 'wb') as f:
        f.write(track_a_bike.raw_data)
