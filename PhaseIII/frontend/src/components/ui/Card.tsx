import React from 'react'

interface CardProps {
  children: React.ReactNode
  className?: string
  title?: string
  description?: string
  hoverable?: boolean
  active?: boolean
  onClick?: () => void
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  title,
  description,
  hoverable = false,
  active = false,
  onClick
}) => {
  const baseClasses = `rounded-xl border bg-white text-card-foreground shadow transition-all duration-150 ${
    hoverable ? 'hover:shadow-md hover:border-blue-300' : ''
  } ${
    active ? 'ring-2 ring-blue-500 ring-offset-2' : ''
  } ${
    onClick ? 'cursor-pointer' : ''
  } focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`

  return (
    <div
      className={`${baseClasses} ${className}`}
      onClick={onClick}
      tabIndex={onClick ? 0 : -1}
      onKeyDown={(e) => {
        if (onClick && (e.key === 'Enter' || e.key === ' ')) {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {(title || description) && (
        <div className="p-6 pb-0">
          {title && <h3 className="font-semibold text-lg mb-1">{title}</h3>}
          {description && <p className="text-muted-foreground text-sm">{description}</p>}
        </div>
      )}
      <div className={title || description ? 'p-6 pt-0' : 'p-6'}>
        {children}
      </div>
    </div>
  )
}