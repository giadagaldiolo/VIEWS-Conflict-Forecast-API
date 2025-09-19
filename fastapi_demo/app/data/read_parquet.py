import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)  

df = pd.read_parquet('preds_001.parquet', engine='pyarrow')
print(df.head())

df = pd.read_parquet('preds_001_90_hdi.parquet', engine='pyarrow')
print(df.head())

df = pd.read_csv('fatalities002_2025_07_t01_pgm.csv', engine='pyarrow')
print(df.head())

df = pd.read_csv('fatalities002_2025_07_t01_cm.csv', engine='pyarrow')
print(df.head())