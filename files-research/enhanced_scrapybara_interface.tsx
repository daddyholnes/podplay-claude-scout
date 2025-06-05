import React, { useState, useEffect, useRef } from 'react';
import { 
  Globe, 
  Monitor, 
  Shield, 
  Search, 
  Users, 
  Play, 
  Pause, 
  Square, 
  Camera,
  MousePointer,
  Keyboard,
  Eye,
  Lock,
  Unlock
} from 'lucide-react';

// Enhanced Scrapybara Interface Component
const EnhancedScrapybaraInterface = ({ userId = 'nathan_sanctuary' }) => {
  // State management
  const [activeTab, setActiveTab] = useState('shared-browser');
  const [sharedSession, setSharedSession] = useState(null);
  const [computerControl, setComputerControl] = useState({
    enabled: false,
    currentWorkflow: null,
    actionHistory: []
  });
  const [researchEnvironment, setResearchEnvironment] = useState(null);
  const [authSessions, setAuthSessions] = useState([]);
  const [collaborationStatus, setCollaborationStatus] = useState('disconnected');
  
  // WebSocket connection
  const wsRef = useRef(null);
  const [wsConnected, setWsConnected] = useState(false);

  // Initialize WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      // In a real implementation, this would connect to your WebSocket server
      const mockWs = {
        send: (data) => console.log('WebSocket send:', data),
        close: () => console.log('WebSocket closed'),
        readyState: 1 // OPEN
      };
      
      wsRef.current = mockWs;
      setWsConnected(true);
      
      // Simulate some WebSocket events
      setTimeout(() => {
        setCollaborationStatus('connected');
      }, 1000);
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Start shared browser session
  const startSharedBrowserSession = async () => {
    try {
      const response = await fetch('/api/scrapybara/shared-browser/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_id: userId,
          agent_id: 'research_specialist'
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setSharedSession(data.session);
        
        // Join WebSocket room for collaboration
        if (wsRef.current) {
          wsRef.current.send(JSON.stringify({
            type: 'join_shared_browser',
            session_id: data.session.session_id,
            user_id: userId
          }));
        }
      }
    } catch (error) {
      console.error('Error starting shared browser session:', error);
    }
  };

  // Execute computer control action
  const executeComputerAction = async (actionType, target, parameters = {}) => {
    try {
      const response = await fetch('/api/scrapybara/computer-control/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action_type: actionType,
          target,
          parameters,
          user_id: userId,
          permission_level: 'elevated'
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setComputerControl(prev => ({
          ...prev,
          actionHistory: [...prev.actionHistory, data.result]
        }));
      }
      
      return data;
    } catch (error) {
      console.error('Error executing computer action:', error);
      return { success: false, error: error.message };
    }
  };

  // Create research environment
  const createResearchEnvironment = async (topic) => {
    try {
      const response = await fetch('/api/scrapybara/research/environment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          research_topic: topic,
          user_id: userId
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setResearchEnvironment(data.research_environment);
      }
      
      return data;
    } catch (error) {
      console.error('Error creating research environment:', error);
      return { success: false, error: error.message };
    }
  };

  // Login to external service
  const loginToService = async (serviceName) => {
    try {
      const response = await fetch('/api/scrapybara/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service_name: serviceName,
          user_id: userId,
          credentials_vault_key: `${serviceName}_${userId}`
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setAuthSessions(prev => [...prev, data.authentication]);
      }
      
      return data;
    } catch (error) {
      console.error('Error logging into service:', error);
      return { success: false, error: error.message };
    }
  };

  // Shared Browser Session Tab
  const SharedBrowserTab = () => (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Globe className="w-5 h-5 text-blue-500" />
            Shared Browser Session
          </h3>
          <div className={`px-3 py-1 rounded-full text-sm ${
            collaborationStatus === 'connected' 
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
          }`}>
            {collaborationStatus}
          </div>
        </div>

        {!sharedSession ? (
          <div className="text-center py-8">
            <Globe className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Start a shared browser session to collaborate with Mama Bear in real-time
            </p>
            <button
              onClick={startSharedBrowserSession}
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center gap-2 mx-auto"
            >
              <Users className="w-4 h-4" />
              Start Shared Session
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
              <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                🌐 Session Active
              </h4>
              <p className="text-sm text-blue-700 dark:text-blue-300 mb-3">
                You and Mama Bear are now sharing the same browser session!
              </p>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <strong>Session ID:</strong> {sharedSession.session_id}
                </div>
                <div>
                  <strong>Participants:</strong> {sharedSession.participants.join(', ')}
                </div>
              </div>
            </div>

            <div className="border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden">
              <div className="bg-gray-100 dark:bg-gray-700 p-3 flex items-center justify-between">
                <span className="text-sm font-medium">Shared Browser View</span>
                <div className="flex items-center gap-2">
                  <Eye className="w-4 h-4 text-green-500" />
                  <span className="text-xs text-green-600 dark:text-green-400">Live</span>
                </div>
              </div>
              <div className="bg-white dark:bg-gray-800 p-8 text-center min-h-64 flex items-center justify-center">
                <div className="text-gray-500 dark:text-gray-400">
                  <Monitor className="w-12 h-12 mx-auto mb-2" />
                  <p>Shared browser content would appear here</p>
                  <p className="text-sm mt-1">URL: {sharedSession.current_url || 'about:blank'}</p>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <button className="flex-1 bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2">
                <MousePointer className="w-4 h-4" />
                Enable Cursor Sync
              </button>
              <button className="flex-1 bg-purple-500 hover:bg-purple-600 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2">
                <Users className="w-4 h-4" />
                Collaborative Mode
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  // Computer Control Tab
  const ComputerControlTab = () => (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
          <Monitor className="w-5 h-5 text-purple-500" />
          Computer Use Agent
        </h3>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <button
            onClick={() => executeComputerAction('screenshot', {})}
            className="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-lg flex flex-col items-center gap-2"
          >
            <Camera className="w-6 h-6" />
            <span className="text-sm">Screenshot</span>
          </button>
          
          <button
            onClick={() => executeComputerAction('click', { selector: '.target-element' })}
            className="bg-green-500 hover:bg-green-600 text-white p-4 rounded-lg flex flex-col items-center gap-2"
          >
            <MousePointer className="w-6 h-6" />
            <span className="text-sm">Click Element</span>
          </button>
          
          <button
            onClick={() => executeComputerAction('type', { text: 'Hello World!' })}
            className="bg-yellow-500 hover:bg-yellow-600 text-white p-4 rounded-lg flex flex-col items-center gap-2"
          >
            <Keyboard className="w-6 h-6" />
            <span className="text-sm">Type Text</span>
          </button>
          
          <button
            onClick={() => executeComputerAction('extract_data', { selector: '.data-container' })}
            className="bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-lg flex flex-col items-center gap-2"
          >
            <Search className="w-6 h-6" />
            <span className="text-sm">Extract Data</span>
          </button>
        </div>

        {computerControl.actionHistory.length > 0 && (
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h4 className="font-medium mb-3">Recent Actions</h4>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {computerControl.actionHistory.slice(-5).map((action, index) => (
                <div key={index} className="text-sm p-2 bg-white dark:bg-gray-600 rounded border">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">{action.action_type}</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      action.success 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                    }`}>
                      {action.success ? 'Success' : 'Failed'}
                    </span>
                  </div>
                  <div className="text-gray-600 dark:text-gray-400 mt-1">
                    {action.timestamp}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="mt-6 p-4 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800">
          <div className="flex items-start gap-3">
            <Shield className="w-5 h-5 text-amber-500 mt-0.5" />
            <div>
              <h4 className="font-medium text-amber-900 dark:text-amber-100">
                Safe Computer Control
              </h4>
              <p className="text-sm text-amber-700 dark:text-amber-300 mt-1">
                All computer actions are safety-checked and require appropriate permissions. 
                Mama Bear will ask for permission before performing sensitive operations.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Authentication Tab
  const AuthenticationTab = () => (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
          <Lock className="w-5 h-5 text-green-500" />
          Authenticated Sessions
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {['github', 'google', 'linkedin'].map((service) => (
            <div key={service} className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium capitalize">{service}</h4>
                {authSessions.some(s => s.service === service) ? (
                  <Unlock className="w-4 h-4 text-green-500" />
                ) : (
                  <Lock className="w-4 h-4 text-gray-400" />
                )}
              </div>
              
              <button
                onClick={() => loginToService(service)}
                className={`w-full py-2 px-4 rounded-lg text-sm font-medium ${
                  authSessions.some(s => s.service === service)
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                }`}
                disabled={authSessions.some(s => s.service === service)}
              >
                {authSessions.some(s => s.service === service) ? 'Authenticated' : 'Login'}
              </button>
            </div>
          ))}
        </div>

        {authSessions.length > 0 && (
          <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <h4 className="font-medium text-green-900 dark:text-green-100 mb-2">
              🔐 Active Sessions
            </h4>
            <div className="space-y-2">
              {authSessions.map((session, index) => (
                <div key={index} className="flex justify-between items-center text-sm">
                  <span className="capitalize font-medium">{session.service}</span>
                  <span className="text-green-600 dark:text-green-400">
                    Expires: {new Date(session.expires_at).toLocaleTimeString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="flex items-start gap-3">
            <Shield className="w-5 h-5 text-blue-500 mt-0.5" />
            <div>
              <h4 className="font-medium text-blue-900 dark:text-blue-100">
                Secure Authentication
              </h4>
              <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                Credentials are encrypted and stored securely. Sessions are automatically 
                refreshed and expired sessions are cleaned up for your security.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Research Environment Tab
  const ResearchTab = () => (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
          <Search className="w-5 h-5 text-blue-500" />
          Research Environment
        </h3>

        {!researchEnvironment ? (
          <div className="text-center py-8">
            <Search className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Create a dedicated research environment with multiple instances
            </p>
            <div className="max-w-md mx-auto">
              <input
                type="text"
                placeholder="Research topic (e.g., 'AI startups 2024')"
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg mb-4 
                         bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    createResearchEnvironment(e.target.value);
                  }
                }}
              />
              <button
                onClick={() => {
                  const input = document.querySelector('input[placeholder*="Research topic"]');
                  if (input.value) {
                    createResearchEnvironment(input.value);
                  }
                }}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center gap-2 mx-auto"
              >
                <Play className="w-4 h-4" />
                Create Environment
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
              <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                🔍 Research Environment Active
              </h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <strong>Environment ID:</strong> {researchEnvironment.research_environment_id}
                </div>
                <div>
                  <strong>Instances:</strong> {researchEnvironment.instances?.length || 0}
                </div>
                <div>
                  <strong>Primary Instance:</strong> {researchEnvironment.primary_instance}
                </div>
                <div>
                  <strong>Data Instance:</strong> {researchEnvironment.data_instance}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                <h5 className="font-medium mb-2">Primary Research Instance</h5>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  Configured with Python, Node.js, and research tools
                </p>
                <button className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded text-sm">
                  Connect
                </button>
              </div>

              <div className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                <h5 className="font-medium mb-2">Data Collection Instance</h5>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  Browser with extensions for data scraping
                </p>
                <button className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded text-sm">
                  Open Browser
                </button>
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
              <h4 className="font-medium text-green-900 dark:text-green-100 mb-2">
                🧠 Collaborative Research Ready
              </h4>
              <p className="text-sm text-green-700 dark:text-green-300">
                Your research environment is ready for parallel data collection and analysis. 
                Mama Bear can now help you execute complex research workflows across multiple instances.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  const tabs = [
    { id: 'shared-browser', label: 'Shared Browser', icon: Globe, component: SharedBrowserTab },
    { id: 'computer-control', label: 'Computer Control', icon: Monitor, component: ComputerControlTab },
    { id: 'authentication', label: 'Authentication', icon: Lock, component: AuthenticationTab },
    { id: 'research', label: 'Research Environment', icon: Search, component: ResearchTab }
  ];

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          🐻 Enhanced Mama Bear Features
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Next-level browser control, computer automation, and collaborative AI capabilities
        </p>
        
        {/* Connection Status */}
        <div className="mt-4 flex items-center gap-4">
          <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm ${
            wsConnected 
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
          }`}>
            <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
            WebSocket {wsConnected ? 'Connected' : 'Disconnected'}
          </div>
          
          <div className="flex items-center gap-2 px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
            <Users className="w-3 h-3" />
            Collaboration {collaborationStatus}
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="min-h-96">
        {tabs.find(tab => tab.id === activeTab)?.component()}
      </div>

      {/* Footer Info */}
      <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          🚀 Transform Your Development Environment
        </h3>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          With these enhanced capabilities, Mama Bear becomes your intelligent computer companion who can:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            '👀 See what you see on your screen',
            '🖱️ Click, type, and navigate like you do',
            '🔑 Remember and reuse login sessions',
            '🤝 Work alongside you in real-time',
            '⚙️ Automate complex workflows',
            '🧠 Learn from your patterns'
          ].map((capability, index) => (
            <div key={index} className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 bg-blue-500 rounded-full" />
              {capability}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EnhancedScrapybaraInterface;