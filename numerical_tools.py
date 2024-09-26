from langchain.tools import tool


class NumericalTools():

  @tool("Make a calculation")
  def calculate(operation):
    """facilitates various numerical computations, 
    including addition, subtraction, multiplication, division, 
    and other mathematical operations.

    Input should be formatted as a standard arithmetic expression.

    Sample inputs:
    1. Product of two numbers: `150*6`
    2. Complex operation: `4000/4+25*3`
    """
    return eval(operation)
