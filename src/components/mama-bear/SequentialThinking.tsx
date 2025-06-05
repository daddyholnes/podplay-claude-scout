// SequentialThinking.tsx
// Visualizes Mama Bear's thought process in real-time (foundation)
import * as React from 'react';
import Sheet from '@mui/joy/Sheet';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';

export interface SequentialThinkingProps {
  steps: Array<{ stage: string; icon: string; text: string; status: 'completed' | 'active' | 'pending'; }>;
  visible?: boolean;
}

export const SequentialThinking: React.FC<SequentialThinkingProps> = ({ steps, visible = false }) => {
  if (!visible) return null;
  return (
    <Sheet sx={{ position: 'fixed', bottom: 120, right: 32, zIndex: 1501, p: 2, borderRadius: 2, minWidth: 260, boxShadow: '0 4px 24px rgba(0,0,0,0.16)', background: 'var(--sanctuary-surface, #fff)' }}>
      <Typography level="h5" sx={{ fontFamily: 'Inter', mb: 1 }}>Mama Bear is thinking…</Typography>
      <Box>
        {steps.map((step, idx) => (
          <Box key={step.stage} sx={{ display: 'flex', alignItems: 'center', mb: 0.5, opacity: step.status === 'pending' ? 0.5 : 1 }}>
            <span style={{ fontSize: 22, marginRight: 8 }}>{step.icon}</span>
            <Typography sx={{ fontFamily: 'Inter', fontWeight: step.status === 'active' ? 700 : 400 }}>{step.text}</Typography>
            {step.status === 'active' && <span style={{ marginLeft: 8, color: '#EC4899' }}>•</span>}
            {step.status === 'completed' && <span style={{ marginLeft: 8, color: '#10B981' }}>✓</span>}
          </Box>
        ))}
      </Box>
    </Sheet>
  );
};

export default SequentialThinking;
