export function Topbar({ title }: { title: string }) {
  return (
    <header style={{ height: 72, borderBottom: '1px solid rgba(148,163,184,0.2)', display: 'flex', alignItems: 'center', padding: '0 24px', background: '#0f172a' }}>
      <div style={{ fontSize: 24, fontWeight: 700 }}>{title}</div>
    </header>
  )
}
