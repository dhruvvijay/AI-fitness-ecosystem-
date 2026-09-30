"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import { Footprints, Plus, Trophy, TrendingUp, Target } from "lucide-react"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"
import { cn } from "@/lib/utils"
import { ProgressRing } from "@/components/charts/DashboardWidgets"

const weeklyData = [
  { day: "Mon", steps: 8432 }, { day: "Tue", steps: 12045 }, { day: "Wed", steps: 9876 },
  { day: "Thu", steps: 11234 }, { day: "Fri", steps: 7654 }, { day: "Sat", steps: 14320 }, { day: "Sun", steps: 10567 },
]
const hourlyData = Array.from({ length: 24 }, (_, i) => ({ hour: `${i}:00`, steps: Math.floor(Math.random() * 1200) }))

export default function StepsPage() {
  const [todaySteps, setTodaySteps] = useState(8743)
  const goal = 10000

  return (
    <div className="space-y-6 pb-8">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-green-500 to-emerald-400 shadow-lg shadow-green-500/25">
            <Footprints className="h-6 w-6 text-white" />
          </div>
          <div><h1 className="text-2xl font-bold tracking-tight">Steps Tracker</h1><p className="text-sm text-muted-foreground">Track your daily movement</p></div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="glass-card p-6 flex flex-col items-center justify-center lg:col-span-1">
          <ProgressRing value={todaySteps} max={goal} size={160} strokeWidth={10} color="#22c55e" label="Today's Steps" unit="steps" />
          <p className="text-sm text-muted-foreground mt-3">{(todaySteps / goal * 100).toFixed(0)}% of daily goal</p>
          <div className="flex gap-2 mt-4">
            {[1000, 2500, 5000].map((s) => (
              <button key={s} onClick={() => setTodaySteps(prev => prev + s)}
                className="rounded-xl px-3 py-2 text-xs font-medium bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 transition-colors">+{s.toLocaleString()}</button>
            ))}
          </div>
        </div>

        <div className="glass-card p-5 lg:col-span-2">
          <h3 className="text-sm font-semibold mb-4">Weekly Steps</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={weeklyData}>
                <defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} /><stop offset="95%" stopColor="#22c55e" stopOpacity={0} /></linearGradient></defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
                <Area type="monotone" dataKey="steps" stroke="#22c55e" strokeWidth={2} fill="url(#sg)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="glass-card p-5">
        <h3 className="text-sm font-semibold mb-4">Hourly Breakdown</h3>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={hourlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="hour" stroke="rgba(255,255,255,0.3)" fontSize={10} interval={2} />
              <YAxis stroke="rgba(255,255,255,0.3)" fontSize={10} />
              <Bar dataKey="steps" fill="#22c55e" radius={[2, 2, 0, 0]} opacity={0.7} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Distance</p><p className="text-lg font-bold">6.3 km</p></div>
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Calories Burned</p><p className="text-lg font-bold text-orange-400">350 kcal</p></div>
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Active Minutes</p><p className="text-lg font-bold text-blue-400">68 min</p></div>
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Floors Climbed</p><p className="text-lg font-bold text-purple-400">12</p></div>
      </div>
    </div>
  )
}
