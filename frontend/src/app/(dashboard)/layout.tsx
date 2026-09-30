"use client"

import React, { useEffect } from "react"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { Sidebar } from "@/components/layout/Sidebar"
import { Header } from "@/components/layout/Header"
import { useAppDispatch, useAppSelector } from "@/store"
import { fetchCurrentUser } from "@/store/slices/authSlice"
import { cn } from "@/lib/utils"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const dispatch = useAppDispatch()
  const { isAuthenticated, isLoading } = useAppSelector((s) => s.auth)
  const { sidebarOpen } = useAppSelector((s) => s.ui)

  useEffect(() => {
    const token = localStorage.getItem("access_token")
    if (token) {
      dispatch(fetchCurrentUser())
    } else {
      router.push("/login")
    }
  }, [dispatch, router])

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[hsl(var(--background))]">
        <div className="flex flex-col items-center gap-4">
          <div className="relative h-12 w-12">
            <div className="absolute inset-0 rounded-full border-2 border-blue-500/20" />
            <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-blue-500 animate-spin" />
          </div>
          <p className="text-sm text-muted-foreground animate-pulse">Loading your fitness data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen overflow-hidden bg-[hsl(var(--background))]">
      <Sidebar />
      <motion.main
        initial={false}
        animate={{ marginLeft: sidebarOpen ? 260 : 72 }}
        transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
        className="flex-1 flex flex-col overflow-hidden"
      >
        <Header />
        <div className="flex-1 overflow-y-auto scrollbar-thin p-4 md:p-6">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            {children}
          </motion.div>
        </div>
      </motion.main>
    </div>
  )
}
