'use client'

import Link from 'next/link'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'

export default function LoginPage() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Topbar title="Iniciar sesión" />
        <main className="page" style={{ maxWidth: 520 }}>
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Acceso</h2>
            <input placeholder="Correo electrónico" style={{ marginBottom: 10 }} />
            <input placeholder="Contraseña" type="password" style={{ marginBottom: 10 }} />
            <button className="primary" style={{ width: '100%' }}>Entrar</button>
            <div style={{ marginTop: 12 }} className="text-muted">
              ¿No tienes cuenta? <Link href="/register">Regístrate</Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
