import React, { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Bot, Play, Pause, Square, FileText, CheckCircle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Textarea } from '../components/ui/textarea';

export default function ScoutAgent() {
  const { theme } = useTheme();
  const [task, setTask] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [steps] = useState([
    '🐻 Scout analyzing task requirements...',
    '📋 Breaking down task into actionable steps...',
    '🚀 Creating new workspace environment...',
    '⚙️ Installing required dependencies...',
    '📝 Writing initial code structure...',
    '🧪 Testing implementation...',
    '✨ Optimizing and finalizing...',
    '✅ Task completed successfully!'
  ]);

  const startTask = () => {
    setIsRunning(true);
    setProgress(0);
    // Simulate progress
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsRunning(false);
          return 100;
        }
        return prev + 12.5;
      });
    }, 1000);
  };

  return (
    <div className="pt-16 min-h-screen">
      <div className="max-w-7xl mx-auto p-6">
        
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">🐻 Scout Commander</h1>
              <p className="text-lg opacity-75">
                Autonomous task execution with strategic planning
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Task Input */}
          <Card className={`${theme.card} p-6`}>
            <h2 className="text-xl font-semibold mb-4">Mission Brief</h2>
            <Textarea
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="Describe the task you want Scout to accomplish autonomously..."
              className="mb-4"
              rows={6}
              disabled={isRunning}
            />
            
            <div className="flex space-x-3">
              <Button
                onClick={startTask}
                disabled={!task.trim() || isRunning}
                className={theme.button}
              >
                {isRunning ? (
                  <>
                    <Pause className="w-4 h-4 mr-2" />
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 mr-2" />
                    Deploy Scout
                  </>
                )}
              </Button>
              
              {isRunning && (
                <Button
                  onClick={() => {
                    setIsRunning(false);
                    setProgress(0);
                  }}
                  variant="outline"
                >
                  <Square className="w-4 h-4 mr-2" />
                  Stop
                </Button>
              )}
            </div>
          </Card>

          {/* Progress */}
          <Card className={`${theme.card} p-6`}>
            <h2 className="text-xl font-semibold mb-4">Scout Progress</h2>
            
            {progress > 0 && (
              <div className="mb-4">
                <div className="flex justify-between text-sm mb-2">
                  <span>Overall Progress</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-orange-500 to-red-500 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            )}

            <div className="space-y-3">
              {steps.map((step, index) => {
                const isCompleted = progress > (index / steps.length) * 100;
                const isCurrent = progress >= (index / steps.length) * 100 && progress < ((index + 1) / steps.length) * 100;
                
                return (
                  <div
                    key={index}
                    className={`
                      flex items-center space-x-3 p-3 rounded-lg transition-all
                      ${isCompleted ? 'bg-green-100 text-green-800' : 
                        isCurrent ? 'bg-orange-100 text-orange-800' : 
                        'bg-gray-100 text-gray-600'}
                    `}
                  >
                    {isCompleted ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : isCurrent ? (
                      <div className="w-5 h-5 border-2 border-orange-600 rounded-full animate-spin border-t-transparent" />
                    ) : (
                      <div className="w-5 h-5 border-2 border-gray-400 rounded-full" />
                    )}
                    <span className="text-sm">{step}</span>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>

        {/* Scout Capabilities */}
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Scout Capabilities</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className={`${theme.card} p-4`}>
              <FileText className="w-8 h-8 mb-3 text-blue-500" />
              <h3 className="font-semibold mb-2">Code Generation</h3>
              <p className="text-sm opacity-75">Create complete applications from descriptions</p>
            </Card>
            
            <Card className={`${theme.card} p-4`}>
              <Bot className="w-8 h-8 mb-3 text-purple-500" />
              <h3 className="font-semibold mb-2">Environment Setup</h3>
              <p className="text-sm opacity-75">Configure development environments automatically</p>
            </Card>
            
            <Card className={`${theme.card} p-4`}>
              <CheckCircle className="w-8 h-8 mb-3 text-green-500" />
              <h3 className="font-semibold mb-2">Testing & Validation</h3>
              <p className="text-sm opacity-75">Test and validate implementations</p>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}