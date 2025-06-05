// ContextContinuity.tsx
// Maintains conversation thread across pages (foundation)
import * as React from 'react';
import Sheet from '@mui/joy/Sheet';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';

export interface ContextContinuityProps {
  threadTitle: string;
  messages: Array<{ sender: string; text: string; timestamp: string }>;
  onContinue?: () => void;
}

export const ContextContinuity: React.FC<ContextContinuityProps> = ({ threadTitle, messages, onContinue }) => {
  return (
    <Sheet sx={{ p: 2, borderRadius: 2, boxShadow: '0 4px 24px rgba(0,0,0,0.14)', background: 'var(--sanctuary-surface, #fff)', maxWidth: 340 }}>
      <Typography level="h6" sx={{ fontFamily: 'Inter', mb: 1 }}>{threadTitle}</Typography>
      <Box sx={{ maxHeight: 120, overflowY: 'auto', mb: 1 }}>
        {messages.map((msg, idx) => (
          <Box key={idx} sx={{ mb: 0.5, display: 'flex', alignItems: 'flex-start' }}>
            <Typography sx={{ fontWeight: 700, color: msg.sender === 'mama-bear' ? '#EC4899' : '#1E40AF', mr: 1 }}>{msg.sender === 'mama-bear' ? '🐻' : 'You'}</Typography>
            <Typography sx={{ fontFamily: 'Inter', fontSize: 14 }}>{msg.text}</Typography>
            <Typography sx={{ fontSize: 12, color: '#888', ml: 1 }}>{msg.timestamp}</Typography>
          </Box>
        ))}
      </Box>
      {onContinue && <button onClick={onContinue} style={{ background: '#EC4899', color: '#fff', border: 'none', borderRadius: 6, padding: '6px 16px', fontWeight: 600, cursor: 'pointer' }}>Continue Conversation</button>}
    </Sheet>
  );
};

export default ContextContinuity;
