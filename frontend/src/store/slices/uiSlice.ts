import { createSlice, PayloadAction } from "@reduxjs/toolkit"

interface UIState {
  sidebarOpen: boolean
  mobileMenuOpen: boolean
  theme: "dark" | "light" | "system"
}

const initialState: UIState = {
  sidebarOpen: true,
  mobileMenuOpen: false,
  theme: "dark",
}

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload
    },
    toggleMobileMenu: (state) => {
      state.mobileMenuOpen = !state.mobileMenuOpen
    },
    setTheme: (state, action: PayloadAction<"dark" | "light" | "system">) => {
      state.theme = action.payload
    },
  },
})

export const { toggleSidebar, setSidebarOpen, toggleMobileMenu, setTheme } = uiSlice.actions
export default uiSlice.reducer
