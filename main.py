from crewai import Crew
from textwrap import dedent

from all_finan_agents import CompanyExamAgents
from all_finan_tasks import CompanySearchAndAnalysisTasks
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import pdfkit
import os
load_dotenv()

class FinancialReportCrew:
  def __init__(self, company):
    self.company = company
    # self.data = data

  def run(self):
    agents = CompanyExamAgents()
    tasks = CompanySearchAndAnalysisTasks()

    research_analyst_agent = agents.data_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_recommendator_agent = agents.investment_recommendator()
    

    research_task = tasks.research_task(research_analyst_agent, self.company)
    financial_task = tasks.financial_analysis(financial_analyst_agent)
    filings_task = tasks.filings_analysis(financial_analyst_agent)
    recommend_task = tasks.recommend_task(investment_recommendator_agent)
    
    crew = Crew(
      agents=[
        research_analyst_agent,
        financial_analyst_agent,
        investment_recommendator_agent
      ],
      tasks=[
        research_task,
        financial_task,
        filings_task,
        recommend_task
      ],
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
    filename = "financial_analysis_report.md"
    with open(filename, 'w') as f:
        f.write("# Financial Analysis Report\n\n")
        f.write(result_str)
    return filename


if __name__ == "__main__":
  print("## Welcome to Financial Analysis Crew")
  print('-------------------------------')
  company = input(
    dedent("""
      What is the company you want to analyze?
    """))
 
  financial_crew = FinancialReportCrew(company)
  result = financial_crew.run()
  filename = save_to_markdown(result)

  ## following four lines were original ##
  print("\n\n########################")
  print("## Here is the Report")
  print("########################\n")
  print(result)
