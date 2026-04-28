import React, { useState, useEffect } from 'react'
import { analysisAPI } from '../services/api'
import BreakoutSignals from '../components/BreakoutSignals'
import TechnicalAnalysisChart from '../components/TechnicalAnalysisChart'

const Analysis = () => {
  const [breakoutSignals, setBreakoutSignals] = useState([])
  const [technicalAnalysis, setTechnicalAnalysis] = useState([])
  const [loading, setLoading] = useState(true)
  const [timeframe, setTimeframe] = useState('H1')

  useEffect(() => {
    loadAnalysisData()
  }, [timeframe])

  const loadAnalysisData = async () => {
    try {
      setLoading(true)
      
      const [breakoutsResponse, analysisResponse] = await Promise.all([
        analysisAPI.getBreakouts(timeframe),
        analysisAPI.getTechnicalAnalysis(timeframe)
      ])
      
      setBreakoutSignals(breakoutsResponse.data)
      setTechnicalAnalysis(analysisResponse.data)
    } catch (error) {
      console.error('Error loading analysis data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Cargando análisis técnico...</div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Análisis Técnico</h1>
        
        <div className="flex space-x-4">
          <select 
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="M1">1 Minuto</option>
            <option value="M5">5 Minutos</option>
            <option value="M15">15 Minutos</option>
            <option value="M30">30 Minutos</option>
            <option value="H1">1 Hora</option>
            <option value="H4">4 Horas</option>
            <option value="D1">1 Día</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <BreakoutSignals 
            signals={breakoutSignals}
            timeframe={timeframe}
          />
        </div>
        
        <div>
          <TechnicalAnalysisChart 
            analysis={technicalAnalysis}
            timeframe={timeframe}
          />
        </div>
      </div>
    </div>
  )
}

export default Analysis