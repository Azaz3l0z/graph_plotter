import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from error_manager import ScientificErrorNotation
from thread_requests import make_requests
from evaluate_solutions import eval_all
    
    
def main():
    # Declare equations and variables
    n = np.linspace(0.1, 2, 5)
    equation = "4*pi^2*b/(pi*(D/2)^2*P*a)"
    variables = {
        "a": {
            "value": [1.16*10**(-2)],
            "error": 0.04*10**(-2)
        },
        "P": {
            "value": [1.01*10**5],
            "error": 0
        },
        "b": {
            "value": [35*10**(-3)],
            "error": 0.6*10**(-3)
        },
        "D": {
            "value": [32.5*10**(-3)],
            "error": 0.1*10**(-3)
        },
    }
    
    # Get the solutions from wolfram alpha and evaluate them
    solution = make_requests(equation, variables)
    function_values = eval_all(solution)
    for i in function_values:
        print(i)


if __name__ == "__main__":
    main()

# for x_n in variables:
    


# print(x, y)   

# plt.plot(x, y, color="red", marker=".", linestyle="-")
# plt.xlabel("$\infty$")
# plt.ylabel("Lol2")
# plt.show()