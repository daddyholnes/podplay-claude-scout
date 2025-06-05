// ThemeSelector.tsx
// Theme mode selector for Sanctuary (Sky, Neon, Stellar)
import * as React from 'react';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';

export interface ThemeSelectorProps {
  currentTheme: 'sky' | 'neon' | 'stellar';
  onThemeChange: (mode: 'sky' | 'neon' | 'stellar') => void;
}

const themeOptions = [
  { mode: 'sky', label: '🌤️ Sky' },
  { mode: 'neon', label: '🌌 Neon' },
  { mode: 'stellar', label: '⭐ Stellar' },
];

export const ThemeSelector: React.FC<ThemeSelectorProps> = ({ currentTheme, onThemeChange }) => (
  <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', ml: 2 }}>
    {themeOptions.map(opt => (
      <Button
        key={opt.mode}
        size="sm"
        variant={currentTheme === opt.mode ? 'solid' : 'outlined'}
        color="primary"
        onClick={() => onThemeChange(opt.mode as 'sky' | 'neon' | 'stellar')}
        sx={{ fontWeight: 700, minWidth: 64 }}
      >
        {opt.label}
      </Button>
    ))}
  </Box>
);

export default ThemeSelector;
