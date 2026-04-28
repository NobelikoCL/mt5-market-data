import React, { useState, useEffect } from 'react';
import { marketAPI } from '../services/api';

const SignalAnalysis = () => {
  const [signals, setSignals] = useState([]);
  const [symbols, setSymbols] = useState([]);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [selectedTimeframe, setSelectedTimeframe] = useState('M15');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [signalsResponse, symbolsResponse] = await Promise.all([
        marketAPI.getSignals(),
        marketAPI.getSymbols()
      ]);
      
      setSignals(signalsResponse.data.results || signalsResponse.data);
      setSymbols(symbolsResponse.data.results || symbolsResponse.data);
    } catch (err) {
      setError('Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeSignals = async () => {
    if (!selectedSymbol) {
      setError('Selecciona un símbolo primero');
      return;
    }

    try {
      setAnalyzing(true);
      const response = await marketAPI.analyzeSignals(selectedSymbol, selectedTimeframe);
      
      if (response.data.signals && response.data.signals.length > 0) {
        setSignals(prev => [...response.data.signals, ...prev]);
        setError('');
        alert(`Se generaron ${response.data.signals.length} señales para ${selectedSymbol}`);
      } else {
        alert('No se encontraron señales significativas');
      }
    } catch (err) {
      setError('Error al analizar señales');
    } finally {
      setAnalyzing(false);
    }
  };

  const getSignalColor = (signalType) => {
    switch (signalType) {
      case 'BUY':
        return '#10b981';
      case 'SELL':
        return '#ef4444';
      case 'BREAKOUT':
        return '#f59e0b';
      case 'REVERSAL':
        return '#8b5cf6';
      default:
        return '#6b7280';
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
        <div className="loading">Cargando señales...</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Análisis de Señales</h1>
        <p>Genera y revisa señales de trading</p>
      </div>

      {error && (
        <div className="error">{error}</div>
      )}

      <div className="grid">
        <div className="card">
          <h3>Análisis de Señales</h3>
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
              value={selectedTimeframe}
              onChange={(e) => setSelectedTimeframe(e.target.value)}
              style={{ padding: '0.5rem', borderRadius: '0.375rem', border: '1px solid #334155' }}
            >
              {timeframes.map(tf => (
                <option key={tf.value} value={tf.value}>
                  {tf.label}
                </option>
              ))}
            </select>

            <button 
              className="btn" 
              onClick={handleAnalyzeSignals}
              disabled={analyzing || !selectedSymbol}
            >
              {analyzing ? 'Analizando...' : 'Generar Señales'}
            </button>
          </div>
        </div>

        <div className="card">
          <h3>Estadísticas</h3>
          <p>Total señales: {signals.length}</p>
          <div style={{ fontSize: '0.875rem' }}>
            <div>BUY: {signals.filter(s => s.signal_type === 'BUY').length}</div>
            <div>SELL: {signals.filter(s => s.signal_type === 'SELL').length}</div>
            <div>BREAKOUT: {signals.filter(s => s.signal_type === 'BREAKOUT').length}</div>
            <div>REVERSAL: {signals.filter(s => s.signal_type === 'REVERSAL').length}</div>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '2rem' }}>
        <h3>Últimas Señales</h3>
        <div style={{ 
          maxHeight: '500px', 
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          {signals.slice(0, 20).map(signal => (
            <div key={signal.id} style={{ 
              background: '#334155', 
              padding: '1rem', 
              borderRadius: '0.375rem',
              borderLeft: `4px solid ${getSignalColor(signal.signal_type)}`
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong style={{ color: getSignalColor(signal.signal_type) }}>
                    {signal.signal_type}
                  </strong>
                  <span style={{ marginLeft: '1rem', opacity: 0.8 }}>
                    {signal.symbol_name || signal.symbol}
                  </span>
                </div>
                <div style={{ fontSize: '0.875rem', opacity: 0.8 }}>
                  {new Date(signal.timestamp).toLocaleString()}
                </div>
              </div>
              
              <div style={{ marginTop: '0.5rem', fontSize: '0.875rem' }}>
                <div>Confianza: <strong>{signal.confidence}%</strong></div>
                <div>Precio: <strong>{signal.price_level}</strong></div>
                <div>Timeframe: {signal.timeframe}</div>
              </div>
              
              {signal.description && (
                <div style={{ marginTop: '0.5rem', fontSize: '0.875rem', opacity: 0.8 }}>
                  {signal.description}
                </div>
              )}
            </div>
          ))}
          
          {signals.length === 0 && (
            <div style={{ textAlign: 'center', padding: '2rem', opacity: 0.6 }}>
              No hay señales disponibles. Genera algunas usando el formulario de arriba.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SignalAnalysis;