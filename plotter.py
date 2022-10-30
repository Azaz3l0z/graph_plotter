import numpy as np
import matplotlib as plt

from error_manager import ScientificErrorNotation
def awesome_plot(x: list, y: list, err_y: list, fig_name: str = "fig.png"):
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
    plt.subplots_adjust(left=0.17)
    plt.savefig("fig.png")
    plt.show()