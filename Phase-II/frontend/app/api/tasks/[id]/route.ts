import { NextRequest, NextResponse } from 'next/server';
import { headers } from 'next/headers';
import { unstable_noStore as noStore } from 'next/cache';

// Dynamic route for individual tasks
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  noStore(); // Disable caching for this route

  try {
    // Use NEXT_PUBLIC_API_BASE_URL only (BACKEND_URL is for Docker, not Vercel)
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const authHeader = request.headers.get('authorization');
    const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.substring(7) : null;
    const taskId = params.id;

    const response = await fetch(`${backendUrl}/tasks/${taskId}`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` }),
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch task' }, { status: 500 });
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // Use NEXT_PUBLIC_API_BASE_URL only (BACKEND_URL is for Docker, not Vercel)
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const authHeader = headers().get('authorization');
    const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.substring(7) : null;
    const taskId = params.id;
    const body = await request.json();

    const response = await fetch(`${backendUrl}/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` }),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to update task' }, { status: 500 });
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // Use NEXT_PUBLIC_API_BASE_URL only (BACKEND_URL is for Docker, not Vercel)
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const authHeader = headers().get('authorization');
    const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.substring(7) : null;
    const taskId = params.id;

    const response = await fetch(`${backendUrl}/tasks/${taskId}`, {
      method: 'DELETE',
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` }),
        'Content-Type': 'application/json',
      },
    });

    return new NextResponse(null, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to delete task' }, { status: 500 });
  }
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // Use NEXT_PUBLIC_API_BASE_URL only (BACKEND_URL is for Docker, not Vercel)
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const authHeader = headers().get('authorization');
    const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.substring(7) : null;
    const taskId = params.id;

    const response = await fetch(`${backendUrl}/tasks/${taskId}/toggle-complete`, {
      method: 'PATCH',
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` }),
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to toggle task completion' }, { status: 500 });
  }
}