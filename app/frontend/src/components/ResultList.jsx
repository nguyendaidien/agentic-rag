import React from 'react'

export default function ResultList({ results }) {
  if (!results.length) return <p style={{ color: '#9ca3af' }}>No results yet.</p>

  return (
    <div>
      {results.map((r, i) => (
        <div key={r.doc_id} style={{ background: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: 8, padding: '12px 16px', marginBottom: 8 }}>
          <div style={{ fontWeight: 700, color: '#1d4ed8', marginBottom: 4 }}>{r.title}</div>
          <div style={{ fontSize: 14, color: '#374151', marginBottom: 8 }}>{r.snippet}…</div>
          <div style={{ fontSize: 12, color: '#9ca3af', display: 'flex', gap: 8 }}>
            <span style={{ background: '#dcfce7', color: '#166534', borderRadius: 4, padding: '1px 6px' }}>score: {r.score.toFixed(3)}</span>
            <span style={{ background: '#dbeafe', color: '#1e40af', borderRadius: 4, padding: '1px 6px' }}>{r.method}</span>
            <span style={{ background: '#f3f4f6', borderRadius: 4, padding: '1px 6px' }}>#{i + 1}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
