import React, { useState } from "react";

interface ForecastQueryProps {
  onData: (data: ForecastData[] | null) => void;
}

interface ForecastData {
  id: number;
  forecast: number;
  region: string;
  [key: string]: any;
}

export function ForecastQuery({ onData }: ForecastQueryProps) {
  const [run, setRun] = useState("");
  const [loa, setLoa] = useState("");
  const [typeOfViolence, setTypeOfViolence] = useState("");
  const [monthId, setMonthId] = useState("");
  const [countryId, setCountryId] = useState("");
  const [priogridId, setPriogridId] = useState("");
  const [metrics, setMetrics] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      // パスパラメータにデフォルト値を設定
      const runVal = run || "v1";
      const loaVal = loa || "standard";
      const violenceVal = typeOfViolence || "armed_conflict";

      const segments = ["api", runVal, loaVal, violenceVal, "forecasts"];

      // クエリパラメータを必要なものだけ追加
      const params = new URLSearchParams();
      if (monthId) params.append("month_id", monthId);
      if (countryId) params.append("country_id", countryId);
      if (priogridId) params.append("priogrid_id", priogridId);
      if (metrics) {
        // 複数のmetricsをカンマ区切りで指定された場合に対応
        metrics.split(",").map(m => m.trim()).forEach(m => {
          if (m) params.append("metrics", m);
        });
      }

      const url = `http://localhost:8000/${segments.join("/")}?${params.toString()}`;

      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

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

  return (
    <div>
      <h2>Forecast API Query</h2>
      <form onSubmit={(e) => { e.preventDefault(); fetchData(); }}>
        <fieldset disabled={loading} style={{ marginBottom: "1rem" }}>
          <label>
            Run:
            <input
              value={run}
              onChange={e => setRun(e.target.value)}
              placeholder="v1"
            />
          </label>
          <br />

          <label>
            LoA:
            <input
              value={loa}
              onChange={e => setLoa(e.target.value)}
              placeholder="standard"
            />
          </label>
          <br />

          <label>
            Type of Violence:
            <input
              value={typeOfViolence}
              onChange={e => setTypeOfViolence(e.target.value)}
              placeholder="armed_conflict"
            />
          </label>
          <br />

          <label>
            Month ID:
            <input
              value={monthId}
              onChange={e => setMonthId(e.target.value)}
              placeholder="e.g. 1"
            />
          </label>
          <br />

          <label>
            Country ID:
            <input
              value={countryId}
              onChange={e => setCountryId(e.target.value)}
              placeholder="e.g. 840"
            />
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
            Metrics (comma-separated):
            <input
              value={metrics}
              onChange={e => setMetrics(e.target.value)}
              placeholder="e.g. MAP,MAE"
            />
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
