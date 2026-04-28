import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = ({ connectionStatus }) => {
  const location = useLocation();
  
  const getStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'Conectado';
      case 'error':
        return 'Error de conexión';
      default:
        return 'Verificando...';
    }
  };

  const getStatusClass = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'status-connected';
      case 'error':
        return 'status-error';
      default:
        return 'status-checking';
    }
  };

  return (
    <header className="header">
      <div className="container">
        <nav className="nav">
          <div className="logo">
            <span>📊 MT5 Market Analyzer</span>
            <span style={{ marginLeft: '1rem', fontSize: '0.875rem', opacity: 0.8 }}>
              <span className={`status-indicator ${getStatusClass()}`}></span>
              {getStatusText()}
            </span>
          </div>
          
          <div className="nav-links">
            <Link 
              to="/" 
              className={location.pathname === '/' ? 'active' : ''}
            >
              Dashboard
            </Link>
            <Link 
              to="/symbols" 
              className={location.pathname === '/symbols' ? 'active' : ''}
            >
              Símbolos
            </Link>
            <Link 
              to="/signals" 
              className={location.pathname === '/signals' ? 'active' : ''}
            >
              Señales
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
};

export default Header;