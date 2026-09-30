"use client"

import React from "react"
import { motion } from "framer-motion"
import { Target, Trophy, Calendar, CheckCircle2, Circle, Flame } from "lucide-react"
import { cn } from "@/lib/utils"

const goals = [
  { title: "Lose 10 kg", target: 10, current: 6.8, unit: "kg", deadline: "Oct 2026", category: "Weight", color: "from-purple-500 to-violet-400" },
  { title: "Run 5K under 25 min", target: 25, current: 27.5, unit: "min", deadline: "Sep 2026", category: "Cardio", color: "from-rose-500 to-pink-400" },
  { title: "Bench Press 100 kg", target: 100, current: 82, unit: "kg", deadline: "Dec 2026", category: "Strength", color: "from-indigo-500 to-blue-400" },
  { title: "1000 Push-ups/month", target: 1000, current: 680, unit: "reps", deadline: "Monthly", category: "Challenge", color: "from-amber-500 to-orange-400" },
]

const achievements = [
  { name: "First Workout", icon: "🏋️", desc: "Complete your first workout", earned: true },
  { name: "7-Day Streak", icon: "🔥", desc: "Work out 7 consecutive days", earned: true },
  { name: "Calorie Master", icon: "🥗", desc: "Hit calorie target 30 days in a row", earned: true },
  { name: "10K Steps Club", icon: "🚶", desc: "Reach 10,000 steps in a day", earned: true },
  { name: "Iron Warrior", icon: "⚔️", desc: "Lift 100,000 kg total volume", earned: false },
  { name: "Marathon Runner", icon: "🏃", desc: "Run 42 km total distance", earned: false },
  { name: "Perfect Week", icon: "⭐", desc: "Hit all daily targets for a full week", earned: false },
  { name: "Century Club", icon: "💯", desc: "Log 100 workouts", earned: false },
]

const dailyChallenges = [
  { title: "Walk 8,000 steps", progress: 87, done: false },
  { title: "Drink 3L water", progress: 58, done: false },
  { title: "Eat 150g protein", progress: 65, done: false },
  { title: "30 min workout", progress: 100, done: true },
]

export default function GoalsPage() {
  return (
    <div className="space-y-6 pb-8">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-yellow-500 to-orange-400 shadow-lg shadow-yellow-500/25">
          <Target className="h-6 w-6 text-white" />
        </div>
        <div><h1 className="text-2xl font-bold tracking-tight">Goals & Achievements</h1><p className="text-sm text-muted-foreground">Track your fitness milestones</p></div>
      </div>

      {/* Daily Challenges */}
      <div className="glass-card p-5">
        <h3 className="text-sm font-semibold mb-4 flex items-center gap-2"><Flame className="h-4 w-4 text-orange-400" /> Today&apos;s Challenges</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {dailyChallenges.map((c, i) => (
            <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-white/[0.02] border border-white/[0.04]">
              {c.done ? <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" /> : <Circle className="h-5 w-5 text-muted-foreground shrink-0" />}
              <div className="flex-1">
                <p className={cn("text-sm font-medium", c.done && "line-through text-muted-foreground")}>{c.title}</p>
                <div className="mt-1 h-1.5 w-full rounded-full bg-white/[0.06] overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${c.progress}%` }} transition={{ duration: 1 }}
                    className={cn("h-full rounded-full", c.done ? "bg-emerald-500" : "bg-amber-500")} />
                </div>
              </div>
              <span className="text-xs text-muted-foreground">{c.progress}%</span>
            </div>
          ))}
        </div>
      </div>

      {/* Long-term Goals */}
      <div className="glass-card p-5">
        <h3 className="text-sm font-semibold mb-4">My Goals</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {goals.map((goal, i) => {
            const pct = Math.min(100, (goal.current / goal.target) * 100)
            return (
              <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
                className="rounded-xl bg-white/[0.02] border border-white/[0.06] p-4 hover:bg-white/[0.04] transition-colors">
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <p className="text-sm font-semibold">{goal.title}</p>
                    <p className="text-xs text-muted-foreground">{goal.category} • Due {goal.deadline}</p>
                  </div>
                  <span className="text-lg font-bold">{Math.round(pct)}%</span>
                </div>
                <div className="h-2.5 w-full rounded-full bg-white/[0.06] overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ duration: 1.2, delay: i * 0.1 }}
                    className={cn("h-full rounded-full bg-gradient-to-r", goal.color)} />
                </div>
                <p className="text-xs text-muted-foreground mt-2">{goal.current} / {goal.target} {goal.unit}</p>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Achievements */}
      <div className="glass-card p-5">
        <h3 className="text-sm font-semibold mb-4 flex items-center gap-2"><Trophy className="h-4 w-4 text-amber-400" /> Achievements ({achievements.filter(a => a.earned).length}/{achievements.length})</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {achievements.map((a, i) => (
            <motion.div key={i} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.05 }}
              className={cn("rounded-xl p-4 text-center border transition-all",
                a.earned ? "bg-amber-500/5 border-amber-500/20" : "bg-white/[0.01] border-white/[0.06] opacity-50")}>
              <span className="text-3xl">{a.icon}</span>
              <p className="text-xs font-semibold mt-2">{a.name}</p>
              <p className="text-[10px] text-muted-foreground mt-0.5">{a.desc}</p>
              {a.earned && <span className="text-[10px] text-amber-400 font-medium mt-1 block">✓ Earned</span>}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}
