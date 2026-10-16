'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { getMe } from '@/lib/api'

export function useAuth() {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const load = async () => {
      const token = localStorage.getItem('tp_token')
      if (!token) {
        setLoading(false)
        router.replace('/login')
        return
      }

      try {
        const me = await getMe()
        setUser(me)
      } catch (e) {
        localStorage.removeItem('tp_token')
        router.replace('/login')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [router])

  return { user, loading }
}
