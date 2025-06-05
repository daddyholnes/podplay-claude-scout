// frontend/src/components/orchestration/MamaBearOrchestration.tsx
import React, { useState, useEffect } from 'react';
import { io, Socket } from 'socket.io-client';

// Types
interface Agent {
  id: string;
  state: 'idle' | 'thinking' | 'working' | 'waiting' | 'collaborating' | 'error';
  current_task?: string;
  last_activity: string;
  message_queue_size: number;
}

interface SystemStatus {
  timestamp: string;
  agents: Record<string, Agent>;
  active_tasks: number;
  queued_tasks: number;
  completed_tasks: number;
  model_manager_status: any;
  global_context: string[];
}

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'mama_bear';
  timestamp: string;
  agent_id?: string;
  collaboration_id?: string;
  metadata?: any;
}

interface OrchestrationResponse {
  type: 'simple_response' | 'collaborative_response' | 'plan_proposal';
  content: string;
  agent_id?: string;
  participating_agents?: string[];
  collaboration_id?: string;
  plan?: any;
  metadata?: any;
}

// Custom hooks
const useSocket = (userId: string) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const newSocket = io('http://localhost:5000', {
      transports: ['websocket']
    });

    newSocket.on('connect', () => {
      setConnected(true);
      newSocket.emit('join_orchestration', { user_id: userId });
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [userId]);

  return { socket, connected };
};

const useSystemStatus = (socket: Socket | null) => {
  const [status, setStatus] = useState<SystemStatus | null>(null);

  useEffect(() => {
    if (!socket) return;

    const handleStatusUpdate = (data: SystemStatus) => {
      setStatus(data);
    };

    socket.on('system_status_update', handleStatusUpdate);
    socket.emit('get_agent_status');

    return () => {
      socket.off('system_status_update', handleStatusUpdate);
    };
  }, [socket]);

  return status;
};

// Agent Status Component
const AgentStatusCard: React.FC<{ agent: Agent; agentId: string }> = ({ agent, agentId }) => {
  const getStateColor = (state: string) => {
    switch (state) {
      case 'idle': return 'bg-gray-500';
      case 'thinking': return 'bg-yellow-500 animate-pulse';
      case 'working': return 'bg-blue-500 animate-pulse';
      case 'collaborating': return 'bg-purple-500 animate-pulse';
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getAgentEmoji = (id: string) => {
    const emojis = {
      'research_specialist': '🔍',
      'devops_specialist': '⚙️',
      'scout_commander': '🧭',
      'model_coordinator': '🤖',
      'tool_curator': '🛠️',
      'integration_architect': '🔗',
      'live_api_specialist': '⚡',
      'lead_developer': '👨‍💻'
    };
    return emojis[id as keyof typeof emojis] || '🐻';
  };

  const formatAgentName = (id: string) => {
    return id.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-md border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">{getAgentEmoji(agentId)}</span>
          <h3 className="font-semibold text-gray-900 dark:text-white">
            {formatAgentName(agentId)}
          </h3>
        </div>
        <div className={`w-3 h-3 rounded-full ${getStateColor(agent.state)}`}></div>
      </div>
      
      <div className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
        <div className="flex justify-between">
          <span>Status:</span>
          <span className="capitalize font-medium">{agent.state}</span>
        </div>
        
        {agent.current_task && (
          <div className="flex justify-between">
            <span>Task:</span>
            <span className="truncate ml-2 max-w-24">{agent.current_task}</span>
          </div>
        )}
        
        <div className="flex justify-between">
          <span>Messages:</span>
          <span>{agent.message_queue_size}</span>
        </div>
        
        <div className="text-xs text-gray-500">
          Last active: {new Date(agent.last_activity).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

// Main Chat Interface with Orchestration
const OrchestrationChat: React.FC<{ userId: string; pageContext: string }> = ({ 
  userId, 
  pageContext 
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentThinking, setCurrentThinking] = useState('');
  
  const { socket, connected } = useSocket(userId);

  useEffect(() => {
    if (!socket) return;

    // Handle responses
    socket.on('mama_bear_response', (data: any) => {
      setIsLoading(false);
      setCurrentThinking('');
      
      const response: OrchestrationResponse = data.response;
      
      const newMessage: ChatMessage = {
        id: Date.now().toString(),
        content: response.content,
        sender: 'mama_bear',
        timestamp: new Date().toISOString(),
        agent_id: response.agent_id,
        collaboration_id: response.collaboration_id,
        metadata: response.metadata
      };
      
      setMessages(prev => [...prev, newMessage]);
    });

    // Handle thinking status
    socket.on('mama_bear_thinking', (data: any) => {
      setCurrentThinking(data.message);
    });

    // Handle errors
    socket.on('mama_bear_error', (data: any) => {
      setIsLoading(false);
      setCurrentThinking('');
      
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        content: data.fallback_message || 'Something went wrong, but I\'m here to help!',
        sender: 'mama_bear',
        timestamp: new Date().toISOString(),
        metadata: { error: data.error }
      };
      
      setMessages(prev => [...prev, errorMessage]);
    });

    return () => {
      socket.off('mama_bear_response');
      socket.off('mama_bear_thinking');
      socket.off('mama_bear_error');
    };
  }, [socket]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || !socket || isLoading) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setCurrentThinking('🐻 Analyzing your request...');

    // Send to orchestration system
    socket.emit('mama_bear_chat_realtime', {
      message: inputMessage,
      user_id: userId,
      page_context: pageContext
    });

    setInputMessage('');
  };

  const renderMessage = (message: ChatMessage) => {
    const isUser = message.sender === 'user';
    
    return (
      <div key={message.id} className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
        <div className={`
          max-w-xs lg:max-w-md px-4 py-2 rounded-lg
          ${isUser 
            ? 'bg-blue-500 text-white' 
            : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
          }
        `}>
          <div className="text-sm">{message.content}</div>
          
          {/* Agent info for Mama Bear messages */}
          {!isUser && message.agent_id && (
            <div className="text-xs opacity-70 mt-1">
              {message.collaboration_id ? '👥 Collaborative' : '🐻'} {message.agent_id}
            </div>
          )}
          
          <div className="text-xs opacity-70 mt-1">
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900">
      {/* Connection Status */}
      <div className="bg-gray-100 dark:bg-gray-800 px-4 py-2 border-b">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600 dark:text-gray-300">
              {connected ? 'Connected to Mama Bear' : 'Reconnecting...'}
            </span>
          </div>
          <div className="text-xs text-gray-500">
            Context: {pageContext}
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(renderMessage)}
        
        {/* Thinking indicator */}
        {currentThinking && (
          <div className="flex justify-start">
            <div className="bg-gray-200 dark:bg-gray-700 px-4 py-2 rounded-lg">
              <div className="text-sm text-gray-600 dark:text-gray-300">
                {currentThinking}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask Mama Bear anything..."
            className="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 
                     bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                     focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading || !connected}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !connected || !inputMessage.trim()}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 
                     text-white px-4 py-2 rounded-lg transition-colors"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

// System Status Dashboard
const SystemStatusDashboard: React.FC<{ userId: string }> = ({ userId }) => {
  const { socket } = useSocket(userId);
  const status = useSystemStatus(socket);

  if (!status) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-gray-500">Loading system status...</div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-blue-600">{status.active_tasks}</div>
          <div className="text-sm text-gray-600 dark:text-gray-300">Active Tasks</div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-green-600">{status.completed_tasks}</div>
          <div className="text-sm text-gray-600 dark:text-gray-300">Completed</div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-yellow-600">{status.queued_tasks}</div>
          <div className="text-sm text-gray-600 dark:text-gray-300">Queued</div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-purple-600">
            {Object.keys(status.agents).length}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-300">Agents</div>
        </div>
      </div>

      {/* Agents Grid */}
      <div>
        <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
          🐻 Mama Bear Agents
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {Object.entries(status.agents).map(([agentId, agent]) => (
            <AgentStatusCard key={agentId} agentId={agentId} agent={agent} />
          ))}
        </div>
      </div>

      {/* Global Context */}
      <div>
        <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
          🧠 Global Context
        </h2>
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="flex flex-wrap gap-2">
            {status.global_context.map((key) => (
              <span 
                key={key}
                className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 
                         px-2 py-1 rounded text-sm"
              >
                {key}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Agent Communication Panel
const AgentCommunicationPanel: React.FC<{ userId: string }> = ({ userId }) => {
  const { socket } = useSocket(userId);
  const [fromAgent, setFromAgent] = useState('');
  const [toAgent, setToAgent] = useState('');
  const [message, setMessage] = useState('');

  const agentOptions = [
    'research_specialist',
    'devops_specialist', 
    'scout_commander',
    'model_coordinator',
    'tool_curator',
    'integration_architect',
    'live_api_specialist',
    'lead_developer'
  ];

  const sendAgentMessage = () => {
    if (!socket || !fromAgent || !toAgent || !message) return;

    socket.emit('send_agent_message', {
      from_agent: fromAgent,
      to_agent: toAgent,
      message: message,
      context: { initiated_by_user: userId }
    });

    setMessage('');
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
        🗣️ Agent Communication
      </h3>
      
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">From Agent</label>
            <select 
              value={fromAgent}
              onChange={(e) => setFromAgent(e.target.value)}
              className="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="">Select agent...</option>
              {agentOptions.map(agent => (
                <option key={agent} value={agent}>{agent}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">To Agent</label>
            <select 
              value={toAgent}
              onChange={(e) => setToAgent(e.target.value)}
              className="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="">Select agent...</option>
              {agentOptions.map(agent => (
                <option key={agent} value={agent}>{agent}</option>
              ))}
            </select>
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-1">Message</label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Enter message for agent communication..."
            className="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 h-24
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>
        
        <button
          onClick={sendAgentMessage}
          disabled={!fromAgent || !toAgent || !message}
          className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 
                   text-white px-4 py-2 rounded transition-colors"
        >
          Send Message
        </button>
      </div>
    </div>
  );
};

// Main Orchestration Interface
export const MamaBearOrchestrationInterface: React.FC<{ 
  userId: string; 
  pageContext: string;
  view: 'chat' | 'dashboard' | 'communication';
}> = ({ userId, pageContext, view }) => {
  
  switch (view) {
    case 'chat':
      return <OrchestrationChat userId={userId} pageContext={pageContext} />;
    case 'dashboard':
      return <SystemStatusDashboard userId={userId} />;
    case 'communication':
      return (
        <div className="space-y-6">
          <SystemStatusDashboard userId={userId} />
          <AgentCommunicationPanel userId={userId} />
        </div>
      );
    default:
      return <OrchestrationChat userId={userId} pageContext={pageContext} />;
  }
};

export default MamaBearOrchestrationInterface;