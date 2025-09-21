import React, { useState, useEffect } from "react";
import Select, { MultiValue, SingleValue } from "react-select";
import { ForecastData } from "../model/forecastModel";
import "./ForecastQueryView.css";

interface Option {
    value: string | number;
    label: string;
}

interface ForecastQueryProps {
    /**
     * Callback function to return the fetched forecast data.
     * @param data - Array of forecast data or null if fetch failed.
     */
    onData: (data: ForecastData[] | null) => void;
}

/**
 * ForecastQueryView component allows users to query the Forecast API.
 * Users can select run, level of analysis (LoA), type of violence,
 * months, countries, grid cells (priogrid IDs), and metrics.
 * The component fetches the corresponding data from the backend API
 * and passes it back via the `onData` callback.
 */
export function ForecastQueryView({ onData }: ForecastQueryProps) {
    const [run, setRun] = useState("preds_001");
    const [loa, setLoa] = useState("pgm");
    const [typeOfViolence, setTypeOfViolence] = useState("sb");

    const [monthsOptions, setMonthsOptions] = useState<Option[]>([]);
    const [countriesOptions, setCountriesOptions] = useState<Option[]>([]);
    const [cellsOptions, setCellsOptions] = useState<Option[]>([]);
    const [metricsOptions, setMetricsOptions] = useState<Option[]>([]);

    const [selectedMonths, setSelectedMonths] = useState<Option[]>([]);
    const [selectedCountry, setSelectedCountry] = useState<Option | null>(null);
    const [selectedCells, setSelectedCells] = useState<Option[]>([]);
    const [selectedMetrics, setSelectedMetrics] = useState<Option[]>([]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

    /**
     * Fetch available months, countries, and metrics on component mount
     * or whenever run/loa/typeOfViolence changes.
     */
    useEffect(() => {
        const fetchLists = async () => {
            try {
                const [monthsRes, countriesRes, metricsRes] = await Promise.all([
                    fetch(`${BASE_URL}/${run}/${loa}/${typeOfViolence}/months`),
                    fetch(`${BASE_URL}/${run}/${loa}/${typeOfViolence}/countries`),
                    fetch(`${BASE_URL}/${run}/${loa}/${typeOfViolence}/metrics`),
                ]);

                const monthsData: number[] = await monthsRes.json();
                const countriesData: number[] = await countriesRes.json();
                const metricsData: string[] = await metricsRes.json();

                setMonthsOptions(monthsData.map(m => ({ value: m, label: m.toString() })));
                setCountriesOptions(countriesData.map(c => ({ value: c, label: c.toString() })));
                setMetricsOptions(metricsData.map(m => ({ value: m, label: m })));
            } catch (e: unknown) {
                if (e instanceof Error) setError(e.message);
                else setError(String(e));
            }
        };
        fetchLists();
    }, [run, loa, typeOfViolence, BASE_URL]);

    /**
     * Fetch priogrid IDs (cells) once a country is selected.
     */
    useEffect(() => {
        const fetchCells = async () => {
            if (!selectedCountry) {
                setCellsOptions([]);
                return;
            }
            try {
                const url = `${BASE_URL}/${run}/${loa}/${typeOfViolence}/cells?country_id=${selectedCountry.value}`;
                const cellsData: number[] = await (await fetch(url)).json();
                setCellsOptions(cellsData.map(c => ({ value: c, label: c.toString() })));
            } catch (e: unknown) {
                if (e instanceof Error) setError(e.message);
                else setError(String(e));
            }
        };
        fetchCells();
    }, [selectedCountry, run, loa, typeOfViolence, BASE_URL]);

    /**
     * Fetch forecast data based on the current selections.
     * Selected months, country, priogrid cells, and metrics are included in the query.
     */
    const fetchData = async () => {
        setLoading(true);
        try {
            const segments = [run, loa, typeOfViolence, "forecasts"];
            const params = new URLSearchParams();

            selectedMonths.forEach(m => params.append("month_id", m.value.toString()));
            if (selectedCountry) params.append("country_id", selectedCountry.value.toString());
            selectedCells.forEach(c => params.append("priogrid_id", c.value.toString()));
            selectedMetrics.forEach(m => params.append("metrics", m.value.toString()));

            const url = `${BASE_URL}/${segments.join("/")}?${params.toString()}`;
            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

            const text = await res.text();
            const lines: string[] = text.trim().split("\n");
            const data: ForecastData[] = lines.map(line => JSON.parse(line));

            // Pass fetched data back to parent component
            onData(data);

        } catch (e: unknown) {
            if (e instanceof Error) setError(e.message);
            else setError(String(e));
            onData(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="forecast-query-container">
            <h2>Forecast API Query</h2>

            {/* Run / LoA / Type of Violence inputs */}
            <div className="forecast-query-row">
                <div>
                    <label>Run</label>
                    <input value={run} onChange={e => setRun(e.target.value)} />
                </div>
                <div>
                    <label>LoA</label>
                    <input value={loa} onChange={e => setLoa(e.target.value)} />
                </div>
                <div>
                    <label>Type of Violence</label>
                    <input value={typeOfViolence} onChange={e => setTypeOfViolence(e.target.value)} />
                </div>
            </div>

            {/* Filters: Months, Country, Priogrid, Metrics */}
            <div className="forecast-query-filters">
                <div>
                    <label>Month</label>
                    <Select
                        options={monthsOptions}
                        value={selectedMonths}
                        onChange={(val: MultiValue<Option>) => setSelectedMonths(val as Option[])}
                        isMulti
                        placeholder="Select months..."
                    />
                </div>
                <div>
                    <label>Country</label>
                    <Select
                        options={countriesOptions}
                        value={selectedCountry}
                        onChange={(val: SingleValue<Option>) => setSelectedCountry(val as Option)}
                        placeholder="Select a country..."
                    />
                </div>
                <div>
                    <label>Priogrid</label>
                    <Select
                        options={cellsOptions}
                        value={selectedCells}
                        onChange={(val: MultiValue<Option>) => setSelectedCells(val as Option[])}
                        isMulti
                        placeholder="Select cells..."
                        isDisabled={!selectedCountry}
                    />
                </div>
                <div>
                    <label>Metrics</label>
                    <Select
                        options={metricsOptions}
                        value={selectedMetrics}
                        onChange={(val: MultiValue<Option>) => setSelectedMetrics(val as Option[])}
                        isMulti
                        placeholder="Select metrics..."
                    />
                </div>
            </div>

            {/* Fetch button */}
            <button className="fetch-button" onClick={fetchData} disabled={loading}>
                {loading ? "Fetching..." : "Fetch Forecast"}
            </button>

            {/* Error message */}
            {error && <div className="error-message">{error}</div>}
        </div>
    );
}
