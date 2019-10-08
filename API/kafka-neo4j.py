from kafka import KafkaConsumer
import json
from collections import OrderedDict
from neo4j import GraphDatabase

'''
KAFKA_VERSION = (0, 10)
consumer = KafkaConsumer('messages',
    bootstrap_servers='52.34.245.75:5002',
    auto_offset_reset='earliest', enable_auto_commit=True, group_id='group',
    consumer_timeout_ms=1000, api_version=KAFKA_VERSION)

'''


uri = "bolt://34.212.248.28:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "hipaas2"))
session = driver.session()


#Execute a given query
def executeQuery(query):
    tx = session.begin_transaction()
    result = tx.run(query)
    tx.commit()
    return result

while True:
    consumer = KafkaConsumer('messages',
        bootstrap_servers='52.34.245.75:9094',
        group_id='group',
        auto_offset_reset='earliest',
        consumer_timeout_ms=10000,
        value_deserializer = lambda v: json.loads(v, object_pairs_hook=OrderedDict))

    for msg in consumer:
        print(msg.value)
        endpoint = []
        company = []
        for k,v in msg.value.iteritems():
    	    endpoint.append(k)
    	    company.append(v)
        query = 'MERGE(n:`%s` {name:"%s"}) MERGE(m:`%s` {name:"%s"}) MERGE(n)-[:HL7]->(m)' % (endpoint[0], company[0], endpoint[1], company[1])
        print query
        executeQuery(query)
