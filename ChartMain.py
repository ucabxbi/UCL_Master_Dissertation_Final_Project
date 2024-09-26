import os
import requests
from all_finan_agents import DataResearchAgents
from all_finan_tasks import FinanMetricChartTasks

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from textwrap import dedent
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# quickfs api start
def fetch_data_from_quickfs(symbol: str, metric: str):
    api_key = os.getenv('QUICKFS_API_KEY')
    
    if not api_key:
        raise ValueError("Error: QuickFS API key not found in envirosnment variables.")

    base_url = "https://public-api.quickfs.net/v1"
    endpoint = f"{base_url}/data/{symbol}/{metric}"
    params = {"period": "FY-4:FY"}  # Last 5 years of annual data
    
    headers = {
        "X-QFS-API-Key": api_key,
        "Accept": "application/json"
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.RequestException(f"API call failed with status code: {response.status_code}. Response content: {response.text}")
    
    except requests.RequestException as e:
        raise requests.RequestException(f"An error occurred while making the API request: {str(e)}")
# quickfs api call end

class ChartCrew:
    def __init__(self, symbol, metrics):
        self.symbol = symbol
        self.metrics = metrics.split()  # Assuming metrics are space-separated
    
    def run(self):
        agents = DataResearchAgents()
        tasks = FinanMetricChartTasks()
        
        # Fetch data directly
        try:
            data = {metric: fetch_data_from_quickfs(self.symbol, metric) for metric in self.metrics}
            logger.info(f"Data fetched successfully: {data}")
        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            return f"Failed to fetch data: {str(e)}"

        # AGENTS
        chart_drawer = agents.metric_drawer()
        markdown_writer = agents.markdown_writer()
        
        #Tasks
        create_chart_task = tasks.generate_charts(chart_drawer, self.symbol, data, {})
        create_markdown_file_task = tasks.write_markdown(markdown_writer, [create_chart_task])
        
        # Define your custom crew here
        crew = Crew(
            agents=[chart_drawer, markdown_writer],
            tasks=[create_chart_task, create_markdown_file_task],
            verbose=True,
        )
        
        try:
            result = crew.kickoff()
            return result
        except Exception as e:
            logger.error(f"An error occurred during crew execution: {str(e)}")
            return f"Failed to generate report due to error: {str(e)}"


# main function to run quickfs and related tasks
if __name__ == "__main__":
    print("## Welcome to Metrics Chart Creator Crew")
    print("-------------------------------")
    symbol = input("Enter company symbol: ")
    metrics = input("Enter the metrics you want to analyze (space-separated): ")
    mycrew = ChartCrew(symbol, metrics)
    result = mycrew.run()
    print(result)