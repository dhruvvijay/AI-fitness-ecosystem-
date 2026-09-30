"use client"

import React from "react"
import { useTheme } from "next-themes"
import { motion } from "framer-motion"
import {
  Bell, Search, Sun, Moon, Menu, User, LogOut, Settings, ChevronDown,
} from "lucide-react"
import { cn, getGreeting, getInitials } from "@/lib/utils"
import { useAppDispatch, useAppSelector } from "@/store"
import { logout } from "@/store/slices/authSlice"
import { toggleMobileMenu } from "@/store/slices/uiSlice"

export function Header() {
  const { theme, setTheme } = useTheme()
  const dispatch = useAppDispatch()
  const { user } = useAppSelector((s) => s.auth)
  const { sidebarOpen } = useAppSelector((s) => s.ui)
  const [showProfileMenu, setShowProfileMenu] = React.useState(false)
  const [showSearch, setShowSearch] = React.useState(false)

  const greeting = getGreeting()

  return (
    <header
      className={cn(
        "sticky top-0 z-30 flex h-16 items-center justify-between gap-4",
        "border-b border-white/[0.06] bg-[hsl(var(--background))]/80 backdrop-blur-xl",
        "px-4 md:px-6 transition-all duration-300",
      )}
      style={{ marginLeft: 0 }}
    >
      {/* Left: Mobile menu + Greeting */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => dispatch(toggleMobileMenu())}
          className="flex h-9 w-9 items-center justify-center rounded-lg hover:bg-white/[0.06] md:hidden"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="hidden md:block">
          <p className="text-sm text-muted-foreground">{greeting}</p>
          <h2 className="text-lg font-semibold tracking-tight">
            {user?.full_name?.split(" ")[0] || "User"} 👋
          </h2>
        </div>
      </div>

      {/* Center: Search */}
      <div className="flex-1 max-w-md mx-4 hidden md:block">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search foods, exercises, workouts..."
            className={cn(
              "w-full h-10 rounded-xl pl-10 pr-4 text-sm",
              "bg-white/[0.04] border border-white/[0.08]",
              "placeholder:text-muted-foreground/60",
              "focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500/40",
              "transition-all duration-200"
            )}
          />
          <kbd className="absolute right-3 top-1/2 -translate-y-1/2 hidden sm:inline-flex h-5 items-center gap-0.5 rounded border border-white/[0.1] bg-white/[0.04] px-1.5 text-[10px] text-muted-foreground">
            ⌘K
          </kbd>
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        {/* Theme Toggle */}
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className={cn(
            "flex h-9 w-9 items-center justify-center rounded-lg",
            "hover:bg-white/[0.06] transition-colors duration-200"
          )}
        >
          {theme === "dark" ? (
            <Sun className="h-[18px] w-[18px] text-amber-400" />
          ) : (
            <Moon className="h-[18px] w-[18px]" />
          )}
        </button>

        {/* Notifications */}
        <button className={cn(
          "relative flex h-9 w-9 items-center justify-center rounded-lg",
          "hover:bg-white/[0.06] transition-colors duration-200"
        )}>
          <Bell className="h-[18px] w-[18px]" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-rose-500 ring-2 ring-[hsl(var(--background))]" />
        </button>

        {/* Profile */}
        <div className="relative">
          <button
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            className={cn(
              "flex items-center gap-2 rounded-xl px-2 py-1.5",
              "hover:bg-white/[0.06] transition-all duration-200"
            )}
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-lg gradient-brand text-white text-xs font-bold">
              {user ? getInitials(user.full_name) : "U"}
            </div>
            <span className="hidden md:block text-sm font-medium max-w-[100px] truncate">
              {user?.full_name || "User"}
            </span>
            <ChevronDown className="hidden md:block h-3.5 w-3.5 text-muted-foreground" />
          </button>

          {/* Profile Dropdown */}
          {showProfileMenu && (
            <>
              <div className="fixed inset-0 z-40" onClick={() => setShowProfileMenu(false)} />
              <motion.div
                initial={{ opacity: 0, y: 8, scale: 0.96 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 8, scale: 0.96 }}
                className={cn(
                  "absolute right-0 top-full mt-2 z-50 w-56 rounded-xl p-1.5",
                  "bg-[hsl(var(--card))] border border-white/[0.08] shadow-xl shadow-black/20"
                )}
              >
                <div className="px-3 py-2 border-b border-white/[0.06] mb-1">
                  <p className="text-sm font-medium">{user?.full_name}</p>
                  <p className="text-xs text-muted-foreground">{user?.email}</p>
                </div>
                <a
                  href="/dashboard/settings"
                  className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm hover:bg-white/[0.06] transition-colors"
                >
                  <Settings className="h-4 w-4" /> Settings
                </a>
                <a
                  href="/dashboard/settings"
                  className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm hover:bg-white/[0.06] transition-colors"
                >
                  <User className="h-4 w-4" /> Profile
                </a>
                <button
                  onClick={() => {
                    dispatch(logout())
                    window.location.href = "/login"
                  }}
                  className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm text-rose-400 hover:bg-rose-500/10 transition-colors"
                >
                  <LogOut className="h-4 w-4" /> Sign Out
                </button>
              </motion.div>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
