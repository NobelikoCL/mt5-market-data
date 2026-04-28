import React from 'react'

const SignalCard = ({ signal }) => {
  const getSignalClass = (signalType) => {
    switch (signalType) {
      case 'BUY':
      case 'BREAKOUT_UP':
        return 'buy'
      case 'SELL':
      case 'BREAKOUT_DOWN':
        return 'sell'
      default:
        return 'neutral'
    }
  }

  const getSignalColor = (signalType) => {
    switch (signalType) {
      case 'BUY':
      case 'BREAKOUT_UP':
        return 'bg-green-100 border-green-500 text-green-800'
      case 'SELL':
      case 'BREAKOUT_DOWN':
        return 'bg-red-100 border-red-500 text-red-800'
      default:
        return 'bg-gray-100 border-gray-500 text-gray-800'
    }
  }

  const getSignalIcon = (signalType) => {
    switch (signalType) {
      case 'BUY':
      case 'BREAKOUT_UP':
        return '⬆️'
      case 'SELL':
      case 'BREAKOUT_DOWN':
        return '⬇️'
      default:
        return '➡️'
    }
  }

  const getSignalLabel = (signalType) => {
    switch (signalType) {
      case 'BUY': return 'Compra'
      case 'SELL': return 'Venta'
      case 'BREAKOUT_UP': return 'Ruptura Alcista'
      case 'BREAKOUT_DOWN': return 'Ruptura Bajista'
      default: return 'Sin Señal'
    }
  }

  return (
    <div className={`p-4 rounded-lg border-l-4 ${getSignalColor(signal.signal_type)}`}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{getSignalIcon(signal.signal_type)}</span>
          <div>
            <div className="font-bold text-lg">{signal.symbol.name}</div>
            <div className="text-sm opacity-75">{getSignalLabel(signal.signal_type)}</div>
          </div>
        </div>
        
        <div className="text-right">
          <div className="text-xs opacity-75">
            {new Date(signal.timestamp).toLocaleTimeString()}
          </div>
          <div className="text-xs opacity-75">
            {signal.timeframe}
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <div className="opacity-75">Precio</div>
          <div className="font-semibold">
            {signal.price ? parseFloat(signal.price).toFixed(5) : 'N/A'}
          </div>
        </div>
        
        <div>
          <div className="opacity-75">Volumen</div>
          <div className="font-semibold">
            {signal.volume ? parseFloat(signal.volume).toFixed(2) : 'N/A'}
          </div>
        </div>
      </div>
      
      {signal.confidence && (
        <div className="mt-3">
          <div className="text-xs opacity-75 mb-1">Confianza</div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-500 h-2 rounded-full" 
              style={{ width: `${signal.confidence}%` }}
            ></div>
          </div>
          <div className="text-xs text-right mt-1">{signal.confidence}%</div>
        </div>
      )}
      
      {signal.description && (
        <div className="mt-3 text-sm opacity-75">
          {signal.description}
        </div>
      )}
    </div>
  )
}

export default SignalCard