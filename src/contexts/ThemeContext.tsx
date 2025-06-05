import React, { createContext, useContext, useState, useEffect } from 'react';

// Theme definitions based on the specification
export const themes = {
  light: {
    name: 'Sky Sanctuary',
    id: 'light',
    background: 'bg-gradient-to-br from-blue-50 to-blue-100',
    text: 'text-blue-900',
    accent: 'text-sky-500',
    chat: 'bg-white shadow-lg border border-blue-200',
    button: 'bg-sky-500 hover:bg-sky-600 text-white',
    card: 'bg-white/80 backdrop-blur-sm border border-blue-200',
    overlay: 'bg-blue-50/50',
    animations: {
      clouds: true,
      particles: false,
      stars: false
    },
    colors: {
      primary: '#0ea5e9',
      secondary: '#1e40af',
      background: '#e0f2fe',
      surface: '#ffffff',
      text: '#1e40af',
      accent: '#0ea5e9'
    }
  },
  purple: {
    name: 'Neon Sanctuary',
    id: 'purple',
    background: 'bg-gradient-to-br from-purple-900 via-pink-800 to-blue-900',
    text: 'text-white',
    accent: 'text-pink-400',
    chat: 'bg-purple-900/50 backdrop-blur border border-pink-500/30 shadow-neon-purple',
    button: 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white shadow-neon-pink',
    card: 'bg-purple-900/30 backdrop-blur-md border border-pink-500/20 shadow-neon-purple',
    overlay: 'bg-purple-900/20',
    animations: {
      clouds: false,
      particles: true,
      stars: false
    },
    colors: {
      primary: '#ec4899',
      secondary: '#7c3aed',
      background: '#581c87',
      surface: '#7c2d12',
      text: '#ffffff',
      accent: '#ec4899'
    }
  },
  dark: {
    name: 'Stellar Sanctuary',
    id: 'dark',
    background: 'bg-gray-900',
    text: 'text-gray-100',
    accent: 'text-purple-400',
    chat: 'bg-gray-800 border border-gray-700 shadow-xl',
    button: 'bg-purple-600 hover:bg-purple-700 text-white',
    card: 'bg-gray-800/80 backdrop-blur-sm border border-gray-700',
    overlay: 'bg-gray-900/50',
    animations: {
      clouds: false,
      particles: false,
      stars: true
    },
    colors: {
      primary: '#a855f7',
      secondary: '#6b21a8',
      background: '#0a0a0a',
      surface: '#1f2937',
      text: '#f3f4f6',
      accent: '#a855f7'
    }
  }
};

export type ThemeId = keyof typeof themes;
export type Theme = typeof themes[ThemeId];

interface ThemeContextType {
  theme: Theme;
  themeId: ThemeId;
  setTheme: (themeId: ThemeId) => void;
  themes: typeof themes;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

interface ThemeProviderProps {
  children: React.ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [themeId, setThemeId] = useState<ThemeId>(() => {
    // Load saved theme from localStorage
    const saved = localStorage.getItem('podplay-sanctuary-theme');
    return (saved as ThemeId) || 'light';
  });

  const theme = themes[themeId];

  const setTheme = (newThemeId: ThemeId) => {
    setThemeId(newThemeId);
    localStorage.setItem('podplay-sanctuary-theme', newThemeId);
  };

  // Apply theme classes to document
  useEffect(() => {
    const root = document.documentElement;
    
    // Remove all theme classes
    Object.values(themes).forEach(t => {
      root.classList.remove(t.id);
    });
    
    // Add current theme class
    root.classList.add(theme.id);
    
    // Set CSS custom properties for the theme
    const style = root.style;
    style.setProperty('--theme-primary', theme.colors.primary);
    style.setProperty('--theme-secondary', theme.colors.secondary);
    style.setProperty('--theme-background', theme.colors.background);
    style.setProperty('--theme-surface', theme.colors.surface);
    style.setProperty('--theme-text', theme.colors.text);
    style.setProperty('--theme-accent', theme.colors.accent);
    
  }, [theme]);

  const value: ThemeContextType = {
    theme,
    themeId,
    setTheme,
    themes
  };

  return (
    <ThemeContext.Provider value={value}>
      <div className={`theme-${themeId} ${theme.background} ${theme.text} transition-all duration-500`}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
};