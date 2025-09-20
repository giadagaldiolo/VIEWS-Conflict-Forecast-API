// src/view/ForecastQueryView.tsx
import React, { useState, useEffect } from "react";
import { ForecastData } from "../model/forecastModel";

interface ForecastQueryProps {
    onData: (data: ForecastData[] | null) => void;
}

export function ForecastQueryView({ onData }: ForecastQueryProps) {
    // Parametri selezionabili
    const [run, setRun] = useState("preds_001");
    const [loa, setLoa] = useState("pgm");
    const [typeOfViolence, setTypeOfViolence] = useState("sb");

    const [monthId, setMonthId] = useState("");
    const [countryId, setCountryId] = useState("");
    const [priogridId, setPriogridId] = useState("");
    const [metrics, setMetrics] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Dati recuperati dalle API
    const [months, setMonths] = useState<number[]>([]);
    const [countries, setCountries] = useState<number[]>([]);
    const [cells, setCells] = useState<number[]>([]);

    // URL backend corretto per Docker
    const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

    // Carica months, countries, cells all'avvio
    useEffect(() => {
        const fetchLists = async () => {
            try {
                const [monthsRes, countriesRes, cellsRes] = await Promise.all([
                    fetch(`${BASE_URL}/${run}/${loa}/${typeOfViolence}/months`),
                    fetch(`${BASE_URL}/${run}/${loa}/${typeOfViolence}/countries`),
                    fetch(`${BASE_URL}/${run}/${loa}/${typeOfViolence}/cells`),
                ]);

                const monthsData = await monthsRes.json();
                const countriesData = await countriesRes.json();
                const cellsData = await cellsRes.json();

                setMonths(monthsData);
                setCountries(countriesData);
                setCells(cellsData);
            } catch (e: any) {
                setError(e.message);
            }
        };

        fetchLists();
    }, [run, loa, typeOfViolence]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const segments = [ run, loa, typeOfViolence, "forecasts"];
            const params = new URLSearchParams();
            if (monthId) params.append("month_id", monthId);
            if (countryId) params.append("country_id", countryId);
            if (priogridId) params.append("priogrid_id", priogridId);
            if (metrics) metrics.split(",").forEach(m => params.append("metrics", m));

            const url = `${BASE_URL}/${segments.join("/")}?${params.toString()}`;
            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

            const text = await res.text();
            const lines = text.trim().split("\n");
            const data = lines.map(line => JSON.parse(line));
            onData(data);
        } catch (e: any) {
            setError(e.message);
            onData(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "1rem" }}>
            <h2>Forecast API Query</h2>

            <div>
                <label>
                    Run: <input value={run} onChange={e => setRun(e.target.value)} />
                </label>
                <label>
                    LoA: <input value={loa} onChange={e => setLoa(e.target.value)} />
                </label>
                <label>
                    Type of Violence: <input value={typeOfViolence} onChange={e => setTypeOfViolence(e.target.value)} />
                </label>
            </div>

            <div style={{ marginTop: "1rem" }}>
                <label>
                    Month:
                    <select value={monthId} onChange={e => setMonthId(e.target.value)}>
                        <option value="">-- select month --</option>
                        {months.map(m => (
                            <option key={m} value={m}>{m}</option>
                        ))}
                    </select>
                </label>

                <label>
                    Country:
                    <select value={countryId} onChange={e => setCountryId(e.target.value)}>
                        <option value="">-- select country --</option>
                        {countries.map(c => (
                            <option key={c} value={c}>{c}</option>
                        ))}
                    </select>
                </label>

                <label>
                    Priogrid:
                    <select value={priogridId} onChange={e => setPriogridId(e.target.value)}>
                        <option value="">-- select cell --</option>
                        {cells.map(c => (
                            <option key={c} value={c}>{c}</option>
                        ))}
                    </select>
                </label>

                <label>
                    Metrics: <input value={metrics} onChange={e => setMetrics(e.target.value)} placeholder="MAP,MAE,..." />
                </label>
            </div>

            <button style={{ marginTop: "1rem" }} onClick={fetchData} disabled={loading}>
                {loading ? "Fetching..." : "Fetch Forecast"}
            </button>

            {error && <div style={{ color: "red" }}>{error}</div>}
        </div>
    );
}
