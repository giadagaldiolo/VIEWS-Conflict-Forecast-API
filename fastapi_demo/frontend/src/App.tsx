import React, { useState } from "react";
import { ForecastQueryView } from "./view/ForecastQueryView";
import { ForecastViewerView } from "./view/ForecastViewerView";
import { ForecastData } from "./model/forecastModel";

export function App() {
    const [forecastData, setForecastData] = useState<ForecastData[] | null>(null);

    return (
        <div>
            <h1>VIEWS Forecasts Frontend</h1>
            <ForecastQueryView onData={setForecastData} />
            <ForecastViewerView data={forecastData} />
        </div>
    );
}
