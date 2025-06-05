import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Radio, Play, Settings, Mic } from 'lucide-react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';

export default function LiveAPIStudio() {
  const { theme } = useTheme();

  return (
    <div className="pt-16 min-h-screen">
      <div className="max-w-7xl mx-auto p-6">
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-pink-600 rounded-full flex items-center justify-center">
            <Radio className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold">🐻 Live API Specialist</h1>
            <p className="text-lg opacity-75">
              Real-time API experimentation with voice and video
            </p>
          </div>
        </div>

        <div className="text-center py-20">
          <Radio className="w-20 h-20 mx-auto mb-6 opacity-50" />
          <h2 className="text-2xl font-bold mb-4">Live API Studio</h2>
          <p className="text-lg opacity-75 mb-8">
            Test Gemini Live, voice interactions, and real-time features
          </p>
          
          <Button className={theme.button}>
            <Play className="w-4 h-4 mr-2" />
            Start Live Session
          </Button>
        </div>
      </div>
    </div>
  );
}