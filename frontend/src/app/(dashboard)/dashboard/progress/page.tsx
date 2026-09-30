"use client"

import React from "react"
import { motion } from "framer-motion"
import { TrendingUp, Camera, Scale, Ruler, Calendar } from "lucide-react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { cn } from "@/lib/utils"

const weightData = [
  { date: "Jan", weight: 82 }, { date: "Feb", weight: 80.5 }, { date: "Mar", weight: 79.2 },
  { date: "Apr", weight: 78.1 }, { date: "May", weight: 77.5 }, { date: "Jun", weight: 76.8 },
  { date: "Jul", weight: 75.9 }, { date: "Aug", weight: 75.2 },
]
const measureData = [
  { part: "Chest", current: 102, start: 98, change: "+4 cm", trend: "up" },
  { part: "Waist", current: 82, start: 90, change: "-8 cm", trend: "down" },
  { part: "Hips", current: 96, start: 100, change: "-4 cm", trend: "down" },
  { part: "Biceps", current: 36, start: 33, change: "+3 cm", trend: "up" },
  { part: "Thighs", current: 58, start: 62, change: "-4 cm", trend: "down" },
]

export default function ProgressPage() {
  return (
    <div className="space-y-6 pb-8">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-blue-400 shadow-lg shadow-sky-500/25">
          <TrendingUp className="h-6 w-6 text-white" />
        </div>
        <div><h1 className="text-2xl font-bold tracking-tight">Progress Tracker</h1><p className="text-sm text-muted-foreground">Visual progress of your transformation</p></div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="glass-card p-4 text-center"><p className="text-xs text-muted-foreground">Starting Weight</p><p className="text-xl font-bold">82.0 kg</p></div>
        <div className="glass-card p-4 text-center"><p className="text-xs text-muted-foreground">Current Weight</p><p className="text-xl font-bold text-emerald-400">75.2 kg</p></div>
        <div className="glass-card p-4 text-center"><p className="text-xs text-muted-foreground">Lost</p><p className="text-xl font-bold text-purple-400">-6.8 kg</p></div>
        <div className="glass-card p-4 text-center"><p className="text-xs text-muted-foreground">Goal</p><p className="text-xl font-bold text-blue-400">72.0 kg</p></div>
      </div>

      <div className="glass-card p-5">
        <h3 className="text-sm font-semibold mb-4">Weight Journey</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={weightData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="date" stroke="rgba(255,255,255,0.3)" fontSize={12} />
              <YAxis domain={["dataMin - 2", "dataMax + 2"]} stroke="rgba(255,255,255,0.3)" fontSize={12} />
              <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
              <Line type="monotone" dataKey="weight" stroke="#3b82f6" strokeWidth={2} dot={{ fill: "#3b82f6", r: 4 }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-card p-5">
        <h3 className="text-sm font-semibold mb-4 flex items-center gap-2"><Ruler className="h-4 w-4 text-sky-400" /> Body Measurements</h3>
        <div className="space-y-3">
          {measureData.map((m, i) => (
            <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }}
              className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/[0.04]">
              <span className="text-sm font-medium w-20">{m.part}</span>
              <div className="flex-1 mx-4">
                <div className="h-2 w-full rounded-full bg-white/[0.06] overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${(m.current / 120) * 100}%` }} transition={{ duration: 1, delay: i * 0.1 }}
                    className={cn("h-full rounded-full", m.trend === "up" ? "bg-emerald-500" : "bg-sky-500")} />
                </div>
              </div>
              <span className="text-sm font-bold w-16 text-right">{m.current} cm</span>
              <span className={cn("text-xs font-medium w-16 text-right", m.trend === "down" ? "text-sky-400" : "text-emerald-400")}>{m.change}</span>
            </motion.div>
          ))}
        </div>
      </div>

      <div className="glass-card p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold flex items-center gap-2"><Camera className="h-4 w-4 text-pink-400" /> Progress Photos</h3>
          <button className="text-xs text-pink-400 hover:text-pink-300 font-medium">+ Upload Photo</button>
        </div>
        <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
          {["Jan", "Feb", "Mar", "Apr", "May", "Jun"].map((month) => (
            <div key={month} className="aspect-[3/4] rounded-xl bg-white/[0.04] border border-white/[0.06] flex items-center justify-center cursor-pointer hover:bg-white/[0.06] transition-colors">
              <div className="text-center"><Camera className="h-6 w-6 text-muted-foreground mx-auto mb-1" /><p className="text-[10px] text-muted-foreground">{month}</p></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
