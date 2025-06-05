import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import MultiModalChatBar from '../MultiModalChatBar';

describe('MultiModalChatBar', () => {
  it('renders input and send button', () => {
    render(<MultiModalChatBar onSend={() => {}} />);
    expect(screen.getByPlaceholderText(/type a message/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument();
  });
});
