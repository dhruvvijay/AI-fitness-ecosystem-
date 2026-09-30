import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { dashboardAPI } from "@/lib/api"

interface DashboardState {
  summary: {
    today_steps: number
    today_calories_consumed: number
    today_calories_burned: number
    remaining_calories: number
    workout_time_minutes: number
    heart_rate: number | null
    protein_g: number
    carbs_g: number
    fat_g: number
    fiber_g: number
    water_ml: number
    water_target_ml: number
    weight_kg: number | null
    bmi: number | null
    body_fat: number | null
    workout_streak: number
    daily_goal_progress: number
    weekly_goal_progress: number
    monthly_goal_progress: number
    achievements_count: number
    sleep_hours: number | null
    distance_km: number
    exercise_minutes: number
  } | null
  isLoading: boolean
  error: string | null
}

const initialState: DashboardState = {
  summary: null,
  isLoading: false,
  error: null,
}

export const fetchDashboardSummary = createAsyncThunk(
  "dashboard/fetchSummary",
  async (_unused: string | undefined, { rejectWithValue }) => {
    try {
      const { data } = await dashboardAPI.getDashboard()
      return data.data || data
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || "Failed to load dashboard")
    }
  }
)

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboardSummary.pending, (state) => {
        state.isLoading = true
      })
      .addCase(fetchDashboardSummary.fulfilled, (state, action) => {
        state.isLoading = false
        state.summary = action.payload
      })
      .addCase(fetchDashboardSummary.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
  },
})

export default dashboardSlice.reducer
