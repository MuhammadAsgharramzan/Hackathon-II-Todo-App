/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  // output: "standalone", // Disabled for Vercel deployment (only needed for Docker)
  trailingSlash: undefined, // Let Next.js handle this automatically
  images: {
    unoptimized: true, // For compatibility with static exports if needed
  },
};

module.exports = nextConfig;