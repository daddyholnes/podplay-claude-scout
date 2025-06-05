import React, { useState, useEffect } from 'react';
import { AuroraBackground } from '../effects/AuroraBackground';
import { BackgroundGradientAnimation } from '../effects/BackgroundGradientAnimation';
import { SanctuaryWorkspaceCard } from '../ui/SanctuaryWorkspaceCard';
import { GlowingEffect } from '../ui/GlowingEffect';
import { AgentPlan } from '../ui/AgentPlan';

interface EnhancedTask {
  id: string;
  description: string;
  type: 'research' | 'browser_automation' | 'computer_use' | 'multi_instance' | 'collaboration' | 'analysis';
  status: 'pending' | 'executing' | 'completed' | 'failed';
  progress?: string;
  result?: any;
}

interface SharedSession {
  session_id: string;
  instance_id: string;
  url: string;
  created_at: string;
  shared_with: string[];
}

export const EnhancedMamaBearInterface: React.FC = () => {
  const [activeTasks, setActiveTasks] = useState<EnhancedTask[]>([]);
  const [sharedSessions, setSharedSessions] = useState<SharedSession[]>([]);
  const [selectedWorkspace, setSelectedWorkspace] = useState<string>('computer-use');
  const [taskInput, setTaskInput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);

  // Workspace configurations
  const workspaces = [
    {
      id: 'computer-use',
      title: '🤖 Computer Use Agent',
      description: 'Let Mama Bear control your computer and automate desktop tasks',
      icon: '🖥️',
      color: 'from-blue-600 to-purple-600'
    },
    {
      id: 'shared-browser',
      title: '🌐 Shared Browser',
      description: 'Collaborate with Mama Bear in real-time browser sessions',
      icon: '🌍',
      color: 'from-green-600 to-blue-600'
    },
    {
      id: 'multi-research',
      title: '🔍 Multi-Instance Research',
      description: 'Parallel research across multiple virtual environments',
      icon: '🔬',
      color: 'from-purple-600 to-pink-600'
    },
    {
      id: 'agent-orchestration',
      title: '🎭 Agent Orchestration',
      description: 'Coordinate multiple AI agents for complex workflows',
      icon: '🎪',
      color: 'from-orange-600 to-red-600'
    }
  ];

  // Submit enhanced task
  const submitTask = async (description: string, type: string) => {
    setIsExecuting(true);
    try {
      const response = await fetch('/api/enhanced/submit-task', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description,
          task_type: type,
          user_id: 'nathan_sanctuary',
          priority: 1
        })
      });

      const result = await response.json();
      if (result.success) {
        // Add task to local state
        const newTask: EnhancedTask = {
          id: result.task_id,
          description,
          type: type as any,
          status: 'pending',
          progress: 'Task submitted...'
        };
        setActiveTasks(prev => [...prev, newTask]);
        
        // Start polling for updates
        pollTaskStatus(result.task_id);
      }
    } catch (error) {
      console.error('Failed to submit task:', error);
    } finally {
      setIsExecuting(false);
      setTaskInput('');
    }
  };

  // Poll task status
  const pollTaskStatus = async (taskId: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`/api/enhanced/task-status/${taskId}`);
        const result = await response.json();
        
        if (result.success) {
          setActiveTasks(prev => prev.map(task => 
            task.id === taskId 
              ? { ...task, ...result.status }
              : task
          ));
          
          // Stop polling if task is completed or failed
          if (result.status.status === 'completed' || result.status.status === 'failed') {
            clearInterval(pollInterval);
          }
        }
      } catch (error) {
        console.error('Failed to poll task status:', error);
        clearInterval(pollInterval);
      }
    }, 2000);
  };

  // Create shared browser session
  const createSharedBrowser = async () => {
    try {
      const response = await fetch('/api/enhanced/shared-browser/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 'nathan_sanctuary',
          initial_url: 'https://google.com'
        })
      });

      const result = await response.json();
      if (result.success) {
        setSharedSessions(prev => [...prev, result.session]);
      }
    } catch (error) {
      console.error('Failed to create shared browser:', error);
    }
  };

  // Render workspace content
  const renderWorkspaceContent = () => {
    switch (selectedWorkspace) {
      case 'computer-use':
        return (
          <div className="space-y-6">
            <div className="bg-black/20 backdrop-blur-md rounded-xl p-6 border border-white/10">
              <h3 className="text-xl font-bold text-white mb-4">🤖 Computer Use Agent Tasks</h3>
              <div className="space-y-4">
                <input
                  type="text"
                  value={taskInput}
                  onChange={(e) => setTaskInput(e.target.value)}
                  placeholder="Tell Mama Bear what to do on your computer..."
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <button
                  onClick={() => submitTask(taskInput, 'computer_use')}
                  disabled={!taskInput || isExecuting}
                  className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-300 disabled:opacity-50"
                >
                  {isExecuting ? '🔄 Executing...' : '🚀 Execute Computer Task'}
                </button>
              </div>
            </div>
            
            {/* Task List */}
            <div className="space-y-3">
              {activeTasks.filter(task => task.type === 'computer_use').map(task => (
                <div key={task.id} className="bg-black/20 backdrop-blur-md rounded-lg p-4 border border-white/10">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white font-medium">{task.description}</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      task.status === 'completed' ? 'bg-green-500/20 text-green-300' :
                      task.status === 'executing' ? 'bg-blue-500/20 text-blue-300' :
                      task.status === 'failed' ? 'bg-red-500/20 text-red-300' :
                      'bg-yellow-500/20 text-yellow-300'
                    }`}>
                      {task.status}
                    </span>
                  </div>
                  {task.progress && (
                    <p className="text-white/70 text-sm">{task.progress}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        );

      case 'shared-browser':
        return (
          <div className="space-y-6">
            <div className="bg-black/20 backdrop-blur-md rounded-xl p-6 border border-white/10">
              <h3 className="text-xl font-bold text-white mb-4">🌐 Shared Browser Sessions</h3>
              <button
                onClick={createSharedBrowser}
                className="w-full px-6 py-3 bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-lg font-semibold hover:from-green-700 hover:to-blue-700 transition-all duration-300"
              >
                🔗 Create New Shared Session
              </button>
            </div>
            
            {/* Session List */}
            <div className="space-y-3">
              {sharedSessions.map(session => (
                <div key={session.session_id} className="bg-black/20 backdrop-blur-md rounded-lg p-4 border border-white/10">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white font-medium">Session: {session.session_id}</span>
                    <span className="text-green-300 text-xs">🟢 Active</span>
                  </div>
                  <p className="text-white/70 text-sm">URL: {session.url}</p>
                  <p className="text-white/70 text-xs">Created: {new Date(session.created_at).toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>
        );

      default:
        return (
          <div className="bg-black/20 backdrop-blur-md rounded-xl p-6 border border-white/10">
            <h3 className="text-xl font-bold text-white mb-4">🚧 Coming Soon</h3>
            <p className="text-white/70">This workspace is under development. Stay tuned for amazing features!</p>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated Background */}
      <AuroraBackground />
      <BackgroundGradientAnimation />
      
      {/* Main Content */}
      <div className="relative z-10 p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <GlowingEffect>
            <h1 className="text-4xl font-bold text-white mb-2">
              🐻 Enhanced Mama Bear Sanctuary
            </h1>
          </GlowingEffect>
          <p className="text-white/80 text-lg">
            Next-level AI assistance with Computer Use Agent & MCP Browser
          </p>
        </div>

        {/* Workspace Selector */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {workspaces.map(workspace => (
            <SanctuaryWorkspaceCard
              key={workspace.id}
              title={workspace.title}
              description={workspace.description}
              icon={workspace.icon}
              isActive={selectedWorkspace === workspace.id}
              onClick={() => setSelectedWorkspace(workspace.id)}
              className={`bg-gradient-to-br ${workspace.color} cursor-pointer transition-all duration-300 hover:scale-105`}
            />
          ))}
        </div>

        {/* Active Workspace */}
        <div className="max-w-4xl mx-auto">
          {renderWorkspaceContent()}
        </div>

        {/* Agent Status Panel */}
        <div className="fixed bottom-6 right-6">
          <div className="bg-black/40 backdrop-blur-md rounded-xl p-4 border border-white/10">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-white text-sm">🐻 Mama Bear Online</span>
            </div>
            <p className="text-white/60 text-xs mt-1">
              {activeTasks.length} active tasks
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};