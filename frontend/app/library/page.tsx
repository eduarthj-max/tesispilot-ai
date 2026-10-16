'use client'

import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'

export default function LibraryPage() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Topbar title="Biblioteca" />
        <main className="page">
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Biblioteca documental</h2>
            <p className="text-muted">Aquí puedes subir PDFs, importar referencias y resumir artículos.</p>
            <input type="file" multiple style={{ marginTop: 12 }} />
          </div>
        </main>
      </div>
    </div>
  )
}
