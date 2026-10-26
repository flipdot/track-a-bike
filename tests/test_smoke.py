"""Smoke tests: verify the pipeline modules import against the current
dependencies and that the core parsing/modeling logic still works."""

import os
import sys
import unittest

# The modules use flat imports (e.g. `from constants import ...`), mirroring
# the Docker layout where the contents of src/ form the application root.
SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC not in sys.path:
    sys.path.insert(0, SRC)

SAMPLE_XML = b"""<?xml version="1.0" encoding="ISO-8859-1"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <n1:ListBikesResponse xmlns:n1="http://tempuri.org/">
      <Locations>
        <Description>1 Marktplatz</Description>
        <FreeBikes>
          <Number>1001</Number>
          <canBeRented>true</canBeRented>
          <canBeReturned>false</canBeReturned>
          <Version>2</Version>
          <MarkeID>5</MarkeID>
          <MarkeName>CityRad</MarkeName>
          <isPedelec>false</isPedelec>
        </FreeBikes>
        <Position>
          <Latitude>51.318564</Latitude>
          <Longitude>9.500768</Longitude>
        </Position>
        <isOutside>false</isOutside>
      </Locations>
      <Locations>
        <Description>2 Bahnhof</Description>
        <Position>
          <Latitude>51.310000</Latitude>
          <Longitude>9.490000</Longitude>
        </Position>
        <isOutside>true</isOutside>
      </Locations>
    </n1:ListBikesResponse>
  </soap:Body>
</soap:Envelope>
"""


class ImportTest(unittest.TestCase):
    """Every pipeline module must import against the pinned dependencies."""

    def test_pipeline_modules_import(self):
        import collect.compress  # noqa: F401
        import collect.dump  # noqa: F401
        import constants  # noqa: F401
        import preprocess.xml2csv  # noqa: F401
        import track_a_bike  # noqa: F401
        import utils  # noqa: F401
        import visualize.free_bikes_timeline  # noqa: F401
        import visualize.neo4j2dot  # noqa: F401


class XmlParsingTest(unittest.TestCase):
    def setUp(self):
        from track_a_bike import TrackABike

        self.track = TrackABike()
        self.track.load_xml(SAMPLE_XML)

    def test_no_soap_fault(self):
        self.assertIsNone(self.track.get_error())

    def test_stations_parsed(self):
        stations = self.track.stations
        self.assertEqual(sorted(stations), [1, 2])

        marktplatz = stations[1]
        self.assertEqual(marktplatz["name"], "Marktplatz")
        self.assertAlmostEqual(marktplatz["lat"], 51.318564)
        self.assertAlmostEqual(marktplatz["lng"], 9.500768)
        self.assertFalse(marktplatz["is_outside"])
        self.assertEqual(len(marktplatz["free_bikes"]), 1)

        bike = marktplatz["free_bikes"][0]
        self.assertEqual(bike["number"], 1001)
        self.assertTrue(bike["can_be_rented"])
        self.assertFalse(bike["can_be_returned"])
        self.assertFalse(bike["is_pedelec"])
        self.assertEqual(bike["marke_name"], "CityRad")

        bahnhof = stations[2]
        self.assertEqual(bahnhof["name"], "Bahnhof")
        self.assertTrue(bahnhof["is_outside"])
        self.assertEqual(bahnhof["free_bikes"], [])


class SqlModelTest(unittest.TestCase):
    def test_models_create_tables_and_insert(self):
        from datetime import datetime

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        from models import Base, Bike, Station, TemporalLocation

        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()

        station = Station(id=1, name="Marktplatz", lat=51.318, lng=9.500, is_outside=False)
        bike = Bike(
            id=2,
            can_be_rented=True,
            can_be_returned=False,
            version=2,
            marke_id=5,
            marke_name="CityRad",
            is_pedelec=False,
        )
        location = TemporalLocation(
            time_from=datetime(2026, 10, 27, 8, 0, 0),
            time_to=datetime(2026, 10, 27, 9, 0, 0),
        )
        location.bike = bike
        location.station = station
        session.add(location)
        session.commit()

        loaded = session.query(TemporalLocation).one()
        self.assertEqual(loaded.bike.id, 2)
        self.assertEqual(loaded.station.name, "Marktplatz")


if __name__ == "__main__":
    unittest.main()
