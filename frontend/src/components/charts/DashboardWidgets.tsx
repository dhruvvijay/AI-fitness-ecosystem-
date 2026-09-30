"use client"

import React from "react"
import { motion } from "framer-motion"
import { cn } from "@/lib/utils"
import { LucideIcon } from "lucide-react"

interface StatCardProps {
  title: string
  value: string | number
  subtitle?: string
  icon: LucideIcon
  gradient: string
  trend?: { value: number; label: string }
  onClick?: () => void
}

export function StatCard({ title, value, subtitle, icon: Icon, gradient, trend, onClick }: StatCardProps) {
  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.01 }}
      whileTap={{ scale: 0.99 }}
      onClick={onClick}
      className={cn(
        "glass-card group relative overflow-hidden p-5 cursor-pointer",
        "transition-all duration-300"
      )}
    >
      {/* Background gradient glow */}
      <div className={cn(
        "absolute -top-12 -right-12 h-32 w-32 rounded-full opacity-10 blur-2xl",
        "transition-opacity duration-300 group-hover:opacity-20",
        gradient
      )} />

      <div className="relative z-10 flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
            {title}
          </p>
          <p className="text-2xl font-bold tracking-tight">{value}</p>
          {subtitle && (
            <p className="text-xs text-muted-foreground">{subtitle}</p>
          )}
          {trend && (
            <div className={cn(
              "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-medium",
              trend.value >= 0
                ? "bg-emerald-500/10 text-emerald-400"
                : "bg-rose-500/10 text-rose-400"
            )}>
              {trend.value >= 0 ? "↑" : "↓"} {Math.abs(trend.value)}% {trend.label}
            </div>
          )}
        </div>

        <div className={cn(
          "flex h-11 w-11 shrink-0 items-center justify-center rounded-xl",
          "bg-gradient-to-br shadow-lg",
          gradient
        )}>
          <Icon className="h-5 w-5 text-white" />
        </div>
      </div>
    </motion.div>
  )
}

/* ── Progress Ring Component ─────────────────────────────────── */

interface ProgressRingProps {
  value: number
  max: number
  size?: number
  strokeWidth?: number
  color: string
  label: string
  unit?: string
}

export function ProgressRing({
  value, max, size = 120, strokeWidth = 8,
  color, label, unit = "",
}: ProgressRingProps) {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const percentage = Math.min(100, (value / max) * 100)
  const offset = circumference - (percentage / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={strokeWidth}
            className="text-white/[0.06]"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="progress-ring-circle drop-shadow-[0_0_6px_var(--tw-shadow-color)]"
            style={{ "--tw-shadow-color": color } as React.CSSProperties}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-lg font-bold">{Math.round(value)}</span>
          <span className="text-[10px] text-muted-foreground">{unit}</span>
        </div>
      </div>
      <span className="text-xs font-medium text-muted-foreground">{label}</span>
    </div>
  )
}

/* ── Macro Bar Component ─────────────────────────────────────── */

interface MacroBarProps {
  label: string
  current: number
  target: number
  color: string
  unit?: string
}

export function MacroBar({ label, current, target, color, unit = "g" }: MacroBarProps) {
  const pct = Math.min(100, (current / target) * 100)

  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between text-xs">
        <span className="font-medium">{label}</span>
        <span className="text-muted-foreground">
          {Math.round(current)}{unit} / {Math.round(target)}{unit}
        </span>
      </div>
      <div className="h-2 w-full rounded-full bg-white/[0.06] overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
          className="h-full rounded-full"
          style={{ background: color }}
        />
      </div>
    </div>
  )
}

/* ── Water Glass Component ───────────────────────────────────── */

interface WaterTrackerProps {
  current: number
  target: number
  onAdd: (ml: number) => void
}

export function WaterTracker({ current, target, onAdd }: WaterTrackerProps) {
  const percentage = Math.min(100, (current / target) * 100)
  const glasses = Math.floor(current / 250)
  const totalGlasses = Math.ceil(target / 250)

  return (
    <div className="glass-card p-5 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">Water Intake 💧</h3>
        <span className="text-xs text-muted-foreground">
          {current}ml / {target}ml
        </span>
      </div>

      {/* Water Level */}
      <div className="relative h-32 w-full rounded-2xl bg-white/[0.04] border border-white/[0.06] overflow-hidden">
        <motion.div
          initial={{ height: 0 }}
          animate={{ height: `${percentage}%` }}
          transition={{ duration: 1.2, ease: [0.4, 0, 0.2, 1] }}
          className="absolute bottom-0 left-0 right-0 rounded-b-2xl"
          style={{
            background: "linear-gradient(to top, #0ea5e9, #38bdf8, #7dd3fc)",
            opacity: 0.3,
          }}
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold">{Math.round(percentage)}%</span>
        </div>
      </div>

      {/* Quick Add Buttons */}
      <div className="flex gap-2">
        {[150, 250, 500].map((ml) => (
          <button
            key={ml}
            onClick={() => onAdd(ml)}
            className={cn(
              "flex-1 rounded-xl py-2 text-xs font-medium",
              "bg-sky-500/10 text-sky-400 hover:bg-sky-500/20",
              "transition-colors duration-200"
            )}
          >
            +{ml}ml
          </button>
        ))}
      </div>
    </div>
  )
}

/* ── Streak Component ────────────────────────────────────────── */

interface StreakProps {
  count: number
  label: string
}

export function StreakBadge({ count, label }: StreakProps) {
  return (
    <div className="flex items-center gap-3 glass-card p-4">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-orange-500 to-amber-400 shadow-lg shadow-orange-500/20">
        <span className="text-lg">🔥</span>
      </div>
      <div>
        <p className="text-2xl font-bold">{count}</p>
        <p className="text-xs text-muted-foreground">{label}</p>
      </div>
    </div>
  )
}
