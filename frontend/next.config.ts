import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/proxy/:path*',
        destination: `${process.env.BACKEND_URL || 'http://4.144.73.42:8000'}/:path*`,
      },
    ]
  },
};

export default nextConfig;
