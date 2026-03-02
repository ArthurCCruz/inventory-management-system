// Central theme configuration for the application
export const theme = {
  colors: {
    // Primary green palette
    primary: {
      main: '#10b981',
      dark: '#059669',
      light: '#34d399',
      lighter: '#6ee7b7',
      accent: '#064e3b',
    },
    // Secondary colors
    secondary: {
      gray: '#6b7280',
      lightGray: '#9ca3af',
      darkGray: '#374151',
    },
    // Background colors
    background: {
      main: '#ffffff',
      light: '#f9fafb',
      gradient: 'linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%)',
      greenTint: '#f0fdf4',
      yellowTint: '#ecfccb',
    },
    // Text colors
    text: {
      primary: '#1f2937',
      secondary: '#6b7280',
      light: '#9ca3af',
      white: '#ffffff',
    },
    // Status colors
    status: {
      draft: {
        bg: '#f3f4f6',
        text: '#6b7280',
        border: '#d1d5db',
      },
      confirmed: {
        bg: '#fef3c7',
        text: '#92400e',
        border: '#fcd34d',
      },
      done: {
        bg: '#d1fae5',
        text: '#065f46',
        border: '#6ee7b7',
      },
      reserved: {
        bg: '#dbeafe',
        text: '#1e40af',
        border: '#93c5fd',
      },
    },
    // Border colors
    border: {
      light: '#e5e7eb',
      main: '#d1d5db',
      dark: '#9ca3af',
    },
  },
  // Spacing scale (in rem)
  spacing: {
    xs: '0.25rem',   // 4px
    sm: '0.5rem',    // 8px
    md: '0.75rem',   // 12px
    lg: '1rem',      // 16px
    xl: '1.5rem',    // 24px
    '2xl': '2rem',   // 32px
    '3xl': '3rem',   // 48px
  },
  // Border radius values
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    full: '9999px',
  },
  // Shadow definitions
  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 2px 8px rgba(0, 0, 0, 0.08)',
    lg: '0 4px 12px rgba(0, 0, 0, 0.1)',
    xl: '0 8px 16px rgba(16, 185, 129, 0.15)',
    green: '0 4px 12px rgba(16, 185, 129, 0.2)',
  },
  // Typography
  typography: {
    fontFamily: {
      body: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif",
      heading: "'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    },
    fontSize: {
      xs: '0.75rem',   // 12px
      sm: '0.875rem',  // 14px
      base: '0.95rem', // 15px
      md: '1rem',      // 16px
      lg: '1.125rem',  // 18px
      xl: '1.25rem',   // 20px
      '2xl': '1.5rem', // 24px
      '3xl': '2rem',   // 32px
      '4xl': '2.25rem',// 36px
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
    letterSpacing: {
      tight: '-0.02em',
      normal: '0',
      wide: '0.5px',
    },
  },
  // Animation durations
  animation: {
    fast: '150ms',
    normal: '200ms',
    slow: '300ms',
    verySlow: '500ms',
  },
  // Transition timing functions
  transition: {
    ease: 'ease',
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
  },
  // Breakpoints for responsive design
  breakpoints: {
    xs: '480px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
  // Z-index scale
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modalBackdrop: 1040,
    modal: 1050,
    popover: 1060,
    tooltip: 1070,
  },
} as const;

// Export individual theme sections for convenience
export const colors = theme.colors;
export const spacing = theme.spacing;
export const borderRadius = theme.borderRadius;
export const shadows = theme.shadows;
export const typography = theme.typography;
export const animation = theme.animation;
export const transition = theme.transition;
export const breakpoints = theme.breakpoints;

// Helper function to create gradient
export const gradient = (from: string, to: string) => 
  `linear-gradient(135deg, ${from} 0%, ${to} 100%)`;

// Commonly used gradients
export const gradients = {
  primary: gradient(colors.primary.main, colors.primary.dark),
  background: colors.background.gradient,
};

export default theme;
