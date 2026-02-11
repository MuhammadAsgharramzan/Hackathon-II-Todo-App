import { NextResponse } from 'next/server';

export async function GET() {
  const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  // Test if we can reach the backend
  let backendReachable = false;
  let backendError = null;

  try {
    const response = await fetch(`${backendUrl}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    backendReachable = response.ok;
    backendError = response.ok ? null : `Status: ${response.status}`;
  } catch (error) {
    backendError = error instanceof Error ? error.message : String(error);
  }

  return NextResponse.json({
    backendUrl,
    backendReachable,
    backendError,
    envVars: {
      BACKEND_URL: process.env.BACKEND_URL || 'not set',
      NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'not set',
    },
  });
}
