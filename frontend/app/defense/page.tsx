'use client'

import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'

export default function DefensePage() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Topbar title="Defensa" />
        <main className="page">
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Preparación para la defensa</h2>
            <p className="text-muted">Genera diapositivas y preguntas de defensa para tu tesis.</p>
            <button className="primary">Generar presentación</button>
          </div>
        </main>
      </div>
    </div>
  )
}
