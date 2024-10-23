from crewai_tools import BaseTool
from latest_ai_development.tools.point_hound import FlightScraper


class FlightSearchTool(BaseTool):
    name: str = "Flights_search_engine"
    description: str = (
        "This tool is used to query real-time flight data from a given source airport IATA code to a destination airport IATA code."
    )

    def _run(self, source_airport_iata_code: str, dest_airport_iata_code: str) -> str:
        print(f"Searching for flights from {source_airport_iata_code} to {dest_airport_iata_code}")
        
        scrape_result = FlightScraper().scrape_flights(source_airport_iata_code, dest_airport_iata_code)
        print(scrape_result)
        
        return scrape_result
