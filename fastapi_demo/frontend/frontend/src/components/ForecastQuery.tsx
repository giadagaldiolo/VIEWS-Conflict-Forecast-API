import React, { useState } from "react";

interface ForecastQueryProps {
  onData: (data: any[] | null) => void;
}

export function ForecastQuery({ onData }: ForecastQueryProps) {
  const [run, setRun] = useState("v1");
  const [loa, setLoa] = useState("standard");
  const [typeOfViolence, setTypeOfViolence] = useState("armed_conflict");
  const [monthId, setMonthId] = useState("1");
  const [countryId, setCountryId] = useState("840");
  const [metrics, setMetrics] = useState("MAP");
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    const url = `http://localhost:8000/api/${run}/${loa}/${typeOfViolence}/forecasts?month_id=${monthId}&country_id=${countryId}&metrics=${metrics}`;
    try {
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const text = await res.text();
      // StreamingResponseで複数JSONが改行で区切られている前提
      const lines = text.trim().split("\n");
      const data = lines.map(line => JSON.parse(line));

      onData(data);
      setError(null);
    } catch (e: any) {
      setError(e.message);
      onData(null);
    }
  };

  return (
    <div>
      <h2>Forecast API Query</h2>
      <div>
        <label>Run: <input value={run} onChange={e => setRun(e.target.value)} /></label>
      </div>
      <div>
        <label>LoA: <input value={loa} onChange={e => setLoa(e.target.value)} /></label>
      </div>
      <div>
        <label>Type of Violence: <input value={typeOfViolence} onChange={e => setTypeOfViolence(e.target.value)} /></label>
      </div>
      <div>
        <label>Month ID: <input value={monthId} onChange={e => setMonthId(e.target.value)} /></label>
      </div>
      <div>
        <label>Country ID: <input value={countryId} onChange={e => setCountryId(e.target.value)} /></label>
      </div>
      <div>
        <label>Metrics: <input value={metrics} onChange={e => setMetrics(e.target.value)} /></label>
      </div>
      <button onClick={fetchData}>Fetch Forecast</button>

      {error && <div style={{ color: "red" }}>Error: {error}</div>}
    </div>
  );
}
