import React, { useState, useEffect } from 'react'
import { marketDataAPI } from '../services/api'
import SignalCard from '../components/SignalCard'

const Signals = () => {
  const [signals, setSignals] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    loadSignals()
  }, [filter])

  const loadSignals = async () => {
    try {
      setLoading(true)
      const response = await marketDataAPI.getSignals(filter)
      setSignals(response.data)
    } catch (error) {
      console.error('Error loading signals:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredSignals = signals.filter(signal => {
    if (filter === 'all') return true
    return signal.signal_type === filter
  })

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Cargando señales...</div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Señales de Trading</h1>
        
        <div className="flex space-x-4">
          <select 
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="all">Todas</option>
            <option value="BUY">Compra</option>
            <option value="SELL">Venta</option>
            <option value="BREAKOUT_UP">Ruptura Alcista</option>
            <option value="BREAKOUT_DOWN">Ruptura Bajista</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSignals.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <div className="text-gray-500 text-lg">No hay señales disponibles</div>
            <div className="text-sm text-gray-400 mt-2">
              El sistema está procesando datos del mercado
            </div>
          </div>
        ) : (
          filteredSignals.map(signal => (
            <SignalCard key={signal.id} signal={signal} />
          ))
        )}
      </div>
    </div>
  )
}

export default Signals