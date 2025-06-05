// MiniApps.tsx
// Podplay Sanctuary Mini-Apps: grid of embedded AI tool webviews with logos and agentic overlay
import * as React from 'react';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Sheet from '@mui/joy/Sheet';
import SanctuaryLayout from '@/components/layout/SanctuaryLayout';
import FloatingMamaBear from '@/components/mama-bear/FloatingMamaBear';

const MINI_APPS = [
  { name: 'Scout', url: 'https://scout.new/', logo: '🧭' },
  { name: 'NotebookLM', url: 'https://notebooklm.google/', logo: '📒' },
  { name: 'Grok', url: 'https://grok.com/', logo: '🤖' },
  { name: 'ChatGPT', url: 'https://chat.openai.com/', logo: '⚪' },
  { name: 'Jules', url: 'https://jules.google.com', logo: '🧑‍💼' },
  { name: 'AI Studio', url: 'https://aistudio.google.com/prompts/new_chat?lfhs=2', logo: '🎨' },
  { name: 'Perplexity', url: 'https://www.perplexity.ai/', logo: '🌀' },
  { name: 'GitHub', url: 'https://github.com/', logo: '🐙' },
  { name: 'Firebase Studio', url: 'https://firebase.studio/', logo: '🔥' },
  { name: 'Mem0', url: 'https://mem0.ai/', logo: '🧠' },
  { name: 'Claude', url: 'https://claude.ai/', logo: '🟣' },
  { name: 'GCP', url: 'https://cloud.google.com/gcp', logo: '☁️' },
  { name: 'Gemini', url: 'https://gemini.google.com/', logo: '🔷' },
];

export const MiniApps: React.FC = () => {
  return (
    <SanctuaryLayout>
      <Box sx={{ pt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '90vh' }}>
        <Typography level="h3" sx={{ mb: 3, fontWeight: 800, fontFamily: 'Inter' }}>Mini-Apps</Typography>
        <Typography sx={{ mb: 4, color: '#888', fontSize: 18 }}>Quick access to your favorite AI tools in secure webviews.</Typography>
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 4, width: '100%', maxWidth: 1100 }}>
          {MINI_APPS.map(app => (
            <Sheet key={app.name} sx={{ p: 2, borderRadius: 3, background: 'rgba(255,255,255,0.98)', boxShadow: '0 2px 16px rgba(30,64,175,0.10)', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <Box sx={{ fontSize: 40, mb: 1 }}>{app.logo}</Box>
              <Typography level="h5" sx={{ mb: 1 }}>{app.name}</Typography>
              <Box sx={{ width: '100%', height: 320, borderRadius: 2, overflow: 'hidden', border: '1px solid #eee', mb: 1 }}>
                <iframe src={app.url} title={app.name} width="100%" height="100%" style={{ border: 'none' }} sandbox="allow-scripts allow-same-origin allow-forms" />
              </Box>
            </Sheet>
          ))}
        </Box>
        {/* Agentic overlay always available */}
        <FloatingMamaBear mood="attentive" />
      </Box>
    </SanctuaryLayout>
  );
};

export default MiniApps;
