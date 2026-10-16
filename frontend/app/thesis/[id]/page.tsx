'use client'

import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { ChapterList } from '@/components/ChapterList'
import { Editor } from '@/components/Editor'
import { IAReviewPanel } from '@/components/IAReviewPanel'
import { apiFetch } from '@/lib/api'

export default function ThesisDetailPage() {
  const params = useParams<{ id: string }>()
  const id = params.id

  const [thesis, setThesis] = useState<any>(null)
  const [chapters, setChapters] = useState<any[]>([])
  const [selectedChapter, setSelectedChapter] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  const refresh = async () => {
    try {
      const thesisData = await apiFetch(`/api/theses/${id}`)
      setThesis(thesisData)
      const chapterData = await apiFetch(`/api/chapters/by-thesis/${id}`)
      setChapters(chapterData)
      if (chapterData[0]) setSelectedChapter(chapterData[0])
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (id) refresh()
  }, [id])

  const createChapter = async () => {
    const title = prompt('Título del capítulo') || 'Nuevo capítulo'
    const content = prompt('Contenido inicial') || 'Escribe aquí el capítulo...'
    try {
      await apiFetch('/api/chapters', {
        method: 'POST',
        body: JSON.stringify({
          thesis_id: id,
          title,
          chapter_type: 'section',
          order_index: chapters.length + 1,
          content,
        }),
      })
      refresh()
    } catch (e) {
      alert('No se pudo crear el capítulo')
    }
  }

  if (loading) return <div className="page">Cargando...</div>
  if (!thesis) return <div className="page">Tesis no encontrada</div>

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Topbar title={thesis.title} />
        <main className="page">
          <div className="grid two" style={{ gridTemplateColumns: '300px 1fr 360px' }}>
            <div className="card">
              <h3 style={{ marginTop: 0 }}>Capítulos</h3>
              <button className="primary" style={{ width: '100%', marginBottom: 12 }} onClick={createChapter}>Nuevo capítulo</button>
              <ChapterList chapters={chapters} selectedChapter={selectedChapter} onSelect={setSelectedChapter} />
            </div>

            <div className="card">
              <h3 style={{ marginTop: 0 }}>{selectedChapter?.title || 'Selecciona un capítulo'}</h3>
              {selectedChapter ? (
                <Editor
                  chapter={selectedChapter}
                  onSave={async (content) => {
                    await apiFetch(`/api/chapters/${selectedChapter.id}`, {
                      method: 'PUT',
                      body: JSON.stringify({
                        title: selectedChapter.title,
                        chapter_type: selectedChapter.chapter_type,
                        order_index: selectedChapter.order_index,
                        content,
                      }),
                    })
                    refresh()
                  }}
                />
              ) : (
                <p className="text-muted">No hay capítulo seleccionado.</p>
              )}
            </div>

            <div className="card">
              <IAReviewPanel thesis={thesis} chapter={selectedChapter} refresh={refresh} />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
