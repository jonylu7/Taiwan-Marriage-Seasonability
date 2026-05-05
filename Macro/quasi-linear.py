import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Quasi-linear utility function: U(x,y) = v(x) + y
# where v(x) is concave (typically sqrt(x) or log(x))

def quasi_linear_utility(x, y):
    """
    Quasi-linear utility function: U(x,y) = ln(x) + y
    """
    v = np.log(x)  # Natural logarithm
    return v + y

# Create grid
x = np.linspace(0.1, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)

# Calculate utility for U(x,y) = ln(x) + y
U = quasi_linear_utility(X, Y)

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# 3D surface plot
ax1 = fig.add_subplot(2, 3, 1, projection='3d')
surf1 = ax1.plot_surface(X, Y, U, cmap='viridis', alpha=0.8)
ax1.set_xlabel('Good x', fontsize=10)
ax1.set_ylabel('Good y', fontsize=10)
ax1.set_zlabel('Utility', fontsize=10)
ax1.set_title('Quasi-linear: U(x,y) = ln(x) + y', fontsize=12)
plt.colorbar(surf1, ax=ax1, shrink=0.5)

# Contour plots for different utility levels
utility_levels = [1, 2, 3, 4, 5, 6]

ax2 = fig.add_subplot(2, 3, 2)
contour1 = ax2.contour(X, Y, U, levels=utility_levels, colors='teal')
ax2.clabel(contour1, inline=True, fontsize=8)
ax2.set_xlabel('Good x', fontsize=10)
ax2.set_ylabel('Good y', fontsize=10)
ax2.set_title('Indifference Curves', fontsize=12)
ax2.grid(True, alpha=0.3)

ax3 = fig.add_subplot(2, 3, 3)
# Show filled contour for better visualization
contour3 = ax3.contourf(X, Y, U, levels=20, cmap='YlOrRd')
ax3.set_xlabel('Good x', fontsize=10)
ax3.set_ylabel('Good y', fontsize=10)
ax3.set_title('Utility Heatmap', fontsize=12)
plt.colorbar(contour3, ax=ax3)

# 2D cross-sections showing the relationship
x_values = np.linspace(0.1, 10, 100)

ax4 = fig.add_subplot(2, 3, 4)
y_fixed = 5
u_x = quasi_linear_utility(x_values, y_fixed)

ax4.plot(x_values, u_x, 'teal', linewidth=2, label='ln(x) + 5')
ax4.set_xlabel('Good x (y fixed at 5)', fontsize=10)
ax4.set_ylabel('Utility', fontsize=10)
ax4.set_title('Utility vs x: U(x,5) = ln(x) + 5', fontsize=12)
ax4.legend()
ax4.grid(True, alpha=0.3)

# Show how y affects utility (linear relationship)
ax5 = fig.add_subplot(2, 3, 5)
x_fixed = 5
y_values = np.linspace(0, 10, 100)
u_y = quasi_linear_utility(x_fixed, y_values)

ax5.plot(y_values, u_y, 'purple', linewidth=2, label='ln(5) + y')
ax5.set_xlabel('Good y (x fixed at 5)', fontsize=10)
ax5.set_ylabel('Utility', fontsize=10)
ax5.set_title('Utility vs y: LINEAR!', fontsize=12)
ax5.legend()
ax5.grid(True, alpha=0.3)

# Additional visualization: Marginal rate of substitution
ax6 = fig.add_subplot(2, 3, 6)
# MRS = -MUx/MUy
# For U(x,y) = ln(x) + y
# MUx = 1/x, MUy = 1
# MRS = -(1/x)/1 = -1/x
def mrs_ln(x):
    return -1 / x

ax6.plot(x_values, mrs_ln(x_values), 'darkorange', linewidth=2)
ax6.set_xlabel('Good x', fontsize=10)
ax6.set_ylabel('Marginal Rate of Substitution', fontsize=10)
ax6.set_title('MRS = -1/x (depends only on x)', fontsize=12)
ax6.grid(True, alpha=0.3)
ax6.set_ylim(-15, 0)

plt.tight_layout()
plt.savefig('quasi_linear_function.png', dpi=150, bbox_inches='tight')
plt.show()

print("Quasi-linear function U(x,y) = ln(x) + y plotted successfully!")
print("\nKey properties:")
print("- Linear in y: U increases by 1 unit for each unit increase in y")
print("- Concave in x: ln(x) shows diminishing marginal utility in x")
print("- MRS = -1/x: depends only on x, not on y")
print("- Income effect for y is zero (unique property of quasi-linear preferences)")
