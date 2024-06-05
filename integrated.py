

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os 
import streamlit as st
from plotly import graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
from dotenv import load_dotenv

import sqlite3
load_dotenv()

#API_KEY = os.environ['OPENAI_API_KEY']
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-0125-preview'



st.set_page_config(page_title="Nestor")
st.header("Nestor")

while (True):
    coordinateArray = []
    coordinateArrayFloat =[]
    def latArray():
        latArray = coordinateArray[::2]
        return latArray
    def lonArray():
        lonArray = coordinateArray[1::2]
        return lonArray
    
    input_text = st.text_area(label="LLMinput", placeholder="What do you want to know?", key="input1462")

    import plotly.graph_objects as go
  
    def mapbox():
        mapbox_access_token = "pk.eyJ1Ijoib2FrdHJlZWFuYWx5dGljcyIsImEiOiJjbGhvdWFzOHQxemYwM2ZzNmQxOW1xZXdtIn0.JPcZgPfkVUutq8t8Z_BaHg"
        
        fig = go.Figure(go.Scattermapbox(
            lat=latArray(),
            lon=lonArray(),
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=["The coffee bar","Bistro Bohem","Black Cat",
                "Snap","Columbia Heights Coffee","Azi's Cafe",
                "Blind Dog Cafe","Le Caprice","Filter",
                "Peregrine","Tryst","The Coupe",
                "Big Bear Cafe"],
        ))

        fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=23,
                    lon=120,
                ),
                pitch=0,
                zoom=0
            ),
        )
        fig.update_layout(mapbox_style="satellite")


        return fig

    query = input_text
    from langchain_openai import ChatOpenAI
        
    from tools.queryDatabase import queryDatabase
    from crewai_tools import PDFSearchTool
    queryAIS = queryDatabase
    #pdfSearchTool = PDFSearchTool(pdf="/Users/david/Desktop/David/Coding_Projects/Nestor/hemingway.pdf")

    from crewai import Agent
    databaseAnalyst = Agent(
        role='Database Querier',
        goal='Provide vessel tracking inforrmation from an SQL database findings verbosely given raw database input and context from the user. Provide additional geographical information such as closest country and gepgraphical features of specific location in the ocean.',
        backstory='An expert geospatial analyst with a keen eye illegal fishing vessels and millitary developments.',
        tools=[queryAIS],
        llm=ChatOpenAI(model_name="gpt-4-0125-preview", temperature=1),
        allow_delegation=True
    )
    OSINTresearcher = Agent(
        role='Research Analyst',
        goal='The goal is to search through pdf documents and summarize important data, with the tools at hand.',
        backstory='An expert CIA analyst with a keen eye for finding information regarding military developments in open-source intelligence.',
        tools=[],
        llm=ChatOpenAI(model_name="gpt-4-0125-preview", temperature=1),
        allow_delegation=True
    )

    from crewai import Task
    translate = Task(
        #description = ("Using the context of the question:" + query + ", the database answer:" + queryResponse + ", and memory of previous dialogue provide a verbose response in natural language that satisfies the user's question."),
        description = ("Answer the question:" + query + ", using the tools at hand provide a verbose response in natural language that satisfies the user's question.  If you provide coordinates, follow this format ( LATITUDE , LONGITUDE ), with spaces between parenthesis and commas and digits. Always leave a space after a coordinate floating number."),
        expected_output = 'insightful response, a sentence in length.'
    )

    from crewai import Crew, Process

    crew = Crew(
        agents = [databaseAnalyst],
        manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),
        tasks = [translate],
        process=Process.hierarchical,
        #memory=True,
        verbose=True,
        cache=True,
        max_rpm=100,
        share_crew=True
    )

    result = crew.kickoff(inputs={'topic':'database query'})
    
    st.write(result)

    for i in result.split():
        
        try:
            if float(i) < 180:    
                coordinateArray.append(str(float(i)))  
                coordinateArrayFloat.append(float(i))
        except ValueError:
            pass
        # except len(latArray) != 0:
        #     for j in result.split():
        #         try:
        #             lonArray.append(str(float(j)))
        #         except ValueError:
        #             pass
    
    def displayMap():
        coordinatesExist = False
        mapRequired = False
        if len(coordinateArray) != 0 & len(coordinateArray) != 1:
            coordinatesExist = True
        if "coordinates" in result or "latitude" in result or "longitude" in result or "located" in result:
            mapRequired = True 
        
        if mapRequired == True & coordinatesExist == True:
            return True

    if displayMap() == True:        
        px_map = mapbox()    
        print("map showing!!!!!!")
        st.plotly_chart(px_map, use_container_width=True)


    st.write(coordinateArray)    
    print(coordinateArray)
   