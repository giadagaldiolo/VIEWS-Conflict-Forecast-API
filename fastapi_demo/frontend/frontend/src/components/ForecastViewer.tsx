import React, { useState, useEffect } from "react";

export function ForecastViewer() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/standard/armed_conflict/armed_conflict/forecasts?month_id=1&country_id=840&metrics=MAP")
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then(json => {
        setData(json);  // jsonの形式に合わせて適宜加工することも
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading data...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Forecast Data</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre> {/* とりあえず生データ表示 */}
    </div>
  );
}
