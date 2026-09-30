import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatNumber(num: number, decimals = 1): string {
  if (num >= 1000000) return (num / 1000000).toFixed(decimals) + "M"
  if (num >= 1000) return (num / 1000).toFixed(decimals) + "K"
  return num.toFixed(decimals)
}

export function formatCalories(cal: number): string {
  return Math.round(cal).toLocaleString()
}

export function getGreeting(): string {
  const hour = new Date().getHours()
  if (hour < 12) return "Good Morning"
  if (hour < 17) return "Good Afternoon"
  return "Good Evening"
}

export function calculateProgress(current: number, target: number): number {
  if (target <= 0) return 0
  return Math.min(100, Math.round((current / target) * 100))
}

export function getInitials(name: string): string {
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)
}
