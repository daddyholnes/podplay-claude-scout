import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Brain, MessageCircle, Zap, Star } from 'lucide-react';
import { Card } from '../components/ui/card';

export default function MultiModalChat() {
  const { theme } = useTheme();

  const models = [
    { name: 'Gemini 2.5 Pro', status: 'healthy', usage: '87%' },
    { name: 'Gemini 2.5 Flash', status: 'healthy', usage: '23%' },
    { name: 'Claude 3.5 Sonnet', status: 'healthy', usage: '45%' },
    { name: 'GPT-4o', status: 'degraded', usage: '92%' }
  ];

  return (
    <div className="pt-16 min-h-screen">
      <div className="max-w-7xl mx-auto p-6">
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold">🐻 Model Coordinator</h1>
            <p className="text-lg opacity-75">
              Chat with multiple AI models with persistent memory
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Model Selection */}
          <Card className={`${theme.card} p-4`}>
            <h3 className="font-semibold mb-4">Available Models</h3>
            <div className="space-y-3">
              {models.map((model, index) => (
                <div key={index} className="p-3 rounded-lg border hover:bg-current hover:bg-opacity-5 cursor-pointer">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium">{model.name}</span>
                    <div className={`w-2 h-2 rounded-full ${
                      model.status === 'healthy' ? 'bg-green-400' : 'bg-yellow-400'
                    }`} />
                  </div>
                  <div className="text-xs opacity-50">Usage: {model.usage}</div>
                </div>
              ))}
            </div>
          </Card>

          {/* Chat Area */}
          <div className="lg:col-span-2">
            <Card className={`${theme.card} p-6 h-96`}>
              <div className="text-center py-20">
                <MessageCircle className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <h3 className="text-xl font-semibold mb-2">Model Coordinator Ready</h3>
                <p className="opacity-75">Select a model and start chatting</p>
              </div>
            </Card>
          </div>

          {/* Model Info */}
          <Card className={`${theme.card} p-4`}>
            <h3 className="font-semibold mb-4">Model Features</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Zap className="w-4 h-4 text-yellow-500" />
                <span className="text-sm">Speed Optimization</span>
              </div>
              <div className="flex items-center space-x-2">
                <Star className="w-4 h-4 text-purple-500" />
                <span className="text-sm">Quality Ranking</span>
              </div>
              <div className="flex items-center space-x-2">
                <Brain className="w-4 h-4 text-blue-500" />
                <span className="text-sm">Capability Matching</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}