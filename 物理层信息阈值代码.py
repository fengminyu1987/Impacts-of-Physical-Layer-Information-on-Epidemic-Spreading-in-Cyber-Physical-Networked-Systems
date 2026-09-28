# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator
# # Sigmoid function definition
# def sigmoid(x, alpha=10, theta=0.5):
#     return 1 / (1 + np.exp(-alpha * (x - theta)))
#
# # Generate x values from -5 to 5
# x_values = np.linspace(0, 1, 20)
#
# # Compute the corresponding y values
# y_values = sigmoid(x_values)
#
#
#
# # Set x and y axis ticks with 0.1 intervals
# ax = plt.gca()
# ax.xaxis.set_major_locator(MultipleLocator(0.1))
# ax.yaxis.set_major_locator(MultipleLocator(0.1))
#
# # Add grid and lines
# plt.axhline(0, color='black', linewidth=0.5)
# plt.axvline(0, color='black', linewidth=0.5)
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)
# plt.legend()
# plt.tight_layout()
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Sigmoid function definition
def sigmoid(x, alpha=10, theta=0.5):
    return 1 / (1 + np.exp(-alpha * (x - theta)))

# Generate x values from -1 to 2 to focus on the curve transition
x_values = np.linspace(0, 1, 20)
y_values = sigmoid(x_values)


# Plot
plt.figure(figsize=(8, 5))
plt.plot(x_values, y_values, label=r"$y = \frac{1}{1 + e^{-\alpha (x - \theta)}}$", color='blue')
plt.xlabel("x")
plt.ylabel("y")
plt.title(r"$y = \frac{1}{1 + e^{-\alpha (x - \theta)}}$ with $\alpha=10$, $\theta=0.5$")

# Set x and y limits to start from 0
plt.xlim(0, 1)
plt.ylim(0, 1)

# Set x and y axis ticks with 0.1 intervals
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_major_locator(MultipleLocator(0.1))

# Add grid and lines
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()
