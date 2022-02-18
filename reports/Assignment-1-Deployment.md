# This is a deployment/installation guide

To run the code and system, you first need to be present in the code subdirectory as all of the codes related to this assignment are present in that subdirectory.

# Configuring Cassandra cluster in a container

- cluster name: AirbnbBigDataPlatforms
- Nodes: node1_1, node2_2, node3_3

The configurations of the cassandra cluster is in the docker-compose.yml file. First start the containers by running:

	docker-compose up

To see the running containers, you can do:

	docker ps

It is better to note down the ip address of your containers for further process using following command:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' node1_1


# mysimpdb-coredms

Mysimpdb coredms is implemented in the file mysimpdb-coredms.py. This is the key component of our system to manage and store data. To run the mysimpdb-coredms run the following command:

	python3 mysimpdb.py

This will create a keyspace airbnb and a table airbnblistings with columns id, host_id, host_name, neighbourhood, latitude, longitude, room_type, price, minimum_nights, number_of_reviews, calculated_host_listings_count, availability_365.

# mysimpdb-ingest

While ingesting data from the csv file to mysimbdp-coredms, I do not ingest all of the data. I clean the data to drop some columns and ingest the others. The reason is that these columns do not add any significant value to the dataset. While analyzing data, it is found that neighborhood_group does not have any data and only has NULL. And, there are multiple redundant data related to reviews which do not provide any significant contribution to the schema. So, I decide to drop the data. Before ingesting, run the following script. 

	python3 mysimbdp-data-cleaning.py

Now to ingest the data to mysimbdp. Run the following command. 

	python3 mysimbdp-ingest.py

