'use client'

import { useState } from 'react'

export function VersionHistory({ versions, onRestore }: any) {
  return (
    <div>
      <h4 style={{ marginTop: 0 }}>Historial de versiones</h4>
      {versions.length === 0 ? (
        <div className="text-muted">No hay versiones guardadas.</div>
      ) : (
        <div style={{ display: 'grid', gap: 8 }}>
          {versions.map((v: any) => (
            <div key={v.id} className="card">
              <div style={{ fontSize: 13, color: 'var(--muted)' }}>{new Date(v.created_at).toLocaleString()}</div>
              <pre style={{ maxHeight: 120, overflow: 'auto' }}>{v.content.substring(0, 800)}</pre>
              <div style={{ display: 'flex', gap: 8 }}>
                <button className="ghost" onClick={() => navigator.clipboard.writeText(v.content)}>Copiar</button>
                <button className="ghost" onClick={() => onRestore(v.content)}>Restaurar</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
