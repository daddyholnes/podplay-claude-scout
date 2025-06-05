// MultiModalChatBar.tsx
// Global chat bar: audio, video, file/image, emoji, Mem0, transcription
import * as React from 'react';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Input from '@mui/joy/Input';
import IconButton from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';

export interface MultiModalChatBarProps {
  onSend: (payload: { text?: string; file?: File; audioBlob?: Blob; videoBlob?: Blob; image?: File; emoji?: string }) => void;
  isRecording?: boolean;
  isTranscribing?: boolean;
}

export const MultiModalChatBar: React.FC<MultiModalChatBarProps> = ({ onSend, isRecording, isTranscribing }) => {
  const [input, setInput] = React.useState('');
  const fileRef = React.useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (input.trim()) onSend({ text: input });
    setInput('');
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 1, background: 'rgba(255,255,255,0.93)', borderRadius: 2, boxShadow: '0 2px 8px rgba(30,64,175,0.06)' }}>
      {/* Audio Recording */}
      <IconButton size="sm" color={isRecording ? 'danger' : 'primary'} variant="soft" aria-label="Record Audio">
        🎤
      </IconButton>
      {/* Video Recording */}
      <IconButton size="sm" color="primary" variant="soft" aria-label="Record Video">
        📹
      </IconButton>
      {/* File/Image Upload */}
      <IconButton size="sm" color="primary" variant="soft" aria-label="Upload File" onClick={() => fileRef.current?.click()}>
        📎
      </IconButton>
      <input type="file" hidden ref={fileRef} onChange={e => e.target.files && onSend({ file: e.target.files[0] })} />
      {/* Emoji Picker */}
      <IconButton size="sm" color="primary" variant="soft" aria-label="Emoji Picker">
        😊
      </IconButton>
      {/* Text Input */}
      <Input value={input} onChange={e => setInput(e.target.value)} placeholder="Type a message or paste an image…" sx={{ flex: 1 }} />
      <Button size="sm" color="primary" onClick={handleSend} disabled={!input.trim()}>Send</Button>
      {/* Transcription indicator */}
      {isTranscribing && <Typography sx={{ ml: 2, color: '#BE185D' }}>Transcribing…</Typography>}
    </Box>
  );
};

export default MultiModalChatBar;
