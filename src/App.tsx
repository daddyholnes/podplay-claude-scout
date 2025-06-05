import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { SanctuaryLayout } from './components/layout/SanctuaryLayout';
import { SplashCursor } from './components/effects/SplashCursor';
import { AuroraBackground } from './components/effects/AuroraBackground';
import { BackgroundGradientAnimation } from './components/effects/BackgroundGradientAnimation';
import { GlowingEffect } from './components/ui/GlowingEffect';
import { SanctuaryWorkspaceCard } from './components/ui/SanctuaryWorkspaceCard';
import { AgentPlan } from './components/ui/AgentPlan';
import { EnhancedMamaBearInterface } from './components/enhanced/EnhancedMamaBearInterface';
import { motion, AnimatePresence } from 'framer-motion';
import './index.css';

// Simplified page components for demonstration
const MainChatPage = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '🐻 Hello! I\'m Mama Bear, your research specialist. What would you like to explore today?' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const userMessage = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: inputMessage,
          user_id: 'demo_user',
          page_context: 'main_chat'
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: `🐻 ${data.response}` 
        }]);
      } else {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: '🐻 I\'m having trouble connecting right now. Please try again in a moment!' 
        }]);
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: '🐻 I\'m taking a quick nap. Please try again in a moment! 💤' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center space-y-4">
        <GlowingEffect glow={true} disabled={false}>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
            🐻 Research Specialist Mama Bear
          </h1>
        </GlowingEffect>
        <p className="text-xl text-purple-200 max-w-2xl mx-auto">
          Your caring AI research companion who loves discovering connections and diving deep into topics.
        </p>
      </div>

      <div className="max-w-4xl mx-auto space-y-6">
        {/* Chat Messages */}
        <div className="bg-black/20 backdrop-blur-xl border border-white/10 rounded-xl p-6 min-h-[400px] space-y-4">
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`p-4 rounded-lg ${
                  message.role === 'user' 
                    ? 'bg-purple-500/20 border border-purple-400/30 ml-12' 
                    : 'bg-blue-500/20 border border-blue-400/30 mr-12'
                }`}
              >
                <p className="text-white">{message.content}</p>
              </motion.div>
            ))}
          </AnimatePresence>
          
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-blue-500/20 border border-blue-400/30 mr-12 p-4 rounded-lg"
            >
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-400"></div>
                <p className="text-white">🐻 Mama Bear is thinking...</p>
              </div>
            </motion.div>
          )}
        </div>

        {/* Chat Input */}
        <div className="bg-black/20 backdrop-blur-xl border border-white/10 rounded-xl p-4">
          <div className="flex gap-4">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask Mama Bear anything..."
              className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-400"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const VMHubPage = () => {
  const [instances, setInstances] = useState<Array<{
    name: string;
    status: "idle" | "provisioning" | "active" | "error";
    agent: string;
    stats: { label: string; value: string }[];
  }>>([
    {
      name: "Dev Environment",
      status: "active",
      agent: "DevOps Specialist",
      stats: [
        { label: "CPU", value: "45%" },
        { label: "Memory", value: "2.1GB" },
        { label: "Uptime", value: "2h" }
      ]
    },
    {
      name: "Production Mirror", 
      status: "idle",
      agent: "Scout Commander",
      stats: [
        { label: "CPU", value: "12%" },
        { label: "Memory", value: "1.2GB" },
        { label: "Uptime", value: "1d" }
      ]
    }
  ]);

  const createInstance = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/vm/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          config: { os: 'ubuntu-22.04', size: 'medium' },
          user_id: 'demo_user'
        })
      });

      const data = await response.json();
      
      if (data.success) {
        const newInstance = {
          name: `Instance ${instances.length + 1}`,
          status: "provisioning" as const,
          agent: "DevOps Specialist",
          stats: [
            { label: "CPU", value: "0%" },
            { label: "Memory", value: "0GB" },
            { label: "Uptime", value: "0m" }
          ]
        };
        setInstances(prev => [...prev, newInstance]);
      }
    } catch (error) {
      console.error('VM creation error:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center space-y-4">
        <GlowingEffect glow={true} disabled={false}>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-cyan-400 to-green-400 bg-clip-text text-transparent">
            🖥️ Scrapybara VM Hub
          </h1>
        </GlowingEffect>
        <p className="text-xl text-blue-200 max-w-2xl mx-auto">
          Manage your cloud instances with DevOps Specialist Mama Bear
        </p>
      </div>

      <div className="flex justify-center mb-8">
        <button
          onClick={createInstance}
          className="px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-xl font-medium hover:from-blue-600 hover:to-cyan-600 transition-all shadow-lg shadow-blue-500/25"
        >
          + Create New Instance
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {instances.map((instance, index) => (
          <SanctuaryWorkspaceCard
            key={index}
            name={instance.name}
            status={instance.status}
            agent={instance.agent}
            stats={instance.stats}
            theme="sanctuary"
          >
            <div className="flex gap-2 mt-4">
              <button className="px-4 py-2 bg-green-500/20 text-green-300 rounded-lg text-sm hover:bg-green-500/30 transition-colors">
                Connect
              </button>
              <button className="px-4 py-2 bg-yellow-500/20 text-yellow-300 rounded-lg text-sm hover:bg-yellow-500/30 transition-colors">
                Restart
              </button>
              <button className="px-4 py-2 bg-red-500/20 text-red-300 rounded-lg text-sm hover:bg-red-500/30 transition-colors">
                Stop
              </button>
            </div>
          </SanctuaryWorkspaceCard>
        ))}
      </div>
    </div>
  );
};

const ScoutAgentPage = () => {
  const [plan, setPlan] = useState<any>(null);
  const [taskDescription, setTaskDescription] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  const createPlan = async () => {
    if (!taskDescription.trim()) return;
    
    setIsCreating(true);
    try {
      const response = await fetch('http://localhost:5000/api/plans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: 'Autonomous Task Execution',
          description: taskDescription,
          user_id: 'demo_user',
          context: { page: 'scout' }
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setPlan(data.plan);
      }
    } catch (error) {
      console.error('Plan creation error:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleRunSubtask = async (planId: string, subtaskId: string) => {
    try {
      const response = await fetch(`http://localhost:5000/api/plans/${planId}/subtasks/${subtaskId}/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'demo_user' })
      });

      const data = await response.json();
      console.log('Subtask execution:', data);
    } catch (error) {
      console.error('Subtask execution error:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center space-y-4">
        <GlowingEffect glow={true} disabled={false}>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-orange-400 via-red-400 to-pink-400 bg-clip-text text-transparent">
            🔍 Scout Commander Mama Bear
          </h1>
        </GlowingEffect>
        <p className="text-xl text-orange-200 max-w-2xl mx-auto">
          Your adventurous AI agent who breaks down complex tasks and executes them autonomously
        </p>
      </div>

      {!plan ? (
        <div className="max-w-2xl mx-auto space-y-6">
          <div className="bg-black/20 backdrop-blur-xl border border-white/10 rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-4">🎯 Create Autonomous Task</h3>
            <div className="space-y-4">
              <textarea
                value={taskDescription}
                onChange={(e) => setTaskDescription(e.target.value)}
                placeholder="Describe the task you want Scout Commander to execute autonomously..."
                className="w-full h-32 bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
              />
              <button
                onClick={createPlan}
                disabled={isCreating || !taskDescription.trim()}
                className="w-full px-6 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-lg font-medium hover:from-orange-600 hover:to-red-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCreating ? 'Creating Plan...' : 'Create Execution Plan'}
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="max-w-4xl mx-auto">
          <AgentPlan 
            plan={plan} 
            onRunSubtask={handleRunSubtask}
            onPauseSubtask={(planId, subtaskId) => console.log('Pause:', planId, subtaskId)}
            onReassignSubtask={(planId, subtaskId, agent) => console.log('Reassign:', planId, subtaskId, agent)}
          />
        </div>
      )}
    </div>
  );
};

const App: React.FC = () => {
  const [theme, setTheme] = useState('aurora');

  return (
    <div className="min-h-screen relative">
      {/* Global Cursor Effect */}
      <SplashCursor />
      
      {/* Dynamic Background */}
      {theme === 'aurora' && <AuroraBackground />}
      {theme === 'gradient' && <BackgroundGradientAnimation />}
      
      <Router>
        <Routes>
          <Route path="/" element={<EnhancedMamaBearInterface />} />
          
          <Route path="/classic" element={
            <SanctuaryLayout currentPage="Main Chat">
              <MainChatPage />
            </SanctuaryLayout>
          } />
          
          <Route path="/vm-hub" element={
            <SanctuaryLayout currentPage="VM Hub">
              <VMHubPage />
            </SanctuaryLayout>
          } />
          
          <Route path="/scout" element={
            <SanctuaryLayout currentPage="Scout Agent">
              <ScoutAgentPage />
            </SanctuaryLayout>
          } />
          
          <Route path="/chat" element={
            <SanctuaryLayout currentPage="Multi-Modal">
              <div className="text-center text-2xl text-white">
                🤖 Multi-Modal Chat Coming Soon!
              </div>
            </SanctuaryLayout>
          } />
          
          <Route path="/mcp" element={
            <SanctuaryLayout currentPage="MCP Tools">
              <div className="text-center text-2xl text-white">
                🔧 MCP Marketplace Coming Soon!
              </div>
            </SanctuaryLayout>
          } />
          
          <Route path="/integrations" element={
            <SanctuaryLayout currentPage="Integrations">
              <div className="text-center text-2xl text-white">
                🔗 Integration Workbench Coming Soon!
              </div>
            </SanctuaryLayout>
          } />
          
          <Route path="/live-api" element={
            <SanctuaryLayout currentPage="Live API">
              <div className="text-center text-2xl text-white">
                🎙️ Live API Studio Coming Soon!
              </div>
            </SanctuaryLayout>
          } />
        </Routes>
      </Router>
    </div>
  );
};

export default App;