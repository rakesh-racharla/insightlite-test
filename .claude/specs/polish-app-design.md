# Spec: Polish App Design

## Overview

CSV profiling and basic charting are functionally complete, but the app currently presents results as raw text, tables, and an inline `<style>` block rather than a clear, guided experience. This feature polishes the existing Streamlit UI — layout, empty state, metric presentation, data-quality messaging, and chart labeling — so InsightLite feels calm, obvious, and ready to show a non-technical user, without changing any underlying data logic.

## Depends on

CSV Upload and Basic Dataset Profiling (`.claude/specs/01-csv-profiling.md`) and Basic Charts (`.claude/specs/basic-charts.md`) must be complete, since this feature only restyles their existing output.

## User experience

- Keep the current single-page, top-to-bottom flow: title/intro → upload → preview → quality checks → charts. No new pages or tabs.
- Replace the raw-text row/column/duplicate summary with `st.metric()` cards in `st.columns()` (e.g. Rows, Columns, Missing values, Duplicate rows).
- Turn the duplicate-row and missing-value counts into plain-language `st.warning()` (when issues exist) or `st.success()` (when clean) messages instead of a bare `st.write()` line.
- Keep the empty-state landing content (the "How it works" steps), but simplify it to use standard Streamlit components (`st.info`, `st.columns` with `st.subheader`/`st.caption`) instead of the custom injected `<style>`/HTML card block.
- Give the histogram a clear one-line `st.caption()` underneath explaining what to look for.
- Add a short, lightweight sidebar with a one-paragraph "About InsightLite" description, so the empty state and sidebar aren't duplicating the same explanation verbatim.
- Add `help=` text to the file uploader and column selector so their purpose is clear at a glance.

## Data science behaviour

No specific data science behaviour. This feature only changes how existing results (from `src/profiling.py` and `src/charts.py`) are presented — the computations themselves are untouched.

## Files to change

- `app.py` — restructure presentation: metric cards, warning/success messaging, simplified empty state, chart caption, sidebar, `help=` text on widgets. No changes to `src/profiling.py` or `src/charts.py` logic.

## Files to create

No new files expected. (If `app.py` grows unwieldy, a small presentation helper may be added inside `app.py` itself — do not split into new modules for this feature.)

## New dependencies

No new dependencies.

## Out of scope

- Any change to profiling or charting logic in `src/`.
- Adding the categorical bar-chart selection path if it doesn't already work end-to-end (flag separately if found broken; don't fix silently under a "polish" spec).
- Custom CSS/HTML beyond removing the existing inline `<style>` block — no new injected styling.
- Authentication, databases, multi-page navigation, or new ML features.
- Any new chart types, export functionality, or theming system.

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
- Use only Streamlit's built-in components; do not introduce custom HTML/CSS beyond what already exists unless explicitly asked.
- Preserve all existing functionality exactly — this is a presentation-only change.
- Follow `CLAUDE.md`.

## Definition of done

- [ ] Row count, column count, missing-value count, and duplicate-row count are shown via `st.metric()` cards in `st.columns()`.
- [ ] Missing values and duplicate rows are surfaced via `st.warning()` when present, or `st.success()` when clean, in plain language.
- [ ] The empty-state landing page no longer uses a custom injected `<style>` block; it uses standard Streamlit components and still explains what the app does and how it works.
- [ ] The histogram chart has a one-line `st.caption()` explaining what to look for.
- [ ] The sidebar shows a short "About InsightLite" description.
- [ ] `st.file_uploader` and the column selector have helpful `help=` text.
- [ ] `src/profiling.py` and `src/charts.py` are unchanged.
- [ ] `pytest` passes with no failures.
- [ ] Running `streamlit run app.py` shows the polished empty state, metric cards, quality messaging, and captioned chart with no errors, for both a file with missing/duplicate data and a clean file.
