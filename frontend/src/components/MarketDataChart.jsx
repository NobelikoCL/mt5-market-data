import React from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const MarketDataChart = ({ symbol, marketData }) => {
  if (!symbol || marketData.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center text-gray-500 py-8">
          Selecciona un símbolo para ver los datos del mercado
        </div>
      </div>
    )
  }

  const chartData = {
    labels: marketData.slice(-50).map(data => 
      new Date(data.timestamp).toLocaleTimeString()
    ),
    datasets: [
      {
        label: 'Precio de Cierre',
        data: marketData.slice(-50).map(data => parseFloat(data.close_price)),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.1,
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
        text: `${symbol.name} - Precio Histórico`,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <Line data={chartData} options={options} />
      
      <div className="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="text-center p-4 bg-gray-50 rounded">
          <div className="text-sm text-gray-600">Último Precio</div>
          <div className="text-lg font-semibold">
            {marketData.length > 0 ? parseFloat(marketData[marketData.length - 1].close_price).toFixed(5) : 'N/A'}
          </div>
        </div>
        
        <div className="text-center p-4 bg-gray-50 rounded">
          <div className="text-sm text-gray-600">Máximo</div>
          <div className="text-lg font-semibold">
            {marketData.length > 0 ? Math.max(...marketData.map(d => parseFloat(d.high_price))).toFixed(5) : 'N/A'}
          </div>
        </div>
        
        <div className="text-center p-4 bg-gray-50 rounded">
          <div className="text-sm text-gray-600">Mínimo</div>
          <div className="text-lg font-semibold">
            {marketData.length > 0 ? Math.min(...marketData.map(d => parseFloat(d.low_price))).toFixed(5) : 'N/A'}
          </div>
        </div>
        
        <div className="text-center p-4 bg-gray-50 rounded">
          <div className="text-sm text-gray-600">Volumen</div>
          <div className="text-lg font-semibold">
            {marketData.length > 0 ? parseFloat(marketData[marketData.length - 1].volume).toFixed(2) : 'N/A'}
          </div>
        </div>
      </div>
    </div>
  )
}

export default MarketDataChart