import React from 'react'

const STEP_COLORS = {
  query_understanding: '#4ade80',
  bm25_retrieval: '#60a5fa',
  semantic_retrieval: '#60a5fa',
  hybrid_retrieval: '#60a5fa',
  graph_retrieval: '#a78bfa',
  rerank: '#fbbf24',
  total: '#f87171',
}

export default function TracePanel({ trace }) {
  if (!trace.length) return (
    <div style={{ background: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: 8, padding: 16 }}>
      <div style={{ fontWeight: 700, color: '#6b7280', marginBottom: 8 }}>⚡ Retrieval Trace</div>
      <p style={{ fontSize: 13, color: '#9ca3af' }}>Run a search to see the trace.</p>
    </div>
  )

  return (
    <div style={{ background: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: 8, padding: 16 }}>
      <div style={{ fontWeight: 700, color: '#374151', marginBottom: 12 }}>⚡ Retrieval Trace</div>
      {trace.map((step, i) => (
        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 0', borderBottom: '1px solid #e5e7eb', fontSize: 13 }}>
          <div style={{ width: 8, height: 8, borderRadius: '50%', background: STEP_COLORS[step.step] || '#94a3b8', flexShrink: 0 }} />
          <span style={{ flex: 1, color: '#374151' }}>{step.step.replace(/_/g, ' ')}</span>
          <span style={{ color: '#6b7280', fontWeight: 600 }}>{step.ms}ms</span>
        </div>
      ))}
    </div>
  )
}
