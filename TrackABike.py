import request_templates
import requests
from lxml import etree
import re

DEFAULT_HEADERS = {
    'User-Agent': 'flinkster.android/3.0',
    'Content-Type': 'text/xml',
    'Accept-Encoding': 'gzip',
    'SOAPAction': '',
    'Host': 'xml.dbcarsharing-buchung.de',
}

API_URL = 'https://xml.dbcarsharing-buchung.de/hal2_cabserver/hal2_cabserver_3.php'


class TrackABike:
    def __init__(self, username, password, headers=DEFAULT_HEADERS):
        if not (username and password):
            raise ValueError('Username and password are required')
        self.username = username
        self.password = password
        self.headers = headers
        self.refresh()

    def refresh(self, max_results=60, search_radius=8049, lat=51.318564, long=9.500768):
        body = request_templates.LIST_BIKES.format(
            max_results=max_results,
            search_radius=search_radius,
            lat=lat,
            long=long,
            username=self.username,
            password=self.password,
        )
        response = requests.post(API_URL, body, headers=self.headers)
        self.raw_data = response.content
        self.xml = etree.fromstring(response.content)

    @property
    def stations(self):
        locations = self.xml.findall('.//Locations')
        stations = []
        for location in locations:
            description = location.find('Description')
            match = re.search(r'^(\d+)\s+(.*)$', description.text)
            station_id = match.group(1)
            station_name = match.group(2)
            free_bikes = []
            for bike in location.findall('FreeBikes'):
                free_bikes.append({
                    'number': int(bike.find('Number').text),
                    'can_be_rented': bool(bike.find('canBeRented').text),
                    'can_be_returned': bool(bike.find('canBeReturned').text),
                    'version': int(bike.find('Version').text),
                    'marke_id': int(bike.find('MarkeID').text),
                    'marke_name': bike.find('MarkeName').text,
                    'is_pedelec': bike.find('isPedelec').text,
                })
            print(station_id)
            print(station_name)
            stations.append({
                'id': station_id,
                'name': station_name,
                'free_bikes': free_bikes
            })
        return stations