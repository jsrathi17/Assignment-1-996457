import datetime
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement


cluster = Cluster(['0.0.0.0'],port=9042)
session = cluster.connect()
#print("i am working")


session.execute("""
            CREATE KEYSPACE IF NOT EXISTS airbnb
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ )

session.set_keyspace("airbnb")

session.execute(""" DROP TABLE IF EXISTS airbnblistings """)

session.execute("""
            CREATE TABLE IF NOT EXISTS airbnblistings (
                id int,
                host_id int,
                host_name text,
                neighbourhood text,
                latitude float,
                longitude float, 
                room_type text,
                price int,
                minimum_nights int,
                number_of_reviews int,
                calculated_host_listings_count int, 
                availability_365 int,
                PRIMARY KEY (id, host_id)
            )
            """)

print("Created!")

         
                 