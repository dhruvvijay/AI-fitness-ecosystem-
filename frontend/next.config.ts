import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**" },
    ],
  },
  // NOTE: Removed the /api rewrite that was proxying API calls through
  // the Next.js server. In production on Railway, the frontend calls
  // the backend directly via NEXT_PUBLIC_API_URL. The rewrite was
  // causing login requests to hit the frontend server instead of FastAPI.
};

export default nextConfig;
