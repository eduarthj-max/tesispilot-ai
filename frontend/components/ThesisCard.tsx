import Link from 'next/link'

export function ThesisCard({ thesis }: { thesis: any }) {
  return (
    <Link href={`/thesis/${thesis.id}`}>
      <div className="card" style={{ minHeight: 180, cursor: 'pointer' }}>
        <div style={{ fontSize: 20, fontWeight: 700, marginBottom: 10 }}>{thesis.title}</div>
        <div className="text-muted" style={{ marginBottom: 12 }}>{thesis.topic || 'Sin tema'}</div>
        <div style={{ marginBottom: 8 }}>Estado: {thesis.status || 'draft'}</div>
        <div className="text-muted">{thesis.abstract || 'Sin resumen'}</div>
      </div>
    </Link>
  )
}
