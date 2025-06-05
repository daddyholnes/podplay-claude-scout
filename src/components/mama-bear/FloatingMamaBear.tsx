// FloatingMamaBear.tsx
// Floating, context-aware Mama Bear assistant (foundation)
import * as React from 'react';
import Sheet from '@mui/joy/Sheet';
import Box from '@mui/joy/Box';
import IconButton from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';
import '@fontsource/inter';

export interface FloatingMamaBearProps {
  mood?: 'welcoming' | 'attentive' | 'thinking' | 'helpful';
  onExpand?: () => void;
  hasInsights?: boolean;
  isThinking?: boolean;
}

export const FloatingMamaBear: React.FC<FloatingMamaBearProps> = ({
  mood = 'attentive',
  onExpand,
  hasInsights = false,
  isThinking = false,
}) => {
  return (
    <Sheet
      sx={{
        position: 'fixed',
        bottom: 32,
        right: 32,
        zIndex: 1500,
        p: 2,
        borderRadius: '50%',
        boxShadow: hasInsights ? '0 0 24px 8px #EC4899' : '0 4px 24px rgba(0,0,0,0.18)',
        background: 'var(--sanctuary-surface, #fff)',
        transition: 'box-shadow 0.3s',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: 72,
        height: 72,
      }}
      onClick={onExpand}
      aria-label="Open Mama Bear Chat"
    >
      {/* Mama Bear Avatar/Icon */}
      <Box
        sx={{
          width: 48,
          height: 48,
          borderRadius: '50%',
          background: mood === 'welcoming' ? 'linear-gradient(135deg,#E0F2FE,#DBEAFE)' :
            mood === 'thinking' ? 'linear-gradient(135deg,#581C87,#BE185D)' :
            mood === 'helpful' ? 'linear-gradient(135deg,#6B21A8,#F59E0B)' :
            'linear-gradient(135deg,#EC4899,#1E3A8A)',
          boxShadow: isThinking ? '0 0 16px 6px #BE185D' : undefined,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'background 0.5s, box-shadow 0.3s',
        }}
      >
        <Typography level="h2" sx={{ color: '#fff', fontWeight: 900, fontFamily: 'Inter' }}>
          🐻
        </Typography>
      </Box>
    </Sheet>
  );
};

export default FloatingMamaBear;
