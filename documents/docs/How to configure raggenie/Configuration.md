---
sidebar_position: 2
---

# Configuration

## Configuration details
You should provide a bot name, a short discription about the bot and a long discription about the bots usecase.
Note:- Long dicription will be used when making LLM calls and thus will affect the performance of the chatbot. It is recomended to give detailed description that can help the LLM to understand its usecases.

## Inference endpoint
To add an LLM endpoint choose your LLM inference provider and specify a unique name to reference the particular model.
![LLM inference plugin image](../../static/img/inferance_end_point.png?raw=true)

Specify the model name, inference provider endpoint, and the API key.

## Capabilities
Capabilities can be defined to make your chatbot do custom actions such as fill a form or book a meeting. Currently actions can be defined to interact with your datasources or to webhooks.
### Add Capability Name and Description
Capability Name and discription is used by the intent extraction module to determine which capability is to be exicuted. So it is important to give a detailed discription of the capability.
![Capability initialisation image](../../static/img/Capbilities.png?raw=true)
### Add Capability Parameters
You can specify the parameters nesessary to exicute an action. Raggenie uses LLM calls to see if all the specified parameters could be retreaved from the user input. In case if LLM could not detect all the nesessary parameters raggenie would ask the user to specify the missing parameters
![Capability parameters image](../../static/img/Create_parameter.png?raw=true)
these parameters can be used to trigger an action.