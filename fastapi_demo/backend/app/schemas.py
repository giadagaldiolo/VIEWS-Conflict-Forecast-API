# schemas.py

# Forecast schema definition for flat parquet files
FORECAST_SCHEMA = {
    # Index/ID columns
    "priogrid_id": "int64",
    "month_id": "int64",
    "country_id": "int64",
    "row": "int64",
    "col": "int64",

    # Location metadata
    "lat": "float32",
    "lon": "float32",

    # Forecast values (MAP + HDIs + threshold probs if present)
    "pred_ln_sb_best": "float32",
    "pred_ln_sb_best_hdi_lower": "float32",
    "pred_ln_sb_best_hdi_upper": "float32",

    "pred_ln_ns_best": "float32",
    "pred_ln_ns_best_hdi_lower": "float32",
    "pred_ln_ns_best_hdi_upper": "float32",

    "pred_ln_os_best": "float32",
    "pred_ln_os_best_hdi_lower": "float32",
    "pred_ln_os_best_hdi_upper": "float32",

    # threshold probability columns here
    "pred_ln_sb_prob_hdi_lower": "float32",
    "pred_ln_sb_prob_hdi_upper": "float32",
    "pred_ln_ns_prob_hdi_lower": "float32",
    "pred_ln_ns_prob_hdi_upper": "float32",
    "pred_ln_os_prob_hdi_lower": "float32",
    "pred_ln_os_prob_hdi_upper": "float32"

}
