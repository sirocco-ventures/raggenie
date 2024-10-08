---
sidebar_position: 2
---

# Airtable Plugin

### Plugin name
The name of the plugin is used to differentiare between different connected plugins. These would be used for LLM calls during intent extraction.

### Plugin Description
A brief description of data in the plugin. This is used during LLM calls and may affect the quality of LLM response thus make sure that it is descriptive enough for good LLM output while being short enough to reduce LLM cost.

### Airtable token
The Airtable Token is an API key used to authenticate and access data from Airtable. Airtable integration allows the plugin to retrieve structured datasets and tables that will be used during query generation.

### Airtable workspace id
The Airtable Workspace ID specifies which workspace within your Airtable account the plugin will connect to. A workspace can contain multiple bases, and identifying the correct workspace is important for retrieving the right data.