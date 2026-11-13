

interface SidebarProps {
  activePage: string;
  onNavigate: (page: string) => void;
}

function Sidebar({ activePage, onNavigate }: SidebarProps) {
  const navigation = [
    { name: "Dashboard", icon: "🏠" },
    { name: "My Trips", icon: "🧳" },
    { name: "Explore", icon: "🌍" },
    { name: "Bookings", icon: "🎫" },
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-icon">✈</span>
        <span>PlanMyTrip</span>
      </div>

      <p className="sidebar-label">MENU</p>

      <nav>
        {navigation.map((item) => (
          <button
            key={item.name}
            type="button"
            onClick={() => onNavigate(item.name)}
            className={`nav-item ${activePage === item.name ? "active" : ""}`}
          >
            <span>{item.icon}</span>
            <span>{item.name}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">⚙️ Settings</div>
    </aside>
  );
}

export default Sidebar;

