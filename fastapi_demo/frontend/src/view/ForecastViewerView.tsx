import React from "react";
import { ForecastData } from "../model/forecastModel";

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
