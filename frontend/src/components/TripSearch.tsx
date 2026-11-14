import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

interface TripSearchProps {
  prefilledDestination?: string;
  prefilledBudget?: number;
}

function TripSearch({
  prefilledDestination = "",
  prefilledBudget,
}: TripSearchProps) {
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [travelers, setTravelers] = useState(2);
  const [budget, setBudget] = useState(35000);
  const [preferencesInput, setPreferencesInput] = useState(
    "budget-friendly, sightseeing"
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    if (prefilledDestination) {
      setDestination(prefilledDestination);
    }
  }, [prefilledDestination]);

  useEffect(() => {
    if (prefilledBudget && prefilledBudget > 0) {
      setBudget(prefilledBudget);
    }
  }, [prefilledBudget]);

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

    const preferences = preferencesInput
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

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
          preferences:
            preferences.length > 0 ? preferences : ["budget-friendly"],
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        const detail =
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail);
        throw new Error(
          detail || "Unable to create your trip. Please try again."
        );
      }

      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  const formatMoney = (amount: number, currency = "INR") =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(Number(amount || 0));

  const toBulletPoints = (text: string) =>
    text
      .split(/\.\s+/)
      .map((sentence) => sentence.trim().replace(/\.$/, ""))
      .filter(Boolean);

  const details = result?.plan_details || {};
  const currency = result?.request?.currency || "INR";

  return (
    <section className="search-panel">
      <div className="search-heading">
        <div>
          <h2>Where would you like to go?</h2>
          <p>Let AI & MCP tools plan your next unforgettable journey.</p>
        </div>
        <span className="ai-label">✨ AI + MCP POWERED</span>
      </div>

      <div className="search-fields">
        <label>
          FROM
          <input
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            placeholder="Enter starting city"
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

        <label style={{ gridColumn: "1 / -1" }}>
          PREFERENCES (COMMA SEPARATED)
          <input
            value={preferencesInput}
            onChange={(e) => setPreferencesInput(e.target.value)}
            placeholder="e.g., beaches, local food, culture, adventure"
          />
        </label>

        <button onClick={handleSearch} disabled={loading}>
          {loading ? "Running AI Agents & MCP Tools..." : "✨ Plan My Trip"}
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
              <p>Status: {result.status || "planned"}</p>
            </div>
          </div>

          <div className="result-summary">
            <h3>
              {result.request?.origin} → {result.request?.destination}
            </h3>
            <ul>
              <li>{result.summary}</li>
              {details.destination_overview &&
                toBulletPoints(details.destination_overview).map(
                  (point: string, idx: number) => <li key={idx}>{point}.</li>
                )}
            </ul>
            {result.trip_id && (
              <p className="trip-id">Trip ID: {result.trip_id}</p>
            )}
          </div>

          <div className="result-budget">
            <span>Estimated budget per person</span>
            <strong>
              {formatMoney(result.estimated_budget_per_person, currency)}
            </strong>
          </div>

          {details.budget_breakdown && (
            <div className="result-summary">
              <h4>💰 Budget Breakdown</h4>
              <ul>
                {Object.entries(details.budget_breakdown).map(([cat, amt]) => (
                  <li key={cat} style={{ textTransform: "capitalize" }}>
                    <strong>{cat}:</strong>{" "}
                    {formatMoney(Number(amt), currency)}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {Array.isArray(details.transportation_options) &&
            details.transportation_options.length > 0 && (
              <div className="result-summary">
                <h4>🚆 Transportation Options</h4>
                <ul>
                  {details.transportation_options.map(
                    (opt: any, idx: number) => (
                      <li key={idx}>
                        <strong>{opt.type}:</strong> {opt.description} (Est.{" "}
                        {formatMoney(opt.estimated_cost, currency)})
                      </li>
                    )
                  )}
                </ul>
              </div>
            )}

          {Array.isArray(details.live_flights) &&
            details.live_flights.length > 0 && (
              <div className="result-summary">
                <h4>✈️ Live Flight Matches (Aviationstack)</h4>
                <ul>
                  {details.live_flights.map((f: any, idx: number) => (
                    <li key={idx}>
                      <strong>{f.airline || "Airline"}</strong> (
                      {f.flight_number || "N/A"}) — {f.departure} → {f.arrival}{" "}
                      [{f.status || "scheduled"}]
                    </li>
                  ))}
                </ul>
              </div>
            )}

          {Array.isArray(details.hotel_options) &&
            details.hotel_options.length > 0 && (
              <div className="result-summary">
                <h4>🏨 Recommended Stay Options</h4>
                <ul>
                  {details.hotel_options.map((h: any, idx: number) => (
                    <li key={idx}>
                      <strong>{h.type}:</strong> {h.description} (Est.{" "}
                      {formatMoney(h.estimated_cost_per_night, currency)}/night)
                    </li>
                  ))}
                </ul>
              </div>
            )}

          {Array.isArray(details.live_hotels) &&
            details.live_hotels.length > 0 && (
              <div className="result-summary">
                <h4>🔍 Live Hotel Search Results (Tavily)</h4>
                <ul>
                  {details.live_hotels.map((h: any, idx: number) => (
                    <li key={idx}>
                      <a href={h.url} target="_blank" rel="noreferrer">
                        <strong>{h.title}</strong>
                      </a>{" "}
                      — {h.snippet}
                    </li>
                  ))}
                </ul>
              </div>
            )}

          {Array.isArray(details.itinerary) && details.itinerary.length > 0 && (
            <div className="result-summary">
              <h4>🗓️ Day-by-Day Itinerary</h4>
              {details.itinerary.map((day: any) => (
                <div key={day.day} style={{ marginBottom: "14px" }}>
                  <strong>
                    Day {day.day}: {day.title} (
                    {formatMoney(day.estimated_cost, currency)})
                  </strong>
                  <ul>
                    {(day.activities || []).map((act: string, i: number) => (
                      <li key={i}>{act}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}

          {Array.isArray(details.recommendations) &&
            details.recommendations.length > 0 && (
              <div className="result-summary">
                <h4>💡 Travel Tips & Recommendations</h4>
                <ul>
                  {details.recommendations.map((tip: string, idx: number) => (
                    <li key={idx}>{tip}</li>
                  ))}
                </ul>
              </div>
            )}

          {result.next_steps?.length > 0 && (
            <div className="result-next-steps">
              <h4>✅ Next Steps</h4>
              <ul>
                {result.next_steps.map((step: string, index: number) => (
                  <li key={index}>{step}</li>
                ))}
              </ul>
            </div>
          )}

          <details className="result-details">
            <summary>View raw MCP & Agent JSON payload</summary>
            <pre>{JSON.stringify(result.plan_details, null, 2)}</pre>
          </details>
        </div>
      )}
    </section>
  );
}

export default TripSearch;