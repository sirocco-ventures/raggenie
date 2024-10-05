---
sidebar_position: 3
---

# Using Docker
The raggenie project includes both a Dockerfile and a Docker Compose file, located in the root folder of the repository. These files allow you to build and orchestrate the application using containers.

If you have Docker installed on your machine, you can use the docker-compose.yml file to start the RAGGenie application and its associated services. This command will pull the necessary images, build the application, and start the containers.
```bash
docker compose up
```