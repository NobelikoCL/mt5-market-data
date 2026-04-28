import React from 'react'

const SymbolList = ({ symbols, selectedSymbol, onSymbolSelect }) => {
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h2 className="text-lg font-semibold mb-4">Símbolos Disponibles</h2>
      
      <div className="space-y-2">
        {symbols.map(symbol => (
          <div
            key={symbol.id}
            className={`p-3 rounded cursor-pointer transition-colors ${
              selectedSymbol?.id === symbol.id
                ? 'bg-blue-100 border-l-4 border-blue-500'
                : 'hover:bg-gray-100'
            }`}
            onClick={() => onSymbolSelect(symbol)}
          >
            <div className="font-medium">{symbol.name}</div>
            <div className="text-sm text-gray-600">{symbol.description}</div>
            <div className="text-xs text-gray-400">{symbol.category}</div>
          </div>
        ))}
      </div>
      
      {symbols.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No hay símbolos disponibles
        </div>
      )}
    </div>
  )
}

export default SymbolList