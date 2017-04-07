#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from models import Base, TemporalLocation, Bike, Station
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# from TrackABike import TrackABike, read_xml_dumps
#
# track_a_bike = TrackABike()
# for data in read_xml_dumps():
#     track_a_bike.load_xml(data)

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def create_db():
    Base.metadata.create_all(engine)


def sample_data():
    station = Station(id=3, name='lelkek', lat=32.551, lng=64.112,
                      is_outside=False)
    bike = Bike(id=4, can_be_rented=False, can_be_returned=False, version=2,
                marke_id=23, marke_name="Kekrad", is_pedelec=False)

    location = TemporalLocation(time_from=datetime.now(),
                                time_to=datetime.now())
    location.bike = bike
    location.station = station

    return station, bike, location


station, bike, location = sample_data()
session.add(location)
# session.commit()

# TODO Fix bike_id='None' and station_id='None'
print(location)
