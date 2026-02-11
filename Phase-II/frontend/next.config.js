/** @type {import('next').NextConfig} */
const nextConfig = {
  // App Router is stable in Next.js 14, no experimental flag needed
  trailingSlash: undefined, // Let Next.js handle this automatically
  images: {
    unoptimized: true, // For compatibility with static exports if needed
  },
};

module.exports = nextConfig;