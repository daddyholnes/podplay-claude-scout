// AnimatedSanctuaryBackground.tsx
// Animated background for Sanctuary layout, theme-aware
import * as React from 'react';
import Box from '@mui/joy/Box';

export interface AnimatedSanctuaryBackgroundProps {
  themeMode: 'sky' | 'neon' | 'stellar';
}

export const AnimatedSanctuaryBackground: React.FC<AnimatedSanctuaryBackgroundProps> = ({ themeMode }) => {
  // Theme-specific backgrounds
  const bg =
    themeMode === 'sky'
      ? 'linear-gradient(135deg, #E0F2FE 0%, #DBEAFE 100%)'
      : themeMode === 'neon'
      ? 'linear-gradient(135deg, #581C87 0%, #BE185D 50%, #1E3A8A 100%)'
      : 'radial-gradient(circle at 20% 30%, #eee 2px, transparent 1%), radial-gradient(circle at 40% 70%, rgba(255,255,255,0.5) 2px, transparent 1%), #0A0A0A';
  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 0,
        background: bg,
        opacity: 0.96,
        pointerEvents: 'none',
        transition: 'background 0.8s cubic-bezier(0.4,0,0.2,1)',
      }}
    />
  );
};

export default AnimatedSanctuaryBackground;
