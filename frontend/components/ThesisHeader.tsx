'use client'

import { ExportButton } from '@/components/ExportButton'

export default function ThesisHeader({ thesis }: { thesis: any }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
      <div>
        <h2 style={{ margin: 0 }}>{thesis.title}</h2>
        <div className="text-muted">{thesis.topic || 'Sin tema'}</div>
      </div>
      <ExportButton thesisId={thesis.id} />
    </div>
  )
}
