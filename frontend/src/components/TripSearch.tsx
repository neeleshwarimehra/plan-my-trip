
import { useState } from "react";

function TripSearch() {
  const [origin, setOrigin] = useState("Indore");
  const [destination, setDestination] = useState("");
  const [travelers, setTravelers] = useState(2);
  const [budget, setBudget] = useState(35000);

  function handleSearch() {
    if (!destination.trim()) {
      alert("Please enter your destination");
      return;
    }

    alert(
      `Planning a trip from ${origin} to ${destination} for ${travelers} travelers. Budget: ₹${budget}`
    );
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

        <button onClick={handleSearch}>
          ✨ Plan My Trip
        </button>
      </div>
    </section>
  );
}

export default TripSearch;
