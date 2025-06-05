// Navigation.tsx
// Top navigation for Podplay Sanctuary, links to all core pages
import * as React from 'react';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Typography from '@mui/joy/Typography';

const pages = [
  { path: '/sanctuary', label: 'Sanctuary Home' },
  { path: '/mainchat', label: 'Main Chat' },
  { path: '/workspace', label: 'Workspace' },
  { path: '/marketplace', label: 'Marketplace' },
  { path: '/memory', label: 'Memory Browser' },
  { path: '/settings', label: 'Settings' },
  { path: '/mission', label: 'Mission Control' },
];

export interface NavigationProps {
  onThemeChange?: (mode: 'sky' | 'neon' | 'stellar') => void;
  currentTheme?: 'sky' | 'neon' | 'stellar';
}

export const Navigation: React.FC<NavigationProps> = () => {
  // For demo, use window.location (replace with router as needed)
  const goto = (path: string) => {
    window.location.pathname = path;
  };
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 2, background: 'rgba(255,255,255,0.85)', borderBottom: '1px solid #eee', zIndex: 10 }}>
      <Typography level="h4" sx={{ fontFamily: 'Inter', fontWeight: 900, mr: 3, color: '#BE185D' }}>🐻 Sanctuary</Typography>
      {pages.map(page => (
        <Button key={page.path} onClick={() => goto(page.path)} size="sm" variant="plain" sx={{ fontWeight: 700 }}>{page.label}</Button>
      ))}
    </Box>
  );
};

export default Navigation;
