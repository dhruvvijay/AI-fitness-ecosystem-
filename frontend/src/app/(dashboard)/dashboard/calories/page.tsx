"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import { Flame, Plus, TrendingDown, TrendingUp, Target } from "lucide-react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"
import { cn } from "@/lib/utils"
import { MacroBar } from "@/components/charts/DashboardWidgets"

const weeklyData = [
  { day: "Mon", consumed: 2100, burned: 450 }, { day: "Tue", consumed: 1980, burned: 520 },
  { day: "Wed", consumed: 2250, burned: 380 }, { day: "Thu", consumed: 1850, burned: 600 },
  { day: "Fri", consumed: 2400, burned: 350 }, { day: "Sat", consumed: 2000, burned: 480 },
  { day: "Sun", consumed: 1900, burned: 550 },
]

const macroData = [
  { name: "Protein", value: 98, color: "#3b82f6" },
  { name: "Carbs", value: 195, color: "#22c55e" },
  { name: "Fat", value: 52, color: "#f97316" },
]

const mealLog = [
  { meal: "Breakfast", calories: 420, time: "8:30 AM", items: "Oats, eggs, banana" },
  { meal: "Lunch", calories: 580, time: "1:00 PM", items: "Chicken rice, salad" },
  { meal: "Snack", calories: 180, time: "4:30 PM", items: "Greek yogurt, almonds" },
  { meal: "Dinner", calories: 500, time: "7:30 PM", items: "Salmon, sweet potato" },
]

export default function CaloriesPage() {
  const consumed = 1680, burned = 420, target = 2200
  const net = consumed - burned
  const remaining = Math.max(0, target - consumed + burned)

  return (
    <div className="space-y-6 pb-8">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-orange-500 to-amber-400 shadow-lg shadow-orange-500/25">
          <Flame className="h-6 w-6 text-white" />
        </div>
        <div><h1 className="text-2xl font-bold tracking-tight">Calorie Tracker</h1><p className="text-sm text-muted-foreground">Track your energy balance</p></div>
      </div>

      {/* Top Summary */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <div className="glass-card p-4 text-center"><p className="text-2xl font-bold text-orange-400">{consumed}</p><p className="text-xs text-muted-foreground">Consumed</p></div>
        <div className="glass-card p-4 text-center"><p className="text-2xl font-bold text-blue-400">{burned}</p><p className="text-xs text-muted-foreground">Burned</p></div>
        <div className="glass-card p-4 text-center"><p className="text-2xl font-bold text-emerald-400">{net}</p><p className="text-xs text-muted-foreground">Net Calories</p></div>
        <div className="glass-card p-4 text-center"><p className="text-2xl font-bold text-purple-400">{remaining}</p><p className="text-xs text-muted-foreground">Remaining</p></div>
        <div className="glass-card p-4 text-center"><p className="text-2xl font-bold">{target}</p><p className="text-xs text-muted-foreground">Daily Target</p></div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Weekly Chart */}
        <div className="glass-card p-5 lg:col-span-2">
          <h3 className="text-sm font-semibold mb-4">Weekly Calories</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData} barGap={4}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
                <Bar dataKey="consumed" fill="#f97316" radius={[4, 4, 0, 0]} name="Consumed" />
                <Bar dataKey="burned" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Burned" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Macro Pie */}
        <div className="glass-card p-5 flex flex-col items-center justify-center">
          <h3 className="text-sm font-semibold mb-4 self-start">Macro Split</h3>
          <div className="h-48 w-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={macroData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={3} dataKey="value">
                  {macroData.map((entry, i) => (<Cell key={i} fill={entry.color} />))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex gap-4 mt-2">
            {macroData.map((m) => (<div key={m.name} className="flex items-center gap-1.5 text-xs"><div className="h-2.5 w-2.5 rounded-full" style={{ background: m.color }} />{m.name}: {m.value}g</div>))}
          </div>
        </div>
      </div>

      {/* Today's Meals */}
      <div className="glass-card p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold">Today&apos;s Meals</h3>
          <button className="text-xs text-orange-400 hover:text-orange-300 font-medium">+ Log Meal</button>
        </div>
        <div className="space-y-2">
          {mealLog.map((m, i) => (
            <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/[0.04]">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-orange-500/10 text-sm">
                  {m.meal === "Breakfast" ? "🌅" : m.meal === "Lunch" ? "☀️" : m.meal === "Snack" ? "🍎" : "🌙"}
                </div>
                <div><p className="text-sm font-medium">{m.meal}</p><p className="text-xs text-muted-foreground">{m.items}</p></div>
              </div>
              <div className="text-right"><p className="text-sm font-bold text-orange-400">{m.calories} kcal</p><p className="text-xs text-muted-foreground">{m.time}</p></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
