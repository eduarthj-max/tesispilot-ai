'use client'

import Link from 'next/link'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { useState } from 'react'
import { authRegister } from '@/lib/api'
import { useRouter } from 'next/navigation'

export default function RegisterPage() {
  const router = useRouter()
  const [form, setForm] = useState({ full_name: '', email: '', university: '', password: '' })

  const onChange = (k, v) => setForm((p) => ({ ...p, [k]: v }))

  const submit = async () => {
    try {
      await authRegister(form)
      alert('Cuenta creada, ahora inicia sesión')
      router.push('/login')
    } catch (e) {
      alert('Error creando cuenta: ' + e.message)
    }
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Topbar title="Registrarse" />
        <main className="page" style={{ maxWidth: 520 }}>
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Crear cuenta</h2>
            <input placeholder="Nombre completo" value={form.full_name} onChange={(e) => onChange('full_name', e.target.value)} style={{ marginBottom: 10 }} />
            <input placeholder="Correo electrónico" value={form.email} onChange={(e) => onChange('email', e.target.value)} style={{ marginBottom: 10 }} />
            <input placeholder="Universidad" value={form.university} onChange={(e) => onChange('university', e.target.value)} style={{ marginBottom: 10 }} />
            <input placeholder="Contraseña" type="password" value={form.password} onChange={(e) => onChange('password', e.target.value)} style={{ marginBottom: 10 }} />
            <button className="primary" style={{ width: '100%' }} onClick={submit}>Crear cuenta</button>
            <div style={{ marginTop: 12 }} className="text-muted">
              ¿Ya tienes cuenta? <Link href="/login">Inicia sesión</Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
