import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Link as LinkIcon, Plus, Settings, Zap } from 'lucide-react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';

export default function IntegrationWorkbench() {
  const { theme } = useTheme();

  return (
    <div className="pt-16 min-h-screen">
      <div className="max-w-7xl mx-auto p-6">
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-teal-600 rounded-full flex items-center justify-center">
            <LinkIcon className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold">🐻 Integration Architect</h1>
            <p className="text-lg opacity-75">
              Build and manage integrations with external services
            </p>
          </div>
        </div>

        <div className="text-center py-20">
          <LinkIcon className="w-20 h-20 mx-auto mb-6 opacity-50" />
          <h2 className="text-2xl font-bold mb-4">Integration Workbench</h2>
          <p className="text-lg opacity-75 mb-8">
            Create powerful integrations with APIs, webhooks, and workflows
          </p>
          
          <Button className={theme.button}>
            <Plus className="w-4 h-4 mr-2" />
            Create Integration
          </Button>
        </div>
      </div>
    </div>
  );
}