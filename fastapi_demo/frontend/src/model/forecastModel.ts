/**
 * Forecast data returned from the API.
 */
export interface ForecastData {
    id: number;
    forecast: number;
    region: string;
    [key: string]: any;
}

/**
 * Country object with ID and name.
 */
export interface Country {
    id: number;
    name: string;
}

/**
 * Month object with ID and label.
 */
export interface Month {
    id: number;
    label: string;
}

/**
 * Fetches forecast data based on given filters.
 *
 * @param baseUrl - Base URL of the API.
 * @param run - API version identifier.
 * @param loa - Level of analysis.
 * @param typeOfViolence - Type of violence filter.
 * @param monthId - Optional month ID to filter forecasts.
 * @param countryId - Optional country ID to filter forecasts.
 * @param priogridId - Optional priogrid ID to filter forecasts.
 * @param metrics - Optional comma-separated list of metrics.
 * @returns Promise resolving to an array of ForecastData.
 * @throws Error if the HTTP response is not OK.
 */
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

/**
 * Fetches the list of countries from the API.
 *
 * @param baseUrl - Base URL of the API.
 * @returns Promise resolving to an array of Country objects.
 */
export async function fetchCountries(baseUrl: string): Promise<Country[]> {
    const res = await fetch(`${baseUrl}/api/countries`);
    return res.json();
}

/**
 * Fetches the list of months from the API.
 *
 * @param baseUrl - Base URL of the API.
 * @returns Promise resolving to an array of Month objects.
 */
export async function fetchMonths(baseUrl: string): Promise<Month[]> {
    const res = await fetch(`${baseUrl}/api/months`);
    return res.json();
}

/**
 * Fetches the list of available metrics from the API.
 *
 * @param baseUrl - Base URL of the API.
 * @returns Promise resolving to an array of metric strings.
 */
export async function fetchMetrics(baseUrl: string): Promise<string[]> {
    const res = await fetch(`${baseUrl}/api/metrics`);
    return res.json();
}
