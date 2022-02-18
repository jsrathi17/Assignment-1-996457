import os
import csv
from time import time
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster


def ingestListings(session):
    print("Starting batch load")
    insert_data = session.prepare('INSERT INTO airbnb.airbnblistings (id, host_id, host_name, neighbourhood, latitude, longitude, room_type, price, minimum_nights, number_of_reviews, calculated_host_listings_count, availability_365) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ')
    batch = BatchStatement(consistency_level=ConsistencyLevel.ALL)
    
    with open('../data/data.csv') as listings:
        reader = csv.reader(listings, delimiter = ',')
        next(listings)
        for row in reader:
            try:
                batch.add(insert_data, (int(row[0]), int(row[2]), row[3], row[4], float(row[5]), float(row[6]), row[7], int(row[8]), int(row[9]), int(row[10]), int(row[11]), int(row[12])))
                session.execute(batch)
                batch.clear()

            except Exception as e:
                print('The cassandra error: {}'.format(e))
        

if __name__ == "__main__":
    cluster = Cluster(['0.0.0.0'],port=9042)
    session = cluster.connect()
    start_time = time()
    ingestListings(session)
    stop_time = time()
    print("It took {} seconds".format(stop_time-start_time))
