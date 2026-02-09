import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { AuthProvider } from '../contexts/AuthContext';
import { ThemeProvider } from 'next-themes';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Secure Todo App',
  description: 'Secure multi-user todo application with JWT authentication',
};

import Navigation from './Navigation';
import './globals.css'; // Import CSS at the bottom to avoid TS error

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <AuthProvider>
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
              <Navigation />
              <main>{children}</main>
              {/* Footer */}
              <footer className="bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 border-t border-gray-200 dark:border-gray-700 mt-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                  <div className="flex flex-col md:flex-row justify-between items-center">
                    <div className="mb-4 md:mb-0">
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        © {new Date().getFullYear()} SecureTodo App. All rights reserved.
                      </p>
                      <p className="text-gray-500 dark:text-gray-500 text-xs mt-1">
                        Developed by Syed Farooq Ali
                      </p>
                    </div>
                    <div className="flex space-x-6">
                      <a
                        href="https://www.linkedin.com/in/syed-farooq-ali-8328b4267"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 transition-colors duration-200"
                        aria-label="LinkedIn"
                      >
                        LinkedIn
                      </a>
                      <a
                        href="https://github.com/SyedFarooqAlii"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-colors duration-200"
                        aria-label="GitHub"
                      >
                        GitHub
                      </a>
                    </div>
                  </div>
                </div>
              </footer>
            </div>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}