'use client'

import Link from 'next/link'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { authLogin } from '@/lib/api'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const login = async () => {
    try {
      await authLogin(email, password)
      router.push('/dashboard')
    } catch (e) {
      alert('Error al iniciar sesión: ' + e.message)
    }
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Topbar title="Iniciar sesión" />
        <main className="page" style={{ maxWidth: 520 }}>
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Acceso</h2>
            <input placeholder="Correo electrónico" value={email} onChange={(e) => setEmail(e.target.value)} style={{ marginBottom: 10 }} />
            <input placeholder="Contraseña" type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ marginBottom: 10 }} />
            <button className="primary" style={{ width: '100%' }} onClick={login}>Entrar</button>
            <div style={{ marginTop: 12 }} className="text-muted">
              ¿No tienes cuenta? <Link href="/register">Regístrate</Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
