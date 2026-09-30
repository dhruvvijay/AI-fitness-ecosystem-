"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import { Settings, User, Bell, Shield, Palette, Globe, Activity, Save, Trash2 } from "lucide-react"
import { cn } from "@/lib/utils"

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("profile")

  const sections = [
    { id: "profile", label: "Profile", icon: User },
    { id: "notifications", label: "Notifications", icon: Bell },
    { id: "appearance", label: "Appearance", icon: Palette },
    { id: "privacy", label: "Privacy", icon: Shield },
    { id: "units", label: "Units & Language", icon: Globe },
    { id: "fitness", label: "Fitness Settings", icon: Activity },
  ]

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-8">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-gray-500 to-zinc-400 shadow-lg">
          <Settings className="h-6 w-6 text-white" />
        </div>
        <div><h1 className="text-2xl font-bold tracking-tight">Settings</h1><p className="text-sm text-muted-foreground">Manage your account and preferences</p></div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Nav */}
        <div className="space-y-1">
          {sections.map((s) => (
            <button key={s.id} onClick={() => setActiveSection(s.id)}
              className={cn("flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
                activeSection === s.id ? "bg-white/[0.08] text-foreground" : "text-muted-foreground hover:text-foreground hover:bg-white/[0.04]")}>
              <s.icon className="h-4 w-4" /> {s.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="md:col-span-3 glass-card p-6">
          {activeSection === "profile" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-5">
              <h3 className="text-lg font-semibold">Profile Settings</h3>
              <div className="flex items-center gap-4">
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl gradient-brand text-white text-xl font-bold">JD</div>
                <div><button className="text-xs text-blue-400 hover:text-blue-300 font-medium">Change Avatar</button><p className="text-xs text-muted-foreground mt-0.5">Max 2MB, JPEG or PNG</p></div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5"><label className="text-xs font-medium text-muted-foreground">Full Name</label>
                  <input type="text" defaultValue="John Doe" className="w-full h-11 rounded-xl px-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-blue-500/30 transition-all" /></div>
                <div className="space-y-1.5"><label className="text-xs font-medium text-muted-foreground">Email</label>
                  <input type="email" defaultValue="john@example.com" className="w-full h-11 rounded-xl px-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-blue-500/30 transition-all" /></div>
                <div className="space-y-1.5"><label className="text-xs font-medium text-muted-foreground">Date of Birth</label>
                  <input type="date" defaultValue="1998-05-15" className="w-full h-11 rounded-xl px-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-blue-500/30 transition-all" /></div>
                <div className="space-y-1.5"><label className="text-xs font-medium text-muted-foreground">Gender</label>
                  <select defaultValue="male" className="w-full h-11 rounded-xl px-4 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-blue-500/30 transition-all">
                    <option value="male">Male</option><option value="female">Female</option><option value="other">Other</option></select></div>
              </div>
              <div className="space-y-1.5"><label className="text-xs font-medium text-muted-foreground">Bio</label>
                <textarea rows={3} defaultValue="Fitness enthusiast on a journey to better health 💪" className="w-full rounded-xl px-4 py-3 text-sm bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:ring-2 focus:ring-blue-500/30 transition-all resize-none" /></div>
              <button className="flex h-10 items-center gap-2 rounded-xl px-6 text-sm font-semibold gradient-brand text-white shadow-lg shadow-blue-500/25"><Save className="h-4 w-4" /> Save Changes</button>
            </motion.div>
          )}

          {activeSection === "notifications" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-5">
              <h3 className="text-lg font-semibold">Notification Preferences</h3>
              {[
                { label: "Workout Reminders", desc: "Get reminded to workout at your scheduled time", checked: true },
                { label: "Meal Reminders", desc: "Never miss a meal — breakfast, lunch, dinner alerts", checked: true },
                { label: "Water Reminders", desc: "Hourly reminders to stay hydrated", checked: false },
                { label: "Progress Updates", desc: "Weekly progress summary and insights", checked: true },
                { label: "Achievement Alerts", desc: "Get notified when you unlock achievements", checked: true },
                { label: "AI Coach Tips", desc: "Daily tips from your AI fitness coach", checked: false },
              ].map((n, i) => (
                <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/[0.02] border border-white/[0.04]">
                  <div><p className="text-sm font-medium">{n.label}</p><p className="text-xs text-muted-foreground">{n.desc}</p></div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked={n.checked} className="sr-only peer" />
                    <div className="w-11 h-6 rounded-full bg-white/[0.1] peer-checked:bg-blue-500 peer-focus:ring-2 peer-focus:ring-blue-500/30 transition-colors after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:after:translate-x-5" />
                  </label>
                </div>
              ))}
            </motion.div>
          )}

          {activeSection === "appearance" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-5">
              <h3 className="text-lg font-semibold">Appearance</h3>
              <div className="space-y-2">
                <label className="text-sm font-medium">Theme</label>
                <div className="grid grid-cols-3 gap-3">
                  {["Dark", "Light", "System"].map((t) => (
                    <button key={t} className={cn("rounded-xl p-4 text-center border transition-all",
                      t === "Dark" ? "bg-blue-500/10 border-blue-500/30 text-blue-400" : "bg-white/[0.02] border-white/[0.06] text-muted-foreground hover:bg-white/[0.04]")}>
                      <p className="text-sm font-medium">{t}</p>
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {activeSection === "privacy" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-5">
              <h3 className="text-lg font-semibold">Privacy & Security</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-4 rounded-xl bg-white/[0.02] border border-white/[0.04]">
                  <div><p className="text-sm font-medium">Public Profile</p><p className="text-xs text-muted-foreground">Allow others to view your profile</p></div>
                  <label className="relative inline-flex items-center cursor-pointer"><input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 rounded-full bg-white/[0.1] peer-checked:bg-blue-500 transition-colors after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:after:translate-x-5" /></label>
                </div>
                <div className="flex items-center justify-between p-4 rounded-xl bg-white/[0.02] border border-white/[0.04]">
                  <div><p className="text-sm font-medium">Show on Leaderboard</p><p className="text-xs text-muted-foreground">Appear in community rankings</p></div>
                  <label className="relative inline-flex items-center cursor-pointer"><input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 rounded-full bg-white/[0.1] peer-checked:bg-blue-500 transition-colors after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:after:translate-x-5" /></label>
                </div>
                <button className="flex items-center gap-2 text-sm text-rose-400 hover:text-rose-300 transition-colors mt-4"><Trash2 className="h-4 w-4" /> Delete Account</button>
              </div>
            </motion.div>
          )}

          {(activeSection === "units" || activeSection === "fitness") && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-5">
              <h3 className="text-lg font-semibold">{activeSection === "units" ? "Units & Language" : "Fitness Settings"}</h3>
              <p className="text-sm text-muted-foreground">Settings will be available after connecting to the backend.</p>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}
