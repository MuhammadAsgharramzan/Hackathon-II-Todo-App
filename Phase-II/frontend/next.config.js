/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  output: "standalone", // Enabled for Docker optimization
  trailingSlash: undefined, // Let Next.js handle this automatically
  images: {
    unoptimized: true, // For compatibility with static exports if needed
  },
};

module.exports = nextConfig;