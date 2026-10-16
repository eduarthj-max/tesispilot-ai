'use client'

import { ProtectedPage } from '@/components/ProtectedPage'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { useAuth } from '@/hooks/useAuth'

export default function DashboardPage() {
  const { user } = useAuth()

  return (
    <ProtectedPage>
      <div style={{ display: 'flex', minHeight: '100vh' }}>
        <Sidebar />
        <div style={{ flex: 1 }}>
          <Topbar title={`Dashboard · ${user?.full_name || 'Usuario'}`} />
          <main className="page">
            <div className="card" style={{ marginBottom: 20 }}>
              <h2 style={{ marginTop: 0 }}>Bienvenido</h2>
              <div className="text-muted">Correo: {user?.email}</div>
            </div>
          </main>
        </div>
      </div>
    </ProtectedPage>
  )
}
