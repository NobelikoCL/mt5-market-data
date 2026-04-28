import React, { useState, useEffect, useCallback } from 'react'
import { api } from '../services/api'

const Dashboard = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [lastUpdate, setLastUpdate] = useState(null)
  const [showOnlyActive, setShowOnlyActive] = useState(false)

  const loadDashboard = useCallback(async () => {
    try {
      const response = await api.getDashboard()
      setData(response.data)
      setLastUpdate(new Date())
      setError(null)
    } catch (err) {
      setError('Error cargando datos del dashboard')
      console.error('Dashboard load error:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadDashboard()
    const interval = setInterval(loadDashboard, 30000)
    return () => clearInterval(interval)
  }, [loadDashboard])

  const handleToggleSymbol = async (symbolId) => {
    try {
      await api.toggleSymbol(symbolId)
      loadDashboard()
    } catch (err) {
      console.error('Toggle error:', err)
    }
  }

  const handleAnalyzeAll = async () => {
    try {
      setAnalyzing(true)
      await api.analyzeAll()
      await loadDashboard()
    } catch (err) {
      console.error('Analyze error:', err)
    } finally {
      setAnalyzing(false)
    }
  }

  const formatPrice = (price) => {
    if (!price) return '—'
    const p = parseFloat(price)
    if (p >= 1000) return `$${p.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
    if (p >= 10) return `$${p.toFixed(3)}`
    return `$${p.toFixed(5)}`
  }

  const formatTime = (timestamp) => {
    if (!timestamp) return '—'
    const d = new Date(timestamp)
    const day = d.getDate()
    const month = d.getMonth() + 1
    const hours = d.getHours().toString().padStart(2, '0')
    const mins = d.getMinutes().toString().padStart(2, '0')
    const ampm = d.getHours() >= 12 ? 'p. m.' : 'a. m.'
    return `${day}/${month}, ${hours}:${mins} ${ampm}`
  }

  if (loading) {
    return (
      <div className="loading-state">
        <div className="spinner"></div>
        <div className="loading-text">Cargando dashboard...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-state">
        <div style={{ fontSize: '2rem' }}>⚠️</div>
        <div>{error}</div>
        <button className="btn btn-primary" onClick={loadDashboard}>Reintentar</button>
      </div>
    )
  }

  const { stats, breakouts, symbols } = data

  const filteredSymbols = symbols.filter(s => {
    const matchesSearch = s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         s.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         s.description.toLowerCase().includes(searchTerm.toLowerCase())
    
    if (showOnlyActive) {
      return matchesSearch && s.active
    }
    return matchesSearch
  })

  return (
    <>
      {/* Header */}
      <div className="dashboard-header">
        <h1>
          <span>📊</span> MT5 Market Data — Rupturas H1
        </h1>
        <div className="header-actions">
          {stats.last_heartbeat ? (
            <span className="last-update" style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              <span className="status-dot active" style={{ width: '8px', height: '8px' }}></span>
              Monitor Activo: {formatTime(stats.last_heartbeat)}
            </span>
          ) : (
            <span className="last-update red">Monitor Offline</span>
          )}
          {lastUpdate && (
            <span className="last-update">
              Dashboard: {lastUpdate.toLocaleTimeString()}
            </span>
          )}
          <button
            className={`btn ${stats.telegram_enabled ? 'btn-outline-red' : 'btn-success'}`}
            onClick={async () => {
              try {
                await api.toggleTelegram()
                loadDashboard()
              } catch (err) {
                console.error('Telegram toggle error:', err)
              }
            }}
            title={stats.telegram_enabled ? 'Desactivar notificaciones de Telegram' : 'Activar notificaciones de Telegram'}
          >
            {stats.telegram_enabled ? '🔕 Detener Telegram' : '🔔 Activar Telegram'}
          </button>
          <button
            className="btn btn-primary"
            onClick={handleAnalyzeAll}
            disabled={analyzing}
          >
            {analyzing ? '⏳ Analizando...' : '🔍 Analizar Todos'}
          </button>
          <button className="btn btn-outline" onClick={loadDashboard}>
            ↻ Actualizar
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Activos Monitoreados</div>
          <div className="stat-value blue">{stats.active_symbols}</div>
          <div className="stat-sub">de {stats.total_symbols} totales</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Total Rupturas</div>
          <div className="stat-value amber">{stats.total_breakouts}</div>
          <div className="stat-sub">últimas detectadas</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Rupturas Alcistas</div>
          <div className="stat-value green">{stats.bullish_breakouts}</div>
          <div className="stat-sub">
            <span className="dot green"></span> High Breakouts
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Rupturas Bajistas</div>
          <div className="stat-value red">{stats.bearish_breakouts}</div>
          <div className="stat-sub">
            <span className="dot red"></span> Low Breakouts
          </div>
        </div>
      </div>

      {/* Breakouts Table */}
      <div className="section-card">
        <div className="section-header">
          <div className="section-title">⚡ Rupturas Detectadas</div>
          <div className="section-actions">
            <span className="badge badge-amber">
              {stats.total_breakouts} alertas
            </span>
          </div>
        </div>

        {breakouts.length > 0 ? (
          <div style={{ overflowX: 'auto' }}>
            <table className="breakouts-table">
              <thead>
                <tr>
                  <th>Activo</th>
                  <th>Tipo</th>
                  <th>Precio</th>
                  <th>Máx. Anterior</th>
                  <th>Mín. Anterior</th>
                  <th>Confianza</th>
                  <th>Detección</th>
                </tr>
              </thead>
              <tbody>
                {breakouts.map((b) => (
                  <tr key={b.id}>
                    <td>
                      <span className="symbol-link">
                        {b.symbol_name}
                        <span className="link-icon">🔗</span>
                      </span>
                    </td>
                    <td>
                      <span className={`type-badge ${b.signal_type === 'BREAKOUT_UP' ? 'up' : 'down'}`}>
                        {b.signal_type === 'BREAKOUT_UP' ? '▲ ALZA' : '▼ BAJA'}
                      </span>
                    </td>
                    <td className="price-value">{formatPrice(b.price)}</td>
                    <td className="price-high">{formatPrice(b.high_prev)}</td>
                    <td className="price-low">{formatPrice(b.low_prev)}</td>
                    <td>
                      <span className="badge badge-blue">{b.confidence}%</span>
                    </td>
                    <td className="time-value">
                      <div style={{ fontWeight: '600', color: 'var(--text-primary)' }}>
                        {formatTime(b.updated_at)}
                      </div>
                      <div style={{ fontSize: '0.65rem', opacity: 0.6 }}>
                        Vela: {formatTime(b.timestamp)}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            No se han detectado rupturas activas. Presiona "Analizar Todos" para escanear los activos.
          </div>
        )}
      </div>

      {/* Symbols Grid */}
      <div className="section-card">
        <div className="symbols-header">
          <div className="section-title">
            🪙 Activos Disponibles
          </div>
          <div className="section-actions">
            <span className="badge badge-green">
              {stats.active_symbols} monitoreados / {stats.total_symbols} totales
            </span>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', color: 'var(--text-secondary)', cursor: 'pointer' }}>
              <input 
                type="checkbox" 
                checked={showOnlyActive} 
                onChange={(e) => setShowOnlyActive(e.target.checked)} 
              />
              Solo Activos
            </label>
            <input
              type="text"
              className="search-input"
              placeholder="Buscar activo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div className="symbols-grid">
          {filteredSymbols.map((sym) => (
            <div
              key={sym.id}
              className={`symbol-card ${sym.active ? 'active' : 'inactive'}`}
              onClick={() => handleToggleSymbol(sym.id)}
              title={`Clic para ${sym.active ? 'desactivar' : 'activar'} ${sym.name}`}
            >
              <div>
                <div className="symbol-name" style={{ fontSize: '0.85rem', fontWeight: '700', marginBottom: '2px' }}>{sym.description}</div>
                <div className="symbol-meta" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '6px' }}>
                  {sym.name} • {sym.category}
                </div>
                <div className={`symbol-status ${sym.active ? 'active' : 'inactive'}`}>
                  <span className={`status-dot ${sym.active ? 'active' : 'inactive'}`}></span>
                  {sym.active ? 'ACTIVO' : 'INACTIVO'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  )
}

export default Dashboard