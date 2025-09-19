# fastapi_demo/app/data/repository.py
import pandas as pd
from typing import List, Optional

PRED_PATH = "app/data/preds_001.parquet"
HDI_PATH = "app/data/preds_001_90_hdi.parquet"

# parquet 読み込み
df_preds = pd.read_parquet(PRED_PATH)
df_hdi = pd.read_parquet(HDI_PATH)

# index が同じ前提で結合
DATA = pd.concat([df_preds, df_hdi], axis=1)


def get_available_countries() -> List[str]:
    return sorted(DATA["country_id"].unique().tolist())


def get_available_cells() -> List[dict]:
    return DATA[["row", "col", "country_id", "lat", "lon"]].drop_duplicates().to_dict(orient="records")


def get_available_metrics() -> List[str]:
    return [c for c in DATA.columns if c.startswith("pred_")]


def filter_results(
    df: pd.DataFrame,
    months: Optional[List[str]] = None,   # parquet に month があれば利用
    metrics: Optional[List[str]] = None
):
    # months が parquet に無い場合は無視（今のデータには month がない）
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
