import React from 'react'

const AnalysisChart = ({ analysis }) => {
  if (!analysis || analysis.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Análisis Reciente</h2>
        <div className="text-center text-gray-500 py-8">
          No hay análisis disponibles
        </div>
      </div>
    )
  }

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'STRONG_BUY':
      case 'BUY':
        return 'bg-green-100 text-green-800'
      case 'STRONG_SELL':
      case 'SELL':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">Análisis Reciente</h2>
      
      <div className="space-y-4">
        {analysis.slice(0, 5).map(item => (
          <div key={item.id} className="p-4 border rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <div className="font-semibold">{item.symbol.name}</div>
              <div className={`px-2 py-1 rounded text-xs ${getRecommendationColor(item.recommendation)}`}>
                {item.recommendation}
              </div>
            </div>
            
            <div className="text-sm text-gray-600 mb-2">
              Timeframe: {item.timeframe} | 
              RSI: {item.rsi ? parseFloat(item.rsi).toFixed(2) : 'N/A'} | 
              MACD: {item.macd ? parseFloat(item.macd).toFixed(4) : 'N/A'}
            </div>
            
            {item.breakout_detected && (
              <div className="text-xs text-blue-600 mt-2">
                ⚡ Ruptura detectada: {item.breakout_type}
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="mt-4 text-center">
        <div className="text-sm text-gray-600">
          {analysis.length} análisis realizados
        </div>
      </div>
    </div>
  )
}

export default AnalysisChart