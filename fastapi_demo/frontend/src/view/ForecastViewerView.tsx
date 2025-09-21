import React from "react";
import { ForecastData } from "../model/forecastModel";

/**
 * Displays forecast data in a readable JSON format.
 *
 * Args:
 *   data (ForecastData[] | null): The forecast data to display. If null, shows a placeholder message.
 *
 * Returns:
 *   JSX.Element: A React component showing the forecast data or a message if no data is available.
 */
interface Props {
    data: ForecastData[] | null;
}

export function ForecastViewerView({ data }: Props) {
    if (!data) return <div>No forecast data loaded.</div>;

    return (
        <div>
            <h2>Forecast Data</h2>
            <pre style={{ maxHeight: 400, overflowY: "auto" }}>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
}
