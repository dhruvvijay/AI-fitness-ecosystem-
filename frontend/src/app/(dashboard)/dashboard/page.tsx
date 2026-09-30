"use client"

import React, { useEffect, useState } from "react"
import { motion } from "framer-motion"
import {
  Footprints, Flame, Timer, Heart, Droplets, Weight,
  TrendingUp, Trophy, Moon, Zap, Activity, Target,
} from "lucide-react"
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell,
} from "recharts"
import { StatCard, ProgressRing, MacroBar, WaterTracker, StreakBadge } from "@/components/charts/DashboardWidgets"
import { useAppDispatch, useAppSelector } from "@/store"
import { fetchDashboardSummary } from "@/store/slices/dashboardSlice"
import { cn, formatCalories } from "@/lib/utils"
import { dashboardAPI, nutritionAPI } from "@/lib/api"

// Demo data for charts when API is not connected
const weeklyStepsData = [
  { day: "Mon", steps: 8432, calories: 320 },
  { day: "Tue", steps: 12045, calories: 450 },
  { day: "Wed", steps: 9876, calories: 380 },
  { day: "Thu", steps: 11234, calories: 420 },
  { day: "Fri", steps: 7654, calories: 290 },
  { day: "Sat", steps: 14320, calories: 530 },
  { day: "Sun", steps: 10567, calories: 400 },
]

const weeklyCaloriesData = [
  { day: "Mon", consumed: 2100, burned: 450 },
  { day: "Tue", consumed: 1980, burned: 520 },
  { day: "Wed", consumed: 2250, burned: 380 },
  { day: "Thu", consumed: 1850, burned: 600 },
  { day: "Fri", consumed: 2400, burned: 350 },
  { day: "Sat", consumed: 2000, burned: 480 },
  { day: "Sun", consumed: 1900, burned: 550 },
]

const activityHeatmap = Array.from({ length: 7 }, (_, i) =>
  Array.from({ length: 24 }, (_, j) => ({
    day: i,
    hour: j,
    value: Math.floor(Math.random() * 100),
  }))
).flat()

const MACRO_COLORS = {
  protein: "#3b82f6",
  carbs: "#22c55e",
  fat: "#f97316",
  fiber: "#a855f7",
}

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.06 } },
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
}

export default function DashboardPage() {
  const dispatch = useAppDispatch()
  const { summary, isLoading } = useAppSelector((s) => s.dashboard)
  const { user } = useAppSelector((s) => s.auth)

  // Use demo data when backend is not connected
  const data = summary || {
    today_steps: 8743,
    today_calories_consumed: 1680,
    today_calories_burned: 420,
    remaining_calories: 900,
    workout_time_minutes: 45,
    heart_rate: 72,
    protein_g: 98,
    carbs_g: 195,
    fat_g: 52,
    fiber_g: 18,
    water_ml: 1750,
    water_target_ml: 3000,
    weight_kg: 75.2,
    bmi: 23.4,
    body_fat: 18.5,
    workout_streak: 12,
    daily_goal_progress: 68,
    weekly_goal_progress: 72,
    monthly_goal_progress: 65,
    achievements_count: 14,
    sleep_hours: 7.2,
    distance_km: 6.3,
    exercise_minutes: 45,
  }

  useEffect(() => {
    dispatch(fetchDashboardSummary(undefined))
  }, [dispatch])

  const handleAddWater = async (ml: number) => {
    try {
      await nutritionAPI.logWater(ml)
      dispatch(fetchDashboardSummary(undefined))
    } catch {
      // In demo mode, just update locally
    }
  }

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="space-y-6 pb-8"
    >
      {/* ── Row 1: Quick Stats ──────────────────────────────── */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <motion.div variants={item}>
          <StatCard
            title="Steps"
            value={data.today_steps.toLocaleString()}
            subtitle="/ 10,000 goal"
            icon={Footprints}
            gradient="from-green-500 to-emerald-400"
            trend={{ value: 12, label: "vs yesterday" }}
          />
        </motion.div>
        <motion.div variants={item}>
          <StatCard
            title="Calories In"
            value={formatCalories(data.today_calories_consumed)}
            subtitle="kcal consumed"
            icon={Flame}
            gradient="from-orange-500 to-amber-400"
          />
        </motion.div>
        <motion.div variants={item}>
          <StatCard
            title="Burned"
            value={formatCalories(data.today_calories_burned)}
            subtitle="kcal burned"
            icon={Zap}
            gradient="from-rose-500 to-pink-400"
          />
        </motion.div>
        <motion.div variants={item}>
          <StatCard
            title="Workout"
            value={`${data.workout_time_minutes}m`}
            subtitle="exercise time"
            icon={Timer}
            gradient="from-blue-500 to-cyan-400"
          />
        </motion.div>
        <motion.div variants={item}>
          <StatCard
            title="Heart Rate"
            value={data.heart_rate || "--"}
            subtitle="bpm avg"
            icon={Heart}
            gradient="from-red-500 to-rose-400"
          />
        </motion.div>
        <motion.div variants={item}>
          <StatCard
            title="Distance"
            value={`${data.distance_km} km`}
            subtitle="walked/ran"
            icon={Activity}
            gradient="from-indigo-500 to-violet-400"
          />
        </motion.div>
      </div>

      {/* ── Row 2: Progress Rings + Macros + Water ─────────── */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Progress Rings */}
        <motion.div variants={item} className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-5">Today&apos;s Progress</h3>
          <div className="flex items-center justify-around">
            <ProgressRing
              value={data.today_calories_consumed}
              max={2500}
              color="#f97316"
              label="Calories"
              unit="kcal"
            />
            <ProgressRing
              value={data.protein_g}
              max={150}
              color="#3b82f6"
              label="Protein"
              unit="g"
            />
            <ProgressRing
              value={data.today_steps}
              max={10000}
              size={100}
              color="#22c55e"
              label="Steps"
              unit="steps"
            />
          </div>
        </motion.div>

        {/* Macronutrients */}
        <motion.div variants={item} className="glass-card p-5 space-y-4">
          <h3 className="text-sm font-semibold">Macros Breakdown</h3>
          <MacroBar label="Protein" current={data.protein_g} target={150} color={MACRO_COLORS.protein} />
          <MacroBar label="Carbs" current={data.carbs_g} target={250} color={MACRO_COLORS.carbs} />
          <MacroBar label="Fat" current={data.fat_g} target={65} color={MACRO_COLORS.fat} />
          <MacroBar label="Fiber" current={data.fiber_g} target={30} color={MACRO_COLORS.fiber} />
        </motion.div>

        {/* Water Tracker */}
        <motion.div variants={item}>
          <WaterTracker
            current={data.water_ml}
            target={data.water_target_ml}
            onAdd={handleAddWater}
          />
        </motion.div>
      </div>

      {/* ── Row 3: Charts ────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Steps Chart */}
        <motion.div variants={item} className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4">Weekly Steps</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={weeklyStepsData}>
                <defs>
                  <linearGradient id="stepsGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(15,15,35,0.95)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: "12px",
                    fontSize: "12px",
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="steps"
                  stroke="#22c55e"
                  strokeWidth={2}
                  fill="url(#stepsGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Calories Chart */}
        <motion.div variants={item} className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4">Calories In vs Out</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyCaloriesData} barGap={4}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(15,15,35,0.95)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: "12px",
                    fontSize: "12px",
                  }}
                />
                <Bar dataKey="consumed" fill="#f97316" radius={[4, 4, 0, 0]} name="Consumed" />
                <Bar dataKey="burned" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Burned" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* ── Row 4: Bottom Stats ──────────────────────────────── */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <motion.div variants={item}>
          <StreakBadge count={data.workout_streak} label="Day Workout Streak" />
        </motion.div>

        <motion.div variants={item} className="glass-card p-4 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-purple-500 to-violet-400 shadow-lg shadow-purple-500/20">
            <Weight className="h-5 w-5 text-white" />
          </div>
          <div>
            <p className="text-lg font-bold">{data.weight_kg || "--"} kg</p>
            <p className="text-xs text-muted-foreground">Current Weight</p>
          </div>
        </motion.div>

        <motion.div variants={item} className="glass-card p-4 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-blue-400 shadow-lg shadow-sky-500/20">
            <TrendingUp className="h-5 w-5 text-white" />
          </div>
          <div>
            <p className="text-lg font-bold">{data.bmi || "--"}</p>
            <p className="text-xs text-muted-foreground">BMI (Normal)</p>
          </div>
        </motion.div>

        <motion.div variants={item} className="glass-card p-4 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-amber-500 to-yellow-400 shadow-lg shadow-amber-500/20">
            <Trophy className="h-5 w-5 text-white" />
          </div>
          <div>
            <p className="text-lg font-bold">{data.achievements_count}</p>
            <p className="text-xs text-muted-foreground">Achievements</p>
          </div>
        </motion.div>
      </div>

      {/* ── Row 5: Goal Progress Bars ────────────────────────── */}
      <motion.div variants={item} className="glass-card p-5 space-y-5">
        <h3 className="text-sm font-semibold">Goal Completion</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <GoalProgress label="Daily Goal" value={data.daily_goal_progress} color="from-blue-500 to-cyan-400" />
          <GoalProgress label="Weekly Goal" value={data.weekly_goal_progress} color="from-emerald-500 to-teal-400" />
          <GoalProgress label="Monthly Goal" value={data.monthly_goal_progress} color="from-purple-500 to-violet-400" />
        </div>
      </motion.div>
    </motion.div>
  )
}

function GoalProgress({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium">{label}</span>
        <span className="text-muted-foreground">{Math.round(value)}%</span>
      </div>
      <div className="h-3 w-full rounded-full bg-white/[0.06] overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1.2, ease: "easeOut", delay: 0.3 }}
          className={cn("h-full rounded-full bg-gradient-to-r", color)}
        />
      </div>
    </div>
  )
}
