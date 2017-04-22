import os

DATA_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
CSV_DIRECTORY = os.path.join(DATA_DIRECTORY, 'csv')
XML_DIRECTORY = os.path.join(DATA_DIRECTORY, 'xml')

LOG_FORMAT = '%(asctime)-15s %(message)s'

CREDENTIALS = [
    ('t_andoid_cab', 'c91a49f43a'),
    ('t_andoid_kon', 'a2027c40b1'),
    ('t_andoid_srh', '83ba7e262a'),
    ('t_h2a_lidl_android', 'gYIkGT!*rL'),
]

REQUEST_TEMPLATES = {
    'LIST_BIKES': """
        <?xml version='1.0' encoding='ISO-8859-1'?>
        <v:Envelope xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:d="http://www.w3.org/2001/XMLSchema" xmlns:c="http://schemas.xmlsoap.org/soap/encoding/"
        xmlns:v="http://schemas.xmlsoap.org/soap/envelope/">
          <v:Header/>
          <v:Body>
            <n0:CABSERVER.listFreeBikes xmlns:n0="https://xml.dbcarsharing-buchung.de/hal2_cabserver/">
              <CommonParams>
                <UserData>
                  <User>{username}</User>
                  <Password>{password}</Password>
                </UserData>
                <LanguageUID>1</LanguageUID>
                <RequestTime>{request_time}</RequestTime>
                <Version/>
              </CommonParams>
              <SearchPosition>
                <Longitude>{long}</Longitude>
                <Latitude>{lat}</Latitude>
              </SearchPosition>
              <maxResults>{max_results}</maxResults>
              <searchRadius>{search_radius}</searchRadius>
            </n0:CABSERVER.listFreeBikes>
          </v:Body>
        </v:Envelope>
    """.strip()
}
