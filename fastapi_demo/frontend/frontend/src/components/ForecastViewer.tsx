import React from "react";

interface ForecastViewerProps {
  data: any[] | null;
}

export function ForecastViewer({ data }: ForecastViewerProps) {
  if (!data) return <div>No forecast data loaded.</div>;

  return (
    <div>
      <h2>Forecast Data</h2>
      <pre style={{ maxHeight: 400, overflowY: "auto" }}>
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}
