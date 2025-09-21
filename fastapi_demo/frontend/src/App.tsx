import React, { useState } from "react";
import { ForecastQueryView } from "./view/ForecastQueryView";
import { ForecastViewerView } from "./view/ForecastViewerView";
import { ForecastData } from "./model/forecastModel";

/**
 * Main App component for the VIEWS Forecasts Frontend.
 *
 * Manages the state of the fetched forecast data and renders:
 * - ForecastQueryView: the form to select filters and fetch data
 * - ForecastViewerView: a component to visualize the returned forecast data
 */
export function App() {
    /**
     * State to store fetched forecast data from the API.
     * It is passed down to ForecastViewerView for rendering.
     */
    const [data, setData] = useState<ForecastData[] | null>(null);

    return (
        <div>
            <h1>VIEWS Forecasts Frontend</h1>

            {/* Query form to select filters and request forecast data */}
            <ForecastQueryView onData={setData} />

            {/* Visualization of the fetched forecast data */}
            <ForecastViewerView data={data} />
        </div>
    );
}
