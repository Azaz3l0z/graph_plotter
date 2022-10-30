import numpy as np
import matplotlib.pyplot as plt 

x = np.linspace(0,1,1000)
# comment and uncomment the last term to see how the fit appears in the figure,
# and how the covariances of the single polynomial coefficients vary in turn.
y = np.cos(x) * x**2 + x + np.sin(x - 1.) \
#     + (x * 1.3)**6

p, cov = np.polyfit(x, y, 2, cov=True)

plt.plot(x, y)
plt.plot(x, np.polyval(p,x))
plt.show()

print(np.sqrt(np.diag(cov)))