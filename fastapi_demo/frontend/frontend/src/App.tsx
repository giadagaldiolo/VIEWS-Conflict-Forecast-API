import React, { useState } from "react";
import { ForecastViewer } from "./components/ForecastViewer";
import { ForecastQuery } from "./components/ForecastQuery";

export function App() {
  const [forecastData, setForecastData] = useState(null);

  return (
    <>
      <ForecastQuery onData={setForecastData} />
      <ForecastViewer data={forecastData} />
    </>
  );
}
