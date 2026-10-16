'use client'

import { ProtectedPage } from '@/components/ProtectedPage'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { useAuth } from '@/hooks/useAuth'

export default function NewThesisPage() {
  const { user } = useAuth()

  return (
    <ProtectedPage>
      <div style={{ display: 'flex', minHeight: '100vh' }}>
        <Sidebar />
        <div style={{ flex: 1 }}>
          <Topbar title={`Nueva tesis · ${user?.full_name || 'Usuario'}`} />
          <main className="page">{/* ... */}</main>
        </div>
      </div>
    </ProtectedPage>
  )
}
