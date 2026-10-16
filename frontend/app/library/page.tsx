'use client'

import { ProtectedPage } from '@/components/ProtectedPage'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'

export default function LibraryPage() {
  return (
    <ProtectedPage>
      <div style={{ display: 'flex', minHeight: '100vh' }}>
        <Sidebar />
        <div style={{ flex: 1 }}>
          <Topbar title="Biblioteca" />
          <main className="page">...</main>
        </div>
      </div>
    </ProtectedPage>
  )
}
