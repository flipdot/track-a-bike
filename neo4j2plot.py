#!/usr/bin/env python3
from neo4j.v1 import GraphDatabase, basic_auth
import matplotlib.pyplot as plt
from numpy.random import rand
from datetime import datetime

if __name__ == '__main__':
    fig, ax = plt.subplots()

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "Eiqu3soh"))
    session = driver.session()
    result = list(session.run("MATCH (a) RETURN a.name as name"))
    stations = list(map(lambda x: x['name'], result))
    result = list(session.run("MATCH (a)-[r]->(b) RETURN a.name as name, r.timestamp as timestamp;"))
    x = list(map(lambda x: datetime.fromtimestamp(x['timestamp']).hour, result))
    y = list(map(lambda x: stations.index(x['name']), result))
    # scale =
    ax.scatter(x, y, alpha=0.05, edgecolors='none')

    result = list(session.run("MATCH (a)-[r]->(b) RETURN b.name as name, r.timestamp as timestamp;"))
    x = list(map(lambda x: datetime.fromtimestamp(x['timestamp']).hour + 0.5, result))
    y = list(map(lambda x: stations.index(x['name']), result))
    # scale =
    ax.scatter(x, y, alpha=0.05, color='red', edgecolors='none')

    ax.legend()
    ax.grid(True)

    plt.show()
