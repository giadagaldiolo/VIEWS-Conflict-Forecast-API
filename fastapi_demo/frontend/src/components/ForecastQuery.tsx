import React, { useState, useEffect } from "react";

interface ForecastQueryProps {
  onData: (data: ForecastData[] | null) => void;
}

interface ForecastData {
  id: number;
  forecast: number;
  region: string;
  [key: string]: any;
}

interface Country {
  id: number;
  name: string;
}

export function ForecastQuery({ onData }: ForecastQueryProps) {
  const [run, setRun] = useState("v1");
  const [loa, setLoa] = useState("standard");
  const [typeOfViolence, setTypeOfViolence] = useState("armed_conflict");
  const [monthId, setMonthId] = useState("");
  const [countryId, setCountryId] = useState("");
  const [priogridId, setPriogridId] = useState("");
  const [metrics, setMetrics] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [countries, setCountries] = useState<{id: number, name: string}[]>([]);
  const [months, setMonths] = useState<{id: number, label: string}[]>([]);
  const [availableMetrics, setAvailableMetrics] = useState<string[]>([]);

  const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  // useEffect で API から動的に取得
  useEffect(() => {
    // Countries
    fetch(`${BASE_URL}/api/countries`)
      .then(res => res.json())
      .then(setCountries)
      .catch(err => console.error("Failed to fetch countries:", err));

    // Months
    fetch(`${BASE_URL}/api/months`)
      .then(res => res.json())
      .then(setMonths)
      .catch(err => console.error("Failed to fetch months:", err));

    // Metrics
    fetch(`${BASE_URL}/api/metrics`)
      .then(res => res.json())
      .then(setAvailableMetrics)
      .catch(err => console.error("Failed to fetch metrics:", err));
  }, []);


  // --- Fetch forecast data ---
  const fetchData = async () => {
    setLoading(true);
    try {
      const segments = ["api", run, loa, typeOfViolence, "forecasts"];
      const params = new URLSearchParams();
      if (monthId) params.append("month_id", monthId);
      if (countryId) params.append("country_id", countryId);
      if (priogridId) params.append("priogrid_id", priogridId);
      if (metrics) {
        metrics.split(",").map(m => m.trim()).forEach(m => {
          if (m) params.append("metrics", m);
        });
      }

      const url = `${BASE_URL}/${segments.join("/")}?${params.toString()}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const text = await res.text();
      const lines = text.trim().split("\n");
      const data: ForecastData[] = lines.map(line => JSON.parse(line));

      onData(data);
      setError(null);
    } catch (e: any) {
      setError(e.message);
      onData(null);
    } finally {
      setLoading(false);
    }
  };

  const runOptions = ["v1", "v2"];
  const loaOptions = ["standard", "alternative"];
  const violenceOptions = ["armed_conflict", "other"];

  return (
    <div>
      <h2>Forecast API Query</h2>
      <form onSubmit={e => { e.preventDefault(); fetchData(); }}>
        <fieldset disabled={loading} style={{ marginBottom: "1rem" }}>
          <label>
            Run:
            <select value={run} onChange={e => setRun(e.target.value)}>
              {runOptions.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </label>
          <br />

          <label>
            LoA:
            <select value={loa} onChange={e => setLoa(e.target.value)}>
              {loaOptions.map(l => <option key={l} value={l}>{l}</option>)}
            </select>
          </label>
          <br />

          <label>
            Type of Violence:
            <select value={typeOfViolence} onChange={e => setTypeOfViolence(e.target.value)}>
              {violenceOptions.map(v => <option key={v} value={v}>{v}</option>)}
            </select>
          </label>
          <br />

          <label>
            Month:
            <select value={monthId} onChange={e => setMonthId(e.target.value)}>
              <option value="">-- select month --</option>
              {months.map(m => (
                <option key={m.id} value={m.id}>{m.label}</option>
              ))}
            </select>
          </label>
          <br />

          <label>
            Country:
            <select value={countryId} onChange={e => setCountryId(e.target.value)}>
              <option value="">-- select country --</option>
              {countries.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </label>
          <br />

          <label>
            Priogrid ID:
            <input
              value={priogridId}
              onChange={e => setPriogridId(e.target.value)}
              placeholder="e.g. 123456"
            />
          </label>
          <br />

          <label>
            Metrics:
            <select
              multiple
              value={metrics.split(",").filter(Boolean)}
              onChange={e => {
                const selected = Array.from(e.target.selectedOptions).map(o => o.value);
                setMetrics(selected.join(","));
              }}
            >
              {availableMetrics.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </label>
        </fieldset>

        <button type="submit" disabled={loading}>
          {loading ? "Fetching..." : "Fetch Forecast"}
        </button>
      </form>

      {error && <div style={{ color: "red" }}>Error: {error}</div>}
    </div>
  );
}
