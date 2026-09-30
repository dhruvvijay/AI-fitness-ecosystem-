"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import {
  Shield, Users, Activity, Server, Database, TrendingUp,
  AlertTriangle, CheckCircle2, Clock, Zap, Eye, Ban,
} from "lucide-react"
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell,
} from "recharts"
import { cn } from "@/lib/utils"

const signupTrend = [
  { day: "Mon", users: 24 }, { day: "Tue", users: 31 }, { day: "Wed", users: 28 },
  { day: "Thu", users: 42 }, { day: "Fri", users: 35 }, { day: "Sat", users: 52 },
  { day: "Sun", users: 46 },
]

const apiUsage = [
  { hour: "00", requests: 120 }, { hour: "04", requests: 45 }, { hour: "08", requests: 890 },
  { hour: "12", requests: 1240 }, { hour: "16", requests: 980 }, { hour: "20", requests: 650 },
]

const planDistribution = [
  { name: "Free", value: 32000, color: "#6b7280" },
  { name: "Pro", value: 12000, color: "#3b82f6" },
  { name: "Enterprise", value: 6000, color: "#a855f7" },
]

const recentUsers = [
  { name: "Sarah Johnson", email: "sarah@email.com", plan: "Pro", joined: "2 hours ago", status: "active" },
  { name: "Mike Chen", email: "mike@email.com", plan: "Free", joined: "5 hours ago", status: "active" },
  { name: "Emily Davis", email: "emily@email.com", plan: "Enterprise", joined: "1 day ago", status: "active" },
  { name: "John Smith", email: "john@email.com", plan: "Pro", joined: "2 days ago", status: "suspended" },
  { name: "Lisa Wang", email: "lisa@email.com", plan: "Free", joined: "3 days ago", status: "active" },
]

const systemHealth = [
  { name: "API Server", status: "healthy", uptime: "99.98%", latency: "42ms" },
  { name: "MySQL Database", status: "healthy", uptime: "99.99%", latency: "8ms" },
  { name: "Redis Cache", status: "healthy", uptime: "99.99%", latency: "1ms" },
  { name: "AI Vision Service", status: "degraded", uptime: "98.5%", latency: "1.2s" },
  { name: "Nginx Proxy", status: "healthy", uptime: "100%", latency: "2ms" },
]

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } }
const item = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0 } }

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState<"overview" | "users" | "system">("overview")

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="max-w-7xl mx-auto space-y-6 pb-8 p-4 md:p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-red-500 to-rose-500 shadow-lg shadow-red-500/25">
            <Shield className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Admin Dashboard</h1>
            <p className="text-sm text-muted-foreground">System management & analytics overview</p>
          </div>
        </div>
        <div className="flex gap-1 p-1 rounded-xl bg-white/[0.03] border border-white/[0.06]">
          {(["overview", "users", "system"] as const).map((tab) => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={cn("px-4 py-2 rounded-lg text-sm font-medium transition-all",
                activeTab === tab ? "bg-white/[0.08] text-foreground" : "text-muted-foreground hover:text-foreground")}>
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <motion.div variants={item} className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Total Users</p><p className="text-xl font-bold">50,247</p><p className="text-[10px] text-emerald-400">↑ 12% this week</p></div>
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Active Today</p><p className="text-xl font-bold text-emerald-400">8,432</p><p className="text-[10px] text-muted-foreground">16.8% DAU</p></div>
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">API Requests</p><p className="text-xl font-bold text-blue-400">1.2M</p><p className="text-[10px] text-muted-foreground">today</p></div>
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Meals Scanned</p><p className="text-xl font-bold text-orange-400">24,680</p><p className="text-[10px] text-emerald-400">↑ 8% this week</p></div>
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Revenue</p><p className="text-xl font-bold text-purple-400">$48.2K</p><p className="text-[10px] text-emerald-400">↑ 15% MoM</p></div>
        <div className="glass-card p-4"><p className="text-xs text-muted-foreground">Churn Rate</p><p className="text-xl font-bold text-amber-400">2.1%</p><p className="text-[10px] text-emerald-400">↓ 0.3%</p></div>
      </motion.div>

      {activeTab === "overview" && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Signup Trend */}
            <motion.div variants={item} className="glass-card p-5">
              <h3 className="text-sm font-semibold mb-4">New Signups This Week</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={signupTrend}>
                    <defs><linearGradient id="signupGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} /><stop offset="95%" stopColor="#3b82f6" stopOpacity={0} /></linearGradient></defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                    <XAxis dataKey="day" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                    <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} />
                    <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
                    <Area type="monotone" dataKey="users" stroke="#3b82f6" strokeWidth={2} fill="url(#signupGrad)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            {/* API Usage */}
            <motion.div variants={item} className="glass-card p-5">
              <h3 className="text-sm font-semibold mb-4">API Requests (Today)</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={apiUsage}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                    <XAxis dataKey="hour" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                    <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} />
                    <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
                    <Bar dataKey="requests" fill="#a855f7" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </motion.div>
          </div>

          {/* Plan Distribution */}
          <motion.div variants={item} className="glass-card p-5">
            <h3 className="text-sm font-semibold mb-4">Subscription Distribution</h3>
            <div className="flex items-center gap-8">
              <div className="h-48 w-48">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={planDistribution} cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={3} dataKey="value">
                      {planDistribution.map((entry, i) => (<Cell key={i} fill={entry.color} />))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: "rgba(15,15,35,0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "12px", fontSize: "12px" }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="space-y-3">
                {planDistribution.map((p) => (
                  <div key={p.name} className="flex items-center gap-3">
                    <div className="h-3 w-3 rounded-full" style={{ background: p.color }} />
                    <span className="text-sm font-medium w-24">{p.name}</span>
                    <span className="text-sm text-muted-foreground">{p.value.toLocaleString()} users</span>
                    <span className="text-xs text-muted-foreground">({((p.value / 50000) * 100).toFixed(0)}%)</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </>
      )}

      {activeTab === "users" && (
        <motion.div variants={item} className="glass-card p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold">Recent Users</h3>
            <button className="text-xs text-blue-400 hover:text-blue-300 font-medium">View All →</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/[0.06]">
                  <th className="text-left py-3 px-4 text-xs font-medium text-muted-foreground">User</th>
                  <th className="text-left py-3 px-4 text-xs font-medium text-muted-foreground">Plan</th>
                  <th className="text-left py-3 px-4 text-xs font-medium text-muted-foreground">Joined</th>
                  <th className="text-left py-3 px-4 text-xs font-medium text-muted-foreground">Status</th>
                  <th className="text-right py-3 px-4 text-xs font-medium text-muted-foreground">Actions</th>
                </tr>
              </thead>
              <tbody>
                {recentUsers.map((u, i) => (
                  <tr key={i} className="border-b border-white/[0.03] hover:bg-white/[0.02]">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-8 w-8 items-center justify-center rounded-lg gradient-brand text-white text-xs font-bold">{u.name.split(" ").map(n => n[0]).join("")}</div>
                        <div><p className="font-medium">{u.name}</p><p className="text-xs text-muted-foreground">{u.email}</p></div>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className={cn("text-xs px-2 py-0.5 rounded-full font-medium",
                        u.plan === "Pro" ? "bg-blue-500/10 text-blue-400" : u.plan === "Enterprise" ? "bg-purple-500/10 text-purple-400" : "bg-white/[0.06] text-muted-foreground")}>{u.plan}</span>
                    </td>
                    <td className="py-3 px-4 text-muted-foreground">{u.joined}</td>
                    <td className="py-3 px-4">
                      <span className={cn("flex items-center gap-1 text-xs font-medium",
                        u.status === "active" ? "text-emerald-400" : "text-rose-400")}>
                        <div className={cn("h-1.5 w-1.5 rounded-full", u.status === "active" ? "bg-emerald-400" : "bg-rose-400")} />
                        {u.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end gap-1">
                        <button className="p-1.5 rounded-lg hover:bg-white/[0.06]"><Eye className="h-3.5 w-3.5 text-muted-foreground" /></button>
                        <button className="p-1.5 rounded-lg hover:bg-rose-500/10"><Ban className="h-3.5 w-3.5 text-muted-foreground hover:text-rose-400" /></button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}

      {activeTab === "system" && (
        <motion.div variants={item} className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4 flex items-center gap-2"><Server className="h-4 w-4 text-emerald-400" /> System Health</h3>
          <div className="space-y-3">
            {systemHealth.map((s, i) => (
              <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/[0.02] border border-white/[0.04]">
                <div className="flex items-center gap-3">
                  <div className={cn("flex h-3 w-3 rounded-full",
                    s.status === "healthy" ? "bg-emerald-400" : s.status === "degraded" ? "bg-amber-400 animate-pulse" : "bg-rose-400 animate-pulse")} />
                  <div><p className="text-sm font-medium">{s.name}</p><p className="text-xs text-muted-foreground capitalize">{s.status}</p></div>
                </div>
                <div className="flex items-center gap-6 text-xs text-muted-foreground">
                  <span>Uptime: <span className="text-foreground font-medium">{s.uptime}</span></span>
                  <span>Latency: <span className="text-foreground font-medium">{s.latency}</span></span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}
