import React from 'react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  success?: boolean
  helperText?: string
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  success,
  helperText,
  className = '',
  ...props
}) => {
  const baseClasses = `flex h-10 w-full rounded-md border px-3 py-2 text-sm shadow-sm transition-colors duration-150 file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50`

  let borderClasses = 'border-gray-300 focus:ring-blue-500 focus:ring-offset-blue-50'
  if (error) {
    borderClasses = 'border-red-500 focus:ring-red-500 focus:ring-offset-red-50'
  } else if (success) {
    borderClasses = 'border-green-500 focus:ring-green-500 focus:ring-offset-green-50'
  }

  const inputClass = `${baseClasses} ${borderClasses} ${className}`

  return (
    <div className="w-full">
      {label && (
        <label className={`block text-sm font-medium mb-1 ${error ? 'text-red-700' : success ? 'text-green-700' : 'text-gray-700'}`}>
          {label}
        </label>
      )}
      <input
        className={inputClass}
        {...props}
      />
      {helperText && !error && (
        <p className="mt-1 text-sm text-gray-500">{helperText}</p>
      )}
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
      {success && !error && helperText && (
        <p className="mt-1 text-sm text-green-600">{helperText}</p>
      )}
    </div>
  )
}