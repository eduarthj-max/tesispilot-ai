import Link from 'next/link'

const items = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/thesis/new', label: 'Nueva tesis' },
  { href: '/library', label: 'Biblioteca' },
  { href: '/defense', label: 'Defensa' },
  { href: '#', label: 'Cerrar sesión', action: 'logout' },
]

export function Sidebar() {
  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('tp_token')
      window.location.href = '/login'
    }
  }

  return (
    <aside style={{ width: 240, background: '#0f172a', borderRight: '1px solid rgba(148,163,184,0.2)', padding: 18 }}>
      <div style={{ fontSize: 26, fontWeight: 800, marginBottom: 22 }}>TesisPilot</div>
      <nav style={{ display: 'grid', gap: 8 }}>
        {items.map((item) => (
          item.action === 'logout' ? (
            <button key={item.href} className="ghost" onClick={logout} style={{ width: '100%', textAlign: 'left' }}>
              {item.label}
            </button>
          ) : (
            <Link key={item.href} href={item.href} style={{ color: '#e2e8f0', textDecoration: 'none' }}>
              <div style={{ padding: '10px 12px', borderRadius: 10, background: item.href === '/dashboard' ? 'rgba(56,189,248,0.18)' : 'transparent' }}>
                {item.label}
              </div>
            </Link>
          )
        ))}
      </nav>
    </aside>
  )
}
