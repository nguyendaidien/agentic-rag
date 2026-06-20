import React, { useState } from 'react'

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('')
  const [method, setMethod] = useState('hybrid')
  const [rerank, setRerank] = useState(true)

  return (
    <div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && onSearch(query, method, rerank)}
          placeholder="Search the corpus..."
          style={{ flex: 1, padding: '8px 12px', fontSize: 16, border: '1px solid #d1d5db', borderRadius: 6 }}
        />
        <button
          onClick={() => onSearch(query, method, rerank)}
          disabled={loading || !query}
          style={{ padding: '8px 18px', background: '#1d4ed8', color: 'white', border: 'none', borderRadius: 6, cursor: 'pointer' }}
        >
          {loading ? '…' : 'Search'}
        </button>
      </div>
      <div style={{ display: 'flex', gap: 12, fontSize: 14, color: '#6b7280' }}>
        {['bm25', 'semantic', 'hybrid', 'graph'].map(m => (
          <label key={m} style={{ cursor: 'pointer' }}>
            <input type="radio" value={m} checked={method === m} onChange={() => setMethod(m)} /> {m}
          </label>
        ))}
        <label style={{ marginLeft: 'auto', cursor: 'pointer' }}>
          <input type="checkbox" checked={rerank} onChange={e => setRerank(e.target.checked)} /> rerank
        </label>
      </div>
    </div>
  )
}
