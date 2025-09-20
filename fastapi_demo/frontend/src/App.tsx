import React, { useState } from "react";
import { ForecastQueryView } from "./view/ForecastQueryView";
import { ForecastViewerView } from "./view/ForecastViewerView";
import { ForecastData } from "./model/forecastModel";

export function App() {
    const [data, setData] = useState<ForecastData[] | null>(null);

    return (
        <div>
            <h1>VIEWS Forecasts Frontend</h1>

            {/* Form per query */}
            <ForecastQueryView onData={setData} />

            {/* Visualizzazione dei dati */}
            <ForecastViewerView data={data} />
        </div>
    );
}
