'use client'

export function ProgressRing({ percent = 0 }: { percent?: number }) {
  const radius = 36
  const stroke = 6
  const normalizedRadius = radius - stroke * 2
  const circumference = normalizedRadius * 2 * Math.PI
  const strokeDashoffset = circumference - (percent / 100) * circumference

  return (
    <svg height={radius * 2} width={radius * 2} style={{ transform: 'rotate(-90deg)' }}>
      <circle
        stroke="rgba(255,255,255,0.08)"
        fill="transparent"
        strokeWidth={stroke}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
      />
      <circle
        stroke="#38bdf8"
        fill="transparent"
        strokeWidth={stroke}
        strokeDasharray={`${circumference} ${circumference}`}
        style={{ strokeDashoffset }}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
      />
      <text x="50%" y="50%" dominantBaseline="middle" textAnchor="middle" fill="#e5ecf7" transform="rotate(90,36,36)">{percent}%</text>
    </svg>
  )
}
