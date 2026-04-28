import React from 'react'

const MarketOverview = ({ symbols, marketData }) => {
  if (!symbols || symbols.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Resumen del Mercado</h2>
        <div className="text-center text-gray-500 py-8">
          No hay símbolos disponibles
        </div>
      </div>
    )
  }

  const getSymbolStatus = (symbol) => {
    // Simulación de estado del mercado
    const statuses = ['ALZA', 'BAJA', 'ESTABLE']
    return statuses[Math.floor(Math.random() * statuses.length)]
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'ALZA': return 'text-green-600'
      case 'BAJA': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">Resumen del Mercado</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {symbols.slice(0, 6).map(symbol => (
          <div key={symbol.id} className="p-4 border rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <div className="font-semibold">{symbol.name}</div>
              <div className={`text-sm ${getStatusColor(getSymbolStatus(symbol))}`}>
                {getSymbolStatus(symbol)}
              </div>
            </div>
            
            <div className="text-sm text-gray-600 mb-2">{symbol.description}</div>
            
            <div className="text-xs text-gray-500">
              Categoría: {symbol.category}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 text-center">
        <div className="text-sm text-gray-600">
          {symbols.length} símbolos disponibles
        </div>
      </div>
    </div>
  )
}

export default MarketOverview