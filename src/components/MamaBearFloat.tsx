import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';
import { useSocket } from '../contexts/SocketContext';
import { useMemory } from '../contexts/MemoryContext';
import { MessageCircle, X, Send, Minimize2, Maximize2 } from 'lucide-react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';

const mamaBearVariants = {
  '/': 'Research Specialist',
  '/chat': 'Research Specialist',
  '/vm-hub': 'DevOps Specialist',
  '/scout': 'Scout Commander',
  '/models': 'Model Coordinator',
  '/mcp': 'Tool Curator',
  '/integrations': 'Integration Architect',
  '/live-api': 'Live API Specialist'
};

export default function MamaBearFloat() {
  const { theme } = useTheme();
  const { emit, on, off, connected } = useSocket();
  const { userId } = useMemory();
  const location = useLocation();
  
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Array<{
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
  }>>([]);
  const [isThinking, setIsThinking] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const currentVariant = mamaBearVariants[location.pathname as keyof typeof mamaBearVariants] || 'Research Specialist';
  const pageContext = location.pathname.slice(1) || 'main_chat';

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Socket event listeners
  useEffect(() => {
    const handleResponse = (data: any) => {
      setIsThinking(false);
      if (data.success) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.response,
          timestamp: new Date().toISOString()
        }]);
      } else {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.message || '🐻 I had a small hiccup! Let me try again.',
          timestamp: new Date().toISOString()
        }]);
      }
    };

    const handleThinking = (data: any) => {
      setIsThinking(data.thinking);
    };

    const handleGreeting = (data: any) => {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.message,
        timestamp: new Date().toISOString()
      }]);
    };

    on('mama_bear_response', handleResponse);
    on('mama_bear_thinking', handleThinking);
    on('mama_bear_greeting', handleGreeting);

    return () => {
      off('mama_bear_response', handleResponse);
      off('mama_bear_thinking', handleThinking);
      off('mama_bear_greeting', handleGreeting);
    };
  }, [on, off]);

  // Join page room when location changes
  useEffect(() => {
    if (connected) {
      emit('join_page', {
        page_context: pageContext,
        user_id: userId
      });
    }
  }, [location.pathname, connected, emit, pageContext, userId]);

  const sendMessage = () => {
    if (!message.trim() || isThinking) return;

    const userMessage = {
      role: 'user' as const,
      content: message.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsThinking(true);

    emit('mama_bear_message', {
      message: message.trim(),
      page_context: pageContext,
      user_id: userId
    });

    setMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) {
    return (
      <div className="fixed bottom-4 left-4 z-50">
        <Button
          onClick={() => setIsOpen(true)}
          className={`
            ${theme.button} 
            rounded-full w-14 h-14 p-0 shadow-xl transition-all duration-300
            hover:scale-110 group
          `}
          title={`Chat with Mama Bear ${currentVariant}`}
        >
          <div className="relative">
            <MessageCircle className="w-6 h-6" />
            {connected && (
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse" />
            )}
          </div>
        </Button>
        
        {/* Floating greeting */}
        <div className={`
          absolute bottom-16 left-0 ${theme.card} rounded-lg p-3 shadow-lg max-w-64
          transform transition-all duration-300 opacity-0 group-hover:opacity-100
          pointer-events-none
        `}>
          <div className="text-sm font-medium">🐻 {currentVariant}</div>
          <div className="text-xs opacity-75 mt-1">
            Ready to help with {pageContext.replace('_', ' ')} tasks!
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 left-4 z-50">
      {/* Chat window */}
      <div 
        className={`
          ${theme.card} rounded-xl shadow-2xl border transition-all duration-300
          ${isMinimized ? 'w-80 h-16' : 'w-96 h-96'}
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-current border-opacity-20">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${connected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
            <div>
              <div className="text-sm font-medium">🐻 Mama Bear</div>
              <div className="text-xs opacity-75">{currentVariant}</div>
            </div>
          </div>
          
          <div className="flex items-center space-x-1">
            <Button
              onClick={() => setIsMinimized(!isMinimized)}
              variant="ghost"
              size="sm"
              className="w-8 h-8 p-0"
            >
              {isMinimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
            </Button>
            <Button
              onClick={() => setIsOpen(false)}
              variant="ghost"
              size="sm"
              className="w-8 h-8 p-0"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {!isMinimized && (
          <>
            {/* Messages */}
            <div className="flex-1 p-4 space-y-3 overflow-y-auto h-64">
              {messages.length === 0 && (
                <div className="text-center py-8 opacity-75">
                  <div className="text-4xl mb-2">🐻</div>
                  <div className="text-sm">
                    Hi! I'm your {currentVariant}.<br />
                    How can I help you today?
                  </div>
                </div>
              )}
              
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`
                      max-w-xs p-3 rounded-lg text-sm
                      ${msg.role === 'user' 
                        ? `${theme.button} text-white` 
                        : `bg-current bg-opacity-10 ${theme.text}`
                      }
                    `}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
              
              {isThinking && (
                <div className="flex justify-start">
                  <div className={`max-w-xs p-3 rounded-lg text-sm bg-current bg-opacity-10 ${theme.text}`}>
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-current border-opacity-20">
              <div className="flex space-x-2">
                <Textarea
                  ref={textareaRef}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={handleKeyPress}
                  placeholder={`Ask ${currentVariant} anything...`}
                  className="flex-1 resize-none"
                  rows={1}
                  disabled={isThinking}
                />
                <Button
                  onClick={sendMessage}
                  disabled={!message.trim() || isThinking}
                  size="sm"
                  className={theme.button}
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="text-xs opacity-50 mt-2">
                Press Enter to send, Shift+Enter for new line
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}