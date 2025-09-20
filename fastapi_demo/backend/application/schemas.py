from pydantic import BaseModel
from typing import List, Optional

class ForecastValues(BaseModel):
    MAP: Optional[float] = None
    HDI_50_lower: Optional[float] = None
    HDI_50_upper: Optional[float] = None
    HDI_90_lower: Optional[float] = None
    HDI_90_upper: Optional[float] = None
    HDI_99_lower: Optional[float] = None
    HDI_99_upper: Optional[float] = None
    prob_threshold_1: Optional[float] = None
    prob_threshold_2: Optional[float] = None
    prob_threshold_3: Optional[float] = None
    prob_threshold_4: Optional[float] = None
    prob_threshold_5: Optional[float] = None
    prob_threshold_6: Optional[float] = None

class ForecastCell(BaseModel):
    priogrid_id: int
    month_id: int
    country_id: Optional[int]
    lat: Optional[float]
    lon: Optional[float]
    values: ForecastValues