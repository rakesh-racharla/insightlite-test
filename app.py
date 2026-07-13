import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.charts import build_histogram_figure, get_histogram_data, is_numeric_column
from src.profiling import get_column_info, get_duplicate_count, get_shape

st.set_page_config(page_title="InsightLite", page_icon="📊", layout="centered")

st.title("📊 InsightLite")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview")
    st.dataframe(df.head())

    row_count, column_count = get_shape(df)
    st.write(f"**Rows:** {row_count} &nbsp; **Columns:** {column_count}")

    st.subheader("Columns")
    st.dataframe(pd.DataFrame(get_column_info(df)))

    duplicate_count = get_duplicate_count(df)
    st.write(f"**Duplicate rows:** {duplicate_count}")

    st.subheader("Charts")

    numeric_columns = [col for col in df.columns if is_numeric_column(df, col)]

    if not numeric_columns:
        st.write("No numeric columns available to chart.")
    else:
        selected_column = st.selectbox("Choose a numeric column to visualize", numeric_columns)
        values = get_histogram_data(df, selected_column)

        if values.empty:
            st.write("No data available to chart for this column.")
        else:
            fig = build_histogram_figure(values, selected_column)
            st.pyplot(fig)
            plt.close(fig)

else:
    st.write("A lightweight data profiling assistant for data scientists.")

    st.divider()

    st.subheader("What is InsightLite?")
    st.write(
        "InsightLite helps you quickly understand a new dataset. "
        "Load your data, review its quality, and explore key insights "
        "in just a few steps — no setup required."
    )

    st.subheader("How it works")

    st.markdown(
        """
        <style>
        .step-card {
            background-color: #ffffff;
            border: 1px solid #eaeaea;
            border-radius: 12px;
            padding: 20px;
            height: 100%;
        }
        .step-icon { font-size: 22px; margin-bottom: 8px; }
        .step-title { font-weight: 600; font-size: 17px; margin-bottom: 6px; }
        .step-desc { color: #6b7280; font-size: 14px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    steps = [
        ("📤", "Load data", "Bring in a dataset to get started."),
        ("📋", "Review quality", "Check for missing values and inconsistencies."),
        ("📊", "Explore insights", "Understand trends and patterns at a glance."),
    ]

    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(
                f"""
                <div class="step-card">
                    <div class="step-icon">{icon}</div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
