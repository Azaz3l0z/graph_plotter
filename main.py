import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from error_manager import ScientificErrorNotation
from thread_requests import make_requests
from evaluate_solutions import eval_all
    
    
def main():
    # Declare equations and variables
    n = np.linspace(0.1, 2, 5)
    equation = "pi*x + x^2 +ln(y)"
    variables = {
        "x": {
            "value": n,
            "error": 0.1
        },
        "y": {
            "value": n,
            "error": 0.1
        },
    }
    
    # Get the solutions from wolfram alpha and evaluate them
    solution = make_requests(equation, variables)
    function_values = eval_all(solution)
    
    # Set an x and y for plotting
    x = variables["x"]["value"]
    y = [x.value() for x in function_values]
    err_y = [x.error() for x in function_values]

    # Fit data linearly and taking errors into account (weight)
    coeff, covariance = np.polyfit(x, y, 1, w=err_y, cov=True)
    fit = np.poly1d(coeff)
    fit_error = [np.sqrt(covariance[i, i]) for i in range(fit.order + 1)]
    
    # Get R Squared
    # fit values, and mean
    f_i = fit(x)
    y_hat = sum(y)/len(y)
    ssres = sum([ (yi - fi)**2 for yi, fi in zip(y, f_i)])
    sstot =  sum([(yi - y_hat)**2 for yi in y])
    R_2 = (1 - ssres / sstot)
    
    print(R_2)
    
    # Print fit and error
    txt = ""
    txt += f'Your fit is: {str(fit).replace(chr(10), "")}'
    for i in range(fit.order + 1):
        i_error = ScientificErrorNotation(0, fit_error[fit.order - i])
        txt += f"\n\tError in x^{i}: {i_error.error()}"
     
    print(txt)
    
    # Plot
    plt.errorbar(x, y, fmt='or', yerr=err_y)
    plt.scatter(x, fit(x))
    plt.xlabel("x", fontsize=16)
    plt.ylabel("F(x,y)", fontsize=16)
    
    x_fit = np.linspace(min(x), max(x), 1000)
    plt.plot(x_fit, fit(x_fit))
    plt.show()
    
    # Save to .csv
    df = {"x": x, "y": y, "err_y": err_y}
    pd.DataFrame(df).to_csv("data.csv", index=False)

if __name__ == "__main__":
    main()

# for x_n in variables:
    


# print(x, y)   

# plt.plot(x, y, color="red", marker=".", linestyle="-")
# plt.xlabel("$\infty$")
# plt.ylabel("Lol2")
# plt.show()