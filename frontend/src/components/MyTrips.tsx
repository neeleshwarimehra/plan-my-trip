import { useCallback, useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

interface Trip {
  id: string;
  origin: string;
  destination: string;
  start_date: string;
  end_date: string;
  travelers: number;
  budget: number;
  currency: string;
  status: string;
  summary: string;
  estimated_budget_per_person: number;
  preferences: string[];
}

function MyTrips() {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedTrip, setSelectedTrip] = useState<Trip | null>(null);
  const [deleting, setDeleting] = useState("");

  const loadTrips = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/api/trips?skip=0&limit=100`);
      if (!response.ok) throw new Error("Unable to load trips.");

      const data = await response.json();
      setTrips(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTrips();
  }, [loadTrips]);

  async function deleteTrip(id: string) {
    if (!window.confirm("Are you sure you want to delete this trip?")) return;

    setDeleting(id);
    try {
      const response = await fetch(`${API_URL}/api/trips/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Unable to delete trip.");

      setTrips((current) => current.filter((trip) => trip.id !== id));
      if (selectedTrip?.id === id) setSelectedTrip(null);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Delete failed.");
    } finally {
      setDeleting("");
    }
  }

  const formatDate = (date: string) =>
    new Date(`${date}T00:00:00`).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });

  const formatMoney = (amount: number, currency: string) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: currency || "INR",
      maximumFractionDigits: 0,
    }).format(amount);

  return (
    <section className="trips-page">
      <div className="section-heading">
        <div>
          <h2>My Trips 🧳</h2>
          <p>All your saved travel plans in one place.</p>
        </div>
        <button className="refresh-button" onClick={loadTrips}>
          ↻ Refresh
        </button>
      </div>

      <div className="trip-stats">
        <div className="trip-stat">
          <span>Total trips</span>
          <strong>{trips.length}</strong>
        </div>
        <div className="trip-stat">
          <span>Upcoming trips</span>
          <strong>{trips.filter(t => t.start_date >= new Date().toISOString().slice(0, 10)).length}</strong>
        </div>
        <div className="trip-stat">
          <span>Total planned budget</span>
          <strong>
            {formatMoney(
              trips.reduce((sum, trip) => sum + Number(trip.budget), 0),
              "INR"
            )}
          </strong>
        </div>
      </div>

      {loading && <p className="trip-message">Loading your trips...</p>}

      {error && (
        <div className="trip-message error-message" role="alert">
          {error}
          <button onClick={loadTrips}>Try again</button>
        </div>
      )}

      {!loading && !error && trips.length === 0 && (
        <div className="empty-trips">
          <span>✈️</span>
          <h3>No trips planned yet</h3>
          <p>Your next adventure starts with creating your first trip.</p>
        </div>
      )}

      <div className="my-trips-grid">
        {trips.map((trip) => (
          <article className="my-trip-card" key={trip.id}>
            <div className="trip-card-top">
              <span className="trip-status">{trip.status}</span>
              <span>🗺️</span>
            </div>

            <h3>{trip.origin} → {trip.destination}</h3>
            <p className="trip-dates">
              📅 {formatDate(trip.start_date)} – {formatDate(trip.end_date)}
            </p>
            <p>👥 {trip.travelers} traveler(s)</p>

            <div className="trip-budget">
              <span>Total budget</span>
              <strong>{formatMoney(Number(trip.budget), trip.currency)}</strong>
            </div>

            <div className="trip-actions">
              <button onClick={() => setSelectedTrip(trip)}>
                View details
              </button>
              <button
                className="delete-trip-button"
                disabled={deleting === trip.id}
                onClick={() => deleteTrip(trip.id)}
              >
                {deleting === trip.id ? "Deleting..." : "Delete"}
              </button>
            </div>
          </article>
        ))}
      </div>

      {selectedTrip && (
        <div className="trip-modal-backdrop" onClick={() => setSelectedTrip(null)}>
          <div
            className="trip-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="trip-modal-title"
            onClick={(e) => e.stopPropagation()}
          >
            <button className="modal-close" onClick={() => setSelectedTrip(null)}>
              ✕
            </button>
            <h2 id="trip-modal-title">
              {selectedTrip.origin} → {selectedTrip.destination}
            </h2>
            <p>{selectedTrip.summary}</p>
            <p><strong>Dates:</strong> {formatDate(selectedTrip.start_date)} – {formatDate(selectedTrip.end_date)}</p>
            <p><strong>Travelers:</strong> {selectedTrip.travelers}</p>
            <p><strong>Budget:</strong> {formatMoney(Number(selectedTrip.budget), selectedTrip.currency)}</p>
            <p><strong>Per person:</strong> {formatMoney(Number(selectedTrip.estimated_budget_per_person), selectedTrip.currency)}</p>
            <p><strong>Status:</strong> {selectedTrip.status}</p>
            <p><strong>Preferences:</strong> {selectedTrip.preferences?.join(", ") || "None"}</p>
            <p className="trip-id">Trip ID: {selectedTrip.id}</p>
          </div>
        </div>
      )}
    </section>
  );
}

export default MyTrips;
