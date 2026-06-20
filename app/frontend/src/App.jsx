import React, { useState } from 'react'
import SearchBar from './components/SearchBar'
import ResultList from './components/ResultList'
import TracePanel from './components/TracePanel'

export default function App() {
  const [results, setResults] = useState([])
  const [trace, setTrace] = useState([])
  const [loading, setLoading] = useState(false)

  async function handleSearch(query, method, rerank) {
    setLoading(true)
    try {
      const res = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, method, k: 10, rerank }),
      })
      const data = await res.json()
      setResults(data.results || [])
      setTrace(data.trace || [])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ fontFamily: 'system-ui', maxWidth: 1100, margin: '0 auto', padding: 24 }}>
      <h1 style={{ color: '#1d4ed8' }}>⚡ Agentic RAG</h1>
      <SearchBar onSearch={handleSearch} loading={loading} />
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 16, marginTop: 16 }}>
        <ResultList results={results} />
        <TracePanel trace={trace} />
      </div>
    </div>
  )
}
