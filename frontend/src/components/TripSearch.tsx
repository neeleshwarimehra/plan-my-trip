import { useState } from "react";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function TripSearch() {
  const [origin, setOrigin] = useState("Indore");
  const [destination, setDestination] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [travelers, setTravelers] = useState(2);
  const [budget, setBudget] = useState(35000);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);

  async function handleSearch() {
    setError("");
    setResult(null);

    if (!origin.trim() || !destination.trim()) {
      setError("Please enter your starting city and destination.");
      return;
    }

    if (!startDate || !endDate || endDate < startDate) {
      setError("Please select valid travel dates.");
      return;
    }

    if (travelers < 1 || budget < 1) {
      setError("Travelers and budget must be greater than zero.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/trips/plan`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          origin: origin.trim(),
          destination: destination.trim(),
          start_date: startDate,
          end_date: endDate,
          travelers,
          budget,
          currency: "INR",
          preferences: ["budget-friendly"],
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to create your trip. Please try again.",
        );
      }

      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="search-panel">
      <div className="search-heading">
        <div>
          <h2>Where would you like to go?</h2>
          <p>Let AI plan your next unforgettable journey.</p>
        </div>
        <span className="ai-label">✨ AI POWERED</span>
      </div>

      <div className="search-fields">
        <label>
          FROM
          <input
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            placeholder="Starting city"
          />
        </label>

        <label>
          DESTINATION
          <input
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="Where to?"
          />
        </label>

        <label>
          START DATE
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>

        <label>
          END DATE
          <input
            type="date"
            min={startDate}
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>

        <label>
          TRAVELERS
          <input
            type="number"
            min="1"
            value={travelers}
            onChange={(e) => setTravelers(Number(e.target.value))}
          />
        </label>

        <label>
          BUDGET (₹)
          <input
            type="number"
            min="1"
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
          />
        </label>

        <button onClick={handleSearch} disabled={loading}>
          {loading ? "Planning your trip..." : "✨ Plan My Trip"}
        </button>
      </div>

      {error && (
        <p role="alert" className="error-message">
          {error}
        </p>
      )}

      {result && (
        <div className="trip-result">
          <div className="result-heading">
            <span>🎉</span>
            <div>
              <h3>Your AI travel plan is ready!</h3>
              <p>{result.status || "Trip created successfully"}</p>
            </div>
          </div>

          <div className="result-summary">
            <h3>
              {result.request?.origin} → {result.request?.destination}
            </h3>

            <p>{result.summary}</p>

            {result.trip_id && (
              <p className="trip-id">Trip ID: {result.trip_id}</p>
            )}
          </div>

          <div className="result-budget">
            <span>Estimated budget per person</span>
            <strong>
              {new Intl.NumberFormat("en-IN", {
                style: "currency",
                currency: result.request?.currency || "INR",
                maximumFractionDigits: 0,
              }).format(Number(result.estimated_budget_per_person || 0))}
            </strong>
          </div>

          {result.next_steps?.length > 0 && (
            <div className="result-next-steps">
              <h4>Next steps</h4>
              <ul>
                {result.next_steps.map((step: string, index: number) => (
                  <li key={index}>{step}</li>
                ))}
              </ul>
            </div>
          )}

          {result.plan_details && (
            <details className="result-details">
              <summary>View complete AI travel plan</summary>
              <pre>{JSON.stringify(result.plan_details, null, 2)}</pre>
            </details>
          )}
        </div>
      )}
    </section>
  );
}

export default TripSearch;
