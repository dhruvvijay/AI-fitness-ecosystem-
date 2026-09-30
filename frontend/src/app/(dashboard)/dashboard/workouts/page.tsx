"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import {
  Dumbbell, Play, Clock, Flame, TrendingUp, Trophy,
  Plus, ChevronRight, BarChart3, Calendar,
} from "lucide-react"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"
import { cn } from "@/lib/utils"

const recentWorkouts = [
  { name: "Push Day — Chest & Shoulders", type: "Strength", duration: 52, calories: 380, date: "Today", exercises: 6, volume: 5200 },
  { name: "HIIT Cardio Blast", type: "Cardio", duration: 28, calories: 320, date: "Yesterday", exercises: 8, volume: 0 },
  { name: "Pull Day — Back & Biceps", type: "Strength", duration: 48, calories: 340, date: "2 days ago", exercises: 6, volume: 4800 },
  { name: "Leg Day — Quads & Glutes", type: "Strength", duration: 55, calories: 420, date: "3 days ago", exercises: 7, volume: 6200 },
  { name: "Yoga & Mobility", type: "Flexibility", duration: 35, calories: 120, date: "4 days ago", exercises: 12, volume: 0 },
]

const weeklyVolume = [
  { day: "Mon", volume: 5200, calories: 380 }, { day: "Tue", volume: 0, calories: 320 },
  { day: "Wed", volume: 4800, calories: 340 }, { day: "Thu", volume: 6200, calories: 420 },
  { day: "Fri", volume: 0, calories: 0 }, { day: "Sat", volume: 3800, calories: 280 },
  { day: "Sun", volume: 0, calories: 0 },
]

const plans = [
  { name: "Push/Pull/Legs Split", goal: "Muscle Gain", days: 6, difficulty: "Intermediate", active: true },
  { name: "Full Body 3x", goal: "General Fitness", days: 3, difficulty: "Beginner", active: false },
  { name: "Upper/Lower Split", goal: "Strength", days: 4, difficulty: "Advanced", active: false },
]

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } }
const item = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0 } }

export default function WorkoutsPage() {
  const [activeTab, setActiveTab] = useState<"overview" | "sessions" | "plans">("overview")

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6 pb-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-blue-400 shadow-lg shadow-indigo-500/25">
            <Dumbbell className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Workouts</h1>
            <p className="text-sm text-muted-foreground">Track, plan, and crush your training sessions</p>
          </div>
        </div>
        <button className={cn("flex h-10 items-center gap-2 rounded-xl px-4 text-sm font-semibold gradient-brand text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transition-all")}>
          <Plus className="h-4 w-4" /> Start Workout
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 p-1 rounded-xl bg-white/[0.03] border border-white/[0.06] w-fit">
        {(["overview", "sessions", "plans"] as const).map((tab) => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            className={cn("px-4 py-2 rounded-lg text-sm font-medium transition-all", activeTab === tab ? "bg-white/[0.08] text-foreground" : "text-muted-foreground hover:text-foreground")}>
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Stats Row */}
      <motion.div variants={item} className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="glass-card p-4 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/15"><Dumbbell className="h-5 w-5 text-indigo-400" /></div>
          <div><p className="text-lg font-bold">4</p><p className="text-xs text-muted-foreground">Workouts This Week</p></div>
        </div>
        <div className="glass-card p-4 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-500/15"><Flame className="h-5 w-5 text-orange-400" /></div>
          <div><p className="text-lg font-bold">1,460</p><p className="text-xs text-muted-foreground">Calories Burned</p></div>
        </div>
        <div className="glass-card p-4 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/15"><Clock className="h-5 w-5 text-emerald-400" /></div>
          <div><p className="text-lg font-bold">3h 23m</p><p className="text-xs text-muted-foreground">Total Time</p></div>
        </div>
        <div className="glass-card p-4 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/15"><TrendingUp className="h-5 w-5 text-amber-400" /></div>
          <div><p className="text-lg font-bold">22,200 kg</p><p className="text-xs text-muted-foreground">Total Volume</p></div>
        </div>
      </motion.div>

      {/* Charts + Sessions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <motion.div variants={item} className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4">Weekly Training Volume</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyVolume}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
                <Bar dataKey="volume" fill="#6366f1" radius={[4, 4, 0, 0]} name="Volume (kg)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div variants={item} className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4">Recent Sessions</h3>
          <div className="space-y-2">
            {recentWorkouts.map((w, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/[0.04] hover:bg-white/[0.04] transition-colors cursor-pointer">
                <div className="flex items-center gap-3">
                  <div className={cn("flex h-9 w-9 items-center justify-center rounded-lg text-sm",
                    w.type === "Strength" ? "bg-indigo-500/15 text-indigo-400" : w.type === "Cardio" ? "bg-rose-500/15 text-rose-400" : "bg-teal-500/15 text-teal-400")}>
                    {w.type === "Strength" ? "🏋️" : w.type === "Cardio" ? "🏃" : "🧘"}
                  </div>
                  <div>
                    <p className="text-sm font-medium">{w.name}</p>
                    <p className="text-xs text-muted-foreground">{w.date} • {w.exercises} exercises</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold">{w.duration}m</p>
                  <p className="text-xs text-orange-400">{w.calories} kcal</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Workout Plans */}
      <motion.div variants={item} className="glass-card p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold">My Workout Plans</h3>
          <button className="text-xs text-blue-400 hover:text-blue-300 font-medium transition-colors">+ Create Plan</button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {plans.map((plan, i) => (
            <div key={i} className={cn("relative rounded-xl p-4 border transition-all cursor-pointer hover:scale-[1.01]",
              plan.active ? "bg-indigo-500/10 border-indigo-500/20" : "bg-white/[0.02] border-white/[0.06] hover:bg-white/[0.04]")}>
              {plan.active && <span className="absolute top-3 right-3 rounded-full bg-emerald-500 px-2 py-0.5 text-[10px] font-bold text-white">Active</span>}
              <h4 className="text-sm font-semibold">{plan.name}</h4>
              <p className="text-xs text-muted-foreground mt-1">{plan.goal} • {plan.days}x/week</p>
              <div className="mt-3 flex items-center justify-between">
                <span className={cn("text-xs px-2 py-0.5 rounded-full", plan.difficulty === "Beginner" ? "bg-emerald-500/10 text-emerald-400" : plan.difficulty === "Intermediate" ? "bg-amber-500/10 text-amber-400" : "bg-red-500/10 text-red-400")}>{plan.difficulty}</span>
                <ChevronRight className="h-4 w-4 text-muted-foreground" />
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}
