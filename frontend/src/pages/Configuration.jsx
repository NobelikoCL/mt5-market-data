import React, { useState, useEffect } from 'react'
import { api } from '../services/api'

const Configuration = () => {
  const [config, setConfig] = useState({
    bot_token: '',
    chat_id: '',
    enabled: false
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [testing, setTesting] = useState(false)
  const [message, setMessage] = useState(null)

  useEffect(() => {
    loadConfig()
  }, [])

  const loadConfig = async () => {
    try {
      setLoading(true)
      const response = await api.getTelegramConfig()
      setConfig(response.data)
    } catch (err) {
      console.error('Error loading config:', err)
      setMessage({ type: 'error', text: 'Error al cargar la configuración' })
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async (e) => {
    e.preventDefault()
    try {
      setSaving(true)
      const response = await api.updateTelegramConfig(config)
      setConfig(response.data)
      setMessage({ type: 'success', text: 'Configuración guardada correctamente' })
    } catch (err) {
      console.error('Error saving config:', err)
      setMessage({ type: 'error', text: 'Error al guardar la configuración' })
    } finally {
      setSaving(false)
      setTimeout(() => setMessage(null), 5000)
    }
  }

  const handleTest = async () => {
    try {
      setTesting(true)
      const response = await api.testTelegramMessage()
      setMessage({ type: 'success', text: response.data.status || 'Mensaje de prueba enviado' })
    } catch (err) {
      console.error('Test error:', err)
      const errorMsg = err.response?.data?.error || 'Error al enviar mensaje de prueba'
      setMessage({ type: 'error', text: errorMsg })
    } finally {
      setTesting(false)
      setTimeout(() => setMessage(null), 5000)
    }
  }

  if (loading) {
    return (
      <div className="loading-state">
        <div className="spinner"></div>
        <div className="loading-text">Cargando configuración...</div>
      </div>
    )
  }

  return (
    <div className="config-container">
      <div className="dashboard-header">
        <h1>
          <span>⚙️</span> Configuración de Notificaciones
        </h1>
      </div>

      <div className="section-card" style={{ maxWidth: '600px', margin: '0 auto' }}>
        <div className="section-header">
          <div className="section-title">🤖 Telegram Bot</div>
        </div>

        {message && (
          <div className={`alert alert-${message.type}`} style={{
            padding: '12px',
            borderRadius: '8px',
            marginBottom: '20px',
            backgroundColor: message.type === 'success' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)',
            color: message.type === 'success' ? '#4ade80' : '#f87171',
            border: `1px solid ${message.type === 'success' ? '#22c55e' : '#ef4444'}`
          }}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSave}>
          <div className="form-group" style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#94a3b8' }}>Bot Token</label>
            <input
              type="password"
              className="search-input"
              style={{ width: '100%', padding: '12px' }}
              value={config.bot_token}
              onChange={(e) => setConfig({ ...config, bot_token: e.target.value })}
              placeholder="123456789:ABCDEF..."
            />
            <small style={{ color: '#64748b', fontSize: '0.8rem' }}>Obtén tu token con @BotFather</small>
          </div>

          <div className="form-group" style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#94a3b8' }}>Chat ID (Grupo)</label>
            <input
              type="text"
              className="search-input"
              style={{ width: '100%', padding: '12px' }}
              value={config.chat_id}
              onChange={(e) => setConfig({ ...config, chat_id: e.target.value })}
              placeholder="-100123456789"
            />
            <small style={{ color: '#64748b', fontSize: '0.8rem' }}>ID del grupo o canal donde se enviarán las alertas</small>
          </div>

          <div className="form-group" style={{ marginBottom: '30px', display: 'flex', alignItems: 'center' }}>
            <label className="switch" style={{ position: 'relative', display: 'inline-block', width: '50px', height: '24px', marginRight: '12px' }}>
              <input 
                type="checkbox" 
                checked={config.enabled}
                onChange={(e) => setConfig({ ...config, enabled: e.target.checked })}
                style={{ opacity: 0, width: 0, height: 0 }}
              />
              <span style={{
                position: 'absolute', cursor: 'pointer', top: 0, left: 0, right: 0, bottom: 0,
                backgroundColor: config.enabled ? '#22c55e' : '#334155',
                transition: '.4s', borderRadius: '34px'
              }}>
                <span style={{
                  position: 'absolute', content: '""', height: '18px', width: '18px', left: config.enabled ? '28px' : '4px', bottom: '3px',
                  backgroundColor: 'white', transition: '.4s', borderRadius: '50%'
                }}></span>
              </span>
            </label>
            <span style={{ color: config.enabled ? '#4ade80' : '#94a3b8' }}>
              {config.enabled ? 'Notificaciones Activadas' : 'Notificaciones Desactivadas'}
            </span>
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            <button 
              type="submit" 
              className="btn btn-primary" 
              style={{ flex: 2 }}
              disabled={saving}
            >
              {saving ? 'Guardando...' : '💾 Guardar Configuración'}
            </button>
            <button 
              type="button" 
              className="btn btn-outline" 
              style={{ flex: 1 }}
              onClick={handleTest}
              disabled={testing || !config.bot_token || !config.chat_id}
            >
              {testing ? '...' : '🔔 Probar'}
            </button>
          </div>
        </form>
      </div>

      <div className="section-card" style={{ maxWidth: '600px', margin: '20px auto', backgroundColor: 'rgba(30, 41, 59, 0.5)' }}>
        <div className="section-title" style={{ fontSize: '1rem', marginBottom: '10px' }}>ℹ️ Ayuda</div>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: '1.5' }}>
          Para recibir alertas en un grupo:<br />
          1. Crea un bot con <b>@BotFather</b> y copia el Token.<br />
          2. Crea un grupo de Telegram y añade a tu bot como administrador.<br />
          3. Envía un mensaje en el grupo y usa un bot como <b>@GetIDBot</b> para obtener el Chat ID (suele empezar con -100).<br />
          4. Ingresa los datos arriba y activa las notificaciones.
        </p>
      </div>
    </div>
  )
}

export default Configuration
