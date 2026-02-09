import Link from 'next/link';

const Hero = () => {
  return (
    <section className="min-h-screen flex items-center justify-center pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div className="text-center lg:text-left">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
            Secure, Private Todo Management for the{' '}
            <span className="text-blue-600">Modern Professional</span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto lg:mx-0">
            Protect your productivity with seamless JWT authentication. Your tasks, your privacy, your peace of mind.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <Link
              href="/auth/register"
              className="px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors text-lg text-center"
            >
              Get Started Free
            </Link>

            <Link
              href="/auth/login"
              className="px-8 py-4 bg-white text-gray-900 font-semibold rounded-lg shadow-sm hover:bg-gray-50 transition-colors border border-gray-200 text-lg text-center"
            >
              Login
            </Link>
          </div>
        </div>

        <div className="flex justify-center lg:justify-end">
          <div className="bg-white rounded-2xl shadow-md p-6 w-full max-w-md border border-gray-200">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-bold text-gray-900">My Tasks</h3>
              <div className="flex space-x-2">
                <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                <div className="w-3 h-3 bg-green-400 rounded-full"></div>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-start p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center h-5">
                  <input type="checkbox" className="h-4 w-4 text-blue-600 rounded" />
                </div>
                <div className="ml-3 text-sm">
                  <p className="font-medium text-gray-900">Complete project proposal</p>
                  <p className="text-gray-500">Due tomorrow</p>
                </div>
              </div>

              <div className="flex items-start p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center h-5">
                  <input type="checkbox" className="h-4 w-4 text-blue-600 rounded" />
                </div>
                <div className="ml-3 text-sm">
                  <p className="font-medium text-gray-900">Team meeting preparation</p>
                  <p className="text-gray-500">10:00 AM today</p>
                </div>
              </div>

              <div className="flex items-start p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center h-5">
                  <input type="checkbox" className="h-4 w-4 text-blue-600 rounded" defaultChecked />
                </div>
                <div className="ml-3 text-sm">
                  <p className="font-medium text-gray-900 line-through text-gray-400">Review quarterly reports</p>
                  <p className="text-gray-500">Completed</p>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-gray-200">
              <div className="flex">
                <input
                  type="text"
                  placeholder="Add a new task..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                />
                <button className="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 transition-colors">
                  +
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;