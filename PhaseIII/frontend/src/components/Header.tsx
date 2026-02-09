'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavigation = (path: string) => {
    router.push(path);
    setMobileMenuOpen(false);
  };

  return (
    <>
      {/* Spacer div to prevent content overlap with fixed header */}
      <div className="h-16 md:h-20"></div>

      <header
        className={`fixed top-0 left-0 right-0 z-50 w-full transition-all duration-300 ${
          isScrolled
            ? 'bg-white shadow-md py-2'
            : 'bg-transparent py-4'
        }`}
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-12 md:h-16">
            <div className="flex-shrink-0">
              <Link href="/" className="text-2xl font-bold text-gray-900 hover:text-blue-600 transition-colors">
                SecureTodo
              </Link>
            </div>

            <nav className="hidden md:flex items-center space-x-3">
              <button
                onClick={() => handleNavigation('/auth/login')}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors text-sm md:text-base px-3 py-1.5 rounded-md hover:bg-gray-100"
              >
                Login
              </button>
              <button
                onClick={() => handleNavigation('/auth/register')}
                className="bg-blue-600 text-white px-3 py-1.5 rounded-md font-medium hover:bg-blue-700 transition-colors shadow-sm text-sm md:text-base"
              >
                Sign Up
              </button>
            </nav>

            <div className="md:hidden flex items-center">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="text-gray-700 hover:text-blue-600 focus:outline-none"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  {mobileMenuOpen ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  )}
                </svg>
              </button>
            </div>
          </div>

          {mobileMenuOpen && (
            <div className="md:hidden bg-white border-t mt-0 py-4 absolute top-full left-0 right-0 shadow-lg z-50">
              <div className="flex flex-col space-y-4 px-4 pb-4">
                <button
                  onClick={() => handleNavigation('/auth/login')}
                  className="text-left text-gray-700 hover:text-blue-600 font-medium py-3 px-4 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Login
                </button>
                <button
                  onClick={() => handleNavigation('/auth/register')}
                  className="text-left bg-blue-600 text-white px-4 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors text-center"
                >
                  Get Started
                </button>
              </div>
            </div>
          )}
        </div>
      </header>
    </>
  );
};

export default Header;