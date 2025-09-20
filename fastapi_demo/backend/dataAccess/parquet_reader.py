from pathlib import Path
import polars as pl
from typing import List, Optional, Dict, Any, Iterator
from dataAccess.interface_parquet_reader import IParquetReader

class ParquetFlatReader(IParquetReader):
    """
    Lettura ottimizzata di parquet forecasts:
    - Join dei file main + HDI all'avvio.
    - Tutte le query successive filtrano il DataFrame in memoria.
    - Streaming dei record via generator.
    """

    BASE_COLS = ["priogrid_id", "month_id", "country_id", "lat", "lon", "row", "col"]


    # Colonne previste nei valori
    METRIC_COLS = [
        "MAP",
        "HDI_50_lower", "HDI_50_upper",
        "HDI_90_lower", "HDI_90_upper",
        "HDI_99_lower", "HDI_99_upper",
        "prob_threshold_1", "prob_threshold_2", "prob_threshold_3",
        "prob_threshold_4", "prob_threshold_5", "prob_threshold_6"
    ]

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        df_main = pl.read_parquet(self.base_path / "preds_001.parquet")
        df_hdi = pl.read_parquet(self.base_path / "preds_001_90_hdi.parquet")
        self.df = df_main.join(df_hdi, on=["month_id", "priogrid_id"], how="left")


    def query(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Generator che restituisce record filtrati, con eventuale subset di metriche.
        Streaming riga per riga per performance.
        Calcola MAP come media delle tre liste di previsioni.
        """
        df = self.df

        # Filtri
        if month_ids:
            df = df.filter(pl.col("month_id").is_in(month_ids))
        if priogrid_ids:
            df = df.filter(pl.col("priogrid_id").is_in(priogrid_ids))
        if country_ids:
            df = df.filter(pl.col("country_id").is_in(country_ids))

        # Determina metriche da restituire
        metric_cols = metrics if metrics else self.METRIC_COLS
        metric_cols = [c for c in metric_cols if c in self.METRIC_COLS]

        # Streaming riga per riga
        for row in df.iter_rows(named=True):
            # Calcola MAP come media di pred_ln_*_best
            pred_lists = []
            for key in ["pred_ln_sb_best", "pred_ln_ns_best", "pred_ln_os_best"]:
                lst = row.get(key)
                if lst:
                    pred_lists.extend(lst)
            MAP = float(sum(pred_lists) / len(pred_lists)) if pred_lists else None

            # Costruzione dizionario valori
            values_dict = {
                "MAP": MAP,
                "HDI_50_lower": row.get("pred_ln_sb_best_hdi_lower"),
                "HDI_50_upper": row.get("pred_ln_sb_best_hdi_upper"),
                "HDI_90_lower": row.get("pred_ln_ns_best_hdi_lower"),
                "HDI_90_upper": row.get("pred_ln_ns_best_hdi_upper"),
                "HDI_99_lower": row.get("pred_ln_os_best_hdi_lower"),
                "HDI_99_upper": row.get("pred_ln_os_best_hdi_upper"),
                "prob_threshold_1": row.get("pred_ln_sb_prob_hdi_lower"),
                "prob_threshold_2": row.get("pred_ln_sb_prob_hdi_upper"),
                "prob_threshold_3": row.get("pred_ln_ns_prob_hdi_lower"),
                "prob_threshold_4": row.get("pred_ln_ns_prob_hdi_upper"),
                "prob_threshold_5": row.get("pred_ln_os_prob_hdi_lower"),
                "prob_threshold_6": row.get("pred_ln_os_prob_hdi_upper"),
            }

            # Filtra solo metriche richieste
            values_dict = {k: v for k, v in values_dict.items() if k in metric_cols}

            # Costruisci record finale
            cell_record = {
                "priogrid_id": row["priogrid_id"],
                "lat": row.get("lat"),
                "lon": row.get("lon"),
                "country_id": row.get("country_id"),
                "month_id": row["month_id"],
                "row": row.get("row"),
                "col": row.get("col"),
                "values": values_dict
            }

            yield cell_record


    def list_months(self) -> List[int]:
        return sorted(self.df.select("month_id").unique().to_series().to_list())

    def list_priogrid_ids(self) -> List[int]:
        return sorted(self.df.select("priogrid_id").unique().to_series().to_list())

    def list_country_ids(self) -> List[int]:
        return sorted(self.df.select("country_id").unique().to_series().to_list())
