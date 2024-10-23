from crewai import Agent, Crew, Task
from pydantic import BaseModel, Field
import datetime

# FlightQuery Model
class FlightQuery(BaseModel):
    iata_code_origin: str = Field(description="The IATA code of the origin of the flight")
    iata_code_destination: str = Field(description="The IATA code of the destination of the flight")
    date: datetime.date = Field(description="The date of the flight")
    class_type: str = Field(description="The class type of the flight")

# Agent
parser_agent = Agent(
    role='Travel Agent',
    goal='Parse a user query into a structured format. Extract the relevant flight information, including the city or airport names and convert them to IATA codes, the flight date, and the flight class type.',
    backstory="""
    You're responsible for parsing flight requests into structured information, including IATA codes for airports.
    """
)

# Task
task = Task(
    description='The current date is "{current_date}". Parse the user query "{query}" about flights, extract the origin and destination cities, convert them into IATA codes, determine the class type (e.g., economy, business, first class), and parse the flight date.',
    agent=parser_agent,
    output_json=FlightQuery,
    expected_output='A JSON object with iata_code_origin, iata_code_destination, date, class_type fields.'
)

# Crew
crew = Crew(
    agents=[parser_agent],
    tasks=[task],
    verbose=True
)

# Test query
query = "I would like a business class flight from New York to Tokyo on the 25th of December"
current_date = str(datetime.date.today())

# Run agent
result = crew.kickoff(inputs={'query': query, 'current_date': current_date})

# Output result
print(result)
