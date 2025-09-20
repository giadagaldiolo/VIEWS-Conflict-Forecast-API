import React, { useState } from "react";
import { ForecastQuery } from "./components/ForecastQuery";
import { ForecastViewer } from "./components/ForecastViewer";

export function App() {
  const [forecastData, setForecastData] = useState<any[] | null>(null);

  return (
    <div>
      <h1>VIEWS Forecasts Frontend</h1>
      <ForecastQuery onData={setForecastData} />
      <ForecastViewer data={forecastData} />
    </div>
  );
}
