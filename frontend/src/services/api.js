import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const api = {
  getDashboard: () => apiClient.get('/market-data/dashboard/'),

  toggleSymbol: (symbolId) => apiClient.post('/market-data/symbols/' + symbolId + '/toggle/'),

  analyzeAll: () => apiClient.post('/market-data/analyze-all/'),

  getActiveSignals: () => apiClient.get('/market-data/signals/active/'),

  // Telegram Config
  getTelegramConfig: () => apiClient.get('/analysis/telegram-config/'),
  
  updateTelegramConfig: (data) => apiClient.post('/analysis/telegram-config/', data),
  
  testTelegramMessage: () => apiClient.post('/analysis/telegram-config/test_message/'),
  
  toggleTelegram: () => apiClient.post('/analysis/telegram-config/toggle/'),
}

export default apiClient
