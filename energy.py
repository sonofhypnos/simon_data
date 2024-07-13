import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm

# Load the data
data = pd.read_csv("Simon Data - Tabellenblatt1.csv", parse_dates=["Date"])

# Display the first few rows and data info
print(data.head())
print(data.info())

# Remove the first row which contains column names
data = data.iloc[1:].reset_index(drop=True)

# Convert 'Rest day' to numeric, replacing non-numeric values with NaN
data["Rest day"] = pd.to_numeric(data["Rest day"], errors="coerce")

# Fill NaN values in 'Rest day' with 0
data["Rest day"] = data["Rest day"].fillna(0)

# Calculate days since rest
data["Days since rest"] = (data["Rest day"] == 0).cumsum()

# Identify energy columns
energy_columns = [
    col
    for col in data.columns
    if col.startswith("Session") and pd.api.types.is_numeric_dtype(data[col])
]

# Calculate average energy for available sessions
data["Avg_Energy"] = data[energy_columns].mean(axis=1)

# Convert Date to datetime
data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

# Filter data to start from the first day with energizedness data
first_energy_date = data.loc[data["Avg_Energy"].notna(), "Date"].min()
data = data[data["Date"] >= first_energy_date].copy()

# Bayesian model
with pm.Model() as model:
    # Priors
    alpha = pm.Normal("alpha", mu=80, sd=10)
    beta = pm.HalfNormal("beta", sd=10)
    sigma = pm.HalfNormal("sigma", sd=10)

    # Expected energy level
    mu = alpha - beta * (1 - pm.math.exp(-data["Days since rest"] / 3))

    # Likelihood
    y_obs = pm.Normal("y_obs", mu=mu, sd=sigma, observed=data["Avg_Energy"])

    # Inference
    trace = pm.sample(2000, return_inferencedata=True)

# Plotting
plt.figure(figsize=(12, 10))

# Plot 1: Energy Levels vs Days Since Rest
plt.subplot(2, 1, 1)
x_plot = np.linspace(0, data["Days since rest"].max(), 100)
y_post = trace.posterior["alpha"].values[:, None] - trace.posterior["beta"].values[
    :, None
] * (1 - np.exp(-x_plot / 3))

plt.plot(x_plot, y_post.mean(axis=(0, 1)), color="blue", label="Posterior mean")
plt.fill_between(
    x_plot,
    np.percentile(y_post, 2.5, axis=(0, 1)),
    np.percentile(y_post, 97.5, axis=(0, 1)),
    color="blue",
    alpha=0.3,
    label="95% CI",
)
plt.scatter(
    data["Days since rest"],
    data["Avg_Energy"],
    color="red",
    alpha=0.5,
    label="Observed data",
)
plt.xlabel("Days since last rest day")
plt.ylabel("Average Energizedness")
plt.title("Energy Levels vs Days Since Rest")
plt.legend()

# Plot 2: Posterior Distributions
plt.subplot(2, 1, 2)
pm.plot_posterior(trace, var_names=["alpha", "beta", "sigma"])
plt.title("Posterior Distributions")

plt.tight_layout()
plt.show()

# Print summary statistics
print(pm.summary(trace, var_names=["alpha", "beta", "sigma"]))
