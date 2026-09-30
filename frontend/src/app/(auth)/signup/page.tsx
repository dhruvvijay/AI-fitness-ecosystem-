"use client"

import React, { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { Eye, EyeOff, Mail, Lock, User, Heart, ArrowRight, Check } from "lucide-react"
import { useAppDispatch, useAppSelector } from "@/store"
import { signupUser, clearError } from "@/store/slices/authSlice"
import { cn } from "@/lib/utils"

const passwordRules = [
  { label: "At least 8 characters", test: (p: string) => p.length >= 8 },
  { label: "One uppercase letter", test: (p: string) => /[A-Z]/.test(p) },
  { label: "One lowercase letter", test: (p: string) => /[a-z]/.test(p) },
  { label: "One number", test: (p: string) => /\d/.test(p) },
  { label: "One special character", test: (p: string) => /[!@#$%^&*(),.?":{}|<>]/.test(p) },
]

export default function SignupPage() {
  const router = useRouter()
  const dispatch = useAppDispatch()
  const { isLoading, error } = useAppSelector((s) => s.auth)
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const result = await dispatch(signupUser({ email, password, full_name: fullName }))
    if (signupUser.fulfilled.match(result)) {
      router.push("/dashboard")
    }
  }

  return (
    <div className="flex min-h-screen">
      {/* Left: Hero */}
      <div className="hidden lg:flex flex-1 items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-600 via-teal-500 to-cyan-500 opacity-90" />
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10" />
        <div className="absolute top-1/3 left-1/3 h-72 w-72 rounded-full bg-white/10 blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/3 h-56 w-56 rounded-full bg-emerald-300/20 blur-3xl animate-float" style={{ animationDelay: "2s" }} />

        <div className="relative z-10 max-w-md text-center text-white px-8">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}>
            <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20">
              <Heart className="h-10 w-10" />
            </div>
            <h2 className="text-3xl font-bold mb-3">Start Your<br />Transformation</h2>
            <p className="text-white/70 text-sm leading-relaxed">
              Join thousands who&apos;ve already transformed their fitness journey
              with AI-powered insights, personalized plans, and smart tracking.
            </p>
            <div className="mt-6 flex justify-center gap-8 text-sm">
              <div><p className="text-2xl font-bold">50K+</p><p className="text-white/60 text-xs">Active Users</p></div>
              <div><p className="text-2xl font-bold">2M+</p><p className="text-white/60 text-xs">Meals Tracked</p></div>
              <div><p className="text-2xl font-bold">98%</p><p className="text-white/60 text-xs">Satisfaction</p></div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Right: Form */}
      <div className="flex flex-1 items-center justify-center px-4 py-12 bg-[hsl(var(--background))]">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="w-full max-w-md space-y-7">
          <div className="flex items-center gap-3 lg:hidden">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl gradient-energy shadow-lg shadow-emerald-500/25">
              <Heart className="h-6 w-6 text-white" />
            </div>
            <div><h1 className="text-xl font-bold tracking-tight">AI Fitness</h1></div>
          </div>

          <div>
            <h2 className="text-2xl font-bold tracking-tight">Create your account</h2>
            <p className="mt-1 text-sm text-muted-foreground">Start your fitness journey today — it&apos;s free</p>
          </div>

          {error && (
            <div className="rounded-xl bg-rose-500/10 border border-rose-500/20 px-4 py-3 text-sm text-rose-400">{error}</div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-sm font-medium">Full Name</label>
              <div className="relative">
                <User className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="John Doe" required
                  className={cn("w-full h-12 rounded-xl pl-10 pr-4 text-sm bg-white/[0.04] border border-white/[0.08] placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500/40 transition-all duration-200")} />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-sm font-medium">Email</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input type="email" value={email} onChange={(e) => { setEmail(e.target.value); dispatch(clearError()) }} placeholder="you@example.com" required
                  className={cn("w-full h-12 rounded-xl pl-10 pr-4 text-sm bg-white/[0.04] border border-white/[0.08] placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500/40 transition-all duration-200")} />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-sm font-medium">Password</label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input type={showPassword ? "text" : "password"} value={password} onChange={(e) => { setPassword(e.target.value); dispatch(clearError()) }} placeholder="••••••••" required
                  className={cn("w-full h-12 rounded-xl pl-10 pr-12 text-sm bg-white/[0.04] border border-white/[0.08] placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500/40 transition-all duration-200")} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors">
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {/* Password Strength */}
            {password && (
              <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="space-y-1.5">
                {passwordRules.map((rule) => (
                  <div key={rule.label} className="flex items-center gap-2 text-xs">
                    <div className={cn("flex h-4 w-4 items-center justify-center rounded-full transition-colors", rule.test(password) ? "bg-emerald-500" : "bg-white/[0.06]")}>
                      {rule.test(password) && <Check className="h-3 w-3 text-white" />}
                    </div>
                    <span className={rule.test(password) ? "text-emerald-400" : "text-muted-foreground"}>{rule.label}</span>
                  </div>
                ))}
              </motion.div>
            )}

            <button type="submit" disabled={isLoading || !passwordRules.every((r) => r.test(password))}
              className={cn("flex w-full h-12 items-center justify-center gap-2 rounded-xl text-sm font-semibold bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 hover:scale-[1.01] disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200")}>
              {isLoading ? <div className="h-5 w-5 rounded-full border-2 border-white/30 border-t-white animate-spin" /> : (<>Create Account <ArrowRight className="h-4 w-4" /></>)}
            </button>
          </form>

          <div className="relative">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-white/[0.08]" /></div>
            <div className="relative flex justify-center text-xs"><span className="bg-[hsl(var(--background))] px-3 text-muted-foreground">or continue with</span></div>
          </div>

          <button type="button" className={cn("flex w-full h-12 items-center justify-center gap-3 rounded-xl text-sm font-medium bg-white/[0.04] border border-white/[0.08] hover:bg-white/[0.08] transition-all duration-200")}>
            <svg className="h-5 w-5" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            Continue with Google
          </button>

          <p className="text-center text-sm text-muted-foreground">
            Already have an account? <Link href="/login" className="text-emerald-400 hover:text-emerald-300 font-medium transition-colors">Sign in</Link>
          </p>
        </motion.div>
      </div>
    </div>
  )
}
