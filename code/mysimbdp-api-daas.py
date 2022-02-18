import os
import socket
from time import time
from flask import Flask
from flask import request
from flask import jsonify

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

app = Flask(__name__)

@app.route("/")
def hello():
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    html = html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())
    return html

@app.route("/listings")
def getListings():
    cluster = Cluster(['0.0.0.0'],port=9042)
    session = cluster.connect("airbnb", wait_for_all_pools=True)
    rows = session.execute('SELECT * FROM listings')
    return jsonify({"status": 200, "listings":list(rows)})



if __name__ == "__main__":
    app.run(port=5005, debug=True)
