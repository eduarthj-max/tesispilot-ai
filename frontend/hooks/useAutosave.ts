'use client'

import { useEffect, useRef, useState } from 'react'

export function useAutosave(value: string, saveFn: (v: string) => Promise<void>, delay = 1500) {
  const [status, setStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle')
  const timer = useRef<number | null>(null)
  const lastSaved = useRef<string>(value)

  useEffect(() => {
    if (value === lastSaved.current) return
    setStatus('saving')
    if (timer.current) window.clearTimeout(timer.current)
    timer.current = window.setTimeout(async () => {
      try {
        await saveFn(value)
        lastSaved.current = value
        setStatus('saved')
        setTimeout(() => setStatus('idle'), 1200)
      } catch (e) {
        console.error('Autosave error', e)
        setStatus('error')
      }
    }, delay)

    return () => {
      if (timer.current) window.clearTimeout(timer.current)
    }
  }, [value, saveFn, delay])

  return { status }
}
