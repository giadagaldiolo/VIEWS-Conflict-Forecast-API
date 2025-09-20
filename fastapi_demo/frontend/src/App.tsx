// App.tsx
import React, { useState } from "react";
import { ForecastQuery } from "./components/ForecastQuery";
import { ForecastViewer } from "./components/ForecastViewer";
import { ForecastData } from "./components/types";

export function App() {
  const [forecastData, setForecastData] = useState<ForecastData[] | null>(null);

  return (
    <div>
      <h1>VIEWS Forecasts Frontend</h1>
      <ForecastQuery onData={setForecastData} />
      <ForecastViewer data={forecastData} />
    </div>
  );
}