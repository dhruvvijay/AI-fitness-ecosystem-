"use client"

import React from "react"
import { motion } from "framer-motion"
import { BarChart3, TrendingUp, TrendingDown, Lightbulb, Target, Brain } from "lucide-react"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from "recharts"
import { cn } from "@/lib/utils"

const weightTrend = [
  { week: "W1", weight: 78.5 }, { week: "W2", weight: 78.0 }, { week: "W3", weight: 77.6 },
  { week: "W4", weight: 77.2 }, { week: "W5", weight: 76.5 }, { week: "W6", weight: 76.1 },
  { week: "W7", weight: 75.8 }, { week: "W8", weight: 75.2 },
]

const fitnessRadar = [
  { metric: "Strength", value: 78 }, { metric: "Endurance", value: 65 }, { metric: "Flexibility", value: 45 },
  { metric: "Nutrition", value: 82 }, { metric: "Recovery", value: 70 }, { metric: "Consistency", value: 88 },
]

const insights = [
  { icon: "💪", title: "Strength Up 12%", desc: "Your bench press volume increased 12% this month. Keep progressive overloading!", color: "text-emerald-400" },
  { icon: "🥗", title: "Protein Consistency", desc: "You've hit your protein target 85% of days this week. Great job!", color: "text-blue-400" },
  { icon: "💤", title: "Recovery Needed", desc: "Your workout frequency is high. Consider a deload week to prevent overtraining.", color: "text-amber-400" },
  { icon: "📈", title: "Weight Loss on Track", desc: "You've lost 3.3 kg in 8 weeks — a healthy 0.4 kg/week rate. On track for your goal!", color: "text-purple-400" },
  { icon: "💧", title: "Hydration Gap", desc: "You're averaging 2.1L/day but target is 3L. Try setting hourly water reminders.", color: "text-sky-400" },
]

const item = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0 } }
const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } }

export default function AnalyticsPage() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6 pb-8">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500 to-teal-400 shadow-lg shadow-emerald-500/25">
          <BarChart3 className="h-6 w-6 text-white" />
        </div>
        <div><h1 className="text-2xl font-bold tracking-tight">Analytics & Insights</h1><p className="text-sm text-muted-foreground">AI-powered analysis of your fitness journey</p></div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Weight Trend */}
        <motion.div variants={item} className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4">Weight Trend (8 Weeks)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={weightTrend}>
                <defs><linearGradient id="wg" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#a855f7" stopOpacity={0.3} /><stop offset="95%" stopColor="#a855f7" stopOpacity={0} /></linearGradient></defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="week" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <YAxis domain={["dataMin - 1", "dataMax + 1"]} stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
                <Area type="monotone" dataKey="weight" stroke="#a855f7" strokeWidth={2} fill="url(#wg)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="flex items-center gap-2 mt-3 text-xs text-emerald-400"><TrendingDown className="h-3.5 w-3.5" /> -3.3 kg in 8 weeks (0.4 kg/week avg)</div>
        </motion.div>

        {/* Fitness Radar */}
        <motion.div variants={item} className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4">Fitness Score Breakdown</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={fitnessRadar}>
                <PolarGrid stroke="rgba(255,255,255,0.08)" />
                <PolarAngleAxis dataKey="metric" tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar name="Score" dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.2} strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* AI Insights */}
      <motion.div variants={item} className="glass-card p-5">
        <h3 className="text-sm font-semibold mb-4 flex items-center gap-2"><Brain className="h-4 w-4 text-violet-400" /> AI Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {insights.map((insight, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
              className="rounded-xl bg-white/[0.02] border border-white/[0.06] p-4 hover:bg-white/[0.04] transition-colors">
              <div className="flex items-center gap-2 mb-2"><span className="text-lg">{insight.icon}</span><p className={cn("text-sm font-semibold", insight.color)}>{insight.title}</p></div>
              <p className="text-xs text-muted-foreground leading-relaxed">{insight.desc}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}
