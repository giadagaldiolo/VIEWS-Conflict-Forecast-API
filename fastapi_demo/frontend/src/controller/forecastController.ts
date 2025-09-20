import { useState, useEffect } from "react";
import { ForecastData } from "../model/forecastModel";

export function useForecastController() {
    const [run, setRun] = useState("v1");
    const [loa, setLoa] = useState("standard");
    const [typeOfViolence, setTypeOfViolence] = useState("armed_conflict");
    const [monthId, setMonthId] = useState("");
    const [countryId, setCountryId] = useState("");
    const [priogridId, setPriogridId] = useState("");
    const [metrics, setMetrics] = useState("");

    const [countries, setCountries] = useState<{id: number, name: string}[]>([]);
    const [months, setMonths] = useState<{id: number, label: string}[]>([]);
    const [availableMetrics, setAvailableMetrics] = useState<string[]>([]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

    useEffect(() => {
        // Fetch countries
        fetch(`${BASE_URL}/api/countries`)
            .then(res => res.json())
            .then(setCountries)
            .catch(err => console.error(err));

        // Fetch months
        fetch(`${BASE_URL}/api/months`)
            .then(res => res.json())
            .then(data => setMonths(data.map((m: number) => ({id: m, label: String(m)}))))
            .catch(err => console.error(err));

        // Fetch metrics
        fetch(`${BASE_URL}/api/metrics`)
            .then(res => res.json())
            .then(setAvailableMetrics)
            .catch(err => console.error(err));
    }, []);

    const fetchData = async (): Promise<ForecastData[] | null> => {
        setLoading(true);
        try {
            const segments = ["api", run, loa, typeOfViolence, "forecasts"];
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
