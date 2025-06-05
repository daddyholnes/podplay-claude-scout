// Settings.tsx
// Sanctuary Settings page with agentic overlays and unified MultiModalChatBar
import * as React from 'react';
import SanctuaryLayout from '@/components/layout/SanctuaryLayout';
import FloatingMamaBear from '@/components/mama-bear/FloatingMamaBear';
import ContextContinuity from '@/components/mama-bear/ContextContinuity';
import MultiModalChatBar from '@/components/MultiModalChatBar';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';

export const Settings: React.FC = () => {
  const [messages, setMessages] = React.useState<any[]>([]);
  const handleSend = (payload: any) => {
    if (payload.text) setMessages(msgs => [...msgs, { role: 'user', content: payload.text }]);
    if (payload.audioBlob) setMessages(msgs => [...msgs, { role: 'user', content: '[Audio message]' }]);
    if (payload.videoBlob) setMessages(msgs => [...msgs, { role: 'user', content: '[Video message]' }]);
    if (payload.file) setMessages(msgs => [...msgs, { role: 'user', content: `[File: ${payload.file.name}]` }]);
    if (payload.emoji) setMessages(msgs => [...msgs, { role: 'user', content: `[Emoji: ${payload.emoji}]` }]);
  };

  return (
    <SanctuaryLayout>
      <Box sx={{ pt: 8, pb: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '90vh' }}>
        <Typography level="h3" sx={{ mb: 2, fontWeight: 800 }}>Settings</Typography>
        <Box sx={{ width: 680, minHeight: 100, background: 'rgba(236,72,153,0.07)', borderRadius: 3, mb: 4, p: 2 }}>
          {/* Settings content here */}
        </Box>
        <Box sx={{ width: 680, mb: 3 }}>
          <MultiModalChatBar onSend={handleSend} />
        </Box>
        <Box sx={{ width: 680, mb: 3 }}>
          <ContextContinuity />
        </Box>
        <FloatingMamaBear mood="attentive" />
      </Box>
    </SanctuaryLayout>
  );
};

export default Settings;
