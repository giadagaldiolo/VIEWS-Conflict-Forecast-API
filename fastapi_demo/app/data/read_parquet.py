import pandas as pd

df = pd.read_parquet('preds_001.parquet', engine='pyarrow')

print(df.head())

df = pd.read_parquet('preds_001_90_hdi.parquet', engine='pyarrow')

print(df.head())
