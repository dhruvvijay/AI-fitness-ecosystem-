"use client"

import React from "react"
import Link from "next/link"
import { motion } from "framer-motion"
import {
  Heart, ScanLine, Dumbbell, BarChart3, Bot, Bluetooth,
  Music, Calculator, UtensilsCrossed, TrendingUp, ArrowRight,
  Star, Shield, Zap, CheckCircle2,
} from "lucide-react"
import { cn } from "@/lib/utils"

const features = [
  { icon: ScanLine, title: "AI Food Scanner", desc: "Point your camera at any meal — AI detects food, estimates portions, and calculates complete macros in seconds.", color: "from-rose-500 to-pink-400" },
  { icon: Dumbbell, title: "Smart Workouts", desc: "Browse 200+ exercises with video demos. AI generates personalized plans based on your goals and equipment.", color: "from-indigo-500 to-blue-400" },
  { icon: Bot, title: "AI Fitness Coach", desc: "Chat with FitBot — your 24/7 AI coach. Get workout advice, nutrition tips, and motivation on demand.", color: "from-violet-500 to-purple-400" },
  { icon: BarChart3, title: "Deep Analytics", desc: "Radar charts, weight trends, fitness scores, and AI-powered insights to optimize your journey.", color: "from-emerald-500 to-teal-400" },
  { icon: Calculator, title: "BMI & TDEE Calculator", desc: "Calculate BMI, BMR, TDEE, and get personalized macro recommendations using evidence-based formulas.", color: "from-purple-500 to-violet-400" },
  { icon: UtensilsCrossed, title: "Meal Planning", desc: "AI-generated meal plans for any diet — keto, vegan, Indian, high-protein. Scaled to your calorie targets.", color: "from-teal-500 to-cyan-400" },
  { icon: TrendingUp, title: "Progress Tracking", desc: "Weight journey charts, body measurements, progress photos, and achievement badges to keep you motivated.", color: "from-sky-500 to-blue-400" },
  { icon: Bluetooth, title: "Device Integration", desc: "Connect fitness bands, heart rate monitors, and smart scales via Web Bluetooth for real-time data sync.", color: "from-blue-600 to-indigo-500" },
  { icon: Music, title: "Workout Music", desc: "Curated playlists for every workout type — heavy lifting, HIIT, yoga, running. Spotify integration ready.", color: "from-green-600 to-emerald-500" },
]

const stats = [
  { value: "50K+", label: "Active Users" },
  { value: "2M+", label: "Workouts Logged" },
  { value: "10M+", label: "Meals Tracked" },
  { value: "98%", label: "Satisfaction" },
]

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.08 } } }
const item = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0, transition: { duration: 0.5 } } }

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[hsl(var(--background))]">
      {/* Nav */}
      <nav className="sticky top-0 z-50 border-b border-white/[0.06] bg-[hsl(var(--background))]/80 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl gradient-brand"><Heart className="h-5 w-5 text-white" /></div>
            <span className="text-lg font-bold tracking-tight">AI Fitness</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/login" className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">Sign In</Link>
            <Link href="/signup" className={cn("flex h-10 items-center gap-2 rounded-xl px-5 text-sm font-semibold gradient-brand text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transition-all")}>
              Get Started <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 h-96 w-96 rounded-full bg-blue-500/10 blur-[128px]" />
          <div className="absolute bottom-1/3 right-1/4 h-80 w-80 rounded-full bg-purple-500/10 blur-[128px]" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 py-24 md:py-32 text-center">
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}>
            <div className="inline-flex items-center gap-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-4 py-1.5 text-xs font-medium text-blue-400 mb-6">
              <Zap className="h-3.5 w-3.5" /> Powered by GPT-4o & Gemini AI
            </div>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-black tracking-tight leading-tight">
              Your AI-Powered<br />
              <span className="gradient-brand gradient-text">Fitness Ecosystem</span>
            </h1>
            <p className="mt-6 text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Track workouts, scan food with AI vision, get personalized meal plans,
              chat with your AI fitness coach, and achieve your goals with intelligent insights.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-10">
              <Link href="/signup" className={cn("flex h-14 items-center gap-3 rounded-2xl px-8 text-base font-bold gradient-brand text-white shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-[1.02] transition-all duration-200")}>
                Start Free <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/login" className="flex h-14 items-center gap-2 rounded-2xl px-8 text-base font-medium bg-white/[0.04] border border-white/[0.08] hover:bg-white/[0.08] transition-all">
                Sign In
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats */}
      <section className="border-y border-white/[0.06] bg-white/[0.01]">
        <div className="max-w-7xl mx-auto px-4 py-12 grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((s, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }}
              className="text-center">
              <p className="text-3xl md:text-4xl font-black gradient-brand gradient-text">{s.value}</p>
              <p className="text-sm text-muted-foreground mt-1">{s.label}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight">Everything You Need</h2>
          <p className="mt-3 text-lg text-muted-foreground max-w-lg mx-auto">
            A complete ecosystem built for serious fitness enthusiasts and beginners alike.
          </p>
        </div>

        <motion.div variants={container} initial="hidden" whileInView="show" viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {features.map((f, i) => (
            <motion.div key={i} variants={item} className="glass-card p-6 group">
              <div className={cn("flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br shadow-lg mb-4", f.color)}>
                <f.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-bold mb-2">{f.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* CTA */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 gradient-brand opacity-90" />
        <div className="relative max-w-4xl mx-auto px-4 py-20 text-center text-white">
          <h2 className="text-3xl md:text-4xl font-bold">Ready to Transform Your Body?</h2>
          <p className="mt-4 text-lg text-white/70 max-w-xl mx-auto">
            Join thousands who&apos;ve already revolutionized their fitness journey with AI-powered insights.
          </p>
          <Link href="/signup" className="inline-flex h-14 items-center gap-3 rounded-2xl px-8 text-base font-bold bg-white text-blue-600 shadow-xl hover:shadow-white/25 hover:scale-[1.02] transition-all mt-8">
            Get Started — It&apos;s Free <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/[0.06] py-8">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2"><Heart className="h-5 w-5 text-blue-400" /><span className="text-sm font-bold">AI Fitness Ecosystem</span></div>
          <p className="text-xs text-muted-foreground">© 2026 AI Fitness Ecosystem. Built with ❤️ for your health.</p>
        </div>
      </footer>
    </div>
  )
}
