---
sidebar_position: 1
---

# To run raggenie backend Server

### Clone the project
The first step is to clone the RAGGenie project from its GitHub repository. The `git clone` command copies the repository from GitHub to your local system.
```bash
git clone https://github.com/sirocco-ventures/raggenie
```
Move into the project using
```bash
cd raggenie
```

### Install Requirements
Once the project is cloned, the next step is to install the necessary Python packages that the raggenie backend server depends on. Instead of using `pip`, we will use `Poetry`, a tool for dependency management and packaging in Python projects.
```bash
poetry install
```
You can find more info for setting up poetry [here](../Prerequesites.md)

### To run server
After installing the dependencies, you can run the raggenie backend server. The server uses a configuration file (config.yaml) to set up the environment and specify parameters for LLM usage. The command below will start the server and ensure it operates based on the provided configuration.
```bash
python main.py --config ./config/config.yaml llm
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
