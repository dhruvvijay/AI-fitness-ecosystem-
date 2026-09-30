"use client"

import React, { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Bluetooth, Wifi, WifiOff, Battery, RefreshCw, Heart, Footprints, Activity } from "lucide-react"
import { cn } from "@/lib/utils"

const devices = [
  { name: "Mi Band 8", type: "Fitness Band", connected: true, battery: 72, lastSync: "2 min ago", icon: "⌚", data: { steps: 8743, heartRate: 72, calories: 280 } },
  { name: "Wahoo TICKR", type: "Heart Rate Monitor", connected: false, battery: 95, lastSync: "1 hour ago", icon: "❤️", data: null },
  { name: "Garmin Scale S2", type: "Smart Scale", connected: false, battery: null, lastSync: "3 days ago", icon: "⚖️", data: null },
]

export default function BluetoothPage() {
  const [scanning, setScanning] = useState(false)
  const [showInfo, setShowInfo] = useState(false)

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-8">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-indigo-500 shadow-lg shadow-blue-600/25">
            <Bluetooth className="h-6 w-6 text-white" />
          </div>
          <div><h1 className="text-2xl font-bold tracking-tight">Bluetooth Devices</h1><p className="text-sm text-muted-foreground">Connect fitness trackers and smart devices</p></div>
        </div>
        <button onClick={() => { setScanning(true); setTimeout(() => setScanning(false), 3000) }}
          className={cn("flex h-10 items-center gap-2 rounded-xl px-4 text-sm font-medium bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 transition-colors")}>
          <RefreshCw className={cn("h-4 w-4", scanning && "animate-spin")} /> {scanning ? "Scanning..." : "Scan"}
        </button>
      </div>

      {/* Info Banner */}
      <div className="rounded-xl bg-blue-500/10 border border-blue-500/20 p-4 text-sm text-blue-300">
        <p className="font-semibold">📡 Web Bluetooth API</p>
        <p className="text-xs mt-1 text-blue-300/70">
          This feature uses the Web Bluetooth API. Supported in Chrome, Edge, and Opera on desktop/Android. 
          iOS Safari does not support Web Bluetooth. A native app wrapper can provide full Bluetooth access.
        </p>
      </div>

      {/* Paired Devices */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold">My Devices</h3>
        {devices.map((device, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
            className="glass-card p-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-blue-500/10 text-2xl">{device.icon}</div>
                <div>
                  <p className="text-sm font-semibold">{device.name}</p>
                  <p className="text-xs text-muted-foreground">{device.type}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <div className={cn("flex items-center gap-1 text-xs", device.connected ? "text-emerald-400" : "text-muted-foreground")}>
                      {device.connected ? <Wifi className="h-3 w-3" /> : <WifiOff className="h-3 w-3" />}
                      {device.connected ? "Connected" : "Disconnected"}
                    </div>
                    {device.battery && (
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Battery className="h-3 w-3" /> {device.battery}%
                      </div>
                    )}
                    <span className="text-xs text-muted-foreground">• Synced {device.lastSync}</span>
                  </div>
                </div>
              </div>
              <button className={cn("rounded-xl px-4 py-2 text-xs font-medium transition-colors",
                device.connected ? "bg-rose-500/10 text-rose-400 hover:bg-rose-500/20" : "bg-blue-500/10 text-blue-400 hover:bg-blue-500/20")}>
                {device.connected ? "Disconnect" : "Connect"}
              </button>
            </div>

            {/* Live Data */}
            {device.connected && device.data && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 pt-4 border-t border-white/[0.06] grid grid-cols-3 gap-3">
                <div className="flex items-center gap-2 p-2 rounded-lg bg-green-500/10">
                  <Footprints className="h-4 w-4 text-green-400" />
                  <div><p className="text-sm font-bold text-green-400">{device.data.steps.toLocaleString()}</p><p className="text-[10px] text-muted-foreground">Steps</p></div>
                </div>
                <div className="flex items-center gap-2 p-2 rounded-lg bg-red-500/10">
                  <Heart className="h-4 w-4 text-red-400" />
                  <div><p className="text-sm font-bold text-red-400">{device.data.heartRate} bpm</p><p className="text-[10px] text-muted-foreground">Heart Rate</p></div>
                </div>
                <div className="flex items-center gap-2 p-2 rounded-lg bg-orange-500/10">
                  <Activity className="h-4 w-4 text-orange-400" />
                  <div><p className="text-sm font-bold text-orange-400">{device.data.calories}</p><p className="text-[10px] text-muted-foreground">Calories</p></div>
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  )
}
