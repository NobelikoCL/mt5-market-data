import React from 'react'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const TechnicalAnalysisChart = ({ analysis, timeframe }) => {
  if (!analysis || analysis.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center text-gray-500 py-8">
          No hay análisis técnico disponible
        </div>
      </div>
    )
  }

  // Agrupar análisis por símbolo
  const symbols = [...new Set(analysis.map(a => a.symbol.name))]
  
  const chartData = {
    labels: symbols,
    datasets: [
      {
        label: 'RSI',
        data: symbols.map(symbol => {
          const symbolAnalysis = analysis.filter(a => a.symbol.name === symbol)
          return symbolAnalysis.length > 0 ? parseFloat(symbolAnalysis[0].rsi) || 0 : 0
        }),
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
      },
      {
        label: 'MACD',
        data: symbols.map(symbol => {
          const symbolAnalysis = analysis.filter(a => a.symbol.name === symbol)
          return symbolAnalysis.length > 0 ? parseFloat(symbolAnalysis[0].macd) || 0 : 0
        }),
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
      },
    ],
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `Análisis Técnico - ${timeframe}`,
      },
    },
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <Bar data={chartData} options={options} />
      
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        {analysis.slice(0, 6).map(item => (
          <div key={item.id} className="p-4 bg-gray-50 rounded">
            <div className="font-semibold">{item.symbol.name}</div>
            <div className="text-sm text-gray-600">
              RSI: {item.rsi ? parseFloat(item.rsi).toFixed(2) : 'N/A'} | 
              MACD: {item.macd ? parseFloat(item.macd).toFixed(4) : 'N/A'}
            </div>
            <div className={`text-sm ${
              item.recommendation === 'BUY' || item.recommendation === 'STRONG_BUY' ? 'text-green-600' :
              item.recommendation === 'SELL' || item.recommendation === 'STRONG_SELL' ? 'text-red-600' :
              'text-gray-600'
            }`}>
              Recomendación: {item.recommendation}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TechnicalAnalysisChart