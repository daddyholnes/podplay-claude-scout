// LiveAPIStudio.tsx
// Sanctuary Live API Studio: Gemini live experimentation with voice/video and agentic overlay
import * as React from 'react';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Sheet from '@mui/joy/Sheet';
import Button from '@mui/joy/Button';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import SanctuaryLayout from '@/components/layout/SanctuaryLayout';
import FloatingMamaBear from '@/components/mama-bear/FloatingMamaBear';
import MultiModalChatBar from '@/components/MultiModalChatBar';

const MODELS = [
  { value: 'gemini-2.5-flash-preview-native-audio-dialog', label: 'Gemini 2.5 Flash Preview (Audio Dialog)' },
  { value: 'gemini-2.5-flash-exp-native-audio-thinking-dialog', label: 'Gemini 2.5 Flash Exp (Thinking Dialog)' },
  { value: 'gemini-2.0-flash-live-001', label: 'Gemini 2.0 Flash Live' },
];

export const LiveAPIStudio: React.FC = () => {
  const [model, setModel] = React.useState(MODELS[0].value);
  const [isLive, setIsLive] = React.useState(false);
  const [functionCalls, setFunctionCalls] = React.useState<any[]>([]);
  const [transcript, setTranscript] = React.useState<string[]>([]);

  // Mock Gemini API call
  const handleSend = (payload: any) => {
    // Simulate function call and transcript update
    if (payload.text) {
      setTranscript(t => [...t, `You: ${payload.text}`]);
      setTimeout(() => {
        setTranscript(t => [...t, `Gemini: (mock response to "${payload.text}")`]);
        setFunctionCalls(fc => [...fc, { fn: 'mockFunction', args: [payload.text], time: new Date().toLocaleTimeString() }]);
      }, 800);
    }
    if (payload.audioBlob) {
      setTranscript(t => [...t, 'You sent an audio message.']);
    }
    if (payload.videoBlob) {
      setTranscript(t => [...t, 'You sent a video message.']);
    }
    if (payload.file) {
      setTranscript(t => [...t, `You uploaded file: ${payload.file.name}`]);
    }
    if (payload.emoji) {
      setTranscript(t => [...t, `You sent emoji: ${payload.emoji}`]);
    }
  };

  return (
    <SanctuaryLayout>
      <Box sx={{ pt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '90vh' }}>
        <Typography level="h3" sx={{ mb: 2, fontWeight: 800, fontFamily: 'Inter' }}>🎙️ Live API Studio</Typography>
        <Typography sx={{ mb: 4, color: '#888', fontSize: 18 }}>Experiment with Gemini Live APIs, audio/video, and function calling in real time.</Typography>
        <Sheet sx={{ p: 4, borderRadius: 3, minWidth: 420, background: 'rgba(255,255,255,0.98)', boxShadow: '0 2px 16px rgba(30,64,175,0.10)', mb: 4 }}>
          <Box sx={{ mb: 3 }}>
            <Typography level="h5" sx={{ mb: 1 }}>Model Selection</Typography>
            <Select value={model} onChange={(_, v) => setModel(v || MODELS[0].value)} sx={{ width: 340 }}>
              {MODELS.map((m) => (
                <Option key={m.value} value={m.value}>{m.label}</Option>
              ))}
            </Select>
          </Box>
          <Box sx={{ mb: 3 }}>
            <Typography level="h5" sx={{ mb: 1 }}>Voice/Audio Options</Typography>
            <Button size="sm" variant="outlined" color="primary" sx={{ mr: 2 }}>Configure Voice</Button>
            <Button size="sm" variant="outlined" color="primary">Audio Settings</Button>
          </Box>
          <Box sx={{ mb: 3 }}>
            <Typography level="h5" sx={{ mb: 1 }}>Video/Screen Sharing</Typography>
            <Button size="sm" variant="outlined" color="primary" sx={{ mr: 2 }}>Enable Webcam</Button>
            <Button size="sm" variant="outlined" color="primary">Share Screen</Button>
          </Box>
          <Box sx={{ mb: 3 }}>
            <Typography level="h5" sx={{ mb: 1 }}>Session Controls</Typography>
            <Button onClick={() => setIsLive(!isLive)} color={isLive ? 'danger' : 'success'}>
              {isLive ? 'Stop Live Session' : 'Start Live Session'}
            </Button>
          </Box>
        </Sheet>
        {/* Video preview area, waveform, transcript, function call logger */}
        <Box sx={{ width: 640, minHeight: 220, background: 'rgba(236,72,153,0.09)', borderRadius: 3, mb: 4, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#BE185D', fontWeight: 700, fontSize: 22 }}>
          {isLive ? '🔴 Live Session Running (video/audio preview here)' : 'Video/audio preview will appear here'}
        </Box>
        <Box sx={{ display: 'flex', gap: 3, width: 640 }}>
          <Sheet sx={{ flex: 1, p: 2, borderRadius: 2, minHeight: 120, background: '#fff', overflowY: 'auto', maxHeight: 200 }}>
            <Typography level="h6">Transcript</Typography>
            <Box sx={{ color: '#888', fontSize: 14 }}>
              {transcript.length === 0 ? 'Live transcription will appear here…' : transcript.map((line, i) => <div key={i}>{line}</div>)}
            </Box>
          </Sheet>
          <Sheet sx={{ flex: 1, p: 2, borderRadius: 2, minHeight: 120, background: '#fff', overflowY: 'auto', maxHeight: 200 }}>
            <Typography level="h6">Function Call Logger</Typography>
            <Box sx={{ color: '#888', fontSize: 14 }}>
              {functionCalls.length === 0 ? 'Function calls will be logged here…' : functionCalls.map((fc, i) => <div key={i}>{fc.time}: {fc.fn}({fc.args.join(', ')})</div>)}
            </Box>
          </Sheet>
        </Box>
        <Box sx={{ width: 640, mt: 4 }}>
          <MultiModalChatBar onSend={handleSend} />
        </Box>
        {/* Mama Bear Live API Specialist overlay (always available) */}
        <FloatingMamaBear mood="helpful" />
      </Box>
    </SanctuaryLayout>
  );
};

export default LiveAPIStudio;
