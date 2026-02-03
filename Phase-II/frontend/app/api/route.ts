import { NextResponse } from 'next/server';

// Root API route to confirm API is working
export async function GET() {
  return NextResponse.json({
    message: 'Todo App API is running on Vercel',
    timestamp: new Date().toISOString(),
    status: 'ok'
  });
}