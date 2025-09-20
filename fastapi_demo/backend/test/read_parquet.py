import pyarrow.parquet as pq
from pathlib import Path

data_dir = Path(__file__).parent.parent / "app" / "data"

print("-----------------preds_001.parquet-----------------")
schema_001 = pq.read_schema(data_dir / "preds_001.parquet")
print(schema_001)

print("-----------------preds_001_90_hdi.parquet-----------------")
schema_001_90_hdi = pq.read_schema(data_dir / "preds_001_90_hdi.parquet")
print(schema_001_90_hdi)