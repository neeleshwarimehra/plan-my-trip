
import Sidebar from "./components/Sidebar";
import TripSearch from "./components/TripSearch";
import DestinationCard from "./components/DestinationCard";
import "./App.css";

const destinations = [
  {
    name: "Goa",
    country: "India",
    description: "Beaches, sunsets and coastal adventures.",
    image: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=700",
    price: "₹8,000",
  },
  {
    name: "Manali",
    country: "Himachal Pradesh",
    description: "Mountains, snow and beautiful valleys.",
    image: "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=700",
    price: "₹6,500",
  },
  {
    name: "Jaipur",
    country: "Rajasthan",
    description: "Royal palaces and rich cultural heritage.",
    image: "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700",
    price: "₹5,000",
  },
];

function App() {
  return (
    <div className="app-layout">
      <Sidebar activePage="Dashboard" />

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="welcome-label">YOUR TRAVEL COMPANION</span>
            <h1>Explore the world 🌍</h1>
          </div>

          <div className="profile">
            <span>👤</span>
            <span>Traveler</span>
          </div>
        </header>

        <TripSearch />

        <section className="destinations-section">
          <div className="section-heading">
            <div>
              <h2>Popular destinations</h2>
              <p>Discover places worth exploring.</p>
            </div>
            <span>Explore more →</span>
          </div>

          <div className="destination-grid">
            {destinations.map((destination) => (
              <DestinationCard
                key={destination.name}
                {...destination}
              />
            ))}
          </div>
        </section>

        <footer className="app-footer">
          PlanMyTrip © 2026 · Your AI travel companion
        </footer>
      </main>
    </div>
  );
}

export default App;
