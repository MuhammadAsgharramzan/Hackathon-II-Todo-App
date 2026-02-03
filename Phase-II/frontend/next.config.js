/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  output: undefined, // Don't set to "export" to maintain API route functionality
  trailingSlash: undefined, // Let Next.js handle this automatically
  images: {
    unoptimized: true, // For compatibility with static exports if needed
  },
};

module.exports = nextConfig;