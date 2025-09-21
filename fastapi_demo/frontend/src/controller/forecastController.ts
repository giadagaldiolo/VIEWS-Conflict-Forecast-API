import { useState, useEffect } from "react";
import { ForecastData } from "../model/forecastModel";

/**
 * Custom hook to manage forecast data fetching and filtering.
 * Handles state for API version (run), level of analysis (loa),
 * type of violence, month, country, priogrid, and metrics filters.
 * Fetches lists of countries, months, and available metrics on mount.
 * Provides a fetchData function to retrieve forecast data based on current filters.
 *
 * @returns {{
 *   run: string,
 *   setRun: React.Dispatch<React.SetStateAction<string>>,
 *   loa: string,
 *   setLoa: React.Dispatch<React.SetStateAction<string>>,
 *   typeOfViolence: string,
 *   setTypeOfViolence: React.Dispatch<React.SetStateAction<string>>,
 *   monthId: string,
 *   setMonthId: React.Dispatch<React.SetStateAction<string>>,
 *   countryId: string,
 *   setCountryId: React.Dispatch<React.SetStateAction<string>>,
 *   priogridId: string,
 *   setPriogridId: React.Dispatch<React.SetStateAction<string>>,
 *   metrics: string,
 *   setMetrics: React.Dispatch<React.SetStateAction<string>>,
 *   countries: {id: number, name: string}[],
 *   months: {id: number, label: string}[],
 *   availableMetrics: string[],
 *   loading: boolean,
 *   error: string | null,
 *   fetchData: () => Promise<ForecastData[] | null>
 * }}
 */

export function useForecastController() {
    // State for API version, level of analysis, and violence type filters
    const [run, setRun] = useState("v1");
    const [loa, setLoa] = useState("standard");
    const [typeOfViolence, setTypeOfViolence] = useState("armed_conflict");

    // Filter state variables for month, country, priogrid, and metrics
    const [monthId, setMonthId] = useState("");
    const [countryId, setCountryId] = useState("");
    const [priogridId, setPriogridId] = useState("");
    const [metrics, setMetrics] = useState("");

    // Lists fetched from the API
    const [countries, setCountries] = useState<{id: number, name: string}[]>([]);
    const [months, setMonths] = useState<{id: number, label: string}[]>([]);
    const [availableMetrics, setAvailableMetrics] = useState<string[]>([]);

    // Loading and error states
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Base API URL from environment variables (fallback to localhost)
    const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

    /**
     * Fetch initial data for countries, months, and available metrics in parallel.
     * Set error state if any fetch fails.
    */
    useEffect(() => {
    setLoading(true);
    Promise.all([
      fetch(`${BASE_URL}/api/countries`).then((res) => res.json()),
      fetch(`${BASE_URL}/api/months`).then((res) => res.json()),
      fetch(`${BASE_URL}/api/metrics`).then((res) => res.json()),
    ])
      .then(([countriesData, monthsData, metricsData]) => {
        setCountries(countriesData);
        setMonths(
          monthsData.map((m: number) => ({
            id: m,
            label: String(m),
          }))
        );
        setAvailableMetrics(metricsData);
        setError(null);
      })
      .catch((err) => {
        setError(`Failed to load initial data: ${err.message}`);
      })
      .finally(() => {
        setLoading(false);
      });
    }, [BASE_URL]);

    /**
   * Fetch forecast data from the API based on current filter states.
   * Handles loading and error states.
   * Parses newline-delimited JSON response into ForecastData array.
   *
   * @returns {Promise<ForecastData[] | null>} Array of forecast data or null on error.
   */
    const fetchData = async (): Promise<ForecastData[] | null> => {
        setLoading(true);
        try {
            const segments = ["api", run, loa, typeOfViolence, "forecasts"];
            const params = new URLSearchParams();
            if (monthId) params.append("month_id", monthId);
            if (countryId) params.append("country_id", countryId);
            if (priogridId) params.append("priogrid_id", priogridId);
            if (metrics)
                metrics
                    .split(",")
                    .forEach(m => params.append("metrics", m));

            const url = `${BASE_URL}/${segments.join("/")}?${params.toString()}`;
            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            const text = await res.text();
            const lines = text.trim().split("\n");
            return lines.map(line => JSON.parse(line));
        } catch (e: any) {
            setError(e.message);
            return null;
        } finally {
            setLoading(false);
        }
    };

    return {
        run, setRun, loa, setLoa, typeOfViolence, setTypeOfViolence,
        monthId, setMonthId, countryId, setCountryId,
        priogridId, setPriogridId, metrics, setMetrics,
        countries, months, availableMetrics,
        loading, error, fetchData
    };
}
