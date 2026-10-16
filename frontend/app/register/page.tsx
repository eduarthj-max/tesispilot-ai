'use client'

import Link from 'next/link'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'

export default function RegisterPage() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Topbar title="Registrarse" />
        <main className="page" style={{ maxWidth: 520 }}>
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Crear cuenta</h2>
            <input placeholder="Nombre completo" style={{ marginBottom: 10 }} />
            <input placeholder="Correo electrónico" style={{ marginBottom: 10 }} />
            <input placeholder="Universidad" style={{ marginBottom: 10 }} />
            <input placeholder="Contraseña" type="password" style={{ marginBottom: 10 }} />
            <button className="primary" style={{ width: '100%' }}>Crear cuenta</button>
            <div style={{ marginTop: 12 }} className="text-muted">
              ¿Ya tienes cuenta? <Link href="/login">Inicia sesión</Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
