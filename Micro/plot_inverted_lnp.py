import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Example data - replace with your actual data
# Assuming P is price and you have customer numbers
# You can load from CSV or define your data here

# Sample data generation (replace with your actual data)
np.random.seed(42)
P = np.linspace(10, 100, 50)  # Price values
customer_numbers = np.arange(1, len(P) + 1)  # Customer numbers

# Calculate ln(P)
ln_P = np.log(P)

# Invert ln(P) - using 1/ln(P)
inverted_ln_P = 1 / ln_P

# Alternative: if you want -ln(P) instead, uncomment the line below
# inverted_ln_P = -ln_P

# Create the plot
plt.figure(figsize=(10, 8))
plt.plot(inverted_ln_P, customer_numbers, 'o-', linewidth=2, markersize=6)
plt.xlabel('1/ln(P)', fontsize=12)
plt.ylabel('Customer Number', fontsize=12)
plt.title('Customer Number vs Inverted ln(P)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the plot
plt.savefig('inverted_lnp_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'inverted_lnp_plot.png'")

# Display the plot
plt.show()

# If you have data in a CSV file, uncomment and modify the following:
# df = pd.read_csv('your_data.csv')
# P = df['P'].values  # Replace 'P' with your price column name
# customer_numbers = df['customer_number'].values  # Replace with your customer number column
# ln_P = np.log(P)
# inverted_ln_P = 1 / ln_P

