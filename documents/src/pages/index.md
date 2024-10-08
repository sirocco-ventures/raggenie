<p align="center">
  <a href="https://www.raggenie.com/">
    <img src="https://cdn.prod.website-files.com/664e485574efd184749b7301/6658314c55210573e334ac1b_Group%2042.png" width="150" alt="RAGGENIE Logo"></img>
  </a>
</p>

<h1 align="center">
RAGGENIE
</h1>

## Quick start

### Clone the project
```bash
git clone https://github.com/sirocco-ventures/raggenie
```

### Raggenie Backend

* Installing dependencies

  * **Using `requirements.txt`**

    To install the required dependencies with `pip`, run:
    
    ```bash
    pip install -r requirements.txt
    ```

  * **Using Poetry**

    First, install Poetry:
    
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    
    Then, to install the dependencies, run:
    
    ```bash
    poetry install
    ```


* Running RAGGENIE backend

  To run **RAGGENIE** in API mode, specify the config file to use by running the following command:

  ```bash
  python main.py --config ./config.yaml llm
  ```

  Below is a sample configuration for the vector database setup in `config.yaml`:

  ```yaml
  vector_db:
    name: "chroma"
    params:
      path: "./vector_db"
      embeddings:
        provider: "chroma_default"
  ```
  This configuration ensures that the RAGGENIE system connects to the `chroma` vector database and uses the default embeddings provided by Chroma.

### Raggenie Frontend

* **Move into the ui folder.**
  ```
  cd ./ui
  ```

* Install dependencies
  ```bash
  npm install
  ```

* Running RAGGENIE Frontend

  * To run **RAGGENIE** frontend, create a .env file and add the URL to backend as env variables
    ```env
    VITE_BACKEND_URL=${BACKEND_URL}
    ```

  * To start the server, run
    ```bash
    npm run dev
    ```


<!-- ### Using RAGGENIE backend API
To run just the backend API you can run -->
### Using Docker
Both docker file and the docker compose files are present in the root folder. To run the model you can run
```bash
docker compose up
```

## Connectors/pluggins
Different components in your LLM app can be inserted using plugins.
### Data Sources
Currently these are the datasource plugins that are available in raggenie.
#### Structred Datasources
* [Postgressql](./docs/Connectors/Postgressql)
* [Airtable](./docs/Connectors/Airtable)
* [Bigquery](./docs/Connectors/Bigquery)
#### Unstrunctured Datasources
* [PDFs](./docs/Connectors/PDFs)
* [Websites](./docs/Connectors/Websites)


## LLM Inferences
We currently support these LLM Inference endpoints.
* [OpenAI](https://openai.com/index/openai-api/)
* [Together.ai](https://www.together.ai/)