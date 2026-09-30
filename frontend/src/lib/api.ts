import axios from "axios"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
})

// Request interceptor — attach JWT token
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  }
  return config
})

// Response interceptor — handle 401 and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem("refresh_token")
        if (refreshToken) {
          const { data } = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })
          const tokens = data.data?.tokens || data.tokens || data
          localStorage.setItem("access_token", tokens.access_token)
          localStorage.setItem("refresh_token", tokens.refresh_token)
          originalRequest.headers.Authorization = `Bearer ${tokens.access_token}`
          return api(originalRequest)
        }
      } catch {
        localStorage.removeItem("access_token")
        localStorage.removeItem("refresh_token")
        if (typeof window !== "undefined") {
          window.location.href = "/login"
        }
      }
    }

    return Promise.reject(error)
  }
)

export default api

// ── Auth API ────────────────────────────────────────────────────

export const authAPI = {
  register: (data: { email: string; password: string; full_name: string }) =>
    api.post("/auth/register", data),
  login: (data: { email: string; password: string }) =>
    api.post("/auth/login", data),
  refresh: (refreshToken: string) =>
    api.post("/auth/refresh", { refresh_token: refreshToken }),
  getMe: () => api.get("/auth/me"),
  updateProfile: (data: Record<string, unknown>) =>
    api.put("/auth/me/profile", data),
  logout: () => api.post("/auth/logout"),
}

// ── Dashboard API ───────────────────────────────────────────────

export const dashboardAPI = {
  getDashboard: () => api.get("/dashboard"),
}

// ── Steps API ───────────────────────────────────────────────────

export const stepsAPI = {
  logSteps: (data: { steps: number; date?: string; source?: string }) =>
    api.post("/steps", data),
  getToday: () => api.get("/steps/today"),
  getWeek: () => api.get("/steps/week"),
  getMonth: () => api.get("/steps/month"),
  getStatistics: (days?: number) =>
    api.get("/steps/statistics", { params: { days } }),
}

// ── Nutrition API ───────────────────────────────────────────────

export const nutritionAPI = {
  getToday: () => api.get("/nutrition/today"),
  getWeek: () => api.get("/nutrition/week"),
  getMeals: (date?: string) =>
    api.get("/nutrition/meals", { params: { date } }),
  createMeal: (data: {
    meal_type: string
    name?: string
    date?: string
    items: { food_id: number; servings: number; custom_weight_g?: number }[]
  }) => api.post("/nutrition/meals", data),
  deleteMeal: (mealId: number) => api.delete(`/nutrition/meals/${mealId}`),
  searchFoods: (q: string, category?: string, page?: number, limit?: number) =>
    api.get("/nutrition/foods/search", { params: { q, category, page, limit } }),
  logWater: (amount_ml: number) => api.post("/nutrition/water", { amount_ml }),
  getWaterToday: () => api.get("/nutrition/water/today"),
  scanFood: (file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    return api.post("/ai/food-scanner/analyze", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },
}

// ── Workout API ─────────────────────────────────────────────────

export const workoutAPI = {
  getSessions: (days?: number) =>
    api.get("/workouts/sessions", { params: { days } }),
  startWorkout: (data: { name?: string; workout_type?: string; plan_id?: number }) =>
    api.post("/workouts/sessions", data),
  logExercise: (sessionId: number, data: { exercise_id: number; sets_data: Record<string, unknown>[] }) =>
    api.post(`/workouts/sessions/${sessionId}/exercises`, data),
  completeWorkout: (sessionId: number, data?: Record<string, unknown>) =>
    api.put(`/workouts/sessions/${sessionId}/complete`, data || {}),
  getStats: (days?: number) =>
    api.get("/workouts/stats", { params: { days } }),
  getPlans: () => api.get("/workouts/plans"),
  searchExercises: (params: Record<string, unknown>) =>
    api.get("/workouts/exercises", { params }),
  getExercise: (id: number) =>
    api.get(`/workouts/exercises/${id}`),
}

// ── Goals & BMI API ─────────────────────────────────────────────

export const goalsAPI = {
  calculateBMI: (data: {
    weight_kg: number
    height_cm: number
    age?: number
    gender?: string
    activity_level?: string
    body_fat_percentage?: number | null
  }) =>
    api.post("/goals/bmi", data),
  getBMIHistory: () => api.get("/goals/bmi/history"),
  getWeightProgress: () => api.get("/goals/weight-progress"),
  getAchievements: () => api.get("/goals/achievements"),
}

// ── Analytics API ───────────────────────────────────────────────

export const analyticsAPI = {
  getDaily: (date?: string) =>
    api.get("/analytics/daily", { params: { date } }),
  getWeekly: () => api.get("/analytics/weekly"),
  getMonthly: () => api.get("/analytics/monthly"),
  getWeightHistory: (days?: number) =>
    api.get("/analytics/weight", { params: { days } }),
  getFitnessScore: () => api.get("/analytics/fitness-score"),
}

// ── Notifications API ───────────────────────────────────────────

export const notificationsAPI = {
  getAll: (unreadOnly?: boolean) =>
    api.get("/notifications", { params: { unread_only: unreadOnly } }),
  markRead: (id: number) => api.put(`/notifications/${id}/read`),
  markAllRead: () => api.put("/notifications/read-all"),
}

// ── Devices API ─────────────────────────────────────────────────

export const devicesAPI = {
  getAll: () => api.get("/devices"),
  register: (data: { device_name: string; device_type: string; bluetooth_id?: string }) =>
    api.post("/devices", data),
  sync: (deviceId: number, data: { sync_type: string; value: number; unit?: string }) =>
    api.post(`/devices/${deviceId}/sync`, data),
  remove: (deviceId: number) => api.delete(`/devices/${deviceId}`),
}

// ── AI API ──────────────────────────────────────────────────────

export const aiAPI = {
  chat: (data: { message: string; session_id?: string }) =>
    api.post("/ai/coach/chat", data),
}
