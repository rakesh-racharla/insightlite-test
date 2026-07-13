import pandas as pd

from src.charts import get_histogram_data, is_numeric_column


def test_is_numeric_column_true_for_int_and_float():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [1.5, 2.5, 3.5]})
    assert is_numeric_column(df, "a") is True
    assert is_numeric_column(df, "b") is True


def test_is_numeric_column_false_for_object_column():
    df = pd.DataFrame({"name": ["x", "y", "z"]})
    assert is_numeric_column(df, "name") is False


def test_get_histogram_data_drops_missing_values():
    df = pd.DataFrame({"score": [1.0, None, 3.0, None, 5.0]})
    values = get_histogram_data(df, "score")
    assert values.tolist() == [1.0, 3.0, 5.0]


def test_get_histogram_data_returns_empty_series_when_column_all_missing():
    df = pd.DataFrame({"score": [None, None, None]})
    values = get_histogram_data(df, "score")
    assert values.empty


def test_get_histogram_data_does_not_mutate_original_dataframe():
    df = pd.DataFrame({"score": [1.0, None, 3.0]})
    original = df.copy()
    get_histogram_data(df, "score")
    pd.testing.assert_frame_equal(df, original)
