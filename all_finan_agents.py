from crewai import Agent
from numerical_tools import NumericalTools
from get_info_tools import GetInfoTools
from swot_analysis_tool import SWOTAnalysisGuideTool
from news_tools import DBNewsSearch, GetNews, NewsSearchTools
# from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools import YahooFinanceNewsTool
from metric_chart_tools import MetricChartTools, MarkdownTools
import os
from crewai import Agent
import re
import streamlit as st
from textwrap import dedent
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)
# callback handler to print to app
def streamlit_callback(step_output):
    # This function will be called after each step of the agent's execution
     st.markdown("---")
     for step in step_output:
         if isinstance(step, tuple) and len(step) == 2:
             action, observation = step
             if isinstance(action, dict) and "tool" in action and "tool_input" in action and "log" in action:
                 st.markdown(f"# Action")
                 st.markdown(f"**Tool:** {action['tool']}")
                 st.markdown(f"**Tool Input** {action['tool_input']}")
                 st.markdown(f"**Log:** {action['log']}")
                 st.markdown(f"**Action:** {action['Action']}")
                 st.markdown(
                     f"**Action Input:** ```json\n{action['tool_input']}\n```")
             elif isinstance(action, str):
                 st.markdown(f"**Action:** {action}")
             else:
                 st.markdown(f"**Action:** {str(action)}")

             st.markdown(f"**Observation**")
             if isinstance(observation, str):
                 observation_lines = observation.split('\n')
                 for line in observation_lines:
                     if line.startswith('Title: '):
                         st.markdown(f"**Title:** {line[7:]}")
                     elif line.startswith('Link: '):
                         st.markdown(f"**Link:** {line[6:]}")
                     elif line.startswith('Snippet: '):
                         st.markdown(f"**Snippet:** {line[9:]}")
                     elif line.startswith('-'):
                         st.markdown(line)
                     else:
                         st.markdown(line)
             else:
                 st.markdown(str(observation))
         else:
             st.markdown(step)

class CompanyExamAgents():
  def financial_analyst(self):
    return Agent(
      role='The Best Financial Analyst',
      goal="""Dazzle clients with your insightful economic data 
        interpretation and market dynamic evaluations""",
      backstory="""A highly accomplished economic expert with 
      extensive experience in equity market assessment and portfolio 
      optimization techniques, currently serving a high-profile clientele.""",
      verbose=False,
      llm=llm,
      tools=[
        GetInfoTools.search_internet,
        NumericalTools.calculate,
      ],
       step_callback=streamlit_callback,
    )

  def data_analyst(self):
    return Agent(
      role='Senior Data Insights Specialist',
      goal="""Excel in data collection and analysis, providing 
      clients with remarkable, actionable intelligence""",
      backstory="""Renowned as a top-tier information analyst, you excel 
      at processing industry updates, corporate communications, and 
      market trends. Currently, you're engaged with a high-priority client.""",
      verbose=False,
      llm=llm,
      tools=[
        GetInfoTools.search_internet,
        YahooFinanceNewsTool(),
      ],
      step_callback=streamlit_callback,
  )

  def investment_recommendator(self):
    return Agent(
      role='Personal Portfolio Strategist',
      goal="""Captivate clients with comprehensive stock evaluations 
      and thorough investment guidance, including an expert SWOT analysis which includes a strengths-weaknesses-
      opportunities-threats breakdown""",
      backstory="""As a seasoned wealth management professional, you excel 
      at synthesizing diverse market insights to craft strategic financial 
      recommendations. Your current assignment involves a high-profile client 
      who demands top-tier service. Your speciality lies in producing in-depth 
      quadrant analyses of investment opportunities, grounded in extensive market research.""",
      verbose=False,
      llm=llm,
      tools=[
        GetInfoTools.search_internet,
        GetInfoTools.search_news,
        NumericalTools.calculate,
        YahooFinanceNewsTool(),
        SWOTAnalysisGuideTool.get_structure_guide,
        SWOTAnalysisGuideTool.get_section_example,
        SWOTAnalysisGuideTool.get_writing_style_tips
      ],
      step_callback=streamlit_callback,
    )

class DataResearchAgents():
  def metric_drawer(self):
      return Agent(
          role="Data Visualization Specialist",
          goal=dedent(f"""Transform provided datasets into graphical representations using the tool."""),
          backstory=dedent(f"""Renowned for your precision in converting numerical sequences into visually compelling diagrams. 
                           Your expertise lies in meticulously crafting accurate visual data interpretations. 
                           It is imperative that you employ the specified visualization tool for this task."""),
          tools=[
              MetricChartTools.create_chart
            ] ,
          verbose=True,
          llm=llm,
        )

    
  def markdown_writer(self):
      return Agent(
          role="Report writing Specialist",
          goal=dedent(f"""Incorporate references to local image files (*.png) into a structured markdown document using appropriate syntax."""),
          backstory=dedent(f"""Renowned for your expertise in crafting precise markdown documentation. 
                           Your skill lies in translating textual input into well-formatted markdown content, saving it within the current working directory. 
                           Your methodology includes appending a line break after each content insertion for optimal readability.
                           *CRITICAL: Adhere strictly to markdown formatting conventions for ALL content. 
                           Under no circumstances should non-markdown compliant text be introduced into the report.md file.*"""),
 
          tools=[MarkdownTools.write_text_to_markdown_file],
          verbose=True,
          llm=llm,
        )
      
      
class NewsSearchAgents():
  def news_search_agent(self):
    return Agent(
    role='Industry News Researcher',
    goal='Distill critical insights from latest industry news',
    backstory='Expert in analyzing and generating key points from industry news content for comprehensive updates.',
    tools=[DBNewsSearch().databasenews],
    allow_delegation=True,
    verbose=True,
    llm=llm
)

  def news_writer_agent(self):
    return Agent(
    role='News Writer',
    goal='Identify all the topics received, verify each topic, search for detailed information on each topic, and compile a comprehensive industry report.',
    backstory='Expert in crafting engaging narratives from complex industry information, with a focus on thorough and detailed reporting of industry trends and developments.',
    tools=[GetNews().news, NewsSearchTools().search_news],
    allow_delegation=True,
    verbose=True,
    llm=llm
)
