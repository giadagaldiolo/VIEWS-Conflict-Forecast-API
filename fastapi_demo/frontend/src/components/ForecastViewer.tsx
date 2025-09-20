// ForecastViewer.tsx
import React, { useState } from "react";
import { ForecastData } from "./types";

interface Props {
  data: ForecastData[] | null;
}

export function ForecastViewer({ data }: Props) {
  const [view, setView] = useState<"table" | "json">("table");

  if (!data) return <div>No forecast data loaded.</div>;

  const metricsKeys = data.length > 0 ? Object.keys(data[0].metrics || {}) : [];

  return (
    <div>
      <h2>Forecast Data</h2>
      <div style={{ marginBottom: 10 }}>
        <button onClick={() => setView("table")} disabled={view === "table"}>
          Table View
        </button>
        <button onClick={() => setView("json")} disabled={view === "json"} style={{ marginLeft: 10 }}>
          JSON View
        </button>
      </div>

      {view === "table" ? (
        <table border={1} cellPadding={5} style={{ borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Priogrid</th>
              <th>Country</th>
              <th>Month</th>
              <th>Lat</th>
              <th>Lon</th>
              {metricsKeys.map((k) => (
                <th key={k}>{k}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((d) => (
              <tr key={`${d.priogrid_id}-${d.month_id}`}>
                <td>{d.priogrid_id}</td>
                <td>{d.country_id}</td>
                <td>{d.month_id}</td>
                <td>{d.lat}</td>
                <td>{d.lon}</td>
                {metricsKeys.map((k) => (
                  <td key={k}>{d.metrics?.[k]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <pre style={{ maxHeight: 400, overflowY: "auto", backgroundColor: "#f0f0f0", padding: 10 }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  );
}
