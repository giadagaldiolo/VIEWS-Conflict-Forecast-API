import pyarrow.parquet as pq
import pandas as pd

schema_001 = pq.read_schema('preds_001.parquet')
print(schema_001)

schema_001_90_hdi = pq.read_schema('preds_001_90_hdi.parquet')
print(schema_001_90_hdi)
