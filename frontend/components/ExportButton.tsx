'use client'

import { apiFetch } from '@/lib/api'

export default function ExportButton({ thesisId }: { thesisId: string }) {
  const exportDoc = async (format: 'pdf' | 'docx' | 'md') => {
    try {
      const data = await apiFetch(`/api/theses/${thesisId}/export`, {
        method: 'POST',
        body: JSON.stringify({ format }),
      })
      const url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${data.download_url}`
      window.open(url, '_blank')
    } catch (e) {
      alert('Error exportando el documento: ' + (e as Error).message)
    }
  }

  return (
    <div style={{ display: 'flex', gap: 10, marginTop: 12 }}>
      <button className="primary" onClick={() => exportDoc('pdf')}>Exportar PDF</button>
      <button className="secondary" onClick={() => exportDoc('docx')}>Word</button>
      <button className="ghost" onClick={() => exportDoc('md')}>Markdown</button>
    </div>
  )
}
