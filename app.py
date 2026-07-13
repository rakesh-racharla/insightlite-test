import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.charts import build_histogram_figure, get_histogram_data, is_numeric_column
from src.profiling import get_column_info, get_duplicate_count, get_shape

st.set_page_config(page_title="InsightLite", page_icon="📊", layout="centered")


def show_quality_message(count: int, issue_label: str, clean_label: str) -> None:
    """Show a warning if count > 0, otherwise a success message."""
    if count > 0:
        st.warning(f"⚠️ {issue_label.format(count=f'{count:,}')}")
    else:
        st.success(f"✅ {clean_label}")


st.title("📊 InsightLite")

with st.sidebar:
    st.header("About InsightLite")
    st.write(
        "InsightLite is a quick, no-setup way to sanity-check a CSV before "
        "you dig in — see its shape, spot missing or duplicate data, and "
        "preview how one numeric column is distributed."
    )

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type="csv",
    help="Upload a CSV file from your computer. Only .csv files are supported.",
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview")
    st.dataframe(df.head())

    st.subheader("At a glance")

    row_count, column_count = get_shape(df)
    column_info = get_column_info(df)
    missing_total = sum(col["missing_count"] for col in column_info)
    duplicate_count = get_duplicate_count(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{row_count:,}")
    col2.metric("Columns", f"{column_count:,}")
    col3.metric("Missing values", f"{missing_total:,}")
    col4.metric("Duplicate rows", f"{duplicate_count:,}")

    show_quality_message(
        missing_total,
        issue_label="Found {count} missing value(s). Consider reviewing before analysis.",
        clean_label="No missing values found.",
    )
    show_quality_message(
        duplicate_count,
        issue_label="Found {count} duplicate row(s). Consider removing them before analysis.",
        clean_label="No duplicate rows found.",
    )

    st.subheader("Columns")
    st.dataframe(pd.DataFrame(column_info))

    st.subheader("Charts")

    numeric_columns = [col for col in df.columns if is_numeric_column(df, col)]

    if not numeric_columns:
        st.write("No numeric columns available to chart.")
    else:
        selected_column = st.selectbox(
            "Choose a numeric column to visualize",
            numeric_columns,
            help="Only numeric columns can be charted as a histogram.",
        )
        values = get_histogram_data(df, selected_column)

        if values.empty:
            st.write("No data available to chart for this column.")
        else:
            fig = build_histogram_figure(values, selected_column)
            st.pyplot(fig)
            plt.close(fig)
            st.caption(
                "This histogram shows how values in this column are distributed — "
                "tall bars mean more common values, gaps or outliers stand out visually."
            )

else:
    st.info(
        "📊 A lightweight data profiling assistant for data scientists. "
        "Upload a CSV to preview your data, check its quality, and explore "
        "a quick chart — no setup required."
    )

    st.divider()

    st.subheader("How it works")

    steps = [
        ("📤", "Load data", "Bring in a dataset to get started."),
        ("📋", "Review quality", "Check for missing values and duplicates."),
        ("📊", "Explore insights", "Understand trends and patterns at a glance."),
    ]

    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, steps):
        with col:
            st.subheader(f"{icon} {title}")
            st.caption(desc)
