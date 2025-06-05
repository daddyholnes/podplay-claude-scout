// WorkspaceView.tsx
// Sanctuary WorkspaceView with agentic overlays and unified MultiModalChatBar
import * as React from 'react';
import SanctuaryLayout from '@/components/layout/SanctuaryLayout';
import FloatingMamaBear from '@/components/mama-bear/FloatingMamaBear';
import SequentialThinking from '@/components/mama-bear/SequentialThinking';
import ContextContinuity from '@/components/mama-bear/ContextContinuity';
import MultiModalChatBar from '@/components/MultiModalChatBar';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';

export const WorkspaceView: React.FC = () => {
  const [messages, setMessages] = React.useState<any[]>([]);
  const handleSend = (payload: any) => {
    // Demo: append message and mock agentic response
    if (payload.text) {
      setMessages(msgs => [...msgs, { role: 'user', content: payload.text }]);
      setTimeout(() => setMessages(msgs => [...msgs, { role: 'agent', content: `Mama Bear: (mock reply to "${payload.text}")` }]), 800);
    }
    if (payload.audioBlob) setMessages(msgs => [...msgs, { role: 'user', content: '[Audio message]' }]);
    if (payload.videoBlob) setMessages(msgs => [...msgs, { role: 'user', content: '[Video message]' }]);
    if (payload.file) setMessages(msgs => [...msgs, { role: 'user', content: `[File: ${payload.file.name}]` }]);
    if (payload.emoji) setMessages(msgs => [...msgs, { role: 'user', content: `[Emoji: ${payload.emoji}]` }]);
  };

  return (
    <SanctuaryLayout>
      <Box sx={{ pt: 8, pb: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '90vh' }}>
        <Typography level="h3" sx={{ mb: 2, fontWeight: 800 }}>Workspace View</Typography>
        <Box sx={{ width: 680, minHeight: 320, background: 'rgba(236,72,153,0.07)', borderRadius: 3, mb: 4, p: 2 }}>
          {messages.length === 0 ? (
            <Typography sx={{ color: '#888', fontSize: 16 }}>Start a workspace conversation…</Typography>
          ) : (
            messages.map((msg, i) => (
              <Box key={i} sx={{ mb: 2, textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                <Typography sx={{ fontWeight: msg.role === 'user' ? 600 : 500, color: msg.role === 'user' ? '#334155' : '#BE185D' }}>{msg.content}</Typography>
              </Box>
            ))
          )}
        </Box>
        <Box sx={{ width: 680, mb: 3 }}>
          <MultiModalChatBar onSend={handleSend} />
        </Box>
        <Box sx={{ width: 680, display: 'flex', gap: 2, mb: 3 }}>
          <SequentialThinking />
          <ContextContinuity />
        </Box>
        <FloatingMamaBear mood="attentive" />
      </Box>
    </SanctuaryLayout>
  );
};

export default WorkspaceView;
