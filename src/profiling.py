import pandas as pd


def get_shape(df: pd.DataFrame) -> tuple[int, int]:
    """Return (row_count, column_count)."""
    return df.shape


def get_column_info(df: pd.DataFrame) -> list[dict]:
    """Return one dict per column: {"column", "dtype", "missing_count"}."""
    return [
        {
            "column": col,
            "dtype": str(df[col].dtype),
            "missing_count": int(df[col].isna().sum()),
        }
        for col in df.columns
    ]


def get_duplicate_count(df: pd.DataFrame) -> int:
    """Return count of duplicate rows (pandas default keep='first')."""
    return int(df.duplicated().sum())
