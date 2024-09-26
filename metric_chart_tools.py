import os
import json
from dotenv import load_dotenv
from quickfs import QuickFS
from langchain.tools import tool
from pydantic.v1 import BaseModel, validator, Field
from typing import List
import random
import matplotlib.pyplot as plt
import requests
load_dotenv()

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class CreateChartInput(BaseModel):
    metric: str
    data: List[float]

class CreateChartOutput(BaseModel):
    file_path: str

class MetricChartTools():    
    @tool("Create a chart of the data")
    def create_chart(symbol: str, metric_name: str, data: List[float], years: List[int], config: dict = None) -> CreateChartOutput:
        """
        Creates a bar chart graphic based on the provided metric and data.

        Parameters:
        - symbol (str): The company symbol.
        - metric_name (str): The name of the metric to be visualized on the chart.
        - data (List[float]): A list of numerical data points representing the metric over time.
        - years (List[int]): A list of years corresponding to the data points.
        - config (dict): Optional configuration parameters for the chart.
       
        Returns:
        - file_path (str): The file path to the saved chart image.
        
        Example:
        - create_chart(symbol='AAPL', metric='revenue', data=[100, 150, 120, 200, 180], years=[2016, 2017, 2018, 2019, 2020])
        - Returns: CreateChartOutput(file_path='./AAPL_revenue_chart.png')
        """

        # Determine the appropriate scale (Billion, Million, Thousand, or no scale)
        max_value = max(data)
        if max_value >= 1e9:
            scale = 1e9
            scale_label = "Billions"
            label_suffix = "B"
        elif max_value >= 1e6:
            scale = 1e6
            scale_label = "Millions"
            label_suffix = "M"
        elif max_value >= 1e3:
            scale = 1e3
            scale_label = "Thousands"
            label_suffix = "K"
        else:
            scale = 1  # No scaling for small numbers
            scale_label = ""
            label_suffix = ""

        # Scale data accordingly
        scaled_data = [d / scale for d in data]
        
        # Generate a random color for all bars
        bar_color = f'#{random.randint(0, 0xFFFFFF):06x}'

        fig, ax = plt.subplots()
        bars_container = ax.bar(years, scaled_data, color=bar_color)
        ax.set_xlabel('Years')
        ax.set_xticks(years)  # Set the x-axis ticks to the specific years
        ax.set_ylabel(metric_name)
        ax.set_title(f"{symbol} - {metric_name}")
        # Dynamically set the y-axis label based on the scale
        if scale_label:
            ax.set_ylabel(f'{metric_name} (in {scale_label})')
        else:
            ax.set_ylabel(f'{metric_name}')

        ax.set_xlabel('Years')
        ax.set_title(f"{symbol} - {metric_name}")
        # Add labels to each bar, formatted dynamically
        ax.bar_label(bars_container, labels=[f'{d:.2f}{label_suffix}' for d in scaled_data])

        # Save the figure to the current directory
        file_path = f"./{symbol}_{metric_name.replace(' ', '_')}_chart.png"
        fig.savefig(file_path, format='png')
        plt.close(fig)  # Close the Matplotlib figure to free resources

        return CreateChartOutput(file_path=file_path)
        



class MarkdownTools():
    @tool("Write text to markdown file")
    def write_text_to_markdown_file(text: str) -> str:
        """Facilitates the creation and editing of Markdown-formatted documents.
            Input: 
            - Content: A text string to be formatted in Markdown syntax.
            - Destination: A string specifying the target file path (e.g., 'report.md').

            **Example** Writes `![](revenue_chart.png)` to report.md file.
           
           :param text: str, the string to write to the file
           """
        try:
            markdown_file_path = r'report.md'
            
            with open(markdown_file_path, 'w') as file:
                file.write(text)
            
            return f"File written to {markdown_file_path}."
        except Exception:
            return "Something has gone wrong writing images to markdown file."