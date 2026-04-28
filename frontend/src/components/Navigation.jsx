import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const Navigation = () => {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/market-data', label: 'Datos Mercado', icon: '📈' },
    { path: '/analysis', label: 'Análisis', icon: '🔍' },
    { path: '/signals', label: 'Señales', icon: '🚦' }
  ]

  return (
    <nav className="navigation">
      <div className="nav-brand">
        <h2>MT5 Market Data</h2>
      </div>
      
      <ul className="nav-menu">
        {navItems.map(item => (
          <li key={item.path} className="nav-item">
            <Link 
              to={item.path} 
              className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
      
      <div className="nav-footer">
        <div className="system-status">
          <span className="status-indicator">🟢</span>
          <span>Sistema Activo</span>
        </div>
      </div>
    </nav>
  )
}

export default Navigation