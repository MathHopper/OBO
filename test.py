import os 

os.environ["OPENAI_API_KEY"] = "sk-proj-nddUvPigZVnBuW8luToaT3BlbkFJ5I0iHwHL1y9ytjj6jL4t"
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-0125-preview'

while (True):    
    from crewai import Agent
    Achilles = Agent(
        role='Achilles',
        goal='Provide battle plans to conquer the Trojans, and give your life history.',
        backstory='You are Achilles, the legendary, passionate hero of the Greeks during the Trojan war. You are consumed by grief and anger following the death of Patroculus by the hand of Hector, and seek revenge. He cannot think straight and is fuming with rage and sadness.',
    )

    from crewai import Task
    query = Task(
        description = (input()),
        expected_output = 'insightful response, sentence in length',
        agent = Achilles
    )
    from crewai import Crew, Process

    crew = Crew(
        agents = [Achilles],
        tasks = [query],
        process=Process.sequential,
        memory=True,
        verbose=True,
        cache=True,
        max_rpm=100,
        share_crew=True
    )

    result = crew.kickoff(inputs={'topic':'advice'})
    print(result)