import React, { useState, useEffect } from 'react'
import { marketDataAPI } from '../services/api'
import SymbolList from '../components/SymbolList'
import MarketDataChart from '../components/MarketDataChart'

const MarketData = () => {
  const [symbols, setSymbols] = useState([])
  const [selectedSymbol, setSelectedSymbol] = useState(null)
  const [marketData, setMarketData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSymbols()
  }, [])

  const loadSymbols = async () => {
    try {
      const response = await marketDataAPI.getSymbols()
      setSymbols(response.data)
      if (response.data.length > 0) {
        setSelectedSymbol(response.data[0])
      }
    } catch (error) {
      console.error('Error loading symbols:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadMarketData = async (symbol) => {
    if (!symbol) return
    
    try {
      const response = await marketDataAPI.getMarketData(symbol.id)
      setMarketData(response.data)
    } catch (error) {
      console.error('Error loading market data:', error)
    }
  }

  useEffect(() => {
    if (selectedSymbol) {
      loadMarketData(selectedSymbol)
    }
  }, [selectedSymbol])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Cargando datos del mercado...</div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Datos del Mercado</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <SymbolList 
            symbols={symbols}
            selectedSymbol={selectedSymbol}
            onSymbolSelect={setSelectedSymbol}
          />
        </div>
        
        <div className="lg:col-span-3">
          {selectedSymbol && (
            <MarketDataChart 
              symbol={selectedSymbol}
              marketData={marketData}
            />
          )}
        </div>
      </div>
    </div>
  )
}

export default MarketData