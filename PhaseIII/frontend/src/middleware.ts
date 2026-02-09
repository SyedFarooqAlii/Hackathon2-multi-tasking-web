import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  // Check for protected routes - update to match actual app structure
  const isProtectedRoute = request.nextUrl.pathname.startsWith('/dashboard') ||
                          request.nextUrl.pathname.startsWith('/todos') ||
                          request.nextUrl.pathname.startsWith('/protected')

  // Check for public auth routes
  const isAuthRoute = request.nextUrl.pathname.startsWith('/auth/login') ||
                      request.nextUrl.pathname.startsWith('/auth/register')

  // Note: localStorage tokens are not accessible in middleware (server-side)
  // Authentication is handled client-side in the components
  // For now, let the client-side components handle authentication

  // Allow all routes to be accessed, authentication will be handled client-side
  return NextResponse.next()
}

// Define which paths the middleware should run for
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}