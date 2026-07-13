import pandas as pd

from src.profiling import get_column_info, get_duplicate_count, get_shape


def test_get_shape_returns_row_and_column_counts():
    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [5, 6, 7, 8], "c": [9, 10, 11, 12]})
    assert get_shape(df) == (4, 3)


def test_get_column_info_reports_correct_names_and_dtypes():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "score": [1.5, 2.5, 3.5],
        "name": ["a", "b", "c"],
    })
    info = get_column_info(df)
    assert info == [
        {"column": "id", "dtype": "int64", "missing_count": 0},
        {"column": "score", "dtype": "float64", "missing_count": 0},
        {"column": "name", "dtype": "object", "missing_count": 0},
    ]


def test_get_column_info_counts_missing_values_including_zero_missing_column():
    df = pd.DataFrame({
        "a": [1.0, None, 3.0, None],
        "b": ["x", "y", "z", "w"],
    })
    info = get_column_info(df)
    missing_by_col = {row["column"]: row["missing_count"] for row in info}
    assert missing_by_col == {"a": 2, "b": 0}


def test_get_duplicate_count_with_duplicates():
    df = pd.DataFrame({
        "a": [1, 2, 1, 3],
        "b": ["x", "y", "x", "z"],
    })
    assert get_duplicate_count(df) == 1


def test_get_duplicate_count_no_duplicates():
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": ["x", "y", "z"],
    })
    assert get_duplicate_count(df) == 0
