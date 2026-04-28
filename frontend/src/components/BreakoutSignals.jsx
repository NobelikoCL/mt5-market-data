import React from 'react'

const BreakoutSignals = ({ signals, timeframe }) => {
  const getSignalColor = (direction) => {
    switch (direction) {
      case 'UP':
        return 'bg-green-100 border-green-500'
      case 'DOWN':
        return 'bg-red-100 border-red-500'
      default:
        return 'bg-gray-100 border-gray-500'
    }
  }

  const getSignalIcon = (direction) => {
    switch (direction) {
      case 'UP':
        return '⬆️'
      case 'DOWN':
        return '⬇️'
      default:
        return '➡️'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">
        Señales de Ruptura - {timeframe}
      </h2>
      
      <div className="space-y-4">
        {signals.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No hay señales de ruptura disponibles
          </div>
        ) : (
          signals.map(signal => (
            <div 
              key={signal.id}
              className={`p-4 rounded-lg border-l-4 ${getSignalColor(signal.breakout_direction)}`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-xl">{getSignalIcon(signal.breakout_direction)}</span>
                  <div>
                    <div className="font-semibold">{signal.symbol.name}</div>
                    <div className="text-sm text-gray-600">
                      {signal.breakout_type} - {signal.breakout_direction === 'UP' ? 'Ruptura Alcista' : 'Ruptura Bajista'}
                    </div>
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="text-lg font-bold">
                    {signal.breakout_level ? parseFloat(signal.breakout_level).toFixed(5) : 'N/A'}
                  </div>
                  <div className={`text-sm ${signal.is_valid ? 'text-green-600' : 'text-gray-600'}`}>
                    {signal.is_valid ? '✓ Confirmada' : '⏳ Pendiente'}
                  </div>
                </div>
              </div>
              
              {signal.trading_signal !== 'NONE' && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <div className="text-sm text-gray-600">Señal de Trading:</div>
                  <div className={`font-semibold ${
                    signal.trading_signal === 'BUY' ? 'text-green-600' : 
                    signal.trading_signal === 'SELL' ? 'text-red-600' : 
                    'text-gray-600'
                  }`}>
                    {signal.trading_signal === 'BUY' ? 'COMPRAR' : 
                     signal.trading_signal === 'SELL' ? 'VENDER' : 'ESPERAR'}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default BreakoutSignals