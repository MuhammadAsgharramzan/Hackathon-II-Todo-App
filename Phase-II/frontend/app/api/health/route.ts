import { NextResponse } from 'next/server';

/**
 * Health check endpoint for frontend
 * Returns 200 if the Next.js application is running
 */
export async function GET() {
  return NextResponse.json(
    {
      status: 'healthy',
      service: 'todo-frontend',
      timestamp: new Date().toISOString(),
    },
    { status: 200 }
  );
}
