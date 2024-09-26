from crewai import Crew
from textwrap import dedent
from crewai import Agent, Task, Crew, Process
from all_finan_agents import NewsSearchAgents
from all_finan_tasks import NewsSearchTasks
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import pdfkit
import os
load_dotenv()

class NewsCrew:
  def __init__(self, industry):
    self.industry = industry
    # self.customer_question = customer_question
    
  def run(self):
    agents = NewsSearchAgents()
    tasks = NewsSearchTasks()

    news_search_agent=agents.news_search_agent()
    writer_agent=agents.news_writer_agent()

    news_search_task=tasks.news_search_task(news_search_agent, self.industry)
    writer_task=tasks.writer_task(writer_agent, [news_search_task])

    
    crew = Crew(
      agents=[news_search_agent, writer_agent],
      tasks=[news_search_task, writer_task],
      process=Process.sequential, 
      verbose=True
    )

    result = crew.kickoff()
    return result

#def save_to_pdf(company, result):
#    filename = f"{company.replace(' ', '_').lower()}_analysis.pdf"
#    pdfkit.from_string(result, filename)
#    return filename

#def save_to_markdown(company, result):
#    filename = f"{company.replace(' ', '_').lower()}_analysis.md"
#    with open(filename, 'w') as f:
#        f.write(f"# Financial Analysis Report for {company}\n\n")
#        f.write(result)
#    return filename

def save_to_markdown(result):
    result_str = str(result)
    filename = "news_report.md"
    with open(filename, 'w') as f:
        f.write("# Industry News Report\n\n")
        f.write(result_str)
    return filename


if __name__ == "__main__":
  print("## Welcome to Industry News Search Crew")
  print('-------------------------------')
  industry = input(
    dedent("""
        What industry are you interested in analyzing?
    """))
  news_crew = NewsCrew(industry)
  result = news_crew.run()
  filename = save_to_markdown(result)

  ## following four lines were original ##
  print("\n\n########################")
  print("## Here is the Report")
  print("########################\n")
  print(result)
