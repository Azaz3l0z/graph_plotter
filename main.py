import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from error_manager import ScientificErrorNotation
from thread_requests import make_requests
from evaluate_solutions import eval_all
    
    
def main():
    # Declare equations and variables
    n = np.linspace(0.1, 2, 5)
    equation = "4*pi^2/((2*pi/t)^2 + (b/2)^2)"
    variables = {
        "t": {
            "value": [0.02255,0.02460,0.02730,0.02970,0.03120,0.03285],
            "error": 4*10**-5
        },
        "b": {
            "value": [50, 45, 15.7, 12.6, 16.4, 25.7],
            "error": [6, 4, 0.9, 0.8, 0.2, 1.5]
        },
    }
    
    h = [30, 40, 50, 60, 70, 80]
    
    # Get the solutions from wolfram alpha and evaluate them
    solution = make_requests(equation, variables)
    function_values = eval_all(solution)
    
    # Set an x and y for plotting
    x = h
    y = [x.value() for x in function_values]
    err_y = [x.error() for x in function_values]

    # Fit data linearly and taking errors into account (weight)
    coeff, covariance = np.polyfit(x, y, 1, w=err_y, cov=True)
    fit = np.poly1d(coeff)
    fit_error = np.sqrt(np.diag(covariance))
    
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
        i_error = ScientificErrorNotation(0, fit_error[i])
        txt += f"\n\tError in x^{fit.order - i}: {i_error.error()}"
     
    print(txt)
    
    # Plot
    plt.errorbar(x, y, fmt='or', yerr=err_y)
    plt.plot(x, fit(x))
    plt.xlabel("$h$ / mm", fontsize=16)
    plt.ylabel("$\\tau_0^2$ / s$^2$", fontsize=16)
    
    x_fit = np.linspace(min(x), max(x), 1000)
    plt.plot(x_fit, fit(x_fit))
    plt.show()
    plt.savefig("fig.png")
    
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