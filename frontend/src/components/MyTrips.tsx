
import { useCallback, useEffect, useState } from "react";

const API_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

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
  next_steps?: string[];
}

interface TripEditForm {
  origin: string;
  destination: string;
  start_date: string;
  end_date: string;
  travelers: number;
  budget: number;
}

function MyTrips() {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedTrip, setSelectedTrip] = useState<Trip | null>(null);
  const [deleting, setDeleting] = useState("");
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [editError, setEditError] = useState("");

  const [editForm, setEditForm] = useState<TripEditForm>({
    origin: "",
    destination: "",
    start_date: "",
    end_date: "",
    travelers: 1,
    budget: 1,
  });

  // Fetch all trips
  const loadTrips = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/api/trips?skip=0&limit=100`
      );

      if (!response.ok) {
        throw new Error("Unable to load trips.");
      }

      const data: Trip[] = await response.json();

      setTrips(data);

      // Keep selected trip synchronized with refreshed data
      setSelectedTrip((current) =>
        current
          ? data.find((trip) => trip.id === current.id) || null
          : null
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTrips();
  }, [loadTrips]);

  // Delete trip
  async function deleteTrip(id: string) {
    if (!window.confirm("Are you sure you want to delete this trip?")) {
      return;
    }

    setDeleting(id);

    try {
      const response = await fetch(
        `${API_URL}/api/trips/${id}`,
        { method: "DELETE" }
      );

      if (!response.ok) {
        throw new Error("Unable to delete trip.");
      }

      setTrips((current) =>
        current.filter((trip) => trip.id !== id)
      );

      if (selectedTrip?.id === id) {
        setSelectedTrip(null);
        setEditing(false);
      }
    } catch (err) {
      alert(
        err instanceof Error
          ? err.message
          : "Delete failed."
      );
    } finally {
      setDeleting("");
    }
  }

  // Start editing
  function startEditing() {
    if (!selectedTrip) return;

    setEditForm({
      origin: selectedTrip.origin,
      destination: selectedTrip.destination,
      start_date: selectedTrip.start_date,
      end_date: selectedTrip.end_date,
      travelers: selectedTrip.travelers,
      budget: Number(selectedTrip.budget),
    });

    setEditError("");
    setEditing(true);
  }

  // Update trip
  async function saveTripChanges(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!selectedTrip) return;

    setEditError("");

    if (
      !editForm.origin.trim() ||
      !editForm.destination.trim()
    ) {
      setEditError("Origin and destination are required.");
      return;
    }

    if (
      editForm.origin.trim().toLowerCase() ===
      editForm.destination.trim().toLowerCase()
    ) {
      setEditError("Origin and destination must be different.");
      return;
    }

    if (editForm.end_date < editForm.start_date) {
      setEditError("End date must be on or after start date.");
      return;
    }

    if (
      !Number.isInteger(editForm.travelers) ||
      editForm.travelers < 1 ||
      editForm.travelers > 20 ||
      !Number.isFinite(editForm.budget) ||
      editForm.budget <= 0
    ) {
      setEditError("Please enter valid travelers and budget.");
      return;
    }

    setSaving(true);

    try {
      const response = await fetch(
        `${API_URL}/api/trips/${selectedTrip.id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ...editForm,
            origin: editForm.origin.trim(),
            destination: editForm.destination.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Unable to update trip."
        );
      }

      setTrips((current) =>
        current.map((trip) =>
          trip.id === data.id ? data : trip
        )
      );

      setSelectedTrip(data);
      setEditing(false);
    } catch (err) {
      setEditError(
        err instanceof Error
          ? err.message
          : "Unable to save changes."
      );
    } finally {
      setSaving(false);
    }
  }

  // Format dates
  const formatDate = (date: string) =>
    new Date(`${date}T00:00:00`).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });

  // Format currency
  const formatMoney = (amount: number, currency: string) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: currency || "INR",
      maximumFractionDigits: 0,
    }).format(amount);

  const upcomingTrips = trips.filter(
    (trip) =>
      trip.start_date >= new Date().toISOString().slice(0, 10)
  ).length;

  const totalBudget = trips.reduce(
    (sum, trip) => sum + Number(trip.budget),
    0
  );

  return (
    <section className="trips-page">

      {/* Page heading */}
      <div className="section-heading">
        <div>
          <h2>My Trips 🧳</h2>
          <p>All your saved travel plans in one place.</p>
        </div>

        <button
          className="refresh-button"
          onClick={loadTrips}
          disabled={loading}
        >
          {loading ? "Loading..." : "↻ Refresh"}
        </button>
      </div>

      {/* Statistics */}
      <div className="trip-stats">
        <div className="trip-stat">
          <span>Total trips</span>
          <strong>{trips.length}</strong>
        </div>

        <div className="trip-stat">
          <span>Upcoming trips</span>
          <strong>{upcomingTrips}</strong>
        </div>

        <div className="trip-stat">
          <span>Total planned budget</span>
          <strong>{formatMoney(totalBudget, "INR")}</strong>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <p className="trip-message">
          Loading your trips...
        </p>
      )}

      {/* Error */}
      {error && (
        <div className="trip-message error-message" role="alert">
          {error}
          <button onClick={loadTrips}>
            Try again
          </button>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && trips.length === 0 && (
        <div className="empty-trips">
          <span>✈️</span>
          <h3>No trips planned yet</h3>
          <p>
            Your next adventure starts with creating your first trip.
          </p>
        </div>
      )}

      {/* Trip cards */}
      {!loading && !error && (
        <div className="my-trips-grid">
          {trips.map((trip) => (
            <article className="my-trip-card" key={trip.id}>
              <div className="trip-card-top">
                <span className="trip-status">
                  {trip.status}
                </span>
                <span>🗺️</span>
              </div>

              <h3>
                {trip.origin} → {trip.destination}
              </h3>

              <p className="trip-dates">
                📅 {formatDate(trip.start_date)} –{" "}
                {formatDate(trip.end_date)}
              </p>

              <p>👥 {trip.travelers} traveler(s)</p>

              <div className="trip-budget">
                <span>Total budget</span>
                <strong>
                  {formatMoney(
                    Number(trip.budget),
                    trip.currency
                  )}
                </strong>
              </div>

              <div className="trip-actions">
                <button
                  onClick={() => {
                    setSelectedTrip(trip);
                    setEditing(false);
                  }}
                >
                  View details
                </button>

                <button
                  className="delete-trip-button"
                  disabled={deleting === trip.id}
                  onClick={() => deleteTrip(trip.id)}
                >
                  {deleting === trip.id
                    ? "Deleting..."
                    : "Delete"}
                </button>
              </div>
            </article>
          ))}
        </div>
      )}

      {/* Trip details modal */}
      {selectedTrip && (
        <div
          className="trip-modal-backdrop"
          onClick={() => {
            setSelectedTrip(null);
            setEditing(false);
          }}
        >
          <div
            className="trip-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="trip-modal-title"
            onClick={(event) => event.stopPropagation()}
          >
            <button
              className="modal-close"
              onClick={() => {
                setSelectedTrip(null);
                setEditing(false);
              }}
            >
              ✕
            </button>

            <h2 id="trip-modal-title">
              {selectedTrip.origin} → {selectedTrip.destination}
            </h2>

            {!editing ? (
              <>
                <p>{selectedTrip.summary}</p>

                <p>
                  <strong>Dates:</strong>{" "}
                  {formatDate(selectedTrip.start_date)} –{" "}
                  {formatDate(selectedTrip.end_date)}
                </p>

                <p>
                  <strong>Travelers:</strong>{" "}
                  {selectedTrip.travelers}
                </p>

                <p>
                  <strong>Budget:</strong>{" "}
                  {formatMoney(
                    Number(selectedTrip.budget),
                    selectedTrip.currency
                  )}
                </p>

                <p>
                  <strong>Per person:</strong>{" "}
                  {formatMoney(
                    Number(selectedTrip.estimated_budget_per_person),
                    selectedTrip.currency
                  )}
                </p>

                <p>
                  <strong>Status:</strong>{" "}
                  {selectedTrip.status}
                </p>

                <p>
                  <strong>Preferences:</strong>{" "}
                  {selectedTrip.preferences?.join(", ") || "None"}
                </p>

                <p className="trip-id">
                  Trip ID: {selectedTrip.id}
                </p>

                <button onClick={startEditing}>
                  ✏️ Edit Trip
                </button>
              </>
            ) : (
              <form
                className="trip-edit-form"
                onSubmit={saveTripChanges}
              >
                <h3>Edit Your Trip</h3>

                {editError && (
                  <p className="error-message" role="alert">
                    {editError}
                  </p>
                )}

                <label>
                  Origin
                  <input
                    required
                    minLength={2}
                    maxLength={100}
                    value={editForm.origin}
                    onChange={(event) =>
                      setEditForm({
                        ...editForm,
                        origin: event.target.value,
                      })
                    }
                  />
                </label>

                <label>
                  Destination
                  <input
                    required
                    minLength={2}
                    maxLength={100}
                    value={editForm.destination}
                    onChange={(event) =>
                      setEditForm({
                        ...editForm,
                        destination: event.target.value,
                      })
                    }
                  />
                </label>

                <label>
                  Start Date
                  <input
                    required
                    type="date"
                    value={editForm.start_date}
                    onChange={(event) =>
                      setEditForm({
                        ...editForm,
                        start_date: event.target.value,
                      })
                    }
                  />
                </label>

                <label>
                  End Date
                  <input
                    required
                    type="date"
                    min={editForm.start_date}
                    value={editForm.end_date}
                    onChange={(event) =>
                      setEditForm({
                        ...editForm,
                        end_date: event.target.value,
                      })
                    }
                  />
                </label>

                <label>
                  Travelers
                  <input
                    required
                    type="number"
                    min="1"
                    max="20"
                    value={editForm.travelers}
                    onChange={(event) =>
                      setEditForm({
                        ...editForm,
                        travelers: Number(event.target.value),
                      })
                    }
                  />
                </label>

                <label>
                  Budget (₹)
                  <input
                    required
                    type="number"
                    min="1"
                    step="0.01"
                    value={editForm.budget}
                    onChange={(event) =>
                      setEditForm({
                        ...editForm,
                        budget: Number(event.target.value),
                      })
                    }
                  />
                </label>

                <div className="trip-actions">
                  <button
                    type="submit"
                    disabled={saving}
                  >
                    {saving ? "Saving..." : "Save Changes"}
                  </button>

                  <button
                    type="button"
                    disabled={saving}
                    onClick={() => {
                      setEditing(false);
                      setEditError("");
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </section>
  );
}

export default MyTrips;
