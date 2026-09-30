"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import {
  Calculator, TrendingUp, Target, Activity, Droplets, Scale, Flame,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { goalsAPI } from "@/lib/api"

const activityOptions = [
  { value: "sedentary", label: "Sedentary", desc: "Little/no exercise" },
  { value: "light", label: "Light", desc: "1-3 days/week" },
  { value: "moderate", label: "Moderate", desc: "3-5 days/week" },
  { value: "active", label: "Active", desc: "6-7 days/week" },
  { value: "very_active", label: "Very Active", desc: "Intense daily" },
]

interface BMIResult {
  bmi: number
  category: string
  healthy_weight_range: { min_kg: number; max_kg: number }
  ideal_weight: number
  bmr: number
  tdee: number
  maintenance_calories: number
  recommended_calories: number
  protein_g: number
  carbs_g: number
  fat_g: number
  water_ml: number
  recommended_goal: string
}

export default function BMICalculatorPage() {
  const [weight, setWeight] = useState<number>(70)
  const [height, setHeight] = useState<number>(170)
  const [age, setAge] = useState<number>(25)
  const [gender, setGender] = useState<string>("male")
  const [activity, setActivity] = useState<string>("moderate")
  const [bodyFat, setBodyFat] = useState<string>("")
  const [result, setResult] = useState<BMIResult | null>(null)
  const [loading, setLoading] = useState(false)

  const handleCalculate = async () => {
    setLoading(true)
    try {
      const { data } = await goalsAPI.calculateBMI({
        weight_kg: weight, height_cm: height, age, gender,
        activity_level: activity,
        body_fat_percentage: bodyFat ? parseFloat(bodyFat) : null,
      })
      setResult(data)
    } catch {
      // Local calculation fallback
      const heightM = height / 100
      const bmi = weight / (heightM * heightM)
      const bmr = gender === "male"
        ? (10 * weight) + (6.25 * height) - (5 * age) + 5
        : (10 * weight) + (6.25 * height) - (5 * age) - 161
      const multiplier = { sedentary: 1.2, light: 1.375, moderate: 1.55, active: 1.725, very_active: 1.9 }
      const tdee = bmr * (multiplier[activity as keyof typeof multiplier] || 1.55)
      const recCal = bmi > 25 ? tdee - 500 : bmi < 18.5 ? tdee + 300 : tdee
      const proteinG = weight * 1.6
      const fatG = (recCal * 0.25) / 9
      const carbsG = (recCal - proteinG * 4 - fatG * 9) / 4

      setResult({
        bmi: Math.round(bmi * 10) / 10,
        category: bmi < 18.5 ? "underweight" : bmi < 25 ? "normal" : bmi < 30 ? "overweight" : "obese_class_1",
        healthy_weight_range: { min_kg: Math.round(18.5 * heightM * heightM * 10) / 10, max_kg: Math.round(24.9 * heightM * heightM * 10) / 10 },
        ideal_weight: Math.round((gender === "male" ? 50 + 2.3 * Math.max(0, height / 2.54 - 60) : 45.5 + 2.3 * Math.max(0, height / 2.54 - 60)) * 10) / 10,
        bmr: Math.round(bmr), tdee: Math.round(tdee),
        maintenance_calories: Math.round(tdee),
        recommended_calories: Math.round(recCal),
        protein_g: Math.round(proteinG), carbs_g: Math.round(carbsG), fat_g: Math.round(fatG),
        water_ml: Math.round((weight * 35 + 500) / 100) * 100,
        recommended_goal: bmi > 25 ? "lose_weight" : bmi < 18.5 ? "gain_muscle" : "maintain",
      })
    } finally {
      setLoading(false)
    }
  }

  const getCategoryColor = (cat: string) => {
    const colors: Record<string, string> = {
      underweight: "text-amber-400 bg-amber-500/10", normal: "text-emerald-400 bg-emerald-500/10",
      overweight: "text-orange-400 bg-orange-500/10", obese_class_1: "text-red-400 bg-red-500/10",
      obese_class_2: "text-red-500 bg-red-500/15", obese_class_3: "text-red-600 bg-red-500/20",
      severely_underweight: "text-red-400 bg-red-500/10",
    }
    return colors[cat] || "text-gray-400 bg-gray-500/10"
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-8">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-purple-500 to-violet-400 shadow-lg shadow-purple-500/25">
          <Calculator className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">BMI Calculator</h1>
          <p className="text-sm text-muted-foreground">Calculate BMI, BMR, TDEE, and get personalized macro recommendations</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="glass-card p-6 space-y-5">
          <h3 className="text-sm font-semibold">Your Measurements</h3>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-muted-foreground">Weight (kg)</label>
              <input type="number" value={weight} onChange={(e) => setWeight(Number(e.target.value))} min={20} max={300} step={0.1}
                className="w-full h-11 rounded-xl px-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-purple-500/30 transition-all" />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-muted-foreground">Height (cm)</label>
              <input type="number" value={height} onChange={(e) => setHeight(Number(e.target.value))} min={100} max={250}
                className="w-full h-11 rounded-xl px-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-purple-500/30 transition-all" />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-muted-foreground">Age</label>
              <input type="number" value={age} onChange={(e) => setAge(Number(e.target.value))} min={10} max={100}
                className="w-full h-11 rounded-xl px-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-purple-500/30 transition-all" />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-muted-foreground">Body Fat % (optional)</label>
              <input type="number" value={bodyFat} onChange={(e) => setBodyFat(e.target.value)} placeholder="e.g. 18" min={3} max={60} step={0.1}
                className="w-full h-11 rounded-xl px-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-purple-500/30 transition-all" />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-medium text-muted-foreground">Gender</label>
            <div className="grid grid-cols-2 gap-3">
              {["male", "female"].map((g) => (
                <button key={g} onClick={() => setGender(g)}
                  className={cn("h-11 rounded-xl text-sm font-medium transition-all", gender === g ? "bg-purple-500/20 text-purple-400 border border-purple-500/30" : "bg-white/[0.04] border border-white/[0.08] text-muted-foreground hover:bg-white/[0.06]")}>
                  {g === "male" ? "♂ Male" : "♀ Female"}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-medium text-muted-foreground">Activity Level</label>
            <div className="space-y-1.5">
              {activityOptions.map((opt) => (
                <button key={opt.value} onClick={() => setActivity(opt.value)}
                  className={cn("flex w-full items-center justify-between rounded-xl px-4 py-2.5 text-sm transition-all", activity === opt.value ? "bg-purple-500/15 text-purple-400 border border-purple-500/30" : "bg-white/[0.02] border border-white/[0.06] text-muted-foreground hover:bg-white/[0.04]")}>
                  <span className="font-medium">{opt.label}</span>
                  <span className="text-xs opacity-60">{opt.desc}</span>
                </button>
              ))}
            </div>
          </div>

          <button onClick={handleCalculate} disabled={loading}
            className={cn("flex w-full h-12 items-center justify-center gap-2 rounded-xl text-sm font-semibold bg-gradient-to-r from-purple-500 to-violet-500 text-white shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 disabled:opacity-60 transition-all duration-200")}>
            {loading ? <div className="h-5 w-5 rounded-full border-2 border-white/30 border-t-white animate-spin" /> : <><Calculator className="h-4 w-4" /> Calculate</>}
          </button>
        </div>

        {/* Results */}
        {result ? (
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
            {/* BMI Display */}
            <div className="glass-card p-6 text-center">
              <p className="text-xs text-muted-foreground mb-1">Your BMI</p>
              <p className="text-5xl font-black tracking-tight">{result.bmi}</p>
              <div className={cn("inline-block rounded-full px-4 py-1 text-xs font-bold mt-2", getCategoryColor(result.category))}>
                {result.category.replace(/_/g, " ").toUpperCase()}
              </div>
              <div className="mt-4 h-3 w-full rounded-full bg-white/[0.06] overflow-hidden relative">
                <div className="absolute inset-0 flex">
                  <div className="flex-1 bg-amber-500/30" /><div className="flex-1 bg-emerald-500/30" /><div className="flex-1 bg-orange-500/30" /><div className="flex-1 bg-red-500/30" />
                </div>
                <div className="absolute top-0 bottom-0 w-1 bg-white rounded-full shadow-lg shadow-white/50" style={{ left: `${Math.min(95, Math.max(5, ((result.bmi - 15) / 25) * 100))}%` }} />
              </div>
              <div className="flex justify-between text-[10px] text-muted-foreground mt-1">
                <span>Underweight</span><span>Normal</span><span>Overweight</span><span>Obese</span>
              </div>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-2 gap-3">
              <MetricCard icon={Flame} label="BMR" value={`${result.bmr} kcal`} desc="Basal Metabolic Rate" gradient="from-orange-500 to-amber-400" />
              <MetricCard icon={Activity} label="TDEE" value={`${result.tdee} kcal`} desc="Total Daily Energy" gradient="from-blue-500 to-cyan-400" />
              <MetricCard icon={Target} label="Recommended" value={`${result.recommended_calories} kcal`} desc="Daily Target" gradient="from-emerald-500 to-teal-400" />
              <MetricCard icon={Scale} label="Ideal Weight" value={`${result.ideal_weight} kg`} desc={`Range: ${result.healthy_weight_range.min_kg}-${result.healthy_weight_range.max_kg} kg`} gradient="from-purple-500 to-violet-400" />
            </div>

            {/* Macros */}
            <div className="glass-card p-5">
              <h3 className="text-sm font-semibold mb-4">Recommended Daily Macros</h3>
              <div className="grid grid-cols-3 gap-3">
                <div className="text-center p-3 rounded-xl bg-blue-500/10">
                  <p className="text-xl font-bold text-blue-400">{result.protein_g}g</p>
                  <p className="text-[10px] text-muted-foreground mt-0.5">Protein</p>
                </div>
                <div className="text-center p-3 rounded-xl bg-green-500/10">
                  <p className="text-xl font-bold text-green-400">{result.carbs_g}g</p>
                  <p className="text-[10px] text-muted-foreground mt-0.5">Carbs</p>
                </div>
                <div className="text-center p-3 rounded-xl bg-amber-500/10">
                  <p className="text-xl font-bold text-amber-400">{result.fat_g}g</p>
                  <p className="text-[10px] text-muted-foreground mt-0.5">Fat</p>
                </div>
              </div>
            </div>

            {/* Water */}
            <div className="glass-card p-5 flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-blue-400 shadow-lg shadow-sky-500/20">
                <Droplets className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-lg font-bold">{result.water_ml} ml</p>
                <p className="text-xs text-muted-foreground">Recommended Daily Water Intake ({(result.water_ml / 250).toFixed(0)} glasses)</p>
              </div>
            </div>
          </motion.div>
        ) : (
          <div className="flex items-center justify-center glass-card p-8 min-h-[400px]">
            <div className="text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-purple-500/10 mx-auto mb-4">
                <Calculator className="h-8 w-8 text-purple-400" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Enter Your Details</h3>
              <p className="text-sm text-muted-foreground max-w-xs">
                Fill in your measurements to get a comprehensive health analysis with BMI, BMR, TDEE, and personalized macro targets.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function MetricCard({ icon: Icon, label, value, desc, gradient }: {
  icon: any; label: string; value: string; desc: string; gradient: string
}) {
  return (
    <div className="glass-card p-4 flex items-center gap-3">
      <div className={cn("flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br shadow-lg", gradient)}>
        <Icon className="h-5 w-5 text-white" />
      </div>
      <div>
        <p className="text-xs text-muted-foreground">{label}</p>
        <p className="text-sm font-bold">{value}</p>
        <p className="text-[10px] text-muted-foreground">{desc}</p>
      </div>
    </div>
  )
}
