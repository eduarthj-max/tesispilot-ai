import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="page">
      <div className="card" style={{ maxWidth: 700 }}>
        <h1 style={{ fontSize: 36, marginBottom: 12 }}>TesisPilot</h1>
        <p className="text-muted" style={{ marginBottom: 24 }}>
          Asistente para planificar, investigar, redactar y defender una tesis con ayuda de IA.
        </p>
        <div className="grid two" style={{ gap: 16 }}>
          <Link href="/login" className="card" style={{ textAlign: 'center' }}>
            <button className="primary" style={{ width: '100%' }}>Iniciar sesión</button>
          </Link>
          <Link href="/dashboard" className="card" style={{ textAlign: 'center' }}>
            <button className="secondary" style={{ width: '100%' }}>Ir al dashboard</button>
          </Link>
        </div>
      </div>
    </main>
  )
}
