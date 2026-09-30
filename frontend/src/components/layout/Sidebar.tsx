"use client"

import React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { motion, AnimatePresence } from "framer-motion"
import {
  LayoutDashboard, Footprints, Flame, Calculator, ScanLine,
  UtensilsCrossed, Dumbbell, Library, Target, TrendingUp,
  BarChart3, Bluetooth, Music, Bot, Settings, Shield,
  ChevronLeft, ChevronRight, Sparkles, Heart,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { useAppDispatch, useAppSelector } from "@/store"
import { toggleSidebar } from "@/store/slices/uiSlice"

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard, color: "from-blue-500 to-cyan-400" },
  { label: "Steps", href: "/dashboard/steps", icon: Footprints, color: "from-green-500 to-emerald-400" },
  { label: "Calories", href: "/dashboard/calories", icon: Flame, color: "from-orange-500 to-amber-400" },
  { label: "BMI Calculator", href: "/dashboard/bmi", icon: Calculator, color: "from-purple-500 to-violet-400" },
  { label: "Food Scanner", href: "/dashboard/scanner", icon: ScanLine, color: "from-rose-500 to-pink-400" },
  { label: "Meals", href: "/dashboard/meals", icon: UtensilsCrossed, color: "from-teal-500 to-cyan-400" },
  { label: "Workouts", href: "/dashboard/workouts", icon: Dumbbell, color: "from-indigo-500 to-blue-400" },
  { label: "Exercises", href: "/dashboard/exercises", icon: Library, color: "from-fuchsia-500 to-purple-400" },
  { label: "Goals", href: "/dashboard/goals", icon: Target, color: "from-yellow-500 to-orange-400" },
  { label: "Progress", href: "/dashboard/progress", icon: TrendingUp, color: "from-sky-500 to-blue-400" },
  { label: "Analytics", href: "/dashboard/analytics", icon: BarChart3, color: "from-emerald-500 to-teal-400" },
  { label: "Bluetooth", href: "/dashboard/bluetooth", icon: Bluetooth, color: "from-blue-600 to-indigo-500" },
  { label: "Music", href: "/dashboard/music", icon: Music, color: "from-green-600 to-emerald-500" },
  { label: "AI Coach", href: "/dashboard/coach", icon: Bot, color: "from-violet-500 to-purple-400" },
]

const bottomItems = [
  { label: "Settings", href: "/dashboard/settings", icon: Settings },
  { label: "Admin", href: "/admin", icon: Shield },
]

export function Sidebar() {
  const pathname = usePathname()
  const dispatch = useAppDispatch()
  const { sidebarOpen } = useAppSelector((s) => s.ui)

  return (
    <motion.aside
      initial={false}
      animate={{ width: sidebarOpen ? 260 : 72 }}
      transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
      className={cn(
        "fixed left-0 top-0 z-40 flex h-screen flex-col",
        "border-r border-white/[0.06] bg-[hsl(var(--sidebar))]",
        "overflow-hidden"
      )}
    >
      {/* Logo */}
      <div className="flex h-16 items-center gap-3 px-4 border-b border-white/[0.06]">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl gradient-brand">
          <Heart className="h-5 w-5 text-white" />
        </div>
        <AnimatePresence>
          {sidebarOpen && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              className="flex flex-col"
            >
              <span className="text-sm font-bold tracking-tight">AI Fitness</span>
              <span className="text-[10px] text-muted-foreground">Ecosystem</span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto scrollbar-thin py-3 px-2 space-y-0.5">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium",
                "transition-all duration-200",
                isActive
                  ? "text-white"
                  : "text-muted-foreground hover:text-foreground hover:bg-white/[0.04]"
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="sidebar-active"
                  className={cn("absolute inset-0 rounded-xl bg-gradient-to-r opacity-15", item.color)}
                  transition={{ type: "spring", stiffness: 350, damping: 30 }}
                />
              )}
              {isActive && (
                <motion.div
                  layoutId="sidebar-indicator"
                  className="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-[3px] rounded-r-full bg-gradient-to-b from-blue-400 to-purple-500"
                  transition={{ type: "spring", stiffness: 350, damping: 30 }}
                />
              )}
              <div className={cn(
                "relative z-10 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg",
                "transition-all duration-200",
                isActive
                  ? `bg-gradient-to-br ${item.color} text-white shadow-lg`
                  : "text-muted-foreground group-hover:text-foreground"
              )}>
                <item.icon className="h-[18px] w-[18px]" />
              </div>
              <AnimatePresence>
                {sidebarOpen && (
                  <motion.span
                    initial={{ opacity: 0, x: -8 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -8 }}
                    className="relative z-10 truncate"
                  >
                    {item.label}
                  </motion.span>
                )}
              </AnimatePresence>
            </Link>
          )
        })}
      </nav>

      {/* Bottom Actions */}
      <div className="border-t border-white/[0.06] p-2 space-y-0.5">
        {bottomItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium",
              "text-muted-foreground hover:text-foreground hover:bg-white/[0.04]",
              "transition-all duration-200"
            )}
          >
            <div className="flex h-8 w-8 shrink-0 items-center justify-center">
              <item.icon className="h-[18px] w-[18px]" />
            </div>
            <AnimatePresence>
              {sidebarOpen && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="truncate"
                >
                  {item.label}
                </motion.span>
              )}
            </AnimatePresence>
          </Link>
        ))}

        {/* Collapse Toggle */}
        <button
          onClick={() => dispatch(toggleSidebar())}
          className={cn(
            "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm",
            "text-muted-foreground hover:text-foreground hover:bg-white/[0.04]",
            "transition-all duration-200"
          )}
        >
          <div className="flex h-8 w-8 shrink-0 items-center justify-center">
            {sidebarOpen ? (
              <ChevronLeft className="h-[18px] w-[18px]" />
            ) : (
              <ChevronRight className="h-[18px] w-[18px]" />
            )}
          </div>
          <AnimatePresence>
            {sidebarOpen && (
              <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                Collapse
              </motion.span>
            )}
          </AnimatePresence>
        </button>
      </div>
    </motion.aside>
  )
}
