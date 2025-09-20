export interface ForecastData {
    id: number;
    forecast: number;
    region: string;
    [key: string]: any;
}

export interface Country {
    id: number;
    name: string;
}

export interface Month {
    id: number;
    label: string;
}

export async function fetchForecasts(
    baseUrl: string,
    run: string,
    loa: string,
    typeOfViolence: string,
    monthId?: string,
    countryId?: string,
    priogridId?: string,
    metrics?: string
): Promise<ForecastData[]> {
    const segments = ["api", run, loa, typeOfViolence, "forecasts"];
    const params = new URLSearchParams();
    if (monthId) params.append("month_id", monthId);
    if (countryId) params.append("country_id", countryId);
    if (priogridId) params.append("priogrid_id", priogridId);
    if (metrics) {
        metrics.split(",").map(m => m.trim()).forEach(m => {
            if (m) params.append("metrics", m);
        });
    }

    const url = `${baseUrl}/${segments.join("/")}?${params.toString()}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    const text = await res.text();
    const lines = text.trim().split("\n");
    return lines.map(line => JSON.parse(line));
}

export async function fetchCountries(baseUrl: string): Promise<Country[]> {
    const res = await fetch(`${baseUrl}/api/countries`);
    return res.json();
}

export async function fetchMonths(baseUrl: string): Promise<Month[]> {
    const res = await fetch(`${baseUrl}/api/months`);
    return res.json();
}

export async function fetchMetrics(baseUrl: string): Promise<string[]> {
    const res = await fetch(`${baseUrl}/api/metrics`);
    return res.json();
}
