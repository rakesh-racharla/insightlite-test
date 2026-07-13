# Spec: Basic Charts

## Overview

CSV upload and profiling (shape, column types, missing values, duplicates) already lets users assess data quality, but InsightLite still gives no visual sense of the data itself. This feature adds simple, automatic charts — a histogram for numeric columns and a bar chart of value counts for categorical columns — so users can spot distributions and obvious patterns right after upload, without writing any plotting code themselves.

## Depends on

CSV Upload and Basic Dataset Profiling (`.claude/specs/01-csv-profiling.md`) must be complete, since this feature builds on the already-uploaded DataFrame and existing profiling output.

## User experience

After a CSV is uploaded and the existing profiling sections are shown, add a new "Charts" section below them.

- Let the user pick a column to visualize via a `st.selectbox` (default to the first column).
- If the selected column is numeric, show a histogram of its values.
- If the selected column is categorical (object/bool/category dtype), show a bar chart of the top value counts (e.g. top 10 categories).
- If the column is entirely missing (all `NaN`) or has no data to plot, show a friendly message instead of an empty or broken chart (e.g. "No data available to chart for this column.").
- Keep everything on the same page — no tabs, no new pages.

## Data science behaviour

- Add a function to detect whether a column should be treated as numeric or categorical for charting purposes (based on pandas dtype).
- Add a function to compute histogram-ready data for a numeric column, dropping missing values before plotting (missing values are not imputed or counted as a category).
- Add a function to compute value counts for a categorical column, dropping missing values, and limit to the top N categories (e.g. 10) to keep the chart readable.
- Do not mutate the original uploaded DataFrame — all charting functions should operate on copies or read-only views as needed.
- Make the "numeric vs categorical" classification rule explicit and simple (e.g. `pandas.api.types.is_numeric_dtype`).

## Files to change

- `app.py` — add the column selector and the "Charts" section, calling into the new charting logic and rendering the result with `st.pyplot`.
- `requirements.txt` — add `matplotlib`.

## Files to create

- `src/charts.py` — reusable charting/data-prep logic (column type detection, histogram data prep, value-count computation, and the matplotlib figure-building functions).
- `tests/test_charts.py` — pytest tests for the logic in `src/charts.py`.

## New dependencies

- `matplotlib` — required for rendering simple charts (histogram and bar chart) as specified in `CLAUDE.md`.

## Out of scope

- Interactive/zoomable charts or any charting library beyond matplotlib.
- Scatter plots, correlation matrices, or multi-column/multivariate charts.
- Chart export or download functionality.
- Customization of chart appearance (colors, themes, titles) beyond simple readable defaults.
- Automatic chart recommendations across all columns at once (user selects one column at a time).
- Any database storage, authentication, or ML modelling.

## Rules for implementation

- Keep the implementation simple and readable.
- Keep `app.py` focused on Streamlit UI and orchestration.
- Put reusable data logic in `src/`.
- Do not add databases unless explicitly requested.
- Do not add authentication unless explicitly requested.
- Do not add complex frontend frameworks.
- Do not add heavy ML models unless explicitly requested.
- Use pandas for basic data manipulation.
- Use matplotlib for simple charts if charts are required.
- Handle missing values safely.
- Do not mutate the original dataframe unexpectedly.
- Make assumptions explicit.
- Follow `CLAUDE.md`.

## Definition of done

- [ ] User can upload a CSV and see a new "Charts" section below the existing profiling output.
- [ ] User can select a column from a dropdown to visualize.
- [ ] Selecting a numeric column displays a histogram of its values.
- [ ] Selecting a categorical column displays a bar chart of its top value counts.
- [ ] A column with all missing values shows a friendly message instead of an error or blank chart.
- [ ] Charting logic (type detection, histogram data prep, value-count computation) lives in `src/charts.py`, not in `app.py`.
- [ ] `app.py` only handles the column selector widget and rendering the chart returned by `src/charts.py`.
- [ ] The original uploaded DataFrame is never mutated by the charting logic.
- [ ] `matplotlib` is added to `requirements.txt`.
- [ ] `tests/test_charts.py` covers: numeric vs categorical detection, histogram data prep with missing values dropped, and value-count computation with missing values dropped and top-N limiting.
- [ ] `pytest` passes with no failures.
- [ ] Running `streamlit run app.py` and uploading a CSV shows no errors in the Charts section for both numeric and categorical column selections.
