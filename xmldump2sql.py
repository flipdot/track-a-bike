#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pprint import pprint

from TrackABike import TrackABike, read_xml_dumps

track_a_bike = TrackABike()
for data in read_xml_dumps():
    track_a_bike.load_xml(data)
    pprint(track_a_bike.stations)