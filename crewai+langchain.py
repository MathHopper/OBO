import os 

os.environ["OPENAI_API_KEY"] = "sk-proj-nddUvPigZVnBuW8luToaT3BlbkFJ5I0iHwHL1y9ytjj6jL4t"
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-0125-preview'


while (True):
    from langchain_community.utilities import SQLDatabase
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")

    from langchain.chains import create_sql_query_chain
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = create_sql_query_chain(llm, db)
    query = input()


    from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm, db)
    chain = write_query | execute_query
    chain.invoke({"question": query})

    from operator import itemgetter

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    # answer_prompt = PromptTemplate.from_template(
    #     """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

    #     Question: {question}
    #     SQL Query: {query}
    #     SQL Result: {result}
    #     Answer: """
    # )

    # answer = answer_prompt | llm | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=write_query).assign(
            result=itemgetter("query") | execute_query
        )
        # | answer
    )
    
    queryResponse = chain.invoke({'question':query})

    print(queryResponse)

    from langchain.agents import Tool

    #searchDb = QuerySQLDataBaseTool(db=db)
    # writeQuery = Tool(
    #     name="Writing Database Query",
    #     func=write_query,
    #     description="Ths tool writes the SQL query for the database.",
    # )

    # searchDatabase = Tool(
    #     name="Database Query Execution",
    #     func=execute_query.run,
    #     description="Useful for search-based queries",
    # )

    from crewai import Agent
    agent = Agent(
        role='Research Analyst',
        goal='Provide up-to-date SQL database findings verbosely given raw database input and context from the user.',
        backstory='An expert analyst with a keen eye for data.',
    )

    from crewai import Task
    query = Task(
        description = ("Using the context:" + query + ", and the database answer:" + queryResponse + ", provide a verbose response in natural language that satisfies the user's question."),
        expected_output = 'insightful response, sentence in length',
        agent = agent
    )
    from crewai import Crew, Process

    crew = Crew(
        agents = [agent],
        tasks = [query],
        process=Process.sequential,
        memory=True,
        verbose=True,
        cache=True,
        max_rpm=100,
        share_crew=True
    )

    result = crew.kickoff(inputs={'topic':'databases'})
    print(result)