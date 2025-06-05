import React, { useState, useEffect } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { useSocket } from '../contexts/SocketContext';
import { useMemory } from '../contexts/MemoryContext';
import { 
  Server, 
  Play, 
  Square, 
  Pause,
  Monitor,
  Terminal,
  Settings,
  Plus,
  Activity,
  HardDrive,
  Cpu,
  MemoryStick
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';

interface Workspace {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'creating';
  url?: string;
  resources: {
    cpu: number;
    memory: number;
    disk: number;
  };
  uptime: string;
}

export default function VMHub() {
  const { theme } = useTheme();
  const { emit, on, off, connected } = useSocket();
  const { userId } = useMemory();
  
  const [workspaces, setWorkspaces] = useState<Workspace[]>([
    {
      id: 'ws-1',
      name: 'React Development',
      status: 'running',
      url: 'https://workspace-1.scrapybara.com',
      resources: { cpu: 25, memory: 512, disk: 2.1 },
      uptime: '2h 15m'
    },
    {
      id: 'ws-2', 
      name: 'Python Backend',
      status: 'stopped',
      resources: { cpu: 0, memory: 0, disk: 1.8 },
      uptime: '0m'
    }
  ]);
  
  const [newWorkspaceName, setNewWorkspaceName] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);

  const createWorkspace = () => {
    if (!newWorkspaceName.trim()) return;
    
    const newWorkspace: Workspace = {
      id: `ws-${Date.now()}`,
      name: newWorkspaceName,
      status: 'creating',
      resources: { cpu: 0, memory: 0, disk: 0 },
      uptime: '0m'
    };
    
    setWorkspaces(prev => [...prev, newWorkspace]);
    setNewWorkspaceName('');
    setShowCreateForm(false);
    
    // Simulate workspace creation
    setTimeout(() => {
      setWorkspaces(prev => prev.map(ws => 
        ws.id === newWorkspace.id 
          ? { ...ws, status: 'running' as const, url: `https://workspace-${newWorkspace.id}.scrapybara.com` }
          : ws
      ));
    }, 3000);
  };

  const toggleWorkspace = (id: string) => {
    setWorkspaces(prev => prev.map(ws => {
      if (ws.id === id) {
        const newStatus = ws.status === 'running' ? 'stopped' : 'running';
        return {
          ...ws,
          status: newStatus,
          resources: newStatus === 'stopped' 
            ? { cpu: 0, memory: 0, disk: ws.resources.disk }
            : { cpu: 25, memory: 512, disk: ws.resources.disk }
        };
      }
      return ws;
    }));
  };

  return (
    <div className="pt-16 min-h-screen">
      <div className="max-w-7xl mx-auto p-6">
        
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-blue-600 rounded-full flex items-center justify-center">
              <Server className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">🐻 DevOps Specialist</h1>
              <p className="text-lg opacity-75">
                Scrapybara VM management and infrastructure control
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <Button
              onClick={() => setShowCreateForm(true)}
              className={theme.button}
            >
              <Plus className="w-4 h-4 mr-2" />
              Create Workspace
            </Button>
            
            <div className={`flex items-center space-x-2 px-3 py-2 ${theme.card} rounded-lg`}>
              <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
              <span className="text-sm">
                {connected ? 'Connected to Scrapybara' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>

        {/* Create Workspace Form */}
        {showCreateForm && (
          <Card className={`${theme.card} p-6 mb-6`}>
            <h3 className="text-xl font-semibold mb-4">Create New Workspace</h3>
            <div className="flex space-x-4">
              <Input
                value={newWorkspaceName}
                onChange={(e) => setNewWorkspaceName(e.target.value)}
                placeholder="Workspace name (e.g., 'React Development')"
                className="flex-1"
                onKeyDown={(e) => e.key === 'Enter' && createWorkspace()}
              />
              <Button onClick={createWorkspace} className={theme.button}>
                Create
              </Button>
              <Button 
                onClick={() => setShowCreateForm(false)}
                variant="outline"
              >
                Cancel
              </Button>
            </div>
          </Card>
        )}

        {/* Workspaces Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {workspaces.map((workspace) => (
            <Card key={workspace.id} className={`${theme.card} p-6`}>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">{workspace.name}</h3>
                <div className={`
                  px-2 py-1 rounded-full text-xs font-medium
                  ${workspace.status === 'running' ? 'bg-green-100 text-green-800' : 
                    workspace.status === 'creating' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'}
                `}>
                  {workspace.status}
                </div>
              </div>

              {/* Resource Usage */}
              <div className="space-y-3 mb-6">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <Cpu className="w-4 h-4" />
                    <span>CPU</span>
                  </div>
                  <span>{workspace.resources.cpu}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${workspace.resources.cpu}%` }}
                  />
                </div>

                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <MemoryStick className="w-4 h-4" />
                    <span>Memory</span>
                  </div>
                  <span>{workspace.resources.memory} MB</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(workspace.resources.memory / 1024) * 100}%` }}
                  />
                </div>

                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <HardDrive className="w-4 h-4" />
                    <span>Disk</span>
                  </div>
                  <span>{workspace.resources.disk} GB</span>
                </div>
              </div>

              {/* Actions */}
              <div className="flex space-x-2">
                <Button
                  onClick={() => toggleWorkspace(workspace.id)}
                  disabled={workspace.status === 'creating'}
                  size="sm"
                  className={`flex-1 ${
                    workspace.status === 'running' 
                      ? 'bg-red-500 hover:bg-red-600' 
                      : theme.button
                  }`}
                >
                  {workspace.status === 'running' ? (
                    <>
                      <Square className="w-4 h-4 mr-2" />
                      Stop
                    </>
                  ) : workspace.status === 'creating' ? (
                    <>
                      <Activity className="w-4 h-4 mr-2 animate-spin" />
                      Creating...
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 mr-2" />
                      Start
                    </>
                  )}
                </Button>
                
                {workspace.url && (
                  <Button
                    onClick={() => window.open(workspace.url, '_blank')}
                    size="sm"
                    variant="outline"
                  >
                    <Monitor className="w-4 h-4" />
                  </Button>
                )}
              </div>

              <div className="mt-4 text-xs opacity-50">
                Uptime: {workspace.uptime}
              </div>
            </Card>
          ))}
        </div>

        {/* DevOps Tools */}
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">DevOps Tools</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card className={`${theme.card} p-4 hover:shadow-lg transition-shadow cursor-pointer`}>
              <Terminal className="w-8 h-8 mb-3 text-blue-500" />
              <h3 className="font-semibold mb-2">SSH Terminal</h3>
              <p className="text-sm opacity-75">Direct terminal access to VMs</p>
            </Card>
            
            <Card className={`${theme.card} p-4 hover:shadow-lg transition-shadow cursor-pointer`}>
              <Settings className="w-8 h-8 mb-3 text-purple-500" />
              <h3 className="font-semibold mb-2">Configuration</h3>
              <p className="text-sm opacity-75">Manage VM settings and configs</p>
            </Card>
            
            <Card className={`${theme.card} p-4 hover:shadow-lg transition-shadow cursor-pointer`}>
              <Activity className="w-8 h-8 mb-3 text-green-500" />
              <h3 className="font-semibold mb-2">Monitoring</h3>
              <p className="text-sm opacity-75">Real-time performance metrics</p>
            </Card>
            
            <Card className={`${theme.card} p-4 hover:shadow-lg transition-shadow cursor-pointer`}>
              <HardDrive className="w-8 h-8 mb-3 text-orange-500" />
              <h3 className="font-semibold mb-2">Storage</h3>
              <p className="text-sm opacity-75">Manage files and backups</p>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}