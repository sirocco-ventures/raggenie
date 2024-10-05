---
sidebar_position: 1
---

# Postgressql Plugin

You can connect to an instance of postgress using the postgressql plugin.

### Plugin name
The name of the plugin is used to differentiare between different connected plugins. These would be used for LLM calls during intent extraction.

### Plugin Description
A brief description of data in the plugin. This is used during LLM calls and may affect the quality of LLM response thus make sure that it is descriptive enough for good LLM output while being short enough to reduce LLM cost.

### Database sslmode
SSL Mode determines whether SSL encryption should be used when connecting to the PostgreSQL database. This feature ensures that data transmitted between your raggenie and the database is secure.

* sslmode=disable: No SSL is used when connecting to the database. This option can be used if the database server does not require encrypted connections or if encryption is not a priority. However, this may expose sensitive data to potential interception.

* sslmode=require: Enforces the use of SSL for database connections. This is recommended for environments where sensitive data is transmitted or where security is a concern.

### Database name
The Database Name is the name of the PostgreSQL database that the raggenie will connect to. Each database instance can host multiple databases, and specifying the correct database name is crucial to ensure that your raggenie accesses the intended data.

### Database host
The Database Host refers to the URL or IP address where the PostgreSQL server is running. This could be a local server, a remote machine, or a cloud-hosted instance. Ensure that the specified host is reachable from your application's environment.

### Database port
The Database Port is the TCP/IP port on which the PostgreSQL server is listening. The default port for PostgreSQL is `5432`, but this can be configured to a different port based on your setup.

### Password
The password of the user trying to access the postgressql database.

### User name
The Username is the identity that the application uses to connect to the PostgreSQL database. Each user in PostgreSQL can have different permissions, and it is important to use a user with the necessary roles for the application's functionality.