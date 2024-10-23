#!/usr/bin/env python
import sys
from latest_ai_development.crew import LatestAiDevelopmentCrew
from latest_ai_development.crew_scrape import ScraperCrew

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

from pydantic import BaseModel, Field


# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

class FlightInfo(BaseModel):
    flights: list[dict] = Field(description="A list of flights")
    
def run():
    """
    Run the crew.
    """
    
    inputs = {
        'query': 'flights from Montreal to Dubai'
    }
    # # LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
    ScraperCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        LatestAiDevelopmentCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LatestAiDevelopmentCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        LatestAiDevelopmentCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
