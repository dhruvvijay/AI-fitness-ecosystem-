"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import { Music, Play, Pause, SkipForward, SkipBack, Volume2, Heart, ListMusic, Shuffle, Repeat } from "lucide-react"
import { cn } from "@/lib/utils"

const playlists = [
  { name: "Beast Mode — Heavy Lifting", songs: 24, duration: "1h 32m", mood: "🔥 Intense", color: "from-red-500 to-orange-500" },
  { name: "Cardio Rush — HIIT", songs: 18, duration: "58m", mood: "⚡ Energetic", color: "from-yellow-500 to-amber-500" },
  { name: "Zen Flow — Yoga & Stretch", songs: 15, duration: "1h 10m", mood: "🧘 Calm", color: "from-teal-500 to-emerald-500" },
  { name: "Morning Run Vibes", songs: 20, duration: "1h 15m", mood: "🌅 Uplifting", color: "from-sky-500 to-blue-500" },
  { name: "Pump Up — Pre-Workout", songs: 12, duration: "42m", mood: "💪 Hype", color: "from-purple-500 to-fuchsia-500" },
]

const nowPlaying = {
  title: "Lose Yourself",
  artist: "Eminem",
  album: "8 Mile Soundtrack",
  duration: "5:26",
  elapsed: "2:14",
  progress: 42,
}

const queue = [
  { title: "Eye of the Tiger", artist: "Survivor", duration: "4:04" },
  { title: "Stronger", artist: "Kanye West", duration: "5:11" },
  { title: "Remember the Name", artist: "Fort Minor", duration: "3:50" },
  { title: "Till I Collapse", artist: "Eminem", duration: "4:57" },
]

export default function MusicPage() {
  const [isPlaying, setIsPlaying] = useState(true)

  return (
    <div className="space-y-6 pb-8">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-green-600 to-emerald-500 shadow-lg shadow-green-600/25">
          <Music className="h-6 w-6 text-white" />
        </div>
        <div><h1 className="text-2xl font-bold tracking-tight">Workout Music</h1><p className="text-sm text-muted-foreground">Curated playlists to power your sessions</p></div>
      </div>

      {/* Now Playing */}
      <div className="glass-card p-6 relative overflow-hidden">
        <div className="absolute -top-20 -right-20 h-48 w-48 rounded-full bg-green-500/10 blur-3xl" />
        <div className="relative z-10 flex items-center gap-6">
          <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-green-600 to-emerald-500 text-3xl shadow-lg shadow-green-600/25">🎵</div>
          <div className="flex-1">
            <p className="text-xs text-emerald-400 font-medium mb-1">NOW PLAYING</p>
            <p className="text-lg font-bold">{nowPlaying.title}</p>
            <p className="text-sm text-muted-foreground">{nowPlaying.artist} • {nowPlaying.album}</p>

            {/* Progress */}
            <div className="mt-3 space-y-1">
              <div className="h-1.5 w-full rounded-full bg-white/[0.06] overflow-hidden">
                <motion.div initial={{ width: 0 }} animate={{ width: `${nowPlaying.progress}%` }} transition={{ duration: 1 }}
                  className="h-full rounded-full bg-emerald-500" />
              </div>
              <div className="flex justify-between text-[10px] text-muted-foreground">
                <span>{nowPlaying.elapsed}</span><span>{nowPlaying.duration}</span>
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center gap-4 mt-3">
              <button className="text-muted-foreground hover:text-foreground transition-colors"><Shuffle className="h-4 w-4" /></button>
              <button className="text-muted-foreground hover:text-foreground transition-colors"><SkipBack className="h-5 w-5" /></button>
              <button onClick={() => setIsPlaying(!isPlaying)}
                className="flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500 text-white shadow-lg shadow-emerald-500/30 hover:shadow-emerald-500/50 transition-all">
                {isPlaying ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5 ml-0.5" />}
              </button>
              <button className="text-muted-foreground hover:text-foreground transition-colors"><SkipForward className="h-5 w-5" /></button>
              <button className="text-muted-foreground hover:text-foreground transition-colors"><Repeat className="h-4 w-4" /></button>
              <div className="ml-auto flex items-center gap-2"><Volume2 className="h-4 w-4 text-muted-foreground" /><div className="w-20 h-1 rounded-full bg-white/[0.06]"><div className="w-3/4 h-full rounded-full bg-emerald-500" /></div></div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Playlists */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4">Workout Playlists</h3>
          <div className="space-y-2">
            {playlists.map((p, i) => (
              <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }}
                className="flex items-center gap-3 p-3 rounded-xl bg-white/[0.02] border border-white/[0.04] hover:bg-white/[0.04] cursor-pointer transition-colors">
                <div className={cn("flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br text-sm shadow-lg", p.color)}>🎶</div>
                <div className="flex-1"><p className="text-sm font-medium">{p.name}</p><p className="text-xs text-muted-foreground">{p.songs} songs • {p.duration} • {p.mood}</p></div>
                <button className="flex h-8 w-8 items-center justify-center rounded-full bg-white/[0.06] hover:bg-white/[0.1] transition-colors"><Play className="h-3.5 w-3.5 ml-0.5" /></button>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Queue */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold mb-4 flex items-center gap-2"><ListMusic className="h-4 w-4 text-emerald-400" /> Up Next</h3>
          <div className="space-y-2">
            {queue.map((song, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/[0.04] hover:bg-white/[0.04] cursor-pointer transition-colors">
                <div className="flex items-center gap-3">
                  <span className="text-xs text-muted-foreground w-5 text-center">{i + 1}</span>
                  <div><p className="text-sm font-medium">{song.title}</p><p className="text-xs text-muted-foreground">{song.artist}</p></div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-muted-foreground">{song.duration}</span>
                  <button className="text-muted-foreground hover:text-red-400 transition-colors"><Heart className="h-3.5 w-3.5" /></button>
                </div>
              </div>
            ))}
          </div>
          <p className="text-center text-xs text-muted-foreground mt-4">Connect Spotify for personalized workout playlists</p>
        </div>
      </div>
    </div>
  )
}
