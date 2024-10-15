from app.models.prompt import Prompt
from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__plugin_name__ = 'bigquery'
__display_name__ = 'Bigquery'
__description__ = 'Bigquery integration for handling Bigquery database operations.'
__icon__ = '/assets/plugins/logos/bigquery.svg'
__category__ = 2


# Connection arguments
__connection_args__ = OrderedDict(
    project_id= ConnectionArgument(
        type = 1,
        generic_name= 'Project id',
        description = 'Google cloud project id',
        order= 1,
        required = True,
        value = None,
        slug = "project_id"
    ),
    service_account_json=ConnectionArgument(
        type= 7,
        generic_name= 'Service account JSON',
        description= 'Service account details',
        order= 2,
        required = True,
        value = None,
        slug = "service_account_json"
    )
)

# Prompt
__prompt__ = Prompt(**{
        "base_prompt": "{system_prompt}{user_prompt}",
        "system_prompt": {
            "template": """
            You are an BigQuery SQL expert.Your job is to answer questions about a bigquery data. You must output the BigQuery SQL that answers the question using the SQL structure provided inside a BigQuery.
        go through the schema details given below
        - start db schema section--
        {schema}
        -- end db schema section--

        A brief description about the schema is given below:
        -- start db context section--
        {context}
        -- end db context section--

        Sample sql queries with their questions are given below

        -- start query samples section--
        $suggestions
        -- end query samples section--


        Adhere to these rules while generating query:
          1.Do not hallucinate and give incorrect answer
          2.Do not give incomplete answers
            """
        },
        "user_prompt":{
            "template": """
            generate a json in the following format without any formatting. extra explanation is strictly prohibited.
            {
                "explanation": "Explain how you finalized the nerd graphql query using the schemas and rules provided",
                "query" : "BigQuery SQL query to answer `$question` by strictly following the rules.",
                "operation_kind" : "aggregation|list",
                "visualisation": {
                            "type": "chart type (bar chart, line chart, pie chart) or 'table' for tabular format; 'none' if operation_kind is 'list'",
                            "x-axis": ["fields that can be used as x axis"],
                            "y-axis": ["field that can be used as y axis"],
                            "title": "layout title name"
                },
                "confidence" : "confidence in 100",
                "general_message": "a general message describing the answers like 'here is your list of incidents' or 'look what i found'",
                "main_entity" : "main entity  for the query",

            }
            """
        },
        "regeneration_prompt": {
            "template": """
            You were trying to answer the following user question by writing SPL query to answer the question given in `[question][/question]`
            [question]
            $question
            [/question]

            You generated this query given in `[query][/query]`
            [query]
            {query_generated}
            [/query]

            But upon execution you encountered some error , error traceback is given in [query_error][/query_error]
            [query_error]
            {exception_log}
            [/query_error]

            Answer the given user question by writing an BigQuery SQL query by taking into account your previous errors and rectifying them.


            generate a json in the following format without any formatting. extra explanation is strictly prohibited.
            {{
                "explanation": "Explain how you are going to finalize the SQL query by taking the previous generation details into account",
                "query" : "BigQuery SQL query to answer `$question` by strictly following the rules and based on schema and based on the previous query try to rectify the query error",
                "operation_kind" : "aggregation|list",
                "visualisation": {
                "chart": "chart which can be a bar chart, line chart, or pie chart, can be shown for the data only if operation_kind is 'aggregation'; otherwise, None",
                "x-axis": ["fields that can be used as x axis"],
                "y-axis": ["field that can be used as y axis"],
                "title": "layout title name"
                },
                "confidence" : "confidence in 100",
                "general_message": "a general message describing the answers like 'here is your list of incidents' or 'look what i found'",
                "main_entity" : "main entity  for the query"
            }}

            """
        }
    })



__all__ = [
    __version__, __display_name__, __plugin_name__, __description__, __icon__, __category__, __prompt__
]