# Part -1 Design

## 1. Explain your choice of types of data to be supported and technologies for mysimbdp-coredms. 

For my application, I am using the Airbnb dataset. It is a relational data where the data is organized in different tables which are related to one another. A RDBMS would have been a possible technology for this type of data. However, for the big data platforms implementation, I opt for NOSQL database. The data types are 

The coredms is implemented with Apache Cassandra database. Apache cassandra is a column oriented database provides various advantages over other databases. It stores massive amount of data and can handle thousands of writes per second. Cassandra doesnt have a master node, which allows it to achieve scalability by using peer-to-peer communication with gossip protocol. The gossip protocol allows nodes to communicate and pass metadata allowing adding of new nodes relatively easy. Since, the data is geographically distributed as there is data for airbnb in every location this will allow cheap, geographic expansion of the database.


## 2. Design and explain interactions between main components in your architecture of mysimbdp



## 3. Explain a configuration of a cluster of nodes for mysimbdp-coredms so that you prevent a single-point-of-failure problem for mysimbdp-coredms for your tenants

For this assignment, I have configured a cluster named AirbnbBigDataPlatforms with 3 nodes. Since Cassandra is a peer-to-peer network with no master node, every node has same role in Cassandra. Since, cassandra replicates the data based on replication factor in the nodes, if one node goes down, the other nodes makes sure of the data availability preventing the single point of failure. 

## 4. You decide a pre-defined level of data replication for your tenants/customers. Explain how many nodes are needed in the deployment of mysimbdp-coredms for your choice so that this component can work property.
For this platform, I have kept the replication factor to 2. Which means that there is atleast 2 copies of each row and each copy is in a different node. Since, every node has same role in Cassandra. So, there is no single point of failure. There should be atleast 2 nodes to ensure data availability and consistency. And as a rule of thumb, the replication factor should not exceed the number of Cassandra nodes. Increasing replication factor can alleviate the fault tolerance and ensure high availability. But this increases the latency and decreases the performance. I have 3 cassandra nodes in my design as it allows quorum reads and writes in case one node fails.

## 5. Explain how would you scale mysimbdp to allow many tenants using mysimbdp-dataingest to push data into mysimbdp

One approach to scale for multi-tenant architecture is that each tenant may have different schemas. This hampers with performance and scalability as we store multiple keyspaces in memory. 
Another approach to scale would be to allow multiple tenants where each tenant get their own cluster. This increases the cost significantly, whereas the performance and scalability is traded off. 


# Part -2 Implementation