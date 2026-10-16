'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { apiFetch } from '@/lib/api'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { ThesisCard } from '@/components/ThesisCard'

export default function DashboardPage() {
  const [theses, setTheses] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const data = await apiFetch('/api/theses')
        setTheses(data)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Topbar title="Dashboard" />
        <main className="page">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h2 style={{ margin: 0 }}>Mis tesis</h2>
            <Link href="/thesis/new">
              <button className="primary">Nueva tesis</button>
            </Link>
          </div>

          {loading ? (
            <div className="card">Cargando...</div>
          ) : (
            <div className="grid three">
              {theses.length === 0 ? (
                <div className="card">Aún no hay tesis creadas.</div>
              ) : (
                theses.map((thesis) => (
                  <ThesisCard key={thesis.id} thesis={thesis} />
                ))
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
