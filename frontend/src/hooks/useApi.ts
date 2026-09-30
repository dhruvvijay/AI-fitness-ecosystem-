/**
 * Custom React hooks for API data fetching.
 * Uses SWR-like pattern with React state for simplicity.
 * Wraps all API calls with loading/error states and auto-refetch.
 */

import { useState, useEffect, useCallback } from "react"
import {
  dashboardAPI,
  stepsAPI,
  nutritionAPI,
  workoutAPI,
  goalsAPI,
  analyticsAPI,
  notificationsAPI,
  devicesAPI,
} from "@/lib/api"

interface ApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
  refetch: () => void
}

/**
 * Generic fetch hook — calls an API function and manages state.
 */
function useApi<T>(fetcher: () => Promise<{ data: { data: T } }>, deps: unknown[] = []): ApiState<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetch = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetcher()
      setData(response.data.data)
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "An error occurred"
      setError(message)
    } finally {
      setLoading(false)
    }
  }, deps)

  useEffect(() => {
    fetch()
  }, [fetch])

  return { data, loading, error, refetch: fetch }
}

// ── Dashboard ─────────────────────────────────────────────

export function useDashboard() {
  return useApi(() => dashboardAPI.getDashboard())
}

// ── Steps ─────────────────────────────────────────────────

export function useStepsToday() {
  return useApi(() => stepsAPI.getToday())
}

export function useStepsWeek() {
  return useApi(() => stepsAPI.getWeek())
}

export function useStepsMonth() {
  return useApi(() => stepsAPI.getMonth())
}

export function useStepsStats(days = 30) {
  return useApi(() => stepsAPI.getStatistics(days), [days])
}

// ── Nutrition ─────────────────────────────────────────────

export function useNutritionToday() {
  return useApi(() => nutritionAPI.getToday())
}

export function useNutritionWeek() {
  return useApi(() => nutritionAPI.getWeek())
}

export function useMeals(date?: string) {
  return useApi(() => nutritionAPI.getMeals(date), [date])
}

export function useWaterToday() {
  return useApi(() => nutritionAPI.getWaterToday())
}

// ── Workouts ──────────────────────────────────────────────

export function useWorkoutSessions(days = 30) {
  return useApi(() => workoutAPI.getSessions(days), [days])
}

export function useWorkoutStats(days = 30) {
  return useApi(() => workoutAPI.getStats(days), [days])
}

export function useWorkoutPlans() {
  return useApi(() => workoutAPI.getPlans())
}

// ── Goals ─────────────────────────────────────────────────

export function useBMIHistory() {
  return useApi(() => goalsAPI.getBMIHistory())
}

export function useWeightProgress() {
  return useApi(() => goalsAPI.getWeightProgress())
}

export function useAchievements() {
  return useApi(() => goalsAPI.getAchievements())
}

// ── Analytics ─────────────────────────────────────────────

export function useWeeklyAnalytics() {
  return useApi(() => analyticsAPI.getWeekly())
}

export function useMonthlyAnalytics() {
  return useApi(() => analyticsAPI.getMonthly())
}

export function useFitnessScore() {
  return useApi(() => analyticsAPI.getFitnessScore())
}

export function useWeightHistory(days = 90) {
  return useApi(() => analyticsAPI.getWeightHistory(days), [days])
}

// ── Notifications ─────────────────────────────────────────

export function useNotifications(unreadOnly = false) {
  return useApi(() => notificationsAPI.getAll(unreadOnly), [unreadOnly])
}

// ── Devices ───────────────────────────────────────────────

export function useDevices() {
  return useApi(() => devicesAPI.getAll())
}
