import React, { useState, useRef, useEffect } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { useSocket } from '../contexts/SocketContext';
import { useMemory } from '../contexts/MemoryContext';
import { 
  Send, 
  Paperclip, 
  Image, 
  Mic, 
  Video,
  Search,
  FileText,
  Globe,
  Brain,
  Plus
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Card } from '../components/ui/card';

export default function MainChat() {
  const { theme } = useTheme();
  const { emit, on, off, connected } = useSocket();
  const { userId, currentMessages, addMessage, createNewConversation, getConversationsForPage } = useMemory();
  
  const [message, setMessage] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [attachments, setAttachments] = useState<File[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const conversations = getConversationsForPage('main_chat');

  // Research suggestions for the Research Specialist
  const suggestions = [
    "Research the latest developments in AI model architectures",
    "Analyze the differences between React and Vue.js for my project",
    "Find best practices for implementing microservices architecture",
    "Compare different cloud hosting providers for a startup",
    "Research accessibility guidelines for modern web applications"
  ];

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentMessages]);

  // Socket event listeners
  useEffect(() => {
    const handleResponse = (data: any) => {
      setIsThinking(false);
      addMessage({
        role: 'assistant',
        content: data.response || data.message,
        metadata: data.metadata
      });
      setShowSuggestions(false);
    };

    const handleThinking = (data: any) => {
      setIsThinking(data.thinking);
    };

    on('mama_bear_response', handleResponse);
    on('mama_bear_thinking', handleThinking);

    return () => {
      off('mama_bear_response', handleResponse);
      off('mama_bear_thinking', handleThinking);
    };
  }, [on, off, addMessage]);

  const sendMessage = async () => {
    if (!message.trim() && attachments.length === 0) return;

    // Add user message to conversation
    addMessage({
      role: 'user',
      content: message.trim(),
      metadata: {
        attachments: attachments.map(f => ({ name: f.name, size: f.size, type: f.type }))
      }
    });

    setIsThinking(true);
    setShowSuggestions(false);

    // Send to Mama Bear
    emit('mama_bear_message', {
      message: message.trim(),
      page_context: 'main_chat',
      user_id: userId,
      attachments: attachments
    });

    // Reset form
    setMessage('');
    setAttachments([]);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    setAttachments(prev => [...prev, ...files]);
  };

  const removeFiile = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  const startNewConversation = () => {
    createNewConversation('main_chat');
    setShowSuggestions(true);
  };

  return (
    <div className="pt-16 min-h-screen">
      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-8rem)]">
          
          {/* Conversation History Sidebar */}
          <div className={`${theme.card} rounded-xl p-4 space-y-4`}>
            <div className="flex items-center justify-between">
              <h2 className="font-semibold">Research Sessions</h2>
              <Button
                onClick={startNewConversation}
                size="sm"
                className={theme.button}
              >
                <Plus className="w-4 h-4" />
              </Button>
            </div>
            
            <div className="space-y-2">
              {conversations.slice(0, 10).map((conv) => (
                <button
                  key={conv.id}
                  className={`
                    w-full text-left p-3 rounded-lg transition-colors
                    hover:bg-current hover:bg-opacity-10
                  `}
                >
                  <div className="font-medium text-sm truncate">
                    {conv.messages[0]?.content || 'New Research Session'}
                  </div>
                  <div className="text-xs opacity-50 mt-1">
                    {new Date(conv.lastActive).toLocaleDateString()}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Main Chat Area */}
          <div className="lg:col-span-2 flex flex-col">
            <Card className={`${theme.card} flex-1 flex flex-col`}>
              {/* Header */}
              <div className="p-6 border-b border-current border-opacity-20">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <Brain className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h1 className="text-xl font-semibold">🐻 Research Specialist</h1>
                    <p className="text-sm opacity-75">
                      Curious, thorough research and information discovery
                    </p>
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 p-6 space-y-6 overflow-y-auto">
                {currentMessages.length === 0 && showSuggestions && (
                  <div className="space-y-6">
                    <div className="text-center py-8">
                      <div className="text-6xl mb-4">🐻</div>
                      <h2 className="text-2xl font-bold mb-2">Welcome to Research Central!</h2>
                      <p className="text-lg opacity-75 mb-6">
                        I'm your Research Specialist Mama Bear. I love diving deep into topics and discovering fascinating connections!
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {suggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          onClick={() => setMessage(suggestion)}
                          className={`
                            p-4 text-left rounded-xl border-2 border-dashed border-current border-opacity-20
                            hover:border-opacity-40 hover:bg-current hover:bg-opacity-5 transition-all
                          `}
                        >
                          <Search className="w-5 h-5 mb-2 opacity-60" />
                          <div className="text-sm">{suggestion}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                
                {currentMessages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`
                        max-w-2xl p-4 rounded-2xl
                        ${msg.role === 'user' 
                          ? `${theme.button} text-white` 
                          : `bg-current bg-opacity-10 ${theme.text}`
                        }
                      `}
                    >
                      <div className="whitespace-pre-wrap">{msg.content}</div>
                      {msg.metadata?.attachments && msg.metadata.attachments.length > 0 && (
                        <div className="mt-2 space-y-1">
                          {msg.metadata.attachments.map((att: any, i: number) => (
                            <div key={i} className="text-xs opacity-75 flex items-center space-x-1">
                              <FileText className="w-3 h-3" />
                              <span>{att.name}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {isThinking && (
                  <div className="flex justify-start">
                    <div className={`max-w-2xl p-4 rounded-2xl bg-current bg-opacity-10 ${theme.text}`}>
                      <div className="flex items-center space-x-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
                          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                        </div>
                        <span className="text-sm">Research Specialist is thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="p-6 border-t border-current border-opacity-20">
                {/* Attachments */}
                {attachments.length > 0 && (
                  <div className="mb-4 flex flex-wrap gap-2">
                    {attachments.map((file, index) => (
                      <div
                        key={index}
                        className="flex items-center space-x-2 bg-current bg-opacity-10 rounded-lg px-3 py-2 text-sm"
                      >
                        <FileText className="w-4 h-4" />
                        <span>{file.name}</span>
                        <button
                          onClick={() => removeFiile(index)}
                          className="text-red-500 hover:text-red-700"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}

                <div className="flex space-x-3">
                  <div className="flex-1">
                    <Textarea
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      onKeyDown={handleKeyPress}
                      placeholder="Ask me to research anything..."
                      className="resize-none"
                      rows={3}
                      disabled={isThinking}
                    />
                  </div>
                  
                  <div className="flex flex-col space-y-2">
                    <input
                      ref={fileInputRef}
                      type="file"
                      multiple
                      onChange={handleFileSelect}
                      className="hidden"
                      accept="image/*,.pdf,.doc,.docx,.txt"
                    />
                    
                    <Button
                      onClick={() => fileInputRef.current?.click()}
                      variant="outline"
                      size="sm"
                      title="Attach files"
                    >
                      <Paperclip className="w-4 h-4" />
                    </Button>
                    
                    <Button
                      onClick={sendMessage}
                      disabled={(!message.trim() && attachments.length === 0) || isThinking}
                      className={theme.button}
                    >
                      <Send className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
                
                <div className="text-xs opacity-50 mt-2">
                  🐻 Research Specialist • Press Enter to send, Shift+Enter for new line
                </div>
              </div>
            </Card>
          </div>

          {/* Research Tools Sidebar */}
          <div className={`${theme.card} rounded-xl p-4 space-y-4`}>
            <h3 className="font-semibold">Research Tools</h3>
            
            <div className="space-y-3">
              <button className="w-full p-3 text-left rounded-lg hover:bg-current hover:bg-opacity-10 transition-colors">
                <div className="flex items-center space-x-2">
                  <Globe className="w-4 h-4" />
                  <span className="text-sm">Web Search</span>
                </div>
                <div className="text-xs opacity-50 mt-1">Search the web for information</div>
              </button>
              
              <button className="w-full p-3 text-left rounded-lg hover:bg-current hover:bg-opacity-10 transition-colors">
                <div className="flex items-center space-x-2">
                  <FileText className="w-4 h-4" />
                  <span className="text-sm">Document Analysis</span>
                </div>
                <div className="text-xs opacity-50 mt-1">Analyze uploaded documents</div>
              </button>
              
              <button className="w-full p-3 text-left rounded-lg hover:bg-current hover:bg-opacity-10 transition-colors">
                <div className="flex items-center space-x-2">
                  <Brain className="w-4 h-4" />
                  <span className="text-sm">Deep Research</span>
                </div>
                <div className="text-xs opacity-50 mt-1">Multi-source investigation</div>
              </button>
            </div>
            
            <div className="pt-4 border-t border-current border-opacity-20">
              <div className="text-xs opacity-50">
                🐻 Research Specialist excels at finding patterns, verifying facts, and discovering connections across multiple sources.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}