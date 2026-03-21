import axios from 'axios'

const base = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

export const getHealthz = async () => base.get('/healthz')
export const getSummary = async () => base.get('/summary')
export const getMeasurements = async () => base.get('/measurements')
export const getTrends = async (metric: 'weight' | 'bmi') => base.get('/trends', { params: { metric } })
export const getAlerts = async () => base.get('/alerts')
export const getGoals = async () => base.get('/goals')

export default base
