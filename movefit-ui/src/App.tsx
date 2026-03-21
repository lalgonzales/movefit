import React, { useEffect, useState } from 'react'
import { Link, Route, Routes } from 'react-router-dom'
import { getHealthz, getSummary, getMeasurements, getTrends, getAlerts, getGoals } from './api'

const Home = () => {
  const [health, setHealth] = useState('pending')
  const [summary, setSummary] = useState<any>(null)

  useEffect(() => {
    getHealthz().then((r) => setHealth(r.data.status)).catch(() => setHealth('fail'))
    getSummary().then((r) => setSummary(r.data)).catch(() => setSummary(null))
  }, [])

  return (
    <div>
      <h1>Movefit UI</h1>
      <p>Backend status: {health}</p>
      <pre>{JSON.stringify(summary, null, 2)}</pre>
    </div>
  )
}

const Storage = () => {
  const [items, setItems] = useState<any[]>([])
  useEffect(() => {
    getMeasurements().then((r) => setItems(r.data)).catch(() => setItems([]))
  }, [])
  return (
    <div>
      <h2>Measurements</h2>
      <pre>{JSON.stringify(items.slice(0, 10), null, 2)}</pre>
    </div>
  )
}

const Trends = () => {
  const [data, setData] = useState<any>(null)
  useEffect(() => {
    getTrends('weight').then((r) => setData(r.data)).catch(() => setData(null))
  }, [])
  return (
    <div>
      <h2>Trends (weight)</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

const Alerts = () => {
  const [data, setData] = useState<any>(null)
  useEffect(() => {
    getAlerts().then((r) => setData(r.data)).catch(() => setData(null))
  }, [])
  return (
    <div>
      <h2>Alerts</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

const Goals = () => {
  const [data, setData] = useState<any>(null)
  useEffect(() => {
    getGoals().then((r) => setData(r.data)).catch(() => setData(null))
  }, [])
  return (
    <div>
      <h2>Goals</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

export default function App() {
  return (
    <div className="app">
      <nav>
        <Link to="/">Home</Link> | <Link to="/measurements">Measurements</Link> | <Link to="/trends">Trends</Link> | <Link to="/alerts">Alerts</Link> | <Link to="/goals">Goals</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/measurements" element={<Storage />} />
        <Route path="/trends" element={<Trends />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/goals" element={<Goals />} />
      </Routes>
    </div>
  )
}
