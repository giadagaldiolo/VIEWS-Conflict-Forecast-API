import pandas as pd

df = pd.read_parquet('preds_001.parquet', engine='pyarrow')

print(df.columns.tolist())
