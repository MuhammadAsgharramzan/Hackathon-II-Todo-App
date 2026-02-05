import { NextRequest, NextResponse } from 'next/server';

// Proxy for tasks API
export async function GET(request: NextRequest) {
  try {
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const authHeader = request.headers.get('authorization');
const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.substring(7) : null;

    const response = await fetch(`${backendUrl}/tasks/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` }),
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch tasks' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const authHeader = request.headers.get('authorization');
const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.substring(7) : null;
    const body = await request.json();

    const response = await fetch(`${backendUrl}/tasks/`, {
      method: 'POST',
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` }),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to create task' }, { status: 500 });
  }
}