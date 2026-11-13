
interface SidebarProps {
  activePage: string;
}

function Sidebar({ activePage }: SidebarProps) {
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
          <div
            key={item.name}
            className={`nav-item ${
              activePage === item.name ? "active" : ""
            }`}
          >
            <span>{item.icon}</span>
            <span>{item.name}</span>
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span>⚙️</span>
        Settings
      </div>
    </aside>
  );
}

export default Sidebar;
