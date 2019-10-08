from neo4j import GraphDatabase
from kafka import KafkaConsumer
import json
from collections import OrderedDict
import os.path


uri = "bolt://34.212.248.28:5003"
driver = GraphDatabase.driver(uri, auth=("neo4j", "hipaas2"))
session = driver.session()


#Execute a given query
def executeQuery(query):
    tx = session.begin_transaction()
    result = tx.run(query)
    tx.commit()
    return result


query = 'MATCH (n:`HL7`) RETURN n'
result =  executeQuery(query)
for line in result:
    print line[0]['name']
    print line[0]['id']
    print line[0]['name']
