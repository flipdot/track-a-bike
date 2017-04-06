#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pprint import pprint

from TrackABike import TrackABike
import os

DUMP_DIRECTORY = os.path.abspath('dumps')

track_a_bike = TrackABike()

directories = os.listdir(DUMP_DIRECTORY)
directories.sort()
for directory in directories:
    directory_path = os.path.abspath(os.path.join(DUMP_DIRECTORY, directory))
    if not os.path.isdir(directory_path):
        continue
    files = os.listdir(directory_path)
    files.sort()
    for file in files:
        file_path = os.path.join(directory_path, file)
        print(file_path)
        with open(file_path, 'rb') as f:
            track_a_bike.load_xml(f.read())
        # pprint(track_a_bike.stations)