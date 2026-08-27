import { Activity, Database, Info, Layers3 } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

export function AppShell() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark"><Layers3 size={19} strokeWidth={2.4} /></div>
          <div><strong>RetailFlow</strong><span>Consola de operaciones</span></div>
        </div>
        <div className="sidebar-label">Espacio de trabajo</div>
        <nav className="primary-nav" aria-label="Navegación principal">
          <NavLink to="/" end className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}><Activity size={17} />Nueva ejecución</NavLink>
          <NavLink to="/about" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}><Info size={17} />Arquitectura</NavLink>
        </nav>
        <div className="sidebar-footer">
          <div className="connection-dot"><span />Conexión AWS</div>
          <div className="region-label"><Database size={14} />us-east-1 · dev</div>
        </div>
      </aside>
      <main className="main-content">
        <header className="topbar">
          <div><span className="eyebrow">RETAILFLOW / OPERACIONES DE DATOS</span><span className="topbar-title">ETL Serverless</span></div>
          <span className="environment-chip"><span />DEV</span>
        </header>
        <div className="page-content"><Outlet /></div>
      </main>
    </div>
  );
}
