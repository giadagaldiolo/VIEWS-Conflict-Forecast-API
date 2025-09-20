// types.ts
export interface ForecastData {
  priogrid_id: string;
  country_id: string;
  month_id: string;
  lat: number;
  lon: number;
  metrics: Record<string, number | null>;
}
