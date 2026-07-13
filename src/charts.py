import matplotlib.figure
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_numeric_dtype


def is_numeric_column(df: pd.DataFrame, column: str) -> bool:
    """Return True if the column should be treated as numeric for charting."""
    return is_numeric_dtype(df[column])


def get_histogram_data(df: pd.DataFrame, column: str) -> pd.Series:
    """Return the column's non-null values, ready to histogram."""
    return df[column].dropna()


def build_histogram_figure(values: pd.Series, column: str) -> matplotlib.figure.Figure:
    """Build a matplotlib Figure containing a histogram of values."""
    fig, ax = plt.subplots()
    ax.hist(values)
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    ax.set_title(f"Distribution of {column}")
    return fig
