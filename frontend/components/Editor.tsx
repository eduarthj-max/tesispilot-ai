'use client'

import { useState } from 'react'

export function Editor({ chapter, onSave }: { chapter: any; onSave: (content: string) => Promise<void> }) {
  const [value, setValue] = useState(chapter.content || '')
  const [saving, setSaving] = useState(false)

  const save = async () => {
    setSaving(true)
    try {
      await onSave(value)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        rows={18}
        style={{ marginBottom: 10 }}
      />
      <button className="primary" onClick={save} disabled={saving} style={{ width: '100%' }}>
        {saving ? 'Guardando...' : 'Guardar capítulo'}
      </button>
    </div>
  )
}
