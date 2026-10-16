import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'TesisPilot',
  description: 'Asistente para tesis con IA',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
