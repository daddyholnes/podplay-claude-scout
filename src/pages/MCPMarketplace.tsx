import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Puzzle, Download, Search, Star } from 'lucide-react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';

export default function MCPMarketplace() {
  const { theme } = useTheme();

  const tools = [
    { name: 'File Manager', category: 'Utilities', rating: 4.8, downloads: '10k+' },
    { name: 'Web Scraper', category: 'Data', rating: 4.5, downloads: '5k+' },
    { name: 'Database Connector', category: 'Integration', rating: 4.9, downloads: '15k+' },
    { name: 'Image Processor', category: 'Media', rating: 4.3, downloads: '3k+' }
  ];

  return (
    <div className="pt-16 min-h-screen">
      <div className="max-w-7xl mx-auto p-6">
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <Puzzle className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold">🐻 Tool Curator</h1>
            <p className="text-lg opacity-75">
              Discover and install MCP tools and integrations
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {tools.map((tool, index) => (
            <Card key={index} className={`${theme.card} p-4`}>
              <div className="flex items-center space-x-2 mb-3">
                <Puzzle className="w-8 h-8 text-blue-500" />
                <div>
                  <h3 className="font-semibold">{tool.name}</h3>
                  <p className="text-xs opacity-50">{tool.category}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-2 mb-4">
                <div className="flex items-center space-x-1">
                  <Star className="w-4 h-4 text-yellow-500 fill-current" />
                  <span className="text-sm">{tool.rating}</span>
                </div>
                <span className="text-xs opacity-50">•</span>
                <span className="text-xs opacity-50">{tool.downloads}</span>
              </div>
              
              <Button size="sm" className={`w-full ${theme.button}`}>
                <Download className="w-4 h-4 mr-2" />
                Install
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}