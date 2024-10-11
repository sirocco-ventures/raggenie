---
sidebar_position: 1
---

# Plugins

## Configuration
Plugin configuration is used to specify the metadata of different datasources such as datasource name, description and login details.
You need to specify informations such as:
* Plugin Name: Plugin name is used to differentiate between different connected plugins.
* Database Description: Description is should contain a breafe description about the use case of the database. The description is used during LLM calls, thus more detailed descriptions may help to improve the relevance of LLM output. The decription should be between 100 and 200 characters to make sure that it is detailed enough while also keeping the token count low.
* Database login details: These are specific for different plugins. Refer [Plugins](../Connectors) for more details
after entering all the details use `connection test` button perform a health check. If the health check passes use `save & continue` to save the plugin.

## Database schema
Raggenie automatically fetches your schema from the database on saving the configuration. Edit and add descriptions for different tables and their related columns. These decriptions are used during LLM calls and is nessesary for usable LLM responses. After adding descriptions `save & continue`.

## Documentation
You can add documentation of the plugins. This can be used a add important details regarding the plugins, which helps to fully understand how a plugin functions and how to use it effectively. This can be used to include important conditions and criterias. This data would be split into chunks and retreaved along with the schema during RAG exicution, thus can help to get improved responses from the LLMs. Then `save & continue` to fully save the plugin.