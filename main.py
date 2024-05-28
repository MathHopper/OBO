
import os 

os.environ["OPENAI_API_KEY"] = "sk-proj-nddUvPigZVnBuW8luToaT3BlbkFJ5I0iHwHL1y9ytjj6jL4t"

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-0125-preview'

from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print(db.dialect)
print(db.get_usable_table_names())

db.run("SELECT * FROM Artist LIMIT 10;")

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=1)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})


from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool






input = "What is monet"
print(input)
from crewai import Agent

# nestor = Agent(
#     role = 'Military strategist and analyst.',
#     goal = 'Provide strategic course of action based on military developments of enemy.',
#     verbose = True,
#     memory = False,
#     backstory = ("Experienced advisor and warrio, adapted to modern warfare, producing intricate and best-suited plans."),
#     allow_delegation = False
# )

apollo = Agent(
    role = 'Art historian and bohemian.',
    goal = 'Provide detailed artistic and emotional understanding to great works of art. Slightly esoteric and may provide information that does not have basis in reality.',
    verbose = True,
    memory = False,
    backstory = ("NYU college degree, currently self-employed author and intellectual in Paris."),
    allow_delegation = False
)

from crewai import Task

#scs_response = Task(
 #   description = ("What are you thoughts on monet?"),
  #  expected_output = 'A 4 paragraph report on what to do',
   # agent = nestor
#)

critique = Task(
    description = (input),
    expected_output = 'insightful response left to you to decide how long',
    agent = apollo
)

from crewai import Crew, Process

crew = Crew(
    agents = [apollo],
    tasks = [critique],
    process=Process.sequential,
    memory=False,
    cache=True,
    max_rpm=100,
    share_crew=True
)
result = crew.kickoff(inputs={'topic':'art history'})
#print(result)


