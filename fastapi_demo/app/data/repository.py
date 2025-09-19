# fastapi_demo/app/data/repository.py
import pandas as pd
from typing import List, Optional

PRED_PATH = "app/data/preds_001.parquet"
HDI_PATH = "app/data/preds_001_90_hdi.parquet"

# load parquet files
df_preds = pd.read_parquet(PRED_PATH)
df_hdi = pd.read_parquet(HDI_PATH)

# Merge on the assumption that indices are the same
DATA = pd.concat([df_preds, df_hdi], axis=1)

# load CSV files
CSV_PGM_PATH = "app/data/fatalities002_2025_07_t01_pgm.csv"
CSV_CM_PATH = "app/data/fatalities002_2025_07_t01_cm.csv"

df_csv_pgm = pd.read_csv(CSV_PGM_PATH)
df_csv_cm = pd.read_csv(CSV_CM_PATH)


def get_available_countries() -> List[str]:
    return sorted(DATA["country_id"].unique().tolist())


def get_available_cells() -> List[dict]:
    return DATA[["row", "col", "country_id", "lat", "lon"]].drop_duplicates().to_dict(orient="records")


def get_available_metrics() -> List[str]:
    return [c for c in DATA.columns if c.startswith("pred_")]

def get_available_months() -> List[str]:
    """Return unique months across PGM and CM CSV datasets in YYYY-MM format."""
    months = set()

    # From CM CSV: Combine year and month into YYYY-MM format
    if {"year", "month"}.issubset(df_csv_cm.columns):
        months.update(
            (df_csv_cm["year"].astype(str) + "-" + df_csv_cm["month"].astype(str).str.zfill(2)).tolist()
        )

    # From PGM CSV: Convert month_id to YYYY-MM by referencing CM CSV
    if "month_id" in df_csv_pgm.columns:
        month_map = df_csv_cm.set_index("month_id")[["year", "month"]].drop_duplicates()
        for mid in df_csv_pgm["month_id"].unique():
            if mid in month_map.index:
                y, m = month_map.loc[mid]
                months.add(f"{y}-{str(m).zfill(2)}")

    return sorted(months)

def filter_results(
    df: pd.DataFrame,
    months: Optional[List[str]] = None,   # Use months if available in parquet
    metrics: Optional[List[str]] = None
):
    # Ignore months filter if 'month' column is not in the DataFrame (currently not available in data)）
    if months and "month" in df.columns:
        df = df[df["month"].isin(months)]

    if metrics:
        base_cols = ["row", "col", "country_id", "lat", "lon"]
        df = df[base_cols + [m for m in metrics if m in df.columns]]

    return df.to_dict(orient="records")


def get_forecast_by_cell(
    rows: Optional[List[int]] = None,
    cols: Optional[List[int]] = None,
    metrics: Optional[List[str]] = None
):
    df = DATA
    if rows and cols:
        df = df[df["row"].isin(rows) & df["col"].isin(cols)]
    return filter_results(df, metrics=metrics)


def get_forecast_by_country(
    country_ids: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None
):
    df = DATA
    if country_ids:
        df = df[df["country_id"].isin(country_ids)]
    return filter_results(df, metrics=metrics)
