import { useState } from "react";
import Sidebar from "./components/Sidebar";
import TripSearch from "./components/TripSearch";
import MyTrips from "./components/MyTrips";
import DestinationCard from "./components/DestinationCard";
import "./App.css";

const destinations = [
  {
    name: "Goa",
    country: "India",
    description: "Beaches, sunsets and coastal adventures.",
    image: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=700",
    price: "₹8,000",
    numericPrice: 15000,
  },
  {
    name: "Manali",
    country: "Himachal Pradesh",
    description: "Mountains, snow and beautiful valleys.",
    image: "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=700",
    price: "₹6,500",
    numericPrice: 12000,
  },
  {
    name: "Jaipur",
    country: "Rajasthan",
    description: "Royal palaces and rich cultural heritage.",
    image: "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700",
    price: "₹5,000",
    numericPrice: 10000,
  },
];

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [selectedDestination, setSelectedDestination] = useState("");
  const [selectedBudget, setSelectedBudget] = useState<number | undefined>(
    undefined
  );

  function handleSelectDestination(destinationName: string, price: string) {
    const parsedPrice = Number(price.replace(/[^0-9]/g, ""));
    setSelectedDestination(destinationName);
    if (parsedPrice > 0) {
      setSelectedBudget(parsedPrice);
    }
    setActivePage("Dashboard");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="app-layout">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="welcome-label">YOUR TRAVEL COMPANION</span>
            <h1>
              {activePage === "Dashboard" ? "Explore the world 🌍" : activePage}
            </h1>
          </div>
          <div className="profile">
            <span>👤</span>
            <span>Traveler</span>
          </div>
        </header>

        {activePage === "Dashboard" && (
          <>
            <TripSearch
              prefilledDestination={selectedDestination}
              prefilledBudget={selectedBudget}
            />

            <section className="destinations-section">
              <div className="section-heading">
                <div>
                  <h2>Popular destinations</h2>
                  <p>Discover places worth exploring.</p>
                </div>
                <button
                  className="text-button"
                  onClick={() => setActivePage("Explore")}
                >
                  Explore more →
                </button>
              </div>

              <div className="destination-grid">
                {destinations.map((destination) => (
                  <DestinationCard
                    key={destination.name}
                    {...destination}
                    onSelect={handleSelectDestination}
                  />
                ))}
              </div>
            </section>
          </>
        )}

        {activePage === "My Trips" && <MyTrips />}

        {activePage === "Explore" && (
          <section className="destinations-section">
            <div className="section-heading">
              <div>
                <h2>Explore destinations 🌍</h2>
                <p>Click → on any destination to plan your trip right away.</p>
              </div>
            </div>
            <div className="destination-grid">
              {destinations.map((destination) => (
                <DestinationCard
                  key={destination.name}
                  {...destination}
                  onSelect={handleSelectDestination}
                />
              ))}
            </div>
          </section>
        )}

        {activePage === "Bookings" && (
          <section className="empty-trips">
            <span>🎫</span>
            <h3>Travel bookings</h3>
            <p>
              Flight, train, bus and hotel booking integrations are coming next.
            </p>
          </section>
        )}

        <footer className="app-footer">
          PlanMyTrip © 2026 · Your AI travel companion
        </footer>
      </main>
    </div>
  );
}

export default App;