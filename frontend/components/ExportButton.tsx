'use client'

import { apiFetch } from '@/lib/api'

export default function ExportButton({ thesisId }: { thesisId: string }) {
  const exportDoc = async (format: 'pdf' | 'docx' | 'md', citation = 'APA') => {
    try {
      const data = await apiFetch(`/api/theses/${thesisId}/export`, {
        method: 'POST',
        body: JSON.stringify({ format, citation_style: citation }),
      })
      const url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${data.download_url}`
      window.open(url, '_blank')
    } catch (e) {
      alert('Error exportando el documento: ' + (e as Error).message)
    }
  }

  return (
    <div style={{ display: 'flex', gap: 10, marginTop: 12, alignItems: 'center' }}>
      <select id="citation_select" style={{ padding: 8, borderRadius: 8 }} defaultValue="APA">
        <option value="APA">APA</option>
        <option value="IEEE">IEEE</option>
      </select>
      <button className="primary" onClick={() => exportDoc('pdf', (document.getElementById('citation_select') as HTMLSelectElement).value)}>Exportar PDF</button>
      <button className="secondary" onClick={() => exportDoc('docx', (document.getElementById('citation_select') as HTMLSelectElement).value)}>Word</button>
      <button className="ghost" onClick={() => exportDoc('md', (document.getElementById('citation_select') as HTMLSelectElement).value)}>Markdown</button>
    </div>
  )
}
