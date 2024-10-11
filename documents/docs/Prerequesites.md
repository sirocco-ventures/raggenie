---
sidebar_position: 1
---

# Prerequesites

## Backend

### Python
Raggenie uses python to run its backend server. Currently supported versions are 3.10, 3.11 and 3.12. To install python, [download](https://www.python.org/downloads/) the version compatible.

#### Poetry
Poetry is required to install and run the dependancies for raggenie backend, you can install poetry,

* using pip
  ```bash
  pip install poetry
  ```

* using curl
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```
For more detailed explanation you can follow official [documentation](https://python-poetry.org/docs/#installation).

To install rest of dependancies run
```bash
poetry install
```

## Frontend

### Node.js
The ui requires Node.js for frontend, Currently only versions 20 and above is supported. To install Node [download](https://nodejs.org/en/download/package-manager) the version compatible.

### Npm
You needs to use npm to install the requirements for ui, it is usually installed with Node.js
To install ui dependancies
* go to ui folder
  ```bash
  cd ui
  ```

* install dependancies
  ```bash
  npm install
  ```

## Docker

Raggenie provides docker compose file and docker files which can be used to run raggenie on containers. If you prefer to run raggenie on docker you can find how to install docker [here](https://docs.docker.com/get-started/). And to run raggenie using docker you can find instructions [here](./How%20to%20run%20raggenie/Using%20Docker.md)