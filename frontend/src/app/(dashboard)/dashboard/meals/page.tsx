"use client"

import React from "react"
import { motion } from "framer-motion"
import { UtensilsCrossed, Plus, Sparkles, Clock, Flame } from "lucide-react"
import { cn } from "@/lib/utils"

const todayMeals = [
  { type: "Breakfast", time: "8:30 AM", name: "Oatmeal Power Bowl", cal: 420, protein: 18, carbs: 55, fat: 14, items: ["Oats (50g)", "Mixed berries (80g)", "Eggs (2)", "Honey (10g)"] },
  { type: "Lunch", time: "1:00 PM", name: "Grilled Chicken Rice Bowl", cal: 580, protein: 48, carbs: 55, fat: 12, items: ["Chicken breast (200g)", "Brown rice (1 cup)", "Mixed salad", "Olive oil dressing"] },
  { type: "Snack", time: "4:30 PM", name: "Greek Yogurt & Almonds", cal: 180, protein: 15, carbs: 12, fat: 9, items: ["Greek yogurt (150g)", "Almonds (15g)", "Honey drizzle"] },
  { type: "Dinner", time: "7:30 PM", name: "Salmon with Sweet Potato", cal: 520, protein: 38, carbs: 35, fat: 22, items: ["Baked salmon (180g)", "Sweet potato (150g)", "Steamed broccoli", "Lemon butter"] },
]

export default function MealsPage() {
  const totalCal = todayMeals.reduce((s, m) => s + m.cal, 0)
  const totalPro = todayMeals.reduce((s, m) => s + m.protein, 0)

  return (
    <div className="space-y-6 pb-8">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-teal-500 to-cyan-400 shadow-lg shadow-teal-500/25">
            <UtensilsCrossed className="h-6 w-6 text-white" />
          </div>
          <div><h1 className="text-2xl font-bold tracking-tight">Meal Tracker</h1><p className="text-sm text-muted-foreground">Log and manage your daily nutrition</p></div>
        </div>
        <div className="flex gap-2">
          <button className="flex h-10 items-center gap-2 rounded-xl px-4 text-sm font-medium bg-violet-500/10 text-violet-400 hover:bg-violet-500/20 transition-colors">
            <Sparkles className="h-4 w-4" /> AI Meal Plan
          </button>
          <button className="flex h-10 items-center gap-2 rounded-xl px-4 text-sm font-semibold gradient-energy text-white shadow-lg shadow-emerald-500/25">
            <Plus className="h-4 w-4" /> Log Meal
          </button>
        </div>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-4 gap-3">
        <div className="glass-card p-4 text-center"><p className="text-xl font-bold text-orange-400">{totalCal}</p><p className="text-xs text-muted-foreground">Total Calories</p></div>
        <div className="glass-card p-4 text-center"><p className="text-xl font-bold text-blue-400">{totalPro}g</p><p className="text-xs text-muted-foreground">Total Protein</p></div>
        <div className="glass-card p-4 text-center"><p className="text-xl font-bold text-emerald-400">{todayMeals.length}</p><p className="text-xs text-muted-foreground">Meals Logged</p></div>
        <div className="glass-card p-4 text-center"><p className="text-xl font-bold text-purple-400">500</p><p className="text-xs text-muted-foreground">Remaining</p></div>
      </div>

      {/* Meal Cards */}
      <div className="space-y-4">
        {todayMeals.map((meal, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }} className="glass-card p-5">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-500/10 text-lg">
                  {meal.type === "Breakfast" ? "🌅" : meal.type === "Lunch" ? "☀️" : meal.type === "Snack" ? "🍎" : "🌙"}
                </div>
                <div>
                  <p className="text-sm font-semibold">{meal.name}</p>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground"><Clock className="h-3 w-3" /> {meal.time} • {meal.type}</div>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-orange-400">{meal.cal} <span className="text-xs font-normal text-muted-foreground">kcal</span></p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-2 mb-3">
              <div className="rounded-lg bg-blue-500/10 p-2 text-center"><p className="text-sm font-bold text-blue-400">{meal.protein}g</p><p className="text-[10px] text-muted-foreground">Protein</p></div>
              <div className="rounded-lg bg-green-500/10 p-2 text-center"><p className="text-sm font-bold text-green-400">{meal.carbs}g</p><p className="text-[10px] text-muted-foreground">Carbs</p></div>
              <div className="rounded-lg bg-amber-500/10 p-2 text-center"><p className="text-sm font-bold text-amber-400">{meal.fat}g</p><p className="text-[10px] text-muted-foreground">Fat</p></div>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {meal.items.map((item, j) => (
                <span key={j} className="rounded-full bg-white/[0.04] border border-white/[0.06] px-2.5 py-1 text-[10px] text-muted-foreground">{item}</span>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
