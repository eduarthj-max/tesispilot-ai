'use client'

import { useState } from 'react'

export default function EditorToolbar({ onSaveVersion, onSummarize, onReview, wordCount }: any) {
  return (
    <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
      <button className="ghost" onClick={onSaveVersion} style={{ padding: '8px 10px' }}>Guardar versión</button>
      <button className="ghost" onClick={onSummarize} style={{ padding: '8px 10px' }}>Resumir</button>
      <button className="ghost" onClick={onReview} style={{ padding: '8px 10px' }}>Revisar IA</button>
      <div style={{ marginLeft: 'auto', alignSelf: 'center' }} className="text-muted">Palabras: {wordCount}</div>
    </div>
  )
}
