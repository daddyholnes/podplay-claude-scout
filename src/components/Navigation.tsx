import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';
import { 
  MessageCircle, 
  Server, 
  Bot, 
  Brain, 
  Puzzle, 
  Link as LinkIcon, 
  Radio,
  Sparkles
} from 'lucide-react';

const navigation = [
  {
    name: 'Research Chat',
    href: '/',
    icon: MessageCircle,
    description: '🐻 Research Specialist',
    shortcut: '1'
  },
  {
    name: 'VM Hub',
    href: '/vm-hub',
    icon: Server,
    description: '🐻 DevOps Specialist',
    shortcut: '2'
  },
  {
    name: 'Scout Agent',
    href: '/scout',
    icon: Bot,
    description: '🐻 Scout Commander',
    shortcut: '3'
  },
  {
    name: 'AI Models',
    href: '/models',
    icon: Brain,
    description: '🐻 Model Coordinator',
    shortcut: '4'
  },
  {
    name: 'MCP Tools',
    href: '/mcp',
    icon: Puzzle,
    description: '🐻 Tool Curator',
    shortcut: '5'
  },
  {
    name: 'Integrations',
    href: '/integrations',
    icon: LinkIcon,
    description: '🐻 Integration Architect',
    shortcut: '6'
  },
  {
    name: 'Live API',
    href: '/live-api',
    icon: Radio,
    description: '🐻 Live API Specialist',
    shortcut: '7'
  }
];

export default function Navigation() {
  const { theme } = useTheme();
  const location = useLocation();

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 ${theme.card} border-b transition-all duration-300`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link 
            to="/" 
            className={`flex items-center space-x-2 ${theme.text} hover:${theme.accent} transition-colors`}
          >
            <Sparkles className="w-8 h-8" />
            <div>
              <div className="font-serif text-xl font-bold">Podplay Sanctuary</div>
              <div className="text-xs opacity-75">with Mama Bear AI</div>
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    group relative flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200
                    ${isActive 
                      ? `${theme.button} shadow-lg` 
                      : `${theme.text} hover:${theme.accent} hover:bg-opacity-10 hover:bg-current`
                    }
                  `}
                  title={`${item.description} (Alt+${item.shortcut})`}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  <span className="hidden lg:block">{item.name}</span>
                  
                  {/* Keyboard shortcut indicator */}
                  <span className="hidden xl:block ml-2 text-xs opacity-50">
                    ⌥{item.shortcut}
                  </span>
                  
                  {/* Tooltip for smaller screens */}
                  <div className="lg:hidden absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-black text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap">
                    {item.description}
                  </div>
                </Link>
              );
            })}
          </div>

          {/* Mobile menu placeholder */}
          <div className="md:hidden">
            <button 
              className={`${theme.text} hover:${theme.accent} p-2 rounded-lg transition-colors`}
              aria-label="Menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}