'use client'

import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'

export function ProtectedPage({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  const router = useRouter()

  if (loading) return <div className="page">Cargando sesión...</div>
  if (!user) {
    router.replace('/login')
    return null
  }

  return <>{children}</>
}
