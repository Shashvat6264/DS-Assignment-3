# DS Assignment 3
## Problem Statement
### Part I
System in ToyATM folder.  
Implement a toy ATM network that simulates the behaviour of real-world ATMs. Each ATM can be simulated by a process that runs on a separate terminal window, accepts user commands and displays the appropriate output. Use an existing RAFT library for consistency of data across these processes.

### Part II
System in Fault-Tolerant_Broker folder
In this part of the assignment, you will extend your broker to incorporate a NAT-like design using the RAFT protocol. This design aims to allow for fault-tolerant and consistent replication of partitions across multiple brokers without the need for additional physical hosts. Each partition should have multiple replicas across different brokers. Data consistency must exist between replicas of a partition using RAFT protocol.

## Languages and Libraries
The whole software is written in **Python** programming language. **FastAPI** framework is used to implement HTTP APIs of the logging distributed queue. **SQLAlchemy** is used for ORM of database to support persistence in the system. Currently the brokers use seperate **Sqlite3** databases and managers use a shared **PostgreSQL** database. The [raft-lite](https://github.com/nikwl/raft-lite) library is used to implement the RAFT consensus algorithm. 


