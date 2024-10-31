import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  webpack: (config, { dev, isServer }) => {
    if (dev) {
      config.cache = false;
    }
    
    if (!isServer) {
      config.resolve.fallback = {
        fs: false,
        path: false,
        canvas: false,
      };
    }
    
    return config;
  }
};

export default nextConfig;
