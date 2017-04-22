from datetime import datetime

import requests
from lxml import etree
import re
import os

from constants import XML_DIRECTORY, REQUEST_TEMPLATES, CREDENTIALS

DEFAULT_HEADERS = {
    'User-Agent': 'flinkster.android/3.0',
    'Content-Type': 'text/xml',
    'Accept-Encoding': 'gzip',
    'SOAPAction': '',
    'Host': 'xml.dbcarsharing-buchung.de',
}

API_URL = 'https://xml.dbcarsharing-buchung.de/hal2_cabserver/hal2_cabserver_3.php'

class APIException(BaseException):
    pass

class TrackABike:
    def __init__(self, headers=DEFAULT_HEADERS):
        self.headers = headers
        self.raw_data = None

    def refresh(self, max_results=60, search_radius=8049, lat=51.318564, lng=9.500768, request_time=None):
        request_time = request_time or datetime.now()
        for username, password in CREDENTIALS:
            body = REQUEST_TEMPLATES['LIST_BIKES'].format(
                max_results=max_results,
                search_radius=search_radius,
                lat=lat,
                long=lng,
                username=username,
                password=password,
                request_time=request_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            )
            response = requests.post(API_URL, body, headers=self.headers)
            self.load_xml(response.content)
            error = self.get_error()
            if not error:
                break
            print(error)

    def get_error(self):
        fault = self.xml.find('.//SOAP-ENV:Fault', {'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/'})
        if fault is not None:
            text = fault.find('detail').find('Text')
            return text.text
        return None

    def load_xml(self, raw_data):
        self.raw_data = raw_data
        self.xml = etree.fromstring(raw_data)

    @property
    def stations(self):
        locations = self.xml.findall('.//Locations')
        stations = {}
        for location in locations:
            description = location.find('Description')
            match = re.search(r'^(\d+)\s+(.*)$', description.text)
            station_id = int(match.group(1))
            station_name = match.group(2)
            free_bikes = []
            for bike in location.findall('FreeBikes'):
                free_bikes.append({
                    'number': int(bike.find('Number').text),
                    'can_be_rented': bike.find('canBeRented').text == 'true',
                    'can_be_returned': bike.find('canBeReturned').text == 'true',
                    'version': int(bike.find('Version').text),
                    'marke_id': int(bike.find('MarkeID').text),
                    'marke_name': bike.find('MarkeName').text,
                    'is_pedelec': bike.find('isPedelec').text == 'true',
                })
            stations[station_id] = {
                'id': station_id,
                'name': station_name,
                'free_bikes': free_bikes,
                'lat': float(location.find('Position').find('Latitude').text),
                'lng': float(location.find('Position').find('Longitude').text),
                'is_outside': location.find('isOutside').text == 'true'
            }
        return stations


def read_xml_dumps():
    directories = os.listdir(XML_DIRECTORY)
    directories.sort()
    for directory in directories:
        directory_path = os.path.join(XML_DIRECTORY, directory)
        if not os.path.isdir(directory_path):
            continue
        files = os.listdir(directory_path)
        files.sort()
        for file in files:
            file_path = os.path.join(directory_path, file)
            timestamp = datetime.strptime(file, '%Y-%m-%d_%H.%M.xml')
            with open(file_path, 'rb') as f:
                yield (timestamp, f.read())


def count_xml_dumps():
    result = 0
    directories = os.listdir(XML_DIRECTORY)
    for directory in directories:
        directory_path = os.path.abspath(os.path.join(XML_DIRECTORY, directory))
        if not os.path.isdir(directory_path):
            continue
        files = os.listdir(directory_path)
        result += len(files)
    return result
