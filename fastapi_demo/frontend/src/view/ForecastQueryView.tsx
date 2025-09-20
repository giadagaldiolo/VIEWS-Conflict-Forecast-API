import React from "react";
import { useForecastController } from "../controller/forecastController";
import { ForecastData } from "../model/forecastModel";

interface Props {
    onData: (data: ForecastData[] | null) => void;
}

export function ForecastQueryView({ onData }: Props) {
    const controller = useForecastController();

    const {
        run, setRun, loa, setLoa, typeOfViolence, setTypeOfViolence,
        monthId, setMonthId, countryId, setCountryId,
        priogridId, setPriogridId, metrics, setMetrics,
        countries, months, availableMetrics,
        loading, error
    } = controller;

    // wrap fetchData to update App state
    const handleFetch = async () => {
        const data = await controller.fetchData();  // fetchData deve restituire ForecastData[]
        onData(data);
    }

    const runOptions = ["v1", "v2"];
    const loaOptions = ["standard", "alternative"];
    const violenceOptions = ["armed_conflict", "other"];

    return (
        <div>
            <h2>Forecast API Query</h2>
            <form onSubmit={e => { e.preventDefault(); handleFetch(); }}>
                <fieldset disabled={loading}>
                    {/* ... tutto il resto dei form field rimane uguale */}
                </fieldset>
                <button type="submit" disabled={loading}>
                    {loading ? "Fetching..." : "Fetch Forecast"}
                </button>
            </form>
            {error && <div style={{color: "red"}}>{error}</div>}
        </div>
    );
}
