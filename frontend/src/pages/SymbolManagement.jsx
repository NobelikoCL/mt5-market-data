import React, { useState, useEffect } from 'react';
import { marketAPI } from '../services/api';

const SymbolManagement = () => {
  const [symbols, setSymbols] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [timeframe, setTimeframe] = useState('M15');
  const [daysBack, setDaysBack] = useState(7);

  useEffect(() => {
    fetchSymbols();
  }, []);

  const fetchSymbols = async () => {
    try {
      setLoading(true);
      const response = await marketAPI.getSymbols();
      setSymbols(response.data.results || response.data);
    } catch (err) {
      setError('Error al cargar símbolos');
    } finally {
      setLoading(false);
    }
  };

  const handleFetchMT5Symbols = async () => {
    try {
      setLoading(true);
      const response = await marketAPI.fetchFromMT5();
      setSymbols(response.data.symbols.map(name => ({ name })));
      setError('');
    } catch (err) {
      setError('Error al obtener símbolos de MT5');
    } finally {
      setLoading(false);
    }
  };

  const handleFetchHistoricalData = async () => {
    if (!selectedSymbol) {
      setError('Selecciona un símbolo primero');
      return;
    }

    try {
      setLoading(true);
      await marketAPI.fetchHistoricalData(selectedSymbol, timeframe, daysBack);
      setError('');
      alert(`Datos históricos de ${selectedSymbol} descargados exitosamente`);
    } catch (err) {
      setError('Error al obtener datos históricos');
    } finally {
      setLoading(false);
    }
  };

  const timeframes = [
    { value: 'M1', label: '1 Minuto' },
    { value: 'M5', label: '5 Minutos' },
    { value: 'M15', label: '15 Minutos' },
    { value: 'H1', label: '1 Hora' },
    { value: 'H4', label: '4 Horas' },
    { value: 'D1', label: 'Diario' },
  ];

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">Cargando símbolos...</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Gestión de Símbolos</h1>
        <p>Administra los símbolos financieros disponibles</p>
      </div>

      {error && (
        <div className="error">{error}</div>
      )}

      <div className="grid">
        <div className="card">
          <h3>Símbolos Disponibles</h3>
          <p>{symbols.length} símbolos en total</p>
          <button 
            className="btn" 
            onClick={handleFetchMT5Symbols}
            disabled={loading}
          >
            {loading ? 'Cargando...' : 'Obtener desde MT5'}
          </button>
        </div>

        <div className="card">
          <h3>Datos Históricos</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <select 
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              style={{ padding: '0.5rem', borderRadius: '0.375rem', border: '1px solid #334155' }}
            >
              <option value="">Selecciona un símbolo</option>
              {symbols.map(symbol => (
                <option key={symbol.name} value={symbol.name}>
                  {symbol.name}
                </option>
              ))}
            </select>

            <select 
              value={timeframe}
              onChange={(e) => setTimeframe(e.target.value)}
              style={{ padding: '0.5rem', borderRadius: '0.375rem', border: '1px solid #334155' }}
            >
              {timeframes.map(tf => (
                <option key={tf.value} value={tf.value}>
                  {tf.label}
                </option>
              ))}
            </select>

            <input 
              type="number" 
              value={daysBack}
              onChange={(e) => setDaysBack(parseInt(e.target.value))}
              placeholder="Días hacia atrás"
              style={{ padding: '0.5rem', borderRadius: '0.375rem', border: '1px solid #334155' }}
            />

            <button 
              className="btn" 
              onClick={handleFetchHistoricalData}
              disabled={loading || !selectedSymbol}
            >
              {loading ? 'Descargando...' : 'Obtener Datos'}
            </button>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '2rem' }}>
        <h3>Lista de Símbolos</h3>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', 
          gap: '1rem',
          maxHeight: '400px',
          overflowY: 'auto'
        }}>
          {symbols.map(symbol => (
            <div key={symbol.id || symbol.name} style={{ 
              background: '#334155', 
              padding: '1rem', 
              borderRadius: '0.375rem',
              border: selectedSymbol === symbol.name ? '2px solid #3b82f6' : 'none'
            }}>
              <div style={{ fontWeight: 'bold' }}>{symbol.name}</div>
              {symbol.description && (
                <div style={{ fontSize: '0.875rem', opacity: 0.8, marginTop: '0.5rem' }}>
                  {symbol.description}
                </div>
              )}
              {symbol.active !== undefined && (
                <div style={{ 
                  fontSize: '0.75rem', 
                  color: symbol.active ? '#10b981' : '#ef4444',
                  marginTop: '0.5rem'
                }}>
                  {symbol.active ? 'Activo' : 'Inactivo'}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SymbolManagement;