from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, \
                       String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


DB_PREFIX = 'tab_'
Base = declarative_base()


class TemporalLocation(Base):
    __tablename__ = '{}temporal_locations'.format(DB_PREFIX)
    bike_id = Column(Integer, ForeignKey('{}bikes.id'.format(DB_PREFIX)),
                     primary_key=True)
    station_id = Column(Integer, ForeignKey('{}stations.id'.format(DB_PREFIX)),
                        primary_key=True)
    time_from = Column(DateTime, primary_key=True)
    time_to = Column(DateTime, primary_key=True)

    bike = relationship("Bike", back_populates="temporal_locations")
    station = relationship("Station", back_populates="temporal_locations")

    def __repr__(self):
        return "<TemporalLocation(bike_id='{}', "\
            "station_id='{}', "\
            "time_from='{}', "\
            "time_to='{}')>".format(self.bike_id,
                                    self.station_id,
                                    self.time_from,
                                    self.time_to)


class Bike(Base):
    __tablename__ = '{}bikes'.format(DB_PREFIX)

    id = Column(Integer, primary_key=True)
    can_be_rented = Column(Boolean)
    can_be_returned = Column(Boolean)
    version = Column(Integer)
    marke_id = Column(Integer)
    marke_name = Column(String(256))
    is_pedelec = Column(Boolean)

    temporal_locations = relationship("TemporalLocation",
                                      back_populates="bike")

    def __repr__(self):
        return "<Bike(id='{}', "\
            "can_be_rented='{}', "\
            "can_be_returned='{}', "\
            "version='{}', "\
            "marke_id='{}', "\
            "marke_name='{}', "\
            "is_pedelec='{}')>".format(self.id,
                                       self.can_be_rented,
                                       self.can_be_returned,
                                       self.version,
                                       self.marke_id,
                                       self.marke_name,
                                       self.is_pedelec)


class Station(Base):
    __tablename__ = '{}stations'.format(DB_PREFIX)

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    lat = Column(Float(Precision=64))
    lng = Column(Float(Precision=64))
    is_outside = Column(Boolean())

    temporal_locations = relationship("TemporalLocation",
                                      back_populates="station")

    def __repr__(self):
        return "<Station(id='{}', "\
            "name='{}', "\
            "lat='{}', "\
            "lng='{}', "\
            "is_outside='{}')>".format(self.id,
                                       self.name,
                                       self.lat,
                                       self.lng,
                                       self.is_outside)
