import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit"
import { authAPI } from "@/lib/api"

interface UserProfile {
  id: number
  email: string
  full_name: string
  role: string
  avatar_url: string | null
  height_cm: number | null
  weight_kg: number | null
  target_weight_kg: number | null
  activity_level: string | null
  fitness_goal: string | null
  diet_preference: string | null
  daily_calorie_target: number | null
  daily_protein_target: number | null
  daily_water_target_ml: number | null
  daily_step_target: number | null
}

interface AuthState {
  user: UserProfile | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
}

export const loginUser = createAsyncThunk(
  "auth/login",
  async (credentials: { email: string; password: string }, { rejectWithValue }) => {
    // Demo mode: bypass backend for demo credentials
    if (credentials.email === "demo@aifitness.com" && credentials.password === "Demo@1234") {
      const demoUser: UserProfile = {
        id: 1,
        email: "demo@aifitness.com",
        full_name: "John Doe",
        role: "user",
        avatar_url: null,
        height_cm: 175,
        weight_kg: 75.2,
        target_weight_kg: 72.0,
        activity_level: "moderate",
        fitness_goal: "lose_weight",
        diet_preference: "balanced",
        daily_calorie_target: 2200,
        daily_protein_target: 150,
        daily_water_target_ml: 3000,
        daily_step_target: 10000,
      }
      localStorage.setItem("access_token", "demo_token_aifitness_2026")
      localStorage.setItem("refresh_token", "demo_refresh_token")
      localStorage.setItem("demo_user", JSON.stringify(demoUser))
      return demoUser
    }

    try {
      const { data } = await authAPI.login(credentials)
      const result = data.data || data
      localStorage.setItem("access_token", result.tokens.access_token)
      localStorage.setItem("refresh_token", result.tokens.refresh_token)
      return result.user
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || error.response?.data?.detail || "Login failed. Use demo credentials: demo@aifitness.com / Demo@1234")
    }
  }
)

export const signupUser = createAsyncThunk(
  "auth/signup",
  async (userData: { email: string; password: string; full_name: string }, { rejectWithValue }) => {
    try {
      const { data } = await authAPI.register(userData)
      const result = data.data || data
      localStorage.setItem("access_token", result.tokens.access_token)
      localStorage.setItem("refresh_token", result.tokens.refresh_token)
      return result.user
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || error.response?.data?.detail || "Signup failed")
    }
  }
)

export const fetchCurrentUser = createAsyncThunk(
  "auth/fetchUser",
  async (_, { rejectWithValue }) => {
    // Demo mode: return stored demo user
    const token = localStorage.getItem("access_token")
    if (token === "demo_token_aifitness_2026") {
      const stored = localStorage.getItem("demo_user")
      if (stored) return JSON.parse(stored) as UserProfile
    }

    try {
      const { data } = await authAPI.getMe()
      return data
    } catch (error: any) {
      return rejectWithValue("Session expired")
    }
  }
)

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null
      state.isAuthenticated = false
      state.error = null
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
    },
    clearError: (state) => {
      state.error = null
    },
    setUser: (state, action: PayloadAction<UserProfile>) => {
      state.user = action.payload
      state.isAuthenticated = true
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false
        state.user = action.payload
        state.isAuthenticated = true
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(signupUser.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(signupUser.fulfilled, (state, action) => {
        state.isLoading = false
        state.user = action.payload
        state.isAuthenticated = true
      })
      .addCase(signupUser.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(fetchCurrentUser.pending, (state) => {
        state.isLoading = true
      })
      .addCase(fetchCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false
        state.user = action.payload
        state.isAuthenticated = true
      })
      .addCase(fetchCurrentUser.rejected, (state) => {
        state.isLoading = false
        state.isAuthenticated = false
        state.user = null
      })
  },
})

export const { logout, clearError, setUser } = authSlice.actions
export default authSlice.reducer
