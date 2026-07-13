# Spec 01: CSV Upload and Basic Dataset Profiling

## Problem Statement

Data scientists starting work on a new dataset spend time on repetitive first steps: loading the file, checking its shape, inspecting column types, and spotting obvious quality issues like missing values and duplicate rows. InsightLite should automate this first look so users can get oriented in seconds instead of writing the same boilerplate pandas code every time.

## User Story

As a data scientist, I want to upload a CSV file to InsightLite and immediately see a profile of the dataset (preview, shape, column types, missing values, duplicates), so that I can quickly assess data quality before doing any deeper analysis.

## Scope

- CSV file upload via a Streamlit file uploader widget.
- Preview of the first 5 rows of the uploaded dataset.
- Total row count and column count.
- Column names and their data types.
- Missing value count per column.
- Duplicate row count for the dataset.
- Reusable profiling logic extracted into `src/profiling.py`, kept separate from UI code.

## Out of Scope

- Charts or other visualizations.
- Database storage or persistence of uploaded files.
- Authentication or access control.
- ML model training.
- Advanced data cleaning or transformation (e.g. imputation, deduplication actions).

## Acceptance Criteria

- [ ] User can upload a `.csv` file through the Streamlit UI.
- [ ] After upload, the app displays a table preview of the first 5 rows.
- [ ] The app displays the total number of rows and number of columns.
- [ ] The app displays each column name alongside its data type.
- [ ] The app displays the count of missing values per column.
- [ ] The app displays the total number of duplicate rows in the dataset.
- [ ] If no file is uploaded, the app shows the existing landing page (no errors).
- [ ] All profiling computations (shape, dtypes, missing values, duplicates) live in `src/profiling.py` as plain functions that take a DataFrame and return results — not embedded in `app.py`.
- [ ] `app.py` only handles the file uploader widget and rendering the results returned by `src/profiling.py`.

## Implementation Notes

- Use `st.file_uploader` restricted to `.csv` files, and `pandas.read_csv` to load the upload into a DataFrame.
- `src/profiling.py` should expose small, focused functions, e.g.:
  - `get_shape(df)` → (row_count, column_count)
  - `get_column_info(df)` → column name, dtype (and missing count) per column
  - `get_duplicate_count(df)` → count of duplicate rows
- Keep functions simple and directly built on pandas (`df.shape`, `df.dtypes`, `df.isna().sum()`, `df.duplicated().sum()`) — no custom abstractions beyond what's needed.
- `app.py` stays focused on orchestration: read the upload, call into `src/profiling.py`, render results with `st.write`/`st.dataframe`/`st.table`.

## Testing Notes

- Add pytest tests for the functions in `src/profiling.py` under `tests/`.
- Use small, hand-constructed DataFrames (not real files) to test each function independently.
- Cover: correct row/column counts, correct dtypes reported, correct missing-value counts (including a column with zero missing values), correct duplicate-row count (including a dataset with no duplicates).
- No UI/Streamlit testing required for this spec — keep tests focused on the profiling logic.
