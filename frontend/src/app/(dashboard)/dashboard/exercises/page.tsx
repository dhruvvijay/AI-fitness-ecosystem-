"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import { Library, Search, Filter, Play, ChevronDown, Bookmark } from "lucide-react"
import { cn } from "@/lib/utils"

const categories = ["All", "Chest", "Back", "Shoulders", "Arms", "Legs", "Core", "Cardio", "Full Body"]
const difficulties = ["All", "Beginner", "Intermediate", "Advanced"]

const exerciseData = [
  { name: "Barbell Bench Press", category: "Chest", muscle: "Pectorals", difficulty: "Intermediate", equipment: "Barbell", sets: 4, reps: "8-12", cal: 8.5, compound: true,
    instructions: ["Lie flat on the bench, grip slightly wider than shoulder width", "Unrack the bar, lower to mid-chest", "Press up explosively, lock out at top"] },
  { name: "Pull-ups", category: "Back", muscle: "Lats", difficulty: "Intermediate", equipment: "Pull-up Bar", sets: 3, reps: "8-10", cal: 7.0, compound: true,
    instructions: ["Hang with arms fully extended, overhand grip", "Pull up until chin is above the bar", "Lower slowly with control"] },
  { name: "Barbell Squat", category: "Legs", muscle: "Quadriceps", difficulty: "Intermediate", equipment: "Barbell", sets: 4, reps: "6-10", cal: 10.0, compound: true,
    instructions: ["Bar across upper back, feet shoulder-width", "Brace core, sit back and down", "Drive through heels to stand"] },
  { name: "Overhead Press", category: "Shoulders", muscle: "Deltoids", difficulty: "Intermediate", equipment: "Barbell", sets: 3, reps: "8-10", cal: 7.5, compound: true,
    instructions: ["Bar at front shoulders, grip slightly wider than shoulders", "Press overhead, lock arms out", "Lower slowly under control"] },
  { name: "Deadlift", category: "Back", muscle: "Posterior Chain", difficulty: "Advanced", equipment: "Barbell", sets: 4, reps: "5-8", cal: 12.0, compound: true,
    instructions: ["Bar over mid-foot, hip-width stance", "Hinge at hips, grip just outside legs", "Drive through floor, lock hips at top"] },
  { name: "Bicep Curls", category: "Arms", muscle: "Biceps", difficulty: "Beginner", equipment: "Dumbbells", sets: 3, reps: "10-15", cal: 4.0, compound: false,
    instructions: ["Stand with dumbbells at sides, palms forward", "Curl up keeping elbows pinned to sides", "Squeeze at top, lower slowly"] },
  { name: "Plank", category: "Core", muscle: "Abdominals", difficulty: "Beginner", equipment: "Bodyweight", sets: 3, reps: "30-60s", cal: 3.5, compound: false,
    instructions: ["Forearms on ground, body in straight line", "Engage core, don't let hips sag", "Hold for time, breathe steadily"] },
  { name: "Lateral Raises", category: "Shoulders", muscle: "Lateral Deltoid", difficulty: "Beginner", equipment: "Dumbbells", sets: 3, reps: "12-15", cal: 3.0, compound: false,
    instructions: ["Stand with dumbbells at sides", "Raise arms to sides until parallel to floor", "Lower slowly with control"] },
  { name: "Romanian Deadlift", category: "Legs", muscle: "Hamstrings", difficulty: "Intermediate", equipment: "Barbell", sets: 3, reps: "8-12", cal: 8.0, compound: true,
    instructions: ["Hold bar at hips, slight knee bend", "Hinge at hips, push butt back", "Lower until hamstring stretch, drive hips forward"] },
  { name: "Dumbbell Chest Fly", category: "Chest", muscle: "Pectorals", difficulty: "Beginner", equipment: "Dumbbells", sets: 3, reps: "10-12", cal: 5.0, compound: false,
    instructions: ["Lie on bench, arms extended above chest", "Open arms wide in arc motion", "Squeeze chest to bring dumbbells back together"] },
  { name: "Burpees", category: "Full Body", muscle: "Full Body", difficulty: "Intermediate", equipment: "Bodyweight", sets: 3, reps: "10-15", cal: 10.0, compound: true,
    instructions: ["Stand, then squat and place hands on floor", "Jump feet back to plank, do a push-up", "Jump feet forward, explode upward with jump"] },
  { name: "Mountain Climbers", category: "Cardio", muscle: "Core & Cardio", difficulty: "Beginner", equipment: "Bodyweight", sets: 3, reps: "20-30", cal: 8.0, compound: true,
    instructions: ["Start in push-up position", "Drive knees to chest alternately", "Keep pace fast, core tight"] },
]

export default function ExercisesPage() {
  const [search, setSearch] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("All")
  const [selectedDifficulty, setSelectedDifficulty] = useState("All")
  const [expandedExercise, setExpandedExercise] = useState<number | null>(null)

  const filtered = exerciseData.filter((ex) => {
    const matchSearch = !search || ex.name.toLowerCase().includes(search.toLowerCase()) || ex.muscle.toLowerCase().includes(search.toLowerCase())
    const matchCat = selectedCategory === "All" || ex.category === selectedCategory
    const matchDiff = selectedDifficulty === "All" || ex.difficulty === selectedDifficulty
    return matchSearch && matchCat && matchDiff
  })

  return (
    <div className="space-y-6 pb-8">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-fuchsia-500 to-purple-400 shadow-lg shadow-fuchsia-500/25">
          <Library className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Exercise Library</h1>
          <p className="text-sm text-muted-foreground">{exerciseData.length}+ exercises with instructions & videos</p>
        </div>
      </div>

      {/* Search + Filters */}
      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search exercises, muscles..."
            className="w-full h-11 rounded-xl pl-10 pr-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-fuchsia-500/30 transition-all" />
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex gap-2 overflow-x-auto scrollbar-thin pb-1">
        {categories.map((cat) => (
          <button key={cat} onClick={() => setSelectedCategory(cat)}
            className={cn("shrink-0 rounded-full px-4 py-2 text-xs font-medium transition-all",
              selectedCategory === cat ? "bg-fuchsia-500/20 text-fuchsia-400 border border-fuchsia-500/30" : "bg-white/[0.04] border border-white/[0.06] text-muted-foreground hover:bg-white/[0.06]")}>
            {cat}
          </button>
        ))}
      </div>

      {/* Difficulty Pills */}
      <div className="flex gap-2">
        {difficulties.map((d) => (
          <button key={d} onClick={() => setSelectedDifficulty(d)}
            className={cn("rounded-full px-3 py-1.5 text-xs font-medium transition-all",
              selectedDifficulty === d ? "bg-purple-500/20 text-purple-400 border border-purple-500/30" : "bg-white/[0.03] border border-white/[0.06] text-muted-foreground hover:bg-white/[0.05]")}>
            {d}
          </button>
        ))}
      </div>

      {/* Exercise Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {filtered.map((ex, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.03 }}
            className="glass-card overflow-hidden">
            <button onClick={() => setExpandedExercise(expandedExercise === i ? null : i)} className="flex w-full items-center justify-between p-4 text-left">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-fuchsia-500/20 to-purple-500/20 text-lg">
                  {ex.compound ? "🏋️" : "💪"}
                </div>
                <div>
                  <p className="text-sm font-semibold">{ex.name}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-xs text-muted-foreground">{ex.muscle}</span>
                    <span className="text-[10px] text-muted-foreground">•</span>
                    <span className={cn("text-[10px] px-1.5 py-0.5 rounded-full font-medium",
                      ex.difficulty === "Beginner" ? "bg-emerald-500/10 text-emerald-400" : ex.difficulty === "Intermediate" ? "bg-amber-500/10 text-amber-400" : "bg-red-500/10 text-red-400")}>
                      {ex.difficulty}
                    </span>
                    {ex.compound && <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 font-medium">Compound</span>}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">{ex.sets}×{ex.reps}</span>
                <ChevronDown className={cn("h-4 w-4 text-muted-foreground transition-transform", expandedExercise === i && "rotate-180")} />
              </div>
            </button>

            {expandedExercise === i && (
              <motion.div initial={{ height: 0 }} animate={{ height: "auto" }} className="border-t border-white/[0.06] p-4 space-y-3">
                <div className="flex gap-3">
                  <span className="text-xs px-2 py-1 rounded bg-white/[0.04]">🏷️ {ex.equipment}</span>
                  <span className="text-xs px-2 py-1 rounded bg-white/[0.04]">🔥 {ex.cal} cal/min</span>
                  <span className="text-xs px-2 py-1 rounded bg-white/[0.04]">📋 {ex.category}</span>
                </div>
                <div>
                  <p className="text-xs font-semibold mb-1.5">Instructions:</p>
                  <ol className="space-y-1">
                    {ex.instructions.map((step, j) => (
                      <li key={j} className="flex items-start gap-2 text-xs text-muted-foreground">
                        <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-fuchsia-500/10 text-fuchsia-400 text-[10px] font-bold mt-0.5">{j + 1}</span>
                        {step}
                      </li>
                    ))}
                  </ol>
                </div>
                <div className="flex gap-2">
                  <button className="flex-1 flex items-center justify-center gap-1.5 rounded-xl py-2.5 text-xs font-medium bg-fuchsia-500/10 text-fuchsia-400 hover:bg-fuchsia-500/20 transition-colors">
                    <Play className="h-3.5 w-3.5" /> Watch Demo
                  </button>
                  <button className="flex-1 flex items-center justify-center gap-1.5 rounded-xl py-2.5 text-xs font-medium bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 transition-colors">
                    <Bookmark className="h-3.5 w-3.5" /> Add to Plan
                  </button>
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12">
          <p className="text-sm text-muted-foreground">No exercises found matching your filters</p>
        </div>
      )}
    </div>
  )
}
