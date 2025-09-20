from pydantic import BaseModel
from typing import Optional, List

class ForecastRecord(BaseModel):
    priogrid_id: int
    lat: float
    lon: float
    row: int
    col: int
    country_id: int
    month_id: int

    # 予測値（リスト形式）
    pred_ln_sb_best: Optional[List[float]] = None
    pred_ln_ns_best: Optional[List[float]] = None
    pred_ln_os_best: Optional[List[float]] = None

    # HDI（これは float なのでそのままで OK、必要があれば追加）
    pred_ln_sb_best_hdi_lower: Optional[float] = None
    pred_ln_sb_best_hdi_upper: Optional[float] = None
    pred_ln_ns_best_hdi_lower: Optional[float] = None
    pred_ln_ns_best_hdi_upper: Optional[float] = None
    pred_ln_os_best_hdi_lower: Optional[float] = None
    pred_ln_os_best_hdi_upper: Optional[float] = None
