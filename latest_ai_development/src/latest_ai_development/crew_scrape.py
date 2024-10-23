from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
from latest_ai_development.tools.custom_tool import FlightSearchTool
from pydantic import BaseModel, Field


# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

class FlightInfo(BaseModel):
    flights: list[dict] = Field(description="A list of flights")

@CrewBase
class ScraperCrew():
	"""Scraper crew"""

	@agent
	def flight_explorer(self) -> Agent:
		return Agent(
			config=self.agents_config['flight_explorer'],
			tools=[FlightSearchTool(result_as_answer=True)], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			max_retry_limit=0
		)

	@task
	def search_task(self) -> Task:
		print(self.tasks_config)
		return Task(
			config=self.tasks_config['search_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Scraper crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)