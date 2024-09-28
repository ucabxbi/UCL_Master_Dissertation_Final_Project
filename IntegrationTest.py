import unittest
from unittest.mock import patch, MagicMock
from main import FinancialReportCrew, save_to_markdown
from ChartMain import ChartCrew
from NewsMain import NewsCrew
from get_info_tools import GetInfoTools
from metric_chart_tools import MetricChartTools, MarkdownTools
from news_tools import DBNewsSearch, GetNews, NewsSearchTools

import unittest
from unittest.mock import patch, MagicMock
from main import FinancialReportCrew, save_to_markdown
from ChartMain import ChartCrew
from NewsMain import NewsCrew
from get_info_tools import GetInfoTools
from metric_chart_tools import MetricChartTools, MarkdownTools
from news_tools import DBNewsSearch, GetNews, NewsSearchTools

class TestFinancialReportCrewIntegration(unittest.TestCase):

    @patch('main.Crew')
    @patch('main.CompanyExamAgents')
    @patch('main.CompanySearchAndAnalysisTasks')
    def test_financial_report_creation(self, mock_tasks, mock_agents, mock_crew):
        # Setup
        company = "AAPL"
        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance
        mock_crew_instance.kickoff.return_value = "Mocked financial report"

        # Mock the agent instances
        mock_data_analyst = MagicMock()
        mock_financial_analyst = MagicMock()
        mock_investment_recommendator = MagicMock()
        mock_agents.return_value.data_analyst.return_value = mock_data_analyst
        mock_agents.return_value.financial_analyst.return_value = mock_financial_analyst
        mock_agents.return_value.investment_recommendator.return_value = mock_investment_recommendator

        # Execute
        crew = FinancialReportCrew(company)
        result = crew.run()

        # Assert
        self.assertEqual(result, "Mocked financial report")
        mock_agents.assert_called_once()
        mock_agents.return_value.data_analyst.assert_called_once()
        mock_agents.return_value.financial_analyst.assert_called_once()
        mock_agents.return_value.investment_recommendator.assert_called_once()
        mock_tasks.assert_called_once()
        mock_crew.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()


    # The test_save_to_markdown method remains unchanged

class TestChartCrewIntegration(unittest.TestCase):

    @patch('ChartMain.Crew')
    @patch('ChartMain.DataResearchAgents')
    @patch('ChartMain.FinanMetricChartTasks')
    @patch('ChartMain.fetch_data_from_quickfs')
    def test_chart_crew_run(self, mock_fetch_data, mock_tasks, mock_agents, mock_crew):
        # Setup
        symbol = "AAPL"
        metrics = "revenue fcf"
        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance
        mock_crew_instance.kickoff.return_value = "Mocked chart report"
        mock_fetch_data.return_value = [100, 200, 300]

        # Execute
        crew = ChartCrew(symbol, metrics)
        result = crew.run()

        # Assert
        self.assertEqual(result, "Mocked chart report")
        mock_agents.assert_called_once()
        mock_tasks.assert_called_once()
        mock_crew.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()

class TestNewsSearchCrewIntegration(unittest.TestCase):

    @patch('NewsMain.Crew')
    @patch('NewsMain.NewsSearchAgents')
    @patch('NewsMain.NewsSearchTasks')
    def test_news_search_crew_run(self, mock_tasks, mock_agents, mock_crew):
        # Setup
        industry = "Technology"
        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance
        mock_crew_instance.kickoff.return_value = "Mocked news report"

        # Execute
        crew = NewsCrew(industry)
        result = crew.run()

        # Assert
        self.assertEqual(result, "Mocked news report")
        mock_agents.assert_called_once()
        mock_tasks.assert_called_once()
        mock_crew.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()

if __name__ == '__main__':
    unittest.main()
