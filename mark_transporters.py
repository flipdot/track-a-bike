#!/usr/bin/env python3
from datetime import datetime, timedelta
from neo4j.v1 import GraphDatabase, basic_auth

QUERY_TEMPLATE = """
MATCH (a:Station)-[r:BIKE_MOVED]->(b:Station)
WHERE {start} <= r.timestamp_start < {end}
WITH count(*) AS cnt, a, collect(r) AS r
WHERE cnt >= 6
UNWIND r AS r_
MATCH (a)-[r_]->(b)
WITH count(*) AS cnt, b, collect(a) AS a, collect(r_) AS r
UNWIND r AS r_
WITH a, b, r_, cnt
WHERE cnt >= 3 OR r_.duration > 60 * 60 * 24
SET r_.transporter = true
"""

START_DATE = datetime.strptime('25.03.2017 00:00', '%d.%m.%Y %H:%M')
END_DATE = datetime.strptime('09.04.2017 00:00', '%d.%m.%Y %H:%M')
STEP = timedelta(minutes=5)
WINDOW = timedelta(minutes=15)

if __name__ == '__main__':
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'Eiqu3soh'))
    session = driver.session()

    date = START_DATE
    while date < END_DATE:
        print(date)
        start = date
        end = date + WINDOW
        session.run(QUERY_TEMPLATE, {'start': start.timestamp(), 'end': end.timestamp()})
        date += STEP