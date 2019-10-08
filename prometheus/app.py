from flask import Response, Flask, request 
import json
import os
from prometheus_client.core import CollectorRegistry
from prometheus_client.core import Summary, Counter, Histogram, Gauge
import prometheus_client
import time


app = Flask(__name__)

_INF = float("inf")
graphs = {}
graphs['c'] = Counter('python_request_operation_total', 'Total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds', buckets=(1,2,5,6,10, _INF))

@app.route('/')
def hello():
   start = time.time()
   graphs['c'].inc()
   time.sleep(0.600)
   end = time.time()
   graphs['h'].observe(end - start)
   return "hello"

@app.route('/metrics')
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
