LIST_BIKES = """<?xml version='1.0' encoding='ISO-8859-1'?>
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
        <RequestTime>2017-03-23T18:31:20.516Z</RequestTime>
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
</v:Envelope>"""