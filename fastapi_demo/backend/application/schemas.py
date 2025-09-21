from pydantic import BaseModel
from typing import List, Optional

class ForecastValues(BaseModel):
    """
    Forecast statistical values and probability thresholds.

    Contains point estimates and uncertainty intervals for forecasts,
    along with probabilities of exceeding predefined thresholds.

    Args:
        MAP (Optional[float]): Mean Absolute Prediction or central forecast value.
        HDI_50_lower (Optional[float]): Lower bound of 50% Highest Density Interval.
        HDI_50_upper (Optional[float]): Upper bound of 50% Highest Density Interval.
        HDI_90_lower (Optional[float]): Lower bound of 90% Highest Density Interval.
        HDI_90_upper (Optional[float]): Upper bound of 90% Highest Density Interval.
        HDI_99_lower (Optional[float]): Lower bound of 99% Highest Density Interval.
        HDI_99_upper (Optional[float]): Upper bound of 99% Highest Density Interval.
        prob_threshold_1 (Optional[float]): Probability of exceeding threshold 1.
        prob_threshold_2 (Optional[float]): Probability of exceeding threshold 2.
        prob_threshold_3 (Optional[float]): Probability of exceeding threshold 3.
        prob_threshold_4 (Optional[float]): Probability of exceeding threshold 4.
        prob_threshold_5 (Optional[float]): Probability of exceeding threshold 5.
        prob_threshold_6 (Optional[float]): Probability of exceeding threshold 6.
    """
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
    """
    Represents forecast data for a specific spatial-temporal cell.

    Contains identifiers for location and time, optional geocoordinates,
    and associated forecast values.

    Args:
        priogrid_id (int): Unique identifier for the spatial grid cell.
        month_id (int): Identifier for the forecast month (e.g., 202201 for Jan 2022).
        country_id (Optional[int]): Optional country identifier.
        lat (Optional[float]): Latitude in decimal degrees (WGS84).
        lon (Optional[float]): Longitude in decimal degrees (WGS84).
        values (ForecastValues): Forecast values for the cell.
    """
    priogrid_id: int
    month_id: int
    country_id: Optional[int]
    lat: Optional[float]
    lon: Optional[float]
    values: ForecastValues