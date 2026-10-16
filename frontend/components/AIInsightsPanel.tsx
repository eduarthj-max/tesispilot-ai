'use client'

export default function AIInsightsPanel({ summary, review }: any) {
  return (
    <div>
      <h4 style={{ marginTop: 0 }}>IA - Insights</h4>
      {summary && (
        <div style={{ marginBottom: 12 }}>
          <strong>Resumen</strong>
          <pre>{summary}</pre>
        </div>
      )}
      {review && (
        <div>
          <strong>Revisión</strong>
          <pre>{review}</pre>
        </div>
      )}
    </div>
  )
}
