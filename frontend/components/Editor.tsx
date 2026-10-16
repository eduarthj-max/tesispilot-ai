'use client'

import { useEffect, useState } from 'react'
import EditorToolbar from '@/components/EditorToolbar'
import AIInsightsPanel from '@/components/AIInsightsPanel'
import { VersionHistory } from '@/components/VersionHistory'
import { useAutosave } from '@/hooks/useAutosave'
import { apiFetch } from '@/lib/api'

export function Editor({ chapter, onSave }: any) {
  const [value, setValue] = useState(chapter.content || '')
  const [versions, setVersions] = useState<any[]>([])
  const [summary, setSummary] = useState<string | null>(null)
  const [review, setReview] = useState<string | null>(null)

  useEffect(() => {
    setValue(chapter.content || '')
    fetchVersions()
  }, [chapter.id])

  const fetchVersions = async () => {
    try {
      const data = await apiFetch(`/api/chapters/${chapter.id}/versions`)
      setVersions(data || [])
    } catch (e) {
      console.error('fetchVersions', e)
    }
  }

  const saveImmediate = async (content: string) => {
    await apiFetch(`/api/chapters/${chapter.id}`, {
      method: 'PUT',
      body: JSON.stringify({ title: chapter.title, chapter_type: chapter.chapter_type, order_index: chapter.order_index, content }),
    })
  }

  const { status } = useAutosave(value, saveImmediate, 1500)

  const saveVersion = async () => {
    try {
      await apiFetch(`/api/chapters/${chapter.id}/versions`, {
        method: 'POST',
        body: JSON.stringify({ content: value }),
      })
      fetchVersions()
      alert('Versión guardada')
    } catch (e) {
      alert('Error guardando versión')
    }
  }

  const summarize = async () => {
    try {
      const data = await apiFetch(`/api/chapters/${chapter.id}/summarize`, { method: 'POST', body: JSON.stringify({ text: value }) })
      setSummary(data?.ai?.text || JSON.stringify(data?.ai || ''))
    } catch (e) {
      console.error('summarize', e)
      setSummary('Error generando resumen')
    }
  }

  const reviewChapter = async () => {
    try {
      const data = await apiFetch(`/api/chapters/${chapter.id}/review`, { method: 'POST', body: JSON.stringify({ text: value }) })
      setReview(data?.ai?.text || JSON.stringify(data?.ai || ''))
    } catch (e) {
      console.error('review', e)
      setReview('Error revisando capítulo')
    }
  }

  const restoreContent = (c: string) => {
    setValue(c)
  }

  const wordCount = value.trim() ? value.trim().split(/\s+/).length : 0

  return (
    <div>
      <EditorToolbar
        onSaveVersion={saveVersion}
        onSummarize={summarize}
        onReview={reviewChapter}
        wordCount={wordCount}
      />

      <textarea value={value} onChange={(e) => setValue(e.target.value)} rows={20} style={{ marginBottom: 10 }} />

      <div style={{ display: 'flex', gap: 12 }}>
        <div style={{ flex: 1 }}>
          <div style={{ marginBottom: 10 }} className="text-muted">Estado autosave: {status}</div>
          <AIInsightsPanel summary={summary} review={review} />
        </div>
        <div style={{ width: 360 }}>
          <VersionHistory versions={versions} onRestore={restoreContent} />
        </div>
      </div>
    </div>
  )
}
