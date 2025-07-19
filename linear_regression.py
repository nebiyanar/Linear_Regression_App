# linear_Regression.py

import pandas as pd
import numpy as np

def linear_regr_model(csv_name: str, df: pd.DataFrame = None, plot_ax=None, r: bool = False,
                      xlabel: str = "x-axis", ylabel: str = "y-axis"):
    if df is None:
        try:
            df = pd.read_csv(csv_name)
        except Exception:
            raise KeyError("Wrong File Name or Wrong Path")

    x_arr = np.array(df['x'])
    y_arr = np.array(df['y'])
    length = len(x_arr)

    x_mean = np.mean(x_arr)
    y_mean = np.mean(y_arr)

    # Slope (m)
    numerator = sum((x * y) for x, y in zip(x_arr, y_arr)) - length * x_mean * y_mean
    denominator = sum(x ** 2 for x in x_arr) - length * x_mean ** 2
    slope = numerator / denominator

    # Intercept (b)
    b = y_mean - slope * x_mean

    # Predict values
    Y = slope * x_arr + b
    df['predicted_values'] = Y

    # Optional r and R^2 calculation
    if r:
        r_numerator = sum((x - x_mean)*(y - y_mean) for x, y in zip(x_arr, y_arr))
        r_denominator = np.sqrt(
            sum((x - x_mean) ** 2 for x in x_arr) *
            sum((y - y_mean) ** 2 for y in y_arr)
        )
        correlation_coeff = r_numerator / r_denominator
        determination_coeff = correlation_coeff ** 2
        print(f"r (correlation): {correlation_coeff:.4f}")
        print(f"R² (determination): {determination_coeff:.4f}")

    # Optional plot
    if plot_ax:
        plot_ax.clear()
        plot_ax.plot(x_arr, y_arr, label="Original Data", color="blue", lw=2, marker='o')
        plot_ax.plot(x_arr, Y, label="Regression Line", color="red", lw=2)
        plot_ax.set_xlabel(xlabel)
        plot_ax.set_ylabel(ylabel)
        plot_ax.set_title("Linear Regression")
        plot_ax.grid(True)
        plot_ax.legend()
    return df, correlation_coeff, determination_coeff

