from app.models.prompt import Prompt
from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__plugin_name__ = 'CSV'
__display_name__ = 'CSV loader'
__description__ = 'CSV loader for interacting with CSV data'
__icon__ = '/assets/plugins/logos/csv.svg'
__category__ = 4

# Connection arguments
__connection_args__ = OrderedDict(
    document_files = ConnectionArgument(
        type = 8,
        generic_name= 'csv file',
        description = 'Supports only .csv file.',
        order = 1,
        required = True,
        value = None,
        slug = "document_files"
    )
)

__prompt__ = Prompt(**{
        "base_prompt": "{system_prompt}{user_prompt}",
        "system_prompt": {
            "template": """
            You are an Sqlite expert. Your job is to answer questions about a Sqlite database using only the provided schema details and rules.

            go through the schema details given below
            -- start db schema section--
            {schema}
            -- end db schema section--

            A brief description about the schema is given below

            -- start db context section--
            {context}
            -- end db context section--

            Sample sql queries with their questions are given below

            -- start query samples section--
            $suggestions
            -- end query samples section--

            Adhere to the given rules without failure

            -- start rules section --
            - Use Table Aliases always to prevent ambiguity . For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
            - use LIKE operator with LOWER function for string comparison or equality
            - Always use alias/table name for fields in WHERE condition
            - Do not use non existing tables or fields
            - id columns are mandatory for all operations
            - Do not use JSON_BUILD_OBJECT operation
            - Do not use unwanted joins
            - Do not return incomplete queries
            - Adher to sqlite query syntax
            -- end rules section --
            """
        },
        "user_prompt":{
            "template": """
            Follow these steps to generate query to solve the question `$question`

            1. Deliberately go through schema, context, rules deliberately
            2. Understand the question and check whether it's doable with the given context
            3. Do only the task asked, Don't hallucinate and overdo the task
            4. Strictly return all the fields in the schema during listing operations
            5. Strictly return at least 1 text fields and an id field during aggregation/group by operations
            6. Generate a query to solve the problem using the schema, context, and strictly follow the rules
            7. output in the given json format, extra explanation is strictly prohibited

            {
                "explanation": "Explain how you finalized the sql query using the schemas and rules provided",
                "query" : "sqlite query",
                "operation_kind" : "aggregation|list",
                "schema": "used schema details separated by comma",
                "confidence" : "confidence in 100",
                "visualisation": {
                    "type": "chart type (bar chart, line chart, pie chart) or 'table' for tabular format; 'none' if operation_kind is 'list'",
                    "x-axis": ["fields that can be used as x axis"],
                    "y-axis": ["fields that can be used as y axis"],
                    "title": "layout title name"
                },
                "general_message": "a general message describing the answers like 'here is your list of incidents' or 'look what i found'",
                "main_entity" : "main entity  for the query",
                "next_questions" : [Produce 3 related questions(maximum 8 words) aligned with the current question, db context and which can be answered with only two table . While creating questions strictly prohibit questions which tells to specify for a specific item]

            }
            """
        },
        "regeneration_prompt": {
            "template": """
            You were trying to answer the following user question by writing SQL query to answer the question given in `[question][/question]`
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

            Follow these steps to generate the query

            1. Deliberately go through schema, context, rules deliberately
            2. Understand the question and check whether it's doable with the given context
            3. Use survey answers if available and include it in query for filtering values
            4. Do only the task asked, Don't hallucinate and overdo the task
            5. Strictly return all the fields in the schema during listing operations
            6. Strictly return at least 1 text fields and an id field during aggregation/group by operations
            7. Generate a query to solve the problem using the schema, context and the rules and based on the previous query try to rectify the query error
            8. output in the given json format, extra explanation is strictly prohibited

            {
                "explanation": "Explain how you finalized the sql query using the schemas and rules provided",
                "query" : "sqlite query",
                "operation_kind" : "aggregation|list",
                "visualisation": {
                    "type": "chart type (bar chart, line chart, pie chart) or 'table' for tabular format; 'none' if operation_kind is 'list'",
                    "value_field": "fields in which values are stored",
                    "x-axis": "field that can be used as x axis",
                    "y-axis": "field that can be used as y axis",
                    "title": "layout title name"
                },
                "schema": "used schema details separated by comma",
                "confidence" : "confidence in 100",
                "general_message": "a general message describing the answers like 'here is your list of incidents' or 'look what i found'",
                "main_entity" : "main entity  for the query",
                "next_questions" : [Produce 3 related questions(maximum 8 words) aligned with the current question, db context and which can be answered with only two table . While creating questions strictly prohibit questions which tells to specify for a specific item]
            }
            """
        }
    })



__all__ = [
    __version__, __plugin_name__, __display_name__ , __description__, __icon__, __category__, __prompt__
]