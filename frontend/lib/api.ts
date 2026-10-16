// small helper to include auth token

export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function apiFetch(path, options = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('tp_token') : null
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  const text = await res.text()
  let data
  try { data = text ? JSON.parse(text) : null } catch { data = text }
  if (!res.ok) throw new Error(data?.detail || data || `HTTP ${res.status}`)
  return data
}

export async function authLogin(email, password) {
  const data = await apiFetch('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
  if (data?.access_token) localStorage.setItem('tp_token', data.access_token)
  return data
}

export async function authRegister(payload) {
  const data = await apiFetch('/api/auth/register', { method: 'POST', body: JSON.stringify(payload) })
  return data
}

export async function getMe() {
  return apiFetch('/api/auth/me')
}
