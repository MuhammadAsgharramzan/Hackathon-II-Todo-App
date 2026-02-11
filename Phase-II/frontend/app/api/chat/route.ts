import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Use NEXT_PUBLIC_API_BASE_URL only (BACKEND_URL is for Docker, not Vercel)
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const authHeader = request.headers.get('authorization');
    const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.substring(7) : null;
    const body = await request.json();

    console.log('Backend URL:', backendUrl); // Debug log
    console.log('Chat request body:', body); // Debug log

    // Forward the chat request to the backend with longer timeout
    const response = await fetch(`${backendUrl}/chat/`, {
      method: 'POST',
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` }),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    console.log('Backend response status:', response.status); // Debug log

    if (!response.ok) {
      const errorData = await response.text();
      console.error('Backend error:', errorData); // Debug log
      return NextResponse.json({ error: errorData }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Chat error:', error); // Debug log
    const errorMessage = error instanceof Error ? error.message : 'Chat request failed';
    return NextResponse.json({ error: errorMessage, details: String(error) }, { status: 500 });
  }
}