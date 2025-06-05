import React, { createContext, useContext, useState, useEffect } from 'react';
import { useSocket } from './SocketContext';

interface Conversation {
  id: string;
  pageContext: string;
  messages: Message[];
  createdAt: string;
  lastActive: string;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: any;
}

interface MemoryContextType {
  userId: string;
  currentConversation: string | null;
  conversations: Conversation[];
  currentMessages: Message[];
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  loadConversation: (conversationId: string) => void;
  createNewConversation: (pageContext: string) => string;
  getConversationsForPage: (pageContext: string) => Conversation[];
  clearCurrentConversation: () => void;
}

const MemoryContext = createContext<MemoryContextType | undefined>(undefined);

export const useMemory = () => {
  const context = useContext(MemoryContext);
  if (!context) {
    throw new Error('useMemory must be used within a MemoryProvider');
  }
  return context;
};

interface MemoryProviderProps {
  children: React.ReactNode;
}

export const MemoryProvider: React.FC<MemoryProviderProps> = ({ children }) => {
  const { socket } = useSocket();
  const [userId] = useState(() => {
    // Get or create user ID
    let id = localStorage.getItem('podplay-sanctuary-user-id');
    if (!id) {
      id = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('podplay-sanctuary-user-id', id);
    }
    return id;
  });

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversation, setCurrentConversation] = useState<string | null>(null);
  const [currentMessages, setCurrentMessages] = useState<Message[]>([]);

  // Load conversations from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(`podplay-sanctuary-conversations-${userId}`);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setConversations(parsed);
      } catch (error) {
        console.error('Failed to load conversations:', error);
      }
    }
  }, [userId]);

  // Save conversations to localStorage when they change
  useEffect(() => {
    if (conversations.length > 0) {
      localStorage.setItem(
        `podplay-sanctuary-conversations-${userId}`,
        JSON.stringify(conversations)
      );
    }
  }, [conversations, userId]);

  // Update current messages when conversation changes
  useEffect(() => {
    if (currentConversation) {
      const conversation = conversations.find(c => c.id === currentConversation);
      setCurrentMessages(conversation?.messages || []);
    } else {
      setCurrentMessages([]);
    }
  }, [currentConversation, conversations]);

  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString()
    };

    if (currentConversation) {
      setConversations(prev => prev.map(conv => {
        if (conv.id === currentConversation) {
          return {
            ...conv,
            messages: [...conv.messages, newMessage],
            lastActive: new Date().toISOString()
          };
        }
        return conv;
      }));
    }
  };

  const createNewConversation = (pageContext: string): string => {
    const newConversation: Conversation = {
      id: `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      pageContext,
      messages: [],
      createdAt: new Date().toISOString(),
      lastActive: new Date().toISOString()
    };

    setConversations(prev => [newConversation, ...prev]);
    setCurrentConversation(newConversation.id);
    
    return newConversation.id;
  };

  const loadConversation = (conversationId: string) => {
    const conversation = conversations.find(c => c.id === conversationId);
    if (conversation) {
      setCurrentConversation(conversationId);
      
      // Update last active
      setConversations(prev => prev.map(conv => {
        if (conv.id === conversationId) {
          return {
            ...conv,
            lastActive: new Date().toISOString()
          };
        }
        return conv;
      }));
    }
  };

  const getConversationsForPage = (pageContext: string): Conversation[] => {
    return conversations
      .filter(conv => conv.pageContext === pageContext)
      .sort((a, b) => new Date(b.lastActive).getTime() - new Date(a.lastActive).getTime())
      .slice(0, 10); // Limit to 10 most recent
  };

  const clearCurrentConversation = () => {
    setCurrentConversation(null);
    setCurrentMessages([]);
  };

  const value: MemoryContextType = {
    userId,
    currentConversation,
    conversations,
    currentMessages,
    addMessage,
    loadConversation,
    createNewConversation,
    getConversationsForPage,
    clearCurrentConversation
  };

  return (
    <MemoryContext.Provider value={value}>
      {children}
    </MemoryContext.Provider>
  );
};