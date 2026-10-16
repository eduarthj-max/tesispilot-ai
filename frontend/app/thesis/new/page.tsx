'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { apiFetch } from '@/lib/api'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'

export default function NewThesisPage() {
  const router = useRouter()
  const [form, setForm] = useState({
    title: '',
    topic: '',
    abstract: '',
  })
  const [saving, setSaving] = useState(false)

  const onChange = (key: string, value: string) => setForm((prev) => ({ ...prev, [key]: value }))

  const onSubmit = async () => {
    setSaving(true)
    try {
      const thesis = await apiFetch('/api/theses', {
        method: 'POST',
        body: JSON.stringify(form),
      })
      router.push(`/thesis/${thesis.id}`)
    } catch (e) {
      console.error(e)
      alert('No se pudo crear la tesis')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Topbar title="Nueva tesis" />
        <main className="page" style={{ maxWidth: 760 }}>
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Crear proyecto</h2>
            <input value={form.title} onChange={(e) => onChange('title', e.target.value)} placeholder="Título de la tesis" style={{ marginBottom: 10 }} />
            <input value={form.topic} onChange={(e) => onChange('topic', e.target.value)} placeholder="Tema de investigación" style={{ marginBottom: 10 }} />
            <textarea value={form.abstract} onChange={(e) => onChange('abstract', e.target.value)} placeholder="Resumen o idea general" rows={6} style={{ marginBottom: 10 }} />
            <button className="primary" onClick={onSubmit} disabled={saving} style={{ width: '100%' }}>
              {saving ? 'Creando...' : 'Crear tesis'}
            </button>
          </div>
        </main>
      </div>
    </div>
  )
}
