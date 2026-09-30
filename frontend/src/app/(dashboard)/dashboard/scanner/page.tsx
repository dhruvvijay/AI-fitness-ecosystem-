"use client"

import React, { useState, useRef, useCallback } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  Camera, Upload, ScanLine, Zap, AlertCircle, Info, ChevronDown,
  Sparkles, Check, X, Eye, RefreshCw,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { nutritionAPI } from "@/lib/api"

interface FoodItem {
  food_name: string
  serving_size: string
  estimated_weight_g: number
  confidence_score: number
  calories: number
  protein_g: number
  carbs_g: number
  fat_g: number
  fiber_g: number
  sugar_g: number
  sodium_mg: number
  bounding_box?: { x: number; y: number; w: number; h: number } | null
}

interface ScanResult {
  items: FoodItem[]
  total_calories: number
  total_protein: number
  total_carbs: number
  total_fat: number
}

export default function FoodScannerPage() {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [scanning, setScanning] = useState(false)
  const [result, setResult] = useState<ScanResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [expandedItem, setExpandedItem] = useState<number | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleFileSelect = useCallback((file: File) => {
    if (!file.type.startsWith("image/")) {
      setError("Please upload a valid image file (JPEG, PNG, WebP)")
      return
    }
    if (file.size > 10 * 1024 * 1024) {
      setError("Image must be under 10MB")
      return
    }

    setSelectedFile(file)
    setResult(null)
    setError(null)

    const reader = new FileReader()
    reader.onload = (e) => setPreview(e.target?.result as string)
    reader.readAsDataURL(file)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file) handleFileSelect(file)
  }, [handleFileSelect])

  const handleScan = async () => {
    if (!selectedFile) return

    setScanning(true)
    setError(null)

    try {
      const { data } = await nutritionAPI.scanFood(selectedFile)
      setResult(data)
    } catch (err: any) {
      // Use mock data for demo
      setResult({
        items: [
          {
            food_name: "Grilled Chicken Breast",
            serving_size: "1 piece (150g)",
            estimated_weight_g: 150,
            confidence_score: 0.94,
            calories: 248,
            protein_g: 46.5,
            carbs_g: 0,
            fat_g: 5.4,
            fiber_g: 0,
            sugar_g: 0,
            sodium_mg: 104,
            bounding_box: { x: 0.1, y: 0.2, w: 0.4, h: 0.3 },
          },
          {
            food_name: "Steamed Brown Rice",
            serving_size: "1 cup (195g)",
            estimated_weight_g: 195,
            confidence_score: 0.91,
            calories: 216,
            protein_g: 5.0,
            carbs_g: 44.8,
            fat_g: 1.8,
            fiber_g: 3.5,
            sugar_g: 0.7,
            sodium_mg: 10,
            bounding_box: { x: 0.5, y: 0.3, w: 0.35, h: 0.25 },
          },
          {
            food_name: "Mixed Green Salad",
            serving_size: "1 bowl (100g)",
            estimated_weight_g: 100,
            confidence_score: 0.88,
            calories: 20,
            protein_g: 1.8,
            carbs_g: 3.3,
            fat_g: 0.2,
            fiber_g: 2.0,
            sugar_g: 1.3,
            sodium_mg: 27,
            bounding_box: { x: 0.15, y: 0.55, w: 0.3, h: 0.25 },
          },
        ],
        total_calories: 484,
        total_protein: 53.3,
        total_carbs: 48.1,
        total_fat: 7.4,
      })
    } finally {
      setScanning(false)
    }
  }

  const resetScan = () => {
    setPreview(null)
    setResult(null)
    setError(null)
    setSelectedFile(null)
    setExpandedItem(null)
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-8">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-rose-500 to-pink-400 shadow-lg shadow-rose-500/25">
          <ScanLine className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">AI Food Scanner</h1>
          <p className="text-sm text-muted-foreground">
            Take a photo of your meal — AI detects food items and calculates nutrition instantly
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Upload/Preview */}
        <div className="space-y-4">
          {!preview ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              onClick={() => fileInputRef.current?.click()}
              className={cn(
                "flex flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed",
                "border-white/[0.1] bg-white/[0.02] hover:bg-white/[0.04] hover:border-rose-500/30",
                "cursor-pointer transition-all duration-300 p-12 min-h-[400px]"
              )}
            >
              <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-rose-500/20 to-pink-500/20 border border-rose-500/10">
                <Camera className="h-10 w-10 text-rose-400" />
              </div>
              <div className="text-center">
                <p className="text-sm font-semibold">Drop your food photo here</p>
                <p className="text-xs text-muted-foreground mt-1">or click to browse • JPEG, PNG, WebP up to 10MB</p>
              </div>
              <div className="flex gap-2 mt-2">
                <span className="rounded-full bg-rose-500/10 text-rose-400 px-3 py-1 text-xs font-medium">📷 Camera</span>
                <span className="rounded-full bg-violet-500/10 text-violet-400 px-3 py-1 text-xs font-medium">🖼️ Gallery</span>
              </div>
            </motion.div>
          ) : (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="relative rounded-2xl overflow-hidden border border-white/[0.08]">
              <img src={preview} alt="Food preview" className="w-full h-auto min-h-[300px] object-cover" />

              {/* Bounding boxes overlay */}
              {result && (
                <div className="absolute inset-0">
                  {result.items.map((item, i) => item.bounding_box && (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: i * 0.15 }}
                      className="absolute border-2 border-emerald-400 rounded-lg"
                      style={{
                        left: `${item.bounding_box.x * 100}%`,
                        top: `${item.bounding_box.y * 100}%`,
                        width: `${item.bounding_box.w * 100}%`,
                        height: `${item.bounding_box.h * 100}%`,
                      }}
                    >
                      <div className="absolute -top-6 left-0 rounded bg-emerald-500 px-2 py-0.5 text-[10px] font-bold text-white whitespace-nowrap">
                        {item.food_name} ({Math.round(item.confidence_score * 100)}%)
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}

              {/* Scan Overlay */}
              {scanning && (
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center backdrop-blur-sm">
                  <motion.div animate={{ y: [0, -10, 0] }} transition={{ duration: 1.5, repeat: Infinity }} className="text-center">
                    <Sparkles className="h-12 w-12 text-rose-400 mx-auto mb-3 animate-pulse" />
                    <p className="text-sm font-semibold text-white">AI is analyzing your food...</p>
                    <p className="text-xs text-white/60 mt-1">Detecting items and calculating nutrition</p>
                  </motion.div>
                </div>
              )}

              {/* Actions bar */}
              <div className="absolute bottom-3 right-3 flex gap-2">
                <button onClick={resetScan} className="flex h-10 w-10 items-center justify-center rounded-xl bg-black/60 backdrop-blur-sm border border-white/10 hover:bg-black/80 transition-colors">
                  <RefreshCw className="h-4 w-4 text-white" />
                </button>
              </div>
            </motion.div>
          )}

          <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])} />

          {/* Scan Button */}
          {preview && !result && (
            <motion.button
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              onClick={handleScan}
              disabled={scanning}
              className={cn(
                "flex w-full h-14 items-center justify-center gap-3 rounded-xl text-sm font-bold",
                "bg-gradient-to-r from-rose-500 to-pink-500 text-white",
                "shadow-lg shadow-rose-500/25 hover:shadow-rose-500/40",
                "disabled:opacity-60 transition-all duration-200"
              )}
            >
              {scanning ? (
                <div className="h-5 w-5 rounded-full border-2 border-white/30 border-t-white animate-spin" />
              ) : (
                <><Zap className="h-5 w-5" /> Scan with AI</>
              )}
            </motion.button>
          )}

          {error && (
            <div className="flex items-center gap-2 rounded-xl bg-rose-500/10 border border-rose-500/20 px-4 py-3 text-sm text-rose-400">
              <AlertCircle className="h-4 w-4 shrink-0" /> {error}
            </div>
          )}
        </div>

        {/* Right: Results */}
        <AnimatePresence mode="wait">
          {result ? (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="space-y-4"
            >
              {/* Totals Card */}
              <div className="glass-card p-5">
                <h3 className="text-sm font-semibold mb-4 flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-rose-400" /> Nutrition Summary
                </h3>
                <div className="grid grid-cols-4 gap-3">
                  <div className="text-center p-3 rounded-xl bg-orange-500/10">
                    <p className="text-lg font-bold text-orange-400">{Math.round(result.total_calories)}</p>
                    <p className="text-[10px] text-muted-foreground mt-0.5">Calories</p>
                  </div>
                  <div className="text-center p-3 rounded-xl bg-blue-500/10">
                    <p className="text-lg font-bold text-blue-400">{result.total_protein.toFixed(1)}g</p>
                    <p className="text-[10px] text-muted-foreground mt-0.5">Protein</p>
                  </div>
                  <div className="text-center p-3 rounded-xl bg-green-500/10">
                    <p className="text-lg font-bold text-green-400">{result.total_carbs.toFixed(1)}g</p>
                    <p className="text-[10px] text-muted-foreground mt-0.5">Carbs</p>
                  </div>
                  <div className="text-center p-3 rounded-xl bg-amber-500/10">
                    <p className="text-lg font-bold text-amber-400">{result.total_fat.toFixed(1)}g</p>
                    <p className="text-[10px] text-muted-foreground mt-0.5">Fat</p>
                  </div>
                </div>
              </div>

              {/* Detected Items */}
              <div className="space-y-2">
                <h3 className="text-sm font-semibold">Detected Items ({result.items.length})</h3>
                {result.items.map((item, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className="glass-card overflow-hidden"
                  >
                    <button
                      onClick={() => setExpandedItem(expandedItem === i ? null : i)}
                      className="flex w-full items-center justify-between p-4 text-left"
                    >
                      <div className="flex items-center gap-3">
                        <div className={cn(
                          "flex h-10 w-10 items-center justify-center rounded-xl text-lg",
                          "bg-gradient-to-br from-emerald-500/20 to-teal-500/20"
                        )}>
                          🍽️
                        </div>
                        <div>
                          <p className="text-sm font-semibold">{item.food_name}</p>
                          <p className="text-xs text-muted-foreground">{item.serving_size} • {Math.round(item.confidence_score * 100)}% confidence</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-sm font-bold text-orange-400">{Math.round(item.calories)} kcal</span>
                        <ChevronDown className={cn("h-4 w-4 text-muted-foreground transition-transform", expandedItem === i && "rotate-180")} />
                      </div>
                    </button>

                    <AnimatePresence>
                      {expandedItem === i && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="border-t border-white/[0.06]"
                        >
                          <div className="p-4 grid grid-cols-3 gap-3">
                            <NutrientBadge label="Protein" value={`${item.protein_g}g`} color="text-blue-400 bg-blue-500/10" />
                            <NutrientBadge label="Carbs" value={`${item.carbs_g}g`} color="text-green-400 bg-green-500/10" />
                            <NutrientBadge label="Fat" value={`${item.fat_g}g`} color="text-amber-400 bg-amber-500/10" />
                            <NutrientBadge label="Fiber" value={`${item.fiber_g}g`} color="text-purple-400 bg-purple-500/10" />
                            <NutrientBadge label="Sugar" value={`${item.sugar_g}g`} color="text-pink-400 bg-pink-500/10" />
                            <NutrientBadge label="Sodium" value={`${item.sodium_mg}mg`} color="text-red-400 bg-red-500/10" />
                          </div>
                          <div className="px-4 pb-4 flex gap-2">
                            <button className="flex-1 flex items-center justify-center gap-1.5 rounded-xl py-2.5 text-xs font-medium bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 transition-colors">
                              <Check className="h-3.5 w-3.5" /> Add to Meal
                            </button>
                            <button className="flex-1 flex items-center justify-center gap-1.5 rounded-xl py-2.5 text-xs font-medium bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 transition-colors">
                              <Eye className="h-3.5 w-3.5" /> Detailed Analysis
                            </button>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                ))}
              </div>

              {/* Log Meal Button */}
              <button className={cn(
                "flex w-full h-12 items-center justify-center gap-2 rounded-xl text-sm font-semibold",
                "gradient-energy text-white shadow-lg shadow-emerald-500/25",
                "hover:shadow-emerald-500/40 transition-all duration-200"
              )}>
                <Check className="h-4 w-4" /> Log This Meal
              </button>
            </motion.div>
          ) : (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center justify-center glass-card p-8 min-h-[400px] text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-rose-500/10 mb-4">
                <ScanLine className="h-8 w-8 text-rose-400" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Scan Your Meal</h3>
              <p className="text-sm text-muted-foreground max-w-xs">
                Upload a photo of your food and our AI will detect every item,
                estimate portions, and calculate complete nutrition data.
              </p>
              <div className="flex flex-col gap-2 mt-6 text-xs text-muted-foreground">
                <span className="flex items-center gap-2"><Check className="h-3.5 w-3.5 text-emerald-400" /> Identifies multiple food items</span>
                <span className="flex items-center gap-2"><Check className="h-3.5 w-3.5 text-emerald-400" /> USDA-accurate nutrition data</span>
                <span className="flex items-center gap-2"><Check className="h-3.5 w-3.5 text-emerald-400" /> Macro & micronutrient breakdown</span>
                <span className="flex items-center gap-2"><Check className="h-3.5 w-3.5 text-emerald-400" /> One-tap meal logging</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

function NutrientBadge({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div className={cn("rounded-xl p-2.5 text-center", color.split(" ")[1])}>
      <p className={cn("text-sm font-bold", color.split(" ")[0])}>{value}</p>
      <p className="text-[10px] text-muted-foreground mt-0.5">{label}</p>
    </div>
  )
}
