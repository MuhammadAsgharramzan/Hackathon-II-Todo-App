import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Use NEXT_PUBLIC_API_BASE_URL only (BACKEND_URL is for Docker, not Vercel)
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const body = await request.json();
    const { email, password } = body;

    console.log('Backend URL:', backendUrl); // Debug log
    console.log('Attempting registration for:', email); // Debug log

    // Forward the registration request to the backend
    const response = await fetch(`${backendUrl}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    console.log('Backend response status:', response.status); // Debug log

    if (!response.ok) {
      const errorData = await response.text();
      console.error('Backend error:', errorData); // Debug log
      return NextResponse.json({ error: errorData || 'Registration failed' }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Registration error:', error); // Debug log
    const errorMessage = error instanceof Error ? error.message : 'Registration failed';
    return NextResponse.json({ error: errorMessage, details: String(error) }, { status: 500 });
  }
}