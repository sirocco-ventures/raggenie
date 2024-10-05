---
sidebar_position: 3
---

# Bigquery Plugin

### Plugin name
The name of the plugin is used to differentiare between different connected plugins. These would be used for LLM calls during intent extraction.

### Plugin Description
A brief description of data in the plugin. This is used during LLM calls and may affect the quality of LLM response thus make sure that it is descriptive enough for good LLM output while being short enough to reduce LLM cost.

### Service account JSON
The Service Account JSON contains authentication credentials that allow your RAG application to access Google BigQuery securely. This file is essential for granting the necessary permissions to query data stored in BigQuery.

### Project id
The Project ID refers to the specific Google Cloud project where your BigQuery datasets reside. Each BigQuery query is associated with a project, and the project ID is used to identify which datasets the plugin should access.