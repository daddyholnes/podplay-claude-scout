import React, { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Palette, Check } from 'lucide-react';
import { Button } from './ui/button';

export default function ThemeSelector() {
  const { theme, themeId, setTheme, themes } = useTheme();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Theme selector button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className={`
          ${theme.button} 
          rounded-full w-12 h-12 p-0 shadow-xl transition-all duration-300
          ${isOpen ? 'rotate-180' : 'hover:scale-110'}
        `}
        title="Change Theme"
      >
        <Palette className="w-5 h-5" />
      </Button>

      {/* Theme options */}
      {isOpen && (
        <div 
          className={`
            absolute bottom-16 right-0 ${theme.card} rounded-xl p-4 shadow-2xl border
            transform transition-all duration-300 ease-out
            ${isOpen ? 'scale-100 opacity-100' : 'scale-95 opacity-0'}
          `}
          style={{ minWidth: '280px' }}
        >
          <div className="text-sm font-medium mb-3 opacity-75">
            Choose Your Sanctuary
          </div>
          
          <div className="space-y-2">
            {Object.entries(themes).map(([id, themeOption]) => (
              <button
                key={id}
                onClick={() => {
                  setTheme(id as keyof typeof themes);
                  setIsOpen(false);
                }}
                className={`
                  w-full p-3 rounded-lg text-left transition-all duration-200
                  ${themeId === id 
                    ? 'ring-2 ring-current ring-opacity-50 bg-current bg-opacity-10' 
                    : 'hover:bg-current hover:bg-opacity-5'
                  }
                `}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">{themeOption.name}</div>
                    <div className="text-xs opacity-75 mt-1">
                      {id === 'light' && '☁️ Floating clouds, peaceful blue tones'}
                      {id === 'purple' && '✨ Neon effects, energetic purple gradients'}
                      {id === 'dark' && '⭐ Twinkling stars, professional elegance'}
                    </div>
                  </div>
                  
                  {themeId === id && (
                    <Check className="w-4 h-4 text-current" />
                  )}
                </div>
                
                {/* Theme preview */}
                <div className="flex space-x-1 mt-2">
                  <div 
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: themeOption.colors.primary }}
                  />
                  <div 
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: themeOption.colors.secondary }}
                  />
                  <div 
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: themeOption.colors.accent }}
                  />
                </div>
              </button>
            ))}
          </div>
          
          <div className="mt-4 pt-3 border-t border-current border-opacity-20">
            <div className="text-xs opacity-50">
              🐻 Mama Bear adapts to your chosen sanctuary
            </div>
          </div>
        </div>
      )}
      
      {/* Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-20 backdrop-blur-sm -z-10"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
}