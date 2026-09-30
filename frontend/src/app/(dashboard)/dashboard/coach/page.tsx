"use client"

import React, { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  Bot, Send, User, Sparkles, Dumbbell, UtensilsCrossed,
  TrendingDown, Heart, RotateCcw, Copy, Check,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { aiAPI } from "@/lib/api"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
}

const quickPrompts = [
  { icon: Dumbbell, label: "Create a workout plan", prompt: "Create a 4-day push/pull/legs workout plan for muscle building" },
  { icon: UtensilsCrossed, label: "Suggest a meal plan", prompt: "Suggest a high-protein 2000 calorie meal plan for weight loss" },
  { icon: TrendingDown, label: "How to lose weight", prompt: "What's the best strategy to lose 5kg in 2 months safely?" },
  { icon: Heart, label: "Improve my health", prompt: "What are the top 5 habits I should build for better overall health?" },
]

export default function AICoachPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(scrollToBottom, [messages])

  const sendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text.trim(),
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const { data } = await aiAPI.chat({
        message: text.trim(),
        session_id: sessionId || undefined,
      })
      if (!sessionId) setSessionId(data.session_id)

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, botMessage])
    } catch {
      // Mock response
      const mockMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: getMockResponse(text),
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, mockMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage(input)
    }
  }

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const resetChat = () => {
    setMessages([])
    setSessionId(null)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-120px)] max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-white/[0.06]">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-purple-500 shadow-lg shadow-violet-500/25">
            <Bot className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight flex items-center gap-2">
              FitBot AI Coach <Sparkles className="h-4 w-4 text-violet-400" />
            </h1>
            <p className="text-xs text-muted-foreground">Your personal AI fitness & nutrition advisor</p>
          </div>
        </div>
        <button onClick={resetChat} className="flex h-9 items-center gap-2 rounded-lg px-3 text-xs font-medium text-muted-foreground hover:text-foreground hover:bg-white/[0.06] transition-colors">
          <RotateCcw className="h-3.5 w-3.5" /> New Chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto scrollbar-thin py-6 space-y-6">
        {messages.length === 0 ? (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col items-center justify-center h-full text-center px-4">
            <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500/20 to-purple-500/20 border border-violet-500/10 mb-6">
              <Bot className="h-10 w-10 text-violet-400" />
            </div>
            <h2 className="text-xl font-bold mb-2">How can I help you today?</h2>
            <p className="text-sm text-muted-foreground max-w-md mb-8">
              I&apos;m your AI fitness coach. Ask me about workouts, nutrition, weight management,
              supplements, or anything fitness-related. I&apos;ll give personalized advice based on your profile.
            </p>

            {/* Quick Prompts */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
              {quickPrompts.map((qp) => (
                <button
                  key={qp.label}
                  onClick={() => sendMessage(qp.prompt)}
                  className={cn(
                    "flex items-center gap-3 rounded-xl p-4 text-left",
                    "bg-white/[0.03] border border-white/[0.06]",
                    "hover:bg-white/[0.06] hover:border-violet-500/20",
                    "transition-all duration-200"
                  )}
                >
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-violet-500/10">
                    <qp.icon className="h-4 w-4 text-violet-400" />
                  </div>
                  <span className="text-xs font-medium">{qp.label}</span>
                </button>
              ))}
            </div>
          </motion.div>
        ) : (
          messages.map((msg, i) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={cn(
                "flex gap-3 max-w-3xl",
                msg.role === "user" ? "ml-auto flex-row-reverse" : ""
              )}
            >
              <div className={cn(
                "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg",
                msg.role === "user"
                  ? "gradient-brand"
                  : "bg-gradient-to-br from-violet-500 to-purple-500"
              )}>
                {msg.role === "user" ? <User className="h-4 w-4 text-white" /> : <Bot className="h-4 w-4 text-white" />}
              </div>
              <div className={cn(
                "rounded-2xl px-4 py-3 text-sm leading-relaxed max-w-[80%]",
                msg.role === "user"
                  ? "bg-blue-600/20 border border-blue-500/10"
                  : "bg-white/[0.04] border border-white/[0.06]"
              )}>
                <div className="whitespace-pre-wrap break-words" dangerouslySetInnerHTML={{
                  __html: msg.content
                    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                    .replace(/\*(.*?)\*/g, "<em>$1</em>")
                    .replace(/- /g, "• ")
                    .replace(/\n/g, "<br/>"),
                }} />

                {msg.role === "assistant" && (
                  <div className="mt-2 pt-2 border-t border-white/[0.06] flex justify-end">
                    <button
                      onClick={() => copyToClipboard(msg.content, msg.id)}
                      className="flex items-center gap-1 text-[10px] text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {copiedId === msg.id ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
                      {copiedId === msg.id ? "Copied!" : "Copy"}
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          ))
        )}

        {isLoading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-violet-500 to-purple-500">
              <Bot className="h-4 w-4 text-white" />
            </div>
            <div className="rounded-2xl bg-white/[0.04] border border-white/[0.06] px-4 py-3">
              <div className="flex items-center gap-1.5">
                <div className="h-2 w-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: "0ms" }} />
                <div className="h-2 w-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: "150ms" }} />
                <div className="h-2 w-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-white/[0.06] pt-4">
        <div className={cn(
          "flex items-end gap-3 rounded-2xl p-3",
          "bg-white/[0.03] border border-white/[0.08]",
          "focus-within:border-violet-500/30 focus-within:ring-2 focus-within:ring-violet-500/10",
          "transition-all duration-200"
        )}>
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask FitBot anything about fitness, nutrition, or workouts..."
            rows={1}
            className={cn(
              "flex-1 bg-transparent border-none outline-none text-sm resize-none",
              "placeholder:text-muted-foreground/50 max-h-32"
            )}
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={!input.trim() || isLoading}
            className={cn(
              "flex h-10 w-10 shrink-0 items-center justify-center rounded-xl",
              "bg-gradient-to-r from-violet-500 to-purple-500 text-white",
              "disabled:opacity-40 disabled:cursor-not-allowed",
              "hover:shadow-lg hover:shadow-violet-500/25",
              "transition-all duration-200"
            )}
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <p className="text-[10px] text-muted-foreground text-center mt-2">
          FitBot provides general fitness advice. Always consult a healthcare professional for medical concerns.
        </p>
      </div>
    </div>
  )
}

function getMockResponse(message: string): string {
  const msg = message.toLowerCase()
  if (msg.includes("workout") || msg.includes("exercise") || msg.includes("gym")) {
    return "💪 **Here's a solid 4-day workout plan:**\n\n**Day 1 — Push (Chest/Shoulders/Triceps)**\n- Bench Press: 4×8\n- Overhead Press: 3×10\n- Incline Dumbbell Press: 3×12\n- Lateral Raises: 3×15\n- Tricep Pushdowns: 3×12\n\n**Day 2 — Pull (Back/Biceps)**\n- Deadlifts: 4×6\n- Pull-ups: 3×8\n- Barbell Rows: 3×10\n- Face Pulls: 3×15\n- Bicep Curls: 3×12\n\n**Day 3 — Rest**\n\n**Day 4 — Legs**\n- Squats: 4×8\n- Romanian Deadlifts: 3×10\n- Leg Press: 3×12\n- Leg Curls: 3×12\n- Calf Raises: 4×15\n\n**Day 5 — Upper Body Mix**\n- Dips: 3×10\n- Chin-ups: 3×8\n- Dumbbell Flyes: 3×12\n- Hammer Curls: 3×12\n\nRest 60-90 seconds between sets. Progressive overload weekly! 🎯"
  }
  if (msg.includes("meal") || msg.includes("food") || msg.includes("calorie") || msg.includes("diet") || msg.includes("eat")) {
    return "🥗 **Here's a high-protein 2000 calorie meal plan:**\n\n**Breakfast (450 cal)**\n- 3 egg whites + 1 whole egg omelette\n- ½ cup oats with berries\n- Black coffee\n\n**Lunch (550 cal)**\n- 200g grilled chicken breast\n- 1 cup brown rice\n- Mixed green salad\n- 1 tbsp olive oil dressing\n\n**Snack (250 cal)**\n- Greek yogurt (200g)\n- 15g almonds\n- 1 small banana\n\n**Dinner (500 cal)**\n- 180g baked salmon\n- Sweet potato (150g)\n- Steamed broccoli\n- Lemon squeeze\n\n**Evening Snack (250 cal)**\n- Protein shake\n- 1 apple with peanut butter\n\n**Macros: 165g protein | 180g carbs | 62g fat**\n\nStay hydrated with 3L of water! 💧"
  }
  if (msg.includes("weight") || msg.includes("lose") || msg.includes("fat")) {
    return "⚖️ **Safe plan to lose 5kg in 2 months:**\n\n**The Math:**\n- 5kg fat = ~38,500 calories deficit needed\n- Over 60 days = ~640 cal/day deficit\n- This is very achievable!\n\n**Strategy:**\n1. **Calculate your TDEE** (use our BMI calculator) and eat 500-600 cal below it\n2. **Protein first** — 1.8g per kg body weight to preserve muscle\n3. **Strength train 3-4x/week** — muscle burns more calories at rest\n4. **Add 150 min/week cardio** — mix LISS (walking) and HIIT\n5. **Sleep 7-9 hours** — poor sleep increases cortisol and hunger\n6. **Track everything** — use the food scanner to log meals accurately\n\n**Expected timeline:**\n- Week 1-2: Quick initial drop (water weight)\n- Week 3-6: Steady 0.5-0.7 kg/week\n- Week 7-8: Final push, may need slight adjustment\n\nDon't go below 1200 cal (women) or 1500 cal (men). Be patient! 🎯"
  }
  return "👋 **Great question!**\n\nI can help you with:\n\n- 🏋️ **Workout plans** — customized to your goals\n- 🥗 **Meal planning** — macro-optimized recipes\n- ⚖️ **Weight management** — sustainable strategies\n- 📊 **Progress analysis** — review your trends\n- 💊 **Supplement advice** — evidence-based recommendations\n\nTell me more about your goals and I'll give you a personalized plan! What are you working towards? 💪"
}
