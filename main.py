import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from error_manager import ScientificErrorNotation
from thread_requests import make_requests
from evaluate_solutions import eval_all
from plotter import awesome_plot
    
    
def main():
    # Declare equations and variables
    equation = "x"
    variables = {
        "x": {
            "value": [36, 39, 44, 50, 56, 62],
            "error": 2
        },
        "y": {
            "value": [0.02, 0.019, 0.018, 0.017, 0.016, 0.015],
            "error": (0.02-0.019)*0.20
        }
    }
    
    # Get the solutions from wolfram alpha and evaluate them
    func_1 = eval_all(make_requests(equation, variables))
    
    for i in func_1:
        print(str(i).replace("+-", "pm"))
        
if __name__ == "__main__":
    main()