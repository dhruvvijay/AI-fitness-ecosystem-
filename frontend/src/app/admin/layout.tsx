import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Admin Dashboard — AI Fitness Ecosystem",
  description: "System administration, user management, and analytics overview",
}

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-[hsl(var(--background))]">
      {children}
    </div>
  )
}
