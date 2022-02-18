# Part -1 Design

### 1. Explain your choice of types of data to be supported and technologies for mysimbdp-coredms. 

For my application, I am using the Airbnb dataset. It is a relational data where the data is organized in different tables which are related to one another. A RDBMS would have been a possible technology for this type of data. However, for the big data platforms implementation, I opt for NOSQL database. The data types are 

The coredms is implemented with Apache Cassandra database. Apache cassandra is a column oriented database provides various advantages over other databases. It stores massive amount of data and can handle thousands of writes per second. Cassandra doesnt have a master node, which allows it to achieve scalability by using peer-to-peer communication with gossip protocol. The gossip protocol allows nodes to communicate and pass metadata allowing adding of new nodes relatively easy. Since, the data is geographically distributed as there is data for airbnb in every location this will allow cheap, geographic expansion of the database.


### 2. Design and explain interactions between main components in your architecture of mysimbdp

![Schema](schemas.png)

mysimbdp-coredms is the cassandra cluster with 3 nodes. The data.csv file is the file user wishes to ingest, mysimpdb-ingest is the ingestion module to ingest the data to mysimbdp. The mysimbdp-api-daas module is an API, the provides basic functionality of read and write to the coredms. 

### 3. Explain a configuration of a cluster of nodes for mysimbdp-coredms so that you prevent a single-point-of-failure problem for mysimbdp-coredms for your tenants

For this assignment, I have configured a cluster named AirbnbBigDataPlatforms with 3 nodes. Since Cassandra is a peer-to-peer network with no master node, every node has same role in Cassandra. Since, cassandra replicates the data based on replication factor in the nodes, if one node goes down, the other nodes makes sure of the data availability preventing the single point of failure. 

### 4. You decide a pre-defined level of data replication for your tenants/customers. Explain how many nodes are needed in the deployment of mysimbdp-coredms for your choice so that this component can work property.
For this platform, I have kept the replication factor to 2. Which means that there is atleast 2 copies of each row and each copy is in a different node. Since, every node has same role in Cassandra. So, there is no single point of failure. There should be atleast 2 nodes to ensure data availability and consistency. And as a rule of thumb, the replication factor should not exceed the number of Cassandra nodes. Increasing replication factor can alleviate the fault tolerance and ensure high availability. But this increases the latency and decreases the performance. I have 3 cassandra nodes in my design as it allows quorum reads and writes in case one node fails.

### 5. Explain how would you scale mysimbdp to allow many tenants using mysimbdp-dataingest to push data into mysimbdp

One approach to scale for multi-tenant architecture is that each tenant may have different schemas. This hampers with performance and scalability as we store multiple keyspaces in memory. 
Another approach to scale would be to allow multiple tenants where each tenant get their own cluster. This increases the cost significantly, whereas the performance and scalability is traded off. 


# Part -2 Implementation

### Design, implement and explain one example of the data schema/structure for a tenant whose data will be stored into mysimbdp-coredms

A single table for all airbnb listings is implemented in the Cassandra keyspace. The table schema is defined as follows:

**Airbnblistings**
| Field Name | Data Type |
| --- | --- |
| id | int |
| host_id | int |
| host_name | text |
| neighbourhood | text |
| latitude | float |
| longitude | float |
| room_type | text |
| price | int |
| minimum_nights | int |
| number_of_reviews | int |
| calculated_host_listings_count | int |
| availability_365 | int |

The data from the file is first cleaned, some columns are dropped. Neighborhood group column only had NULL data present. Whereas there were multiple redundant columns for reviews like reviews_per_month, number_of_reviews_ltm, last_review which do not add much meaning to the data. Hence, they are removed from the dataset. Since the implementation is for big data it only makes sense to design with limited columns. 

### Given the data schema/structure of the tenant (Part 2, Point 1), design a strategy for data partitioning/sharding and explain your implementation for data partitioning/sharding together with your design for replication 

Cassandra partitions the data based on the partition key and in this case, the partition key and the primary key is id. The parition key is helpful in the case of reading the data and quering the database. As cassandra partitions the data in nodes based on the range of the hash value of the parition key. This makes efficient quering, since when reading data for a specific id, cassandra calculates the hash value and knows exactly which node will have the requested data. This prevents requerying the node in case when the queried node doesn't have the requested data and the request is forwarded to another node. 

### Assume that you are the tenant, write a mysimbdp-dataingest that takes data from your selected sources and stores the data into mysimbdp-coredms. Explain possible consistency options for writing data in your mysimdbp-dataingest

The data ingestion is implemented in mysimbdp-ingest.py that ingests the data from data.csv to the cassandra database. The script provides a batch insertion of all the entries to the specified table. 
BatchStatment in cassandra is generally used to execute multiple modification statements simultaneously. In this scenario, since it is only a data ingestion using a BatchStatement over a SimpleStatement isn't much different. However, using batch statement provides flexibility to further enhance the ingestion for multiple statements to execute parallely. 

There are various different consistency options in Cassandra. THe consistency level can be set to ALL, ONE, TWO, QUORUM. In cassandra, the consistency level is the minimum number of nodes that must acknowlegde a read or write operation before the operation can complete. Defining consistency majorly depends on whether the task is read intensive or write intensive, and how many nodes failure can be handled at a time. 

- ALL: In the all consistency level, both 2 replicas must succeed. In case of write consistency, if any of the node is down during write operation the write operation fails.
- QUORUM: In the QUORUM consistency level, the write consistency must be written to commit log and memtable on a quorum of replica nodes. For my implementation, for a replica of 2, 2 nodes need to respond foe the operation to succeed. 


### Given your deployment environment, show the performance (response time and failure) of the tests for 1,5, 10, .., n of concurrent mysimbdp-dataingest writing data into mysimbdp-coredms with different speeds/velocities together with the change of the number of nodes of mysimbdp-coredms. Indicate any performance differences due to the choice of consistency options





### Observing the performance and failure problems when you push a lot of data into mysimbdp-coredms, propose the change of your deployment to avoid such problems.