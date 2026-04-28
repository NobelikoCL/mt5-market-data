import React, { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Configuration from './pages/Configuration'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="app">
      {/* Sidebar / Navigation */}
      <nav className="main-nav">
        <div className="nav-logo">
          <span className="logo-icon">💹</span>
          <span className="logo-text">MT5 Monitor</span>
        </div>
        <div className="nav-links">
          <button 
            className={'nav-link ' + (activeTab === 'dashboard' ? 'active' : '')} 
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Dashboard
          </button>
          <button 
            className={'nav-link ' + (activeTab === 'config' ? 'active' : '')} 
            onClick={() => setActiveTab('config')}
          >
            ⚙️ Configuración
          </button>
        </div>
      </nav>

      <main className="main-content">
        {activeTab === 'dashboard' ? <Dashboard /> : <Configuration />}
      </main>
    </div>
  )
}

export default App
