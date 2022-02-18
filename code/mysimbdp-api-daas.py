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

@app.route("/listings", methods = ['GET'])
def getListings():
    cluster = Cluster(['0.0.0.0'],port=9042)
    session = cluster.connect("airbnb", wait_for_all_pools=True)
    rows = session.execute('SELECT * FROM airbnblistings')
    return jsonify({"status": 200, "listings":list(rows)})

@app.route("/listings", methods = ['POST'])
def addListings():
    if not request.json:
        abort(400)
    cluster = Cluster(['0.0.0.0'],port=9042)
    session = cluster.connect("airbnb", wait_for_all_pools=True)
    newlisting = request.json
    query = """INSERT INTO airbnb.airbnblistings (id, host_id, host_name, neighbourhood, latitude, longitude, room_type, price, minimum_nights, number_of_reviews, calculated_host_listings_count, availability_365) VALUES (newlisting["id"], newlisting["host_id"], newlisting["host_name"], newlisting["neighbourhood"], newlisting["latitude"], newlisting["longitude"], newlisting["room_type"], newlisting["price"], newlisting["minimum_nights"], newlisting["number_of_reviews"], newlisting["calculated_host_listings_count"], newlisting["availability_365"]) """
    consistency_level = ConsistencyLevel.ALL
    session_query = SimpleStatement(query, consistency_level=consistency_level)
    session.execute(session_query)
    return jsonify({"status": 201})


if __name__ == "__main__":
    app.run(port=5005, debug=True)

