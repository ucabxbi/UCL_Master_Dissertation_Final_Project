from crewai import Task
from textwrap import dedent


class CompanySearchAndAnalysisTasks():
  def __tip_section(self):
    return "Your EXCEPTIONAL WORK on this project could fast-track you to a senior analyst position and get you a $100,000 bonus!"



  def research_task(self, agent, company):
    return Task(description=dedent(f"""
        Compile and synthesize current media coverage, official company 
        communications, and industry evaluations pertaining to the given 
        equity and its sector.

        Focus on identifying key developments, overall market perceptions, 
        and expert perspectives. Include a timeline of forthcoming corporate 
        events, such as financial disclosures and other relevant milestones.

        Your deliverable should be a comprehensive brief encompassing:
        1. A thorough overview of recent developments
        2. Any notable fluctuations in investor sentiment
        3. Potential ramifications for the stock's performance

        Ensure the stock's trading symbol is clearly stated in your report.
        
        {self.__tip_section()}
  
        Make sure to use the most recent data as possible.
  
        Selected company by the customer: {company}
      """),
      agent=agent,
    )

  def financial_analysis(self, agent): 
    return Task(description=dedent(f"""
        Perform a comprehensive evaluation of the equity's fiscal vitality 
        and market standing. 

        Your assessment should encompass crucial financial indicators, including 
        at least the following but not limited to:
        - P/E ratio
        - EPS
        - Revenue 
        - Net income
        - D/E ratio
        
        Additionally, benchmark the stock's performance against sector peers 
        and broader market movements.

        Your final submission must build upon the initial overview, incorporating:
        1. A lucid appraisal of the company's financial position
        2. An outline of its competitive advantages and potential vulnerabilities
        3. A comparative analysis situating the stock within the current 
          industry landscape and market conditions

        Ensure your analysis is data-driven, providing context for each metric 
        and its implications for the stock's overall health and prospects.
        
        {self.__tip_section()}

        Make sure to use the most recent data possible.
      """),
      agent=agent,
    )

  def filings_analysis(self, agent):
    return Task(description=dedent(f"""

        Scrutinize essential components of corporate disclosures, including:
        - Executive commentary and operational review
        - Fiscal reports and balance sheets
        - Internal stakeholder trading patterns
        - Declared potential challenges and uncertainties

        Distill crucial information and perspectives that may shape the 
        equity's trajectory.

        Your deliverable should be a comprehensive analysis that:
        1. Emphasizes noteworthy discoveries from these official documents
        2. Identifies potential warning signals
        3. Highlights promising indicators

        Ensure your report provides actionable intelligence for your client, 
        synthesizing complex data into clear, strategic insights.
        {self.__tip_section()}        
      """),
      agent=agent,
    )

  def recommend_task(self, agent):
    return Task(description=dedent(f"""
        Review and synthesize the analyses provided by the
        Financial Analyst and the Research Analyst.
        Combine these insights to form a comprehensive
        investment recommendation. 
        
        Your analysis must encompass:
        1. Fiscal robustness indicators
        2. Market perception trends
        3. Qualitative data extracted from regulatory filings

        Incorporate dedicated sections addressing: 
        - insider trading activity
        - upcoming events like corporate milestones, particularly financial disclosures
                 
        Your final answer MUST be a recommendation for your
        customer. It should be a full super detailed report, including a SWOT analysis that follows 
        the structure, depth, and professional writing style learned from the SWOT analysis guide.
        Make it pretty and well formatted for your customer.
        
        Ensure your report is meticulously formatted and visually appealing, 
        befitting a high-caliber client presentation.
        {self.__tip_section()}
      """),
      agent=agent,
      expected_output=dedent(f"""
        A comprehensive investment recommendation report that synthesizes analyses 
        from financial, market sentiment, and qualitative data sources. The report 
        should include:

        1. Executive Summary: A brief overview of the investment recommendation.

        2. Company Overview: Basic information about the company and its business model.

        3. Financial Analysis: 
          - Key financial metrics, including at least the following but not limited to: P/E ratio, 
          EPS, Revenue, Net income, D/E ratio and their trends
          - Comparison with industry peers

        4. Market Analysis:
          - Current market position
          - Industry trends and competitive landscape

        5. SWOT Analysis: Provide a detailed SWOT analysis of the company. 
        Use the SWOT Analysis Guide tools to create a professional SWOT analysis:
        1. Use get_structure_guide() to understand the overall structure of a SWOT analysis.
        2. Use get_section_example(section) to see examples of each section (e.g., "strengths", "weaknesses").
        3. Apply get_writing_style_tips() to ensure a professional writing style.
        
        Following the structure provided by the SWOT Analysis Guide:
          - Introduction
          - Strengths
          - Weaknesses
          - Opportunities
          - Threats
          - Conclusion
          Each section should be well-developed with specific examples and analysis,
          following the professional writing style tips provided.     
        
        6. Insider Trading Activity: Recent significant insider transactions and their implications.

        7. Upcoming Events: Such as earnings releases, product launches, or other significant events.

        8. Risk Assessment: Potential risks and mitigating factors.

        9. Investment Recommendation: 
          - Clear investment stance (e.g., Buy, Hold, Sell)
          - Target price (if applicable)
          - Investment timeframe
          - Supporting evidence for the recommendation

        10. Conclusion: Summarizing key points and reiterating the investment thesis.

        The report must be well-structured, professionally formatted, and provide 
        a clear investment strategy with robust supporting evidence. It should 
        demonstrate a deep understanding of the company, its market position, 
        and future prospects, all presented in a way that's accessible to the client.
        """)
   )

class FinanMetricChartTasks:
    def __tip_section(self):
        return "Your EXCEPTIONAL WORK on this project could fast-track you to a senior analyst position and get you a $100,000 bonus!"

    def user_input(self, agent, data: str):
        return Task(
            description=dedent(f"""
            **Task**: Data Extraction from Text Input.
            **Description**: Take the input string and extract the corporate ticker symbol
            out of it and also isolate any financial metrics present.

            **Parameters**: 
            - data: {data}

            **Notes**
            {self.__tip_section()}
            """
        ),
            agent=agent,
            expected_output="""A list of dictionaries containing the symbol and metric.
            Example output: `[{'symbol': 'TSLA', 'metric': 'revenue'}, {'symbol': 'MSTR', 'metric': 'fcf'}]`"""
        )

    def get_data_from_quickfs(self, agent, context):
        return Task(
               description=dedent(f"""
            **Description**: For each metric, search the metric for the corporate ticker symbol provided by using the tool.

            **Notes**
            You MUST use QuickFS to retrieve data for EVERY metric that the client requests. 
            You may have to iterate this process as necessary to fulfill all client requirements.
            {self.__tip_section()}
            """
        ),
            agent=agent,
            context=context,
            expected_output="""A list of metrics and the data retrieved for each one. 
            Example output: [
                {metric:'fcf', data: [...data_points],
                {metric:'revenue', data: [...data_points],
                {metric:'net_income, data: [...data_points],
                {...}
                ]"""
        )

    def generate_charts(self, agent, symbol: str, data: dict, config: dict = None) -> Task:
        return Task(
            description=dedent(f"""
                Create graphics of the data representing financial metrics for the company {symbol}.
                Use the provided data to create charts for each metric.
                Data: {data}
                Config: {config}

                DO NOT change the metric name when you create the title of the chart.

                {self.__tip_section()}
            """),
            agent=agent,
            expected_output="""
                A list of the file locations of the created charts.
                Example output: [fcf_chart.png, cogs_chart.png]
                """
        )


    def write_markdown(self, agent, context):
            return Task(
                description=dedent(f"""
                    **Task**: Create a markdown report with the financial data and charts
                    **Description**: Create a comprehensive markdown report that includes:
                    1. An overview of the company and the metrics analyzed
                    2. A section for each metric with:
                    - The metric name
                    - The data points
                    - An analysis of the trend
                    - The chart image (use the file paths provided in the context)

                    Use the context provided from the create_charts task to access the data and chart file paths.

                    Context: {context}

                     YOU MUST USE MARKDOWN SYNTAX AT ALL TIMES.

                    **Notes**
                    {self.__tip_section()}
                """
            ),
                agent=agent,
                expected_output="""A report.md file formatted in markdown syntax. 
                Example output: 
                    # Financial Report for [Company Symbol]

                    ## Metric: FCF
                    Data: [...]
                    Analysis: ...
                    ![](./SYMBOL_FCF_chart.png)

                    ## Metric: COGS
                    Data: [...]
                    Analysis: ...
                    ![](./SYMBOL_COGS_chart.png)
                    """,
                context=context,
         )
            
class NewsSearchTasks():
  def __tip_section(self):
    return "Your EXCEPTIONAL WORK on this project could fast-track you to a senior analyst position and get you a $100,000 bonus!"

  def news_search_task(self, agent, industry):
    return Task(description=dedent(f"""Search for the selected industry and create key points for each news article.
        Selected industry by the customer: {industry}
        {self.__tip_section()}        
      """),
      agent=agent
)

  def writer_task(self, agent, context): 
    return Task(description=dedent(f"""
       Follow these steps precisely for each topic in the given context:
        1. Identify and list all topics from the context related to the industry.
        2. For each topic:
           a. Use the Get News Tool to verify the topic's relevance to the industry.
           b. Use the NewsSearchTools to search for detailed information on the topic and find additional perspectives and analyses for each industry-related topic.
           c. Compile all retrieved information for the topic, clearly distinguishing between the information from Get News Tool and NewsSearchTools.
           d. Provide specific sources (URLs when available) for each piece of information related to the topic.
        3. Create a comprehensive industry report that includes:
           - Detailed information on all industry-related topics from Get News Tool
           - Additional views and analyses from NewsSearchTools for each topic
           - For each topic, provide clear citations of sources, including URLs where available
           - An overview of the current state of the industry
           - Major trends and developments in the industry
           - Key players and their recent activities
         Folow the structure and don't skip any steps.
        4. Ensure no relevant industry topic is skipped and provide full details for each.
        Context: {context}

        Remember, thoroughness is key. Do not summarize; provide full details for each industry-related topic.
      {self.__tip_section()}
    """),
    agent=agent,
    expected_output= """        
        Industry Report: [Industry Name]

        1. **[News 1 Title]**
           - **Overview**: [Brief description of the news]
           - **Findings**: [Key findings or updates]
           - **Significance**: [Why this is important for the industry]
           - **Source**:
             - [Source 1 description with link]
             - [Source 2 description with link]

        2. **[News 2 Title]**
           - **Overview**: [Brief description of the news]
           - **Findings**: [Key findings or updates]
           - **Significance**: [Why this is important for the industry]
           - **Source**:
             - [Source 1 description with link]
             - [Source 2 description with link]

        3. **[News 3 Title]**
           - **Overview**: [Brief description of the news]
           - **Findings**: [Key findings or updates]
           - **Significance**: [Why this is important for the industry]
           - **Source**:
             - [Source 1 description with link]
             - [Source 2 description with link]

        [Repeat for all identified topics]

        Industry Overview:
        ------------------
        [Comprehensive overview of the industry, its scope, and current state]

        Major Trends and Developments:
        ------------------------------
        1. [Trend/Development 1]
        2. [Trend/Development 2]
        ...
        [Repeat for all identified Trend/Development]


        Key Players and Recent Activities:
        ----------------------------------
        1. [Company/Organization Name 1]
           - [Recent activity or development]
        2. [Company/Organization Name 2]
           - [Recent activity or development]
        ...
        [Repeat for all identified Company/Organization]

            """,
    context=context
)